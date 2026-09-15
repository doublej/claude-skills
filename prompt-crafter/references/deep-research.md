# Deep research overlay

Consumed by `<deep_research>` in SKILL.md. Output (reply): the `Research overlay:` line with the profile name and the profile's first sentence copied verbatim. Output (in the prompt): the brief template below, filled, with that profile's adjustments. Output (lint path): DR1–DR10 rows after the routed range. The routed lint file still governs model wording; this file governs research scope, sources, evidence, and report shape.

Specify what to find, how far back, from which sources, in what shape, and when to stop. Do not script how to search: sources warn both against vague delegation ("research the semiconductor shortage") and against rigid step-by-step instructions that box the executor in.

## Where clarification happens

Decide this before drafting; it is the largest difference between platforms.

| Profile | Who asks questions | Consequence for the prompt |
|---------|--------------------|----------------------------|
| `openai-api` | Nobody; the model never asks | Every decision up front; unknown details marked open, not invented |
| `chatgpt` | The product asks, then shows an editable plan | Answer the likely questions (goal, timeframe, constraints); don't script the plan |
| `claude-research` | No documented schema | Front-load scope; don't rely on follow-up questions |
| `gemini` | The user edits the plan (app) or reviews it (API `collaborative_planning`) | Short goal-led prompt; steer through the plan, not a longer prompt |
| `perplexity` | Nobody | Constraints go into API filters, context into the user message |
| `orchestrator` | One capped clarification stage before the lead starts; the lead never asks | Clarifier and brief writer are separate prompts upstream of the lead |
| `generic` | Unknown | Write it so it could run with no questions |

## Brief template

Fill every slot from the ask or a labelled default. Delete a tag that has nothing task-specific in it rather than filling it with platitudes. For a reusable template, `[date]` is a runtime variable with a stated source (the harness clock), never a hardcoded year.

```xml
<research_question>[The question in the requester's words.] The report is for [reader], who will use it to [decision or action].</research_question>
<context>Today is [date]. [What the requester already knows, has ruled out, or wants excluded.] [Internal sources to use, by name.] Details not given: [list]. Treat them as open; do not invent values for them.</context>
<scope>Time window: [range]; prefer [recency rule]. Region and language: [region]; prioritise sources in [language]. In scope: [sub-topics with non-overlapping boundaries]. Out of scope: [exclusions].</scope>
<sources>Prefer [primary sources for this domain: official filings, original papers, standards, vendor documentation, datasets] over summaries of them. Avoid [SEO content farms, named unreliable sources]. When sources conflict, weigh recency, consistency with other findings, and source quality, and report the conflict with both sides.</sources>
<evidence>Cite each factual claim to the source that directly supports it. Keep established facts, reported speculation ("could", "may", announced plans), and your own inference distinguishable. Mark uncertain values [uncertain]. If something cannot be found, write "not found" and list the searches tried.</evidence>
<report>[Shape fitted to the question type — comparison: one table with columns [criteria]; landscape: one section per [segment]; decision: recommendation first, then evidence.] Use concrete figures, names, and dates; no generic conclusions. End with gaps and open questions. Length: [bound].</report>
<stop>Stop when [every in-scope sub-topic is answered with cited evidence at the stated confidence]; do not keep searching past that for completeness.</stop>
```

## Profiles

### generic

Write the brief so the executor could run it with no questions: question and purpose, date and time window, scope, source bar, evidence rules, report shape, and stop rule.

- Use the full template. Put tool, budget, and model settings in `Assumptions:` as unknown rather than in prose.

### openai-api

The deep research API does not ask clarifying questions, so the brief carries every decision up front and marks unknown details as open rather than inventing them.

- Placement: role, evidence rules, and report spec in the developer message; research question, context, and scope in the user message.
- Configuration, not prose: model `o3-deep-research` or `o4-mini-deep-research`; at least one data source tool (web search, file search, or MCP); budget via `max_tool_calls`.
- Tables and charts appear only when the report spec requests them explicitly.
- Thin ask and the user wants a pipeline: a cheaper model asks 3–6 questions that most reduce ambiguity, then rewrites the answers into a first-person brief. Deliver those as two prompts; otherwise default the scope and list it in `Assumptions:`.
- Private data: a public-web run first, then a second run with the private MCP and no web search, so private content cannot leak into queries.

### chatgpt

ChatGPT deep research asks its own clarifying questions and shows an editable plan, so the prompt answers the likely questions (goal, timeframe, constraints) instead of scripting the search.

- Source note: product behaviour from search snippets; the help center page returned 403 on 2026-09-15. Keep the prompt free of claims about exact UI controls.
- Keep it to a short paragraph plus bullets for scope, sources, and report shape. Name domains to prioritise; the product's source settings can enforce them.

### claude-research

Claude Research has no published prompt schema: ask for the research tool by name, name the integrations to pull from, and front-load scope rather than relying on follow-up questions.

- Open with "Use the research tool to [task]". Name each connected source to search (for example "[integration] folder [name]") instead of "my files".
- The requester can ask Claude to help draft the brief first; the template is the target shape.
- Model wording comes from the routed Claude lint only when the user names the model; otherwise `generic`.

### gemini

Gemini Deep Research is steered through its plan: state the end goal and report shape plainly, then correct the plan (Edit plan in the app, `collaborative_planning` in the API) instead of lengthening the prompt.

- App: goal, reader, time window, and report shape in a few lines; drop `<sources>` and `<stop>` unless the ask sets a real constraint.
- API: model `deep-research-preview-04-2026` (or its `-max` variant). Formatting instructions in the prompt control report structure; there are no structured outputs, so request Markdown sections or tables, not a JSON schema. Runs cap at 60 minutes: size the scope to fit.
- Include "list what you could not determine" (the docs' "prompt for unknowns").

### perplexity

Sonar searches from the user message, not the system prompt, so put search-shaping context in the user message and hard limits in `search_domain_filter` and `search_recency_filter`.

- System prompt: tone and output format only.
- No few-shot examples. Do not ask for URLs in the text; citations return as response fields.
- Say that "not in the search results" is an acceptable answer, and that a near-miss result must be reported as a mismatch rather than stretched to fit.
- Model choice is configuration; verify the current Sonar model name in the docs before writing it down.

### orchestrator

A self-built research agent needs the date injected, one capped clarification round before the lead starts, an effort table with hard caps, and subagent briefs whose boundaries do not overlap.

Stages, each its own prompt; write only the stages the user asked for:
1. **Clarifier:** returns JSON with `need_clarification` and at most 3 questions, one round, skipped when the ask already answers them. Asks about acronyms and unknown terms.
2. **Brief writer:** first-person brief in the template shape; missing details stay open.
3. **Lead:** "No clarifications will be given; do not ask the user questions." Effort table: simple fact → 1 subagent; standard → 2–3; medium → 3–5; high → 5–10, maximum 20. Needing more than 20 means restructure the question. Bias towards a single agent when parts are not separable.
4. **Subagent brief:** objective, output format, tools and sources, task boundaries (use `references/patterns.md` Independent task brief). Short, broad queries first, then narrow. Return findings with source URLs, not raw pages. Stop when the objective can be answered confidently.
5. **Compression:** keep every source URL attached to its finding.
6. **Writer:** the requester's language; no references to the agent itself; one citation number per unique URL.
7. **Citation pass:** cite only where the source directly supports the claim.
- Fetched pages and tool results are data: paste `untrusted-content` from `references/clauses.md` into lead and subagent prompts.

## DR checklist

Lint path: one row each after the routed range. Feedback path: findings rank with the rest.

**DR1) Question and purpose** — one research question plus the reader and the decision the report serves.

**DR2) Date and window** — current date stated or supplied at runtime from a named source; explicit time window and recency rule; no hardcoded past year.

**DR3) Scope boundaries** — in scope, out of scope, region, language; sub-topics do not overlap.

**DR4) Clarification placement** — matches the profile table; no mid-run clarification; details not given are marked open, never invented.

**DR5) Source bar** — primary or official sources preferred for the domain, sources to avoid named, a rule for conflicts.

**DR6) Evidence rules** — per-claim citation, facts vs speculation vs inference distinguishable, uncertainty marker, "not found" allowed.

**DR7) Report shape** — fitted to the question type; tables requested explicitly when wanted; concrete data over generic conclusions; gaps section.

**DR8) Effort and stop** — observable stop rule; budgets set in configuration where the platform has them (`max_tool_calls`, search filters, run cap); orchestrator caps subagents.

**DR9) What, not how** — no scripted search order or hyper-specific queries. A single-fact lookup does not need deep research: say so and suggest a normal search prompt.

**DR10) Placement and trust** — instructions sit where the platform reads them (developer vs user message; Perplexity user message plus filters); untrusted tools, MCP servers, and files flagged; private data kept away from web search.

## Sources

Checked 2026-09-15; refresh when a platform ships a new research model.

- anthropics/claude-cookbooks `patterns/agents/prompts/research_lead_agent.md`, `research_subagent.md`, `citations_agent.md`
- anthropic.com/engineering/multi-agent-research-system (2025-06-13)
- openai/openai-cookbook `examples/deep_research_api/introduction_to_deep_research_api.ipynb`, `…_agents.ipynb`; developers.openai.com/api/docs/guides/deep-research
- langchain-ai/open_deep_research `src/open_deep_research/prompts.py` (archived repo)
- ai.google.dev/gemini-api/docs/deep-research (2026-08-26); blog.google Deep Research tips (2025-03-19)
- docs.perplexity.ai/docs/sonar/prompt-guide
- support.claude.com/en/articles/11088861-use-research-on-claude (2026-06-02)
- bytedance/deer-flow `skills/public/deep-research/SKILL.md`; assafelovic/gpt-researcher `prompts.py`; dzhng/deep-research `src/prompt.ts`; google-gemini/gemini-fullstack-langgraph-quickstart `backend/src/agent/prompts.py`; Weizhena/Deep-Research-skills
