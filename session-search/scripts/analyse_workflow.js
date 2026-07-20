export const meta = {
  name: 'session-analyse',
  description: 'Fan out categorization + context resolution over extracted session messages, then synthesize a timeline report',
  whenToUse: 'Large session-history corpora (> ~300 messages) extracted by session_search.py extract',
  phases: [
    { title: 'Analyze', detail: 'haiku categorizers per chunk + one context resolver, concurrent', model: 'haiku' },
    { title: 'Synthesize', detail: 'merge chunk outputs into timeline_summary.md' },
  ],
}

// args: { outputDir: string (absolute), messageCount: number, projectName: string, chunkSize?: number }
const out = args.outputDir
const total = args.messageCount
const chunkSize = args.chunkSize || 150

const chunks = []
for (let i = 0; i < total; i += chunkSize) {
  chunks.push({ start: i, end: Math.min(i + chunkSize, total) })
}

const FILE_RESULT = {
  type: 'object',
  properties: {
    file: { type: 'string', description: 'Absolute path of the JSON file written' },
    count: { type: 'number', description: 'Number of entries written' },
  },
  required: ['file', 'count'],
}

log(`Categorizing ${total} messages in ${chunks.length} chunk(s) + resolving context`)

// Categorizer chunks and the context resolver are independent — run them all concurrently.
// The barrier is justified: synthesis needs every chunk file plus resolved_context.json.
const tasks = chunks.map((c, i) => () =>
  agent(
    `Read ${out}/user_messages.json — a flat JSON list of user messages, each {type, uuid, timestamp, content, session_id}; message body is in "content".
Process ONLY the messages at 0-based index ${c.start} through ${c.end - 1}.
Categorize each message as one of:
- TASK: direct work requests ("create", "build", "fix", "add")
- QUESTION: information queries ("how", "what", "where", "why")
- CORRECTION: fixes/adjustments ("no", "wrong", "instead", "actually")
- FEEDBACK: reactions ("good", "thanks", "perfect", interrupts)
- META: commands, model switches, configuration
Write ${out}/categorized_${i}.json as a JSON list: [{timestamp, category, original, one_line_summary}].
Return {file, count}.`,
    { label: `categorize:${c.start}-${c.end - 1}`, phase: 'Analyze', model: 'haiku', effort: 'low', schema: FILE_RESULT }
  )
)

tasks.push(() =>
  agent(
    `Read ${out}/user_messages.json — a flat JSON list of user messages, each {type, uuid, timestamp, content, session_id}; message body is in "content".
For messages containing unresolved references ("that", "it", "the thing", "this", "above"), infer what they refer to from timestamp proximity and surrounding messages in the same session.
Write ${out}/resolved_context.json as a JSON list: [{uuid, timestamp, original, inferred_context, clarified_prompt}].
Return {file, count}.`,
    { label: 'resolve-context', phase: 'Analyze', model: 'haiku', schema: FILE_RESULT }
  )
)

const results = (await parallel(tasks)).filter(Boolean)
const allCatFiles = results.filter(r => r.file && r.file.includes('categorized_')).map(r => r.file)

log(`Synthesizing from ${allCatFiles.length} categorized chunk(s)`)

const summaryPath = await agent(
  `Read these categorized-message files: ${allCatFiles.join(', ')}
and ${out}/resolved_context.json (may be missing if the resolver failed — proceed without it).
Write ${out}/timeline_summary.md with exactly this structure:

# Project Timeline: ${args.projectName}
Period: <start_date> to <end_date>
Messages analyzed: ${total}

## Executive Summary
2-3 sentences: main themes, accomplishments, patterns.

## Chronological Timeline
| Date | Original | Clarified | Category |
Key requests with clarified versions (use resolved_context.json for the Clarified column).

## Communication Patterns
- Common request types
- Prompting style observations
- Areas where context was often missing

## Suggested Prompt Improvements
Rewritten versions of ambiguous prompts.

Return ONLY the absolute path of the written file.`,
  { label: 'synthesize-timeline', phase: 'Synthesize' }
)

return { summary: summaryPath, categorizedFiles: allCatFiles, resolvedContext: `${out}/resolved_context.json` }
