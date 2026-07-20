export const meta = {
  name: 'session-investigate',
  description: 'Per-session investigators: goal / accomplishments / unfinished / next_steps grounded in git state',
  whenToUse: 'INVESTIGATE intent (unfinished work, status) across many sessions (> ~10)',
  phases: [
    { title: 'Investigate', detail: 'one agent per session, cross-referenced against git' },
  ],
}

// args: { outputDir: string (absolute), sessionIds: string[], projectDir: string (absolute repo path) }
const out = args.outputDir
const sessions = args.sessionIds

const SESSION_STATE = {
  type: 'object',
  properties: {
    session_id: { type: 'string' },
    goal: { type: 'string' },
    accomplishments: { type: 'array', items: { type: 'string' } },
    unfinished: { type: 'array', items: { type: 'string' } },
    next_steps: { type: 'array', items: { type: 'string' } },
  },
  required: ['session_id', 'goal', 'accomplishments', 'unfinished', 'next_steps'],
}

log(`Investigating ${sessions.length} session(s)`)

const records = (await parallel(sessions.map(sid => () =>
  agent(
    `Investigate the state of Claude Code session ${sid}.
1. Read ${out}/user_messages.json (flat JSON list, message body in "content") and keep ONLY entries with session_id == "${sid}".
2. Cross-reference ground truth from git in ${args.projectDir}: run \`git status\`, \`git log --oneline -15\`, and \`git log @{u}.. --oneline\` (unpushed) there.
3. Determine what the session set out to do, what verifiably landed (commits, files), what was started but not finished, and concrete next steps.
Ground claims in git state, not just what messages discussed. Return the structured record.`,
    { label: `investigate:${sid.slice(0, 8)}`, phase: 'Investigate', schema: SESSION_STATE }
  )
))).filter(Boolean)

return { sessions: records, dropped: sessions.length - records.length }
