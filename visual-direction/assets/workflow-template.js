export const meta = {
  name: 'visual-direction-fanout',
  description: 'Isolated per-domain design deciders from a shared context packet, coherence synthesis, then a filled direction board',
  phases: [
    { title: 'Decide', detail: '7 isolated deciders, medium effort, packet-only context' },
    { title: 'Synthesize', detail: 'convergence check + reconciled token system' },
    { title: 'Board', detail: 'fill the prebuilt SVG direction board from the tokens' },
  ],
}

// Placeholders — substitute before launching. Packet text must not contain backticks or ${.
const PACKET = `__PACKET__`
const MODEL = '__MODEL__'
const SVG_OUT = '__SVG_OUT__'
const BOARD_TEMPLATE = '/Users/jurrejan/.claude/skills/visual-direction/assets/direction-board.svg'

const CALIBRATION = `Calibration: AI-generated design currently clusters around three default looks: (1) warm cream background (~#F4F1EA) with a high-contrast serif display and terracotta accent; (2) near-black background with a single acid-green or vermilion accent; (3) broadsheet-style hairline rules, zero border-radius, dense newspaper columns. These are defaults, not choices. Do not land on one of them unless the packet genuinely demands it.`

const PREAMBLE = `You are ONE isolated decision-maker in a compartmentalized design process. You see ONLY the context packet below — no conversation history, no other designers' outputs, no existing site or brand assets. Do not hedge or offer options: commit to one decision. Derive everything from the subject's own world (its materials, instruments, vernacular). A decision that would fit any similar product is a failure.

CONTEXT PACKET:
${PACKET}

${CALIBRATION}

First infer the single aesthetic direction word/phrase this subject implies (report it as direction_word), then make your decision.`

const DOMAINS = [
  {
    key: 'typography',
    task: `YOUR SOLE DECISION: typography. Choose a characterful display face and a complementary body face (plus a utility/data face if the subject needs one), with weights and a one-line type-scale note. RESTRICTED — never use: Plus Jakarta Sans, Inter, JetBrains Mono, Space Grotesk, Roboto, Arial, system-ui stacks. Prefer faces available on Google Fonts or with a stated fallback.`,
    schema: {
      type: 'object',
      required: ['direction_word', 'display', 'body', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        display: { type: 'object', required: ['family', 'weights'], properties: { family: { type: 'string' }, weights: { type: 'array', items: { type: 'string' } }, source: { type: 'string' } } },
        body: { type: 'object', required: ['family', 'weights'], properties: { family: { type: 'string' }, weights: { type: 'array', items: { type: 'string' } }, source: { type: 'string' } } },
        utility: { type: 'object', properties: { family: { type: 'string' }, role: { type: 'string' }, source: { type: 'string' } } },
        scale_note: { type: 'string' },
        rationale: { type: 'string' },
      },
    },
  },
  {
    key: 'color',
    task: `YOUR SOLE DECISION: color. Define a palette of 4–6 named hex values with roles (background, surface, ink, accent...), say whether the page is light or dark, and state the dominance/accent strategy (dominant colors with sharp accents beat timid even distribution).`,
    schema: {
      type: 'object',
      required: ['direction_word', 'mode', 'palette', 'accent_strategy', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        mode: { type: 'string', enum: ['light', 'dark'] },
        palette: { type: 'array', minItems: 4, maxItems: 6, items: { type: 'object', required: ['name', 'hex', 'role'], properties: { name: { type: 'string' }, hex: { type: 'string' }, role: { type: 'string' } } } },
        accent_strategy: { type: 'string' },
        rationale: { type: 'string' },
      },
    },
  },
  {
    key: 'signature',
    task: `YOUR SOLE DECISION: the signature element — the ONE thing this page will be remembered by. A visual hook that embodies the subject (could be an interactive moment, a data visualization, a typographic device, an animation). Describe what it is, where it lives, how it behaves, and a short implementation sketch (plain HTML/CSS/JS level).`,
    schema: {
      type: 'object',
      required: ['direction_word', 'element', 'placement', 'behavior', 'implementation_sketch', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        element: { type: 'string' },
        placement: { type: 'string' },
        behavior: { type: 'string' },
        implementation_sketch: { type: 'string' },
        rationale: { type: 'string' },
      },
    },
  },
  {
    key: 'layout',
    task: `YOUR SOLE DECISION: layout and structure. One layout concept for the page (hero through footer), an ASCII wireframe, the grid approach, and any structural devices (numbering, eyebrows, dividers, labels) — each device must encode something true about the content, not decorate. List devices you considered and rejected as decoration.`,
    schema: {
      type: 'object',
      required: ['direction_word', 'concept', 'wireframe', 'grid', 'structural_devices', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        concept: { type: 'string' },
        wireframe: { type: 'string' },
        grid: { type: 'string' },
        structural_devices: { type: 'array', items: { type: 'object', required: ['device', 'encodes'], properties: { device: { type: 'string' }, encodes: { type: 'string' } } } },
        rejected: { type: 'array', items: { type: 'string' } },
        rationale: { type: 'string' },
      },
    },
  },
  {
    key: 'motion',
    task: `YOUR SOLE DECISION: motion. Decide where animation serves this subject: page-load orchestration, scroll reveals, hover micro-interactions, ambient atmosphere — or deliberate stillness. One orchestrated moment usually beats scattered effects. Specify each moment (trigger, effect, rough duration) and how prefers-reduced-motion is respected.`,
    schema: {
      type: 'object',
      required: ['direction_word', 'moments', 'restraint_note', 'reduced_motion', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        moments: { type: 'array', items: { type: 'object', required: ['trigger', 'effect'], properties: { trigger: { type: 'string' }, effect: { type: 'string' }, duration: { type: 'string' } } } },
        restraint_note: { type: 'string' },
        reduced_motion: { type: 'string' },
        rationale: { type: 'string' },
      },
    },
  },
  {
    key: 'texture',
    task: `YOUR SOLE DECISION: background, texture, and atmosphere. Decide how the page gets depth instead of flat solid fills — or argue for disciplined flatness. Options include gradient meshes, noise/grain, geometric pattern, layered transparency, shadow strategy, decorative borders. Choose only what the subject earns. Never fabricate fake data displays: if a device imitates real measurement or content, it must be real or be cut.`,
    schema: {
      type: 'object',
      required: ['direction_word', 'background_treatment', 'depth_devices', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        background_treatment: { type: 'string' },
        depth_devices: { type: 'array', items: { type: 'string' } },
        rationale: { type: 'string' },
      },
    },
  },
  {
    key: 'copy',
    task: `YOUR SOLE DECISION: the words. Voice/register for this audience, the headline, a subhead, the primary CTA label, and 3–6 microcopy rules (naming, tense, tone). Write from the user's side of the screen; specific beats clever; active voice; an action keeps its name through the whole flow.`,
    schema: {
      type: 'object',
      required: ['direction_word', 'voice', 'headline', 'subhead', 'cta_primary', 'microcopy_rules', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        voice: { type: 'string' },
        headline: { type: 'string' },
        subhead: { type: 'string' },
        cta_primary: { type: 'string' },
        microcopy_rules: { type: 'array', items: { type: 'string' } },
        rationale: { type: 'string' },
      },
    },
  },
]

phase('Decide')
log(`Fanning out 7 isolated deciders (${MODEL}, medium effort)...`)
const results = await parallel(DOMAINS.map(d => () =>
  agent(`${PREAMBLE}\n\n${d.task}`, {
    label: `decide:${d.key}`,
    phase: 'Decide',
    schema: d.schema,
    model: MODEL,
    effort: 'medium',
  }).then(r => ({ key: d.key, decision: r }))
))

const decisions = {}
for (const r of results.filter(Boolean)) decisions[r.key] = r.decision
const missing = DOMAINS.map(d => d.key).filter(k => !decisions[k])
if (missing.length) log(`WARNING: deciders returned nothing for: ${missing.join(', ')}`)

phase('Synthesize')
const SYNTH_SCHEMA = {
  type: 'object',
  required: ['convergence', 'conflicts', 'overrides', 'tokens'],
  properties: {
    convergence: { type: 'object', required: ['direction_words', 'verdict', 'dominant_direction'], properties: { direction_words: { type: 'object' }, verdict: { type: 'string' }, dominant_direction: { type: 'string' } } },
    conflicts: { type: 'array', items: { type: 'object', required: ['between', 'issue', 'resolution'], properties: { between: { type: 'string' }, issue: { type: 'string' }, resolution: { type: 'string' } } } },
    overrides: { type: 'array', items: { type: 'object', required: ['domain', 'changed', 'why'], properties: { domain: { type: 'string' }, changed: { type: 'string' }, why: { type: 'string' } } } },
    tokens: { type: 'object', required: ['color', 'type', 'layout', 'motion', 'signature', 'copy'], properties: { color: { type: 'object' }, type: { type: 'object' }, layout: { type: 'object' }, motion: { type: 'object' }, signature: { type: 'object' }, copy: { type: 'object' } } },
    build_notes: { type: 'string' },
  },
}
const synthesis = await agent(`You are the synthesis judge in a compartmentalized design process. Seven deciders each saw ONLY the context packet and decided one domain in isolation. Your job:

1. CONVERGENCE: compare their direction_word values. Report each (keyed by domain), a verdict on how strongly the packet forced convergence, and the dominant direction.
2. CONFLICTS: find cross-domain clashes (palette vs texture atmosphere, motion vs tone, signature vs layout placement, copy register vs visual register). Resolve each — say which decider wins and why.
3. OVERRIDES: change as little as possible. Every override must name the domain, what changed, and why coherence demanded it.
4. TOKENS: emit the final reconciled token system (color, type, layout, motion, signature, copy) — concrete enough that a builder who has seen nothing else can implement it exactly. Include build_notes for anything tricky.

CONTEXT PACKET:
${PACKET}

THE SEVEN ISOLATED DECISIONS:
${JSON.stringify(decisions, null, 2)}`, {
  label: 'synthesize',
  phase: 'Synthesize',
  schema: SYNTH_SCHEMA,
  model: MODEL,
  effort: 'high',
})

phase('Board')
log('Synthesis done — filling the prebuilt direction board from the tokens...')
const boardReport = await agent(`You are the board agent in a compartmentalized design process. The visual direction is already decided; your ONLY job is to fill a prebuilt SVG direction-board template with it. Do not design anything.

1. Read the template at: ${BOARD_TEMPLATE}
2. Follow the FILL RULES comment at the top of the template exactly: replace every {{PLACEHOLDER}} from the token system below, split long text across the numbered line slots within the stated character budgets, set unused line slots to an empty string, delete unused swatch groups, and take the board colors ({{C_BG}}, {{C_INK}}, {{C_ACCENT}}) from the palette roles. Escape any &, < or > in text content as XML entities. Never delete or alter the credits line.
3. Write the filled SVG to exactly: ${SVG_OUT} using the Write tool. It must be valid XML.

CONTEXT PACKET (for the SUBJECT slot and phrasing):
${PACKET}

CONVERGENCE:
${JSON.stringify(synthesis ? synthesis.convergence : {}, null, 2)}

RECONCILED TOKEN SYSTEM:
${JSON.stringify(synthesis ? synthesis.tokens : decisions, null, 2)}`, {
  label: 'board:fill',
  phase: 'Board',
  schema: {
    type: 'object',
    required: ['summary'],
    properties: {
      summary: { type: 'string' },
      swatches_used: { type: 'number' },
      omissions: { type: 'array', items: { type: 'string' } },
    },
  },
  model: MODEL,
  effort: 'medium',
})

return {
  missing,
  convergence: synthesis ? synthesis.convergence : null,
  conflicts: synthesis ? synthesis.conflicts : null,
  overrides: synthesis ? synthesis.overrides : null,
  tokens: synthesis ? synthesis.tokens : null,
  boardReport,
  svgPath: SVG_OUT,
}
