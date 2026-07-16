export const meta = {
  name: 'visual-direction-fanout',
  description: 'Isolated per-domain design deciders from a shared context packet, coherence synthesis, then a filled direction board',
  phases: [
    { title: 'Validate', detail: 'gate the packet: brand context only, no deliverable brief, no pre-named aesthetics' },
    { title: 'Decide', detail: '8 isolated deciders, medium effort, packet-only context' },
    { title: 'Synthesize', detail: 'convergence check + reconciled token system' },
    { title: 'Board', detail: 'demonstrate every decision on the prebuilt SVG direction board' },
  ],
}

// Placeholders — substitute before launching. Packet text must not contain backticks or ${.
const PACKET = `__PACKET__`
const MODEL = '__MODEL__'
const SVG_OUT = '__SVG_OUT__'
const BOARD_TEMPLATE = '/Users/jurrejan/.claude/skills/visual-direction/assets/direction-board.svg'

const CALIBRATION = `Calibration: AI-generated design currently clusters around three default looks: (1) warm cream background (~#F4F1EA) with a high-contrast serif display and terracotta accent; (2) near-black background with a single acid-green or vermilion accent; (3) broadsheet-style hairline rules, zero border-radius, dense newspaper columns. These are defaults, not choices. Do not land on one of them unless the packet genuinely demands it.`

phase('Validate')
const validation = await agent(`You are the input gate of a compartmentalized visual-direction process. Eight isolated deciders will each derive one design domain from ONLY the packet below. The process produces a medium-agnostic brand/visual direction — NOT a specific deliverable. Validate the packet against these rules:

1. BRAND CONTEXT ONLY. The packet should contain: a concrete subject and its facts, the audience, available real content, and hard constraints (e.g. accessibility, trademark, existing name). That is all a direction needs.
2. NO DELIVERABLE BRIEF. Any framing of a target artifact — a page job, "announcement page", "HTML mockup", a deck, an app screen, conversion goals, section lists — biases every decider toward that medium. Flag it for removal.
3. NO PRE-NAMED AESTHETICS. Direction words, tone adjectives, style references, or existing-styling descriptions invalidate the experiment. Flag them for removal.
4. ENOUGH SUBSTANCE. After removals there must still be a concrete subject with its own world (materials, instruments, vernacular) and a named audience. If not, the run cannot produce a grounded direction.

PACKET:
${PACKET}

Return verdict "pass" if the packet is usable (after stripping rule-2/3 violations, if any). Return verdict "fail" only if rule 4 cannot be met. In cleaned_packet return the packet with every flagged passage removed and NOTHING added — no rewording, no invented facts; preserve the original text of everything you keep. On fail, leave cleaned_packet empty.`, {
  label: 'validate:packet',
  phase: 'Validate',
  schema: {
    type: 'object',
    required: ['verdict', 'issues', 'cleaned_packet'],
    properties: {
      verdict: { type: 'string', enum: ['pass', 'fail'] },
      issues: { type: 'array', items: { type: 'object', required: ['rule', 'excerpt', 'why'], properties: { rule: { type: 'string', enum: ['deliverable_brief', 'pre_named_aesthetics', 'insufficient_substance'] }, excerpt: { type: 'string' }, why: { type: 'string' } } } },
      cleaned_packet: { type: 'string' },
    },
  },
  model: MODEL,
  effort: 'medium',
})

if (!validation || validation.verdict === 'fail') {
  log('Packet failed validation — aborting before the fan-out.')
  return { aborted: true, validation }
}
if (validation.issues.length) log(`Validator stripped ${validation.issues.length} passage(s): ${validation.issues.map(i => i.rule).join(', ')}`)
const CLEAN_PACKET = validation.cleaned_packet.trim() || PACKET

const PREAMBLE = `You are ONE isolated decision-maker in a compartmentalized design process. You see ONLY the context packet below — no conversation history, no other designers' outputs, no existing site or brand assets. Do not hedge or offer options: commit to one decision. Derive everything from the subject's own world (its materials, instruments, vernacular). A decision that would fit any similar product is a failure.

CONTEXT PACKET:
${CLEAN_PACKET}

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
    task: `YOUR SOLE DECISION: color. Define a palette of 4–6 named hex values with roles (background, surface, ink, accent...), say whether the world is light or dark by default, and state the dominance/accent strategy (dominant colors with sharp accents beat timid even distribution).`,
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
    task: `YOUR SOLE DECISION: the signature element — the ONE thing this brand will be remembered by. A visual hook that embodies the subject (could be an interactive moment, a data visualization, a typographic device, an animation) and survives translation across media. Describe what it is, where it lives, how it behaves, and a short implementation sketch concrete enough to build in its most likely medium.`,
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
    task: `YOUR SOLE DECISION: layout and structure. One compositional concept for a representative surface of your choosing (pick whatever medium best expresses the subject), an ASCII wireframe of that surface, the grid approach, and any structural devices (numbering, eyebrows, dividers, labels) — each device must encode something true about the content, not decorate. List devices you considered and rejected as decoration.`,
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
    task: `YOUR SOLE DECISION: motion. Decide where animation serves this subject: entrance orchestration, reveal moments, micro-interactions, ambient atmosphere — or deliberate stillness. One orchestrated moment usually beats scattered effects. Specify each moment (trigger, effect, rough duration) and how reduced-motion preferences are respected.`,
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
    task: `YOUR SOLE DECISION: background, texture, and atmosphere. Decide how the direction's surfaces get depth instead of flat solid fills — or argue for disciplined flatness. Options include gradient meshes, noise/grain, geometric pattern, layered transparency, shadow strategy, decorative borders. Choose only what the subject earns. Never fabricate fake data displays: if a device imitates real measurement or content, it must be real or be cut.`,
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
    key: 'shape',
    task: `YOUR SOLE DECISION: shape and form language. Define the geometry the design speaks in: corner treatment (a radius scale in px, or the case for sharp or mixed corners), containment strategy (how content is boxed, ruled, chipped, or left open), iconography style (outline vs filled, stroke weight, drawing grid), and 1–3 recurring shape motifs drawn from the subject's own world. Every motif must encode something true about the subject — a generic blob, orb, or abstract swoosh is a failure.`,
    schema: {
      type: 'object',
      required: ['direction_word', 'corner_treatment', 'radius_scale', 'containment', 'iconography', 'motifs', 'rationale'],
      properties: {
        direction_word: { type: 'string' },
        corner_treatment: { type: 'string' },
        radius_scale: { type: 'array', items: { type: 'object', required: ['token', 'px', 'use'], properties: { token: { type: 'string' }, px: { type: 'string' }, use: { type: 'string' } } } },
        containment: { type: 'string' },
        iconography: { type: 'string' },
        motifs: { type: 'array', minItems: 1, maxItems: 3, items: { type: 'object', required: ['motif', 'encodes'], properties: { motif: { type: 'string' }, encodes: { type: 'string' } } } },
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
log(`Fanning out 8 isolated deciders (${MODEL}, medium effort)...`)
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
    tokens: { type: 'object', required: ['color', 'type', 'layout', 'motion', 'shape', 'signature', 'copy'], properties: { color: { type: 'object' }, type: { type: 'object' }, layout: { type: 'object' }, motion: { type: 'object' }, shape: { type: 'object' }, signature: { type: 'object' }, copy: { type: 'object' } } },
    build_notes: { type: 'string' },
  },
}
const synthesis = await agent(`You are the synthesis judge in a compartmentalized design process. Eight deciders each saw ONLY the context packet and decided one domain in isolation. Your job:

1. CONVERGENCE: compare their direction_word values. Report each (keyed by domain), a verdict on how strongly the packet forced convergence, and the dominant direction.
2. CONFLICTS: find cross-domain clashes (palette vs texture atmosphere, motion vs tone, signature vs layout placement, shape geometry vs layout devices, copy register vs visual register). Resolve each — say which decider wins and why.
3. OVERRIDES: change as little as possible. Every override must name the domain, what changed, and why coherence demanded it.
4. TOKENS: emit the final reconciled token system (color, type, layout, motion, shape, signature, copy) — concrete enough that a builder who has seen nothing else can implement it exactly. Include build_notes for anything tricky.

CONTEXT PACKET:
${CLEAN_PACKET}

THE EIGHT ISOLATED DECISIONS:
${JSON.stringify(decisions, null, 2)}`, {
  label: 'synthesize',
  phase: 'Synthesize',
  schema: SYNTH_SCHEMA,
  model: MODEL,
  effort: 'high',
})

phase('Board')
log('Synthesis done — filling the prebuilt direction board from the tokens...')
const boardReport = await agent(`You are the board agent in a compartmentalized design process. The visual direction is already decided; your job is to make a prebuilt SVG direction-board DEMONSTRATE every decision — the reader must SEE each decision working, not read a description of it. You invent no new direction; every mark derives from the tokens.

1. Read the template at: ${BOARD_TEMPLATE}
2. Follow the FILL RULES comment at the top of the template exactly. Two kinds of work:
   - SUBSTITUTION: replace every {{PLACEHOLDER}} from the token system below — including the real font family names ({{FONT_DISPLAY}}/{{FONT_BODY}}/{{FONT_MONO}}, they will be installed before rendering), corner radii ({{R_SM}}/{{R_MD}}/{{R_PILL}}) from the shape tokens, and type specimens written in the subject's vernacular. Split long text across numbered line slots within the stated budgets; unused slots become empty strings; delete unused swatch groups.
   - DRAWING SLOTS: replace each <!--SLOT:NAME--> comment with an SVG fragment that shows the decision — the texture applied to the board's own background, the signature element sketched as it would look, the layout wireframed with the signature and CTA marked in accent, the motion moments plotted on the provided 0-1200ms timeline, the shape language rendered as labeled radius samples and drawn motifs. Respect each slot's stated bounds and the fragment rules (palette colors only, stroke 1-2, labels <= 13px).
3. Escape any &, < or > in text content as XML entities. Never delete or alter the credits line.
4. Write the filled SVG to exactly: ${SVG_OUT} using the Write tool. It must be valid XML.

CONTEXT PACKET (for the SUBJECT slot, specimens, and phrasing):
${CLEAN_PACKET}

CONVERGENCE:
${JSON.stringify(synthesis ? synthesis.convergence : {}, null, 2)}

RECONCILED TOKEN SYSTEM:
${JSON.stringify(synthesis ? synthesis.tokens : decisions, null, 2)}`, {
  label: 'board:fill',
  phase: 'Board',
  schema: {
    type: 'object',
    required: ['summary', 'fonts'],
    properties: {
      summary: { type: 'string' },
      fonts: { type: 'array', items: { type: 'object', required: ['family', 'weights'], properties: { family: { type: 'string' }, weights: { type: 'string' } } }, description: 'Google Fonts families used in the SVG, with comma-separated weights, so the caller can install them before rendering' },
      swatches_used: { type: 'number' },
      omissions: { type: 'array', items: { type: 'string' } },
    },
  },
  model: MODEL,
  effort: 'high',
})

return {
  validation: { verdict: validation.verdict, issues: validation.issues },
  missing,
  convergence: synthesis ? synthesis.convergence : null,
  conflicts: synthesis ? synthesis.conflicts : null,
  overrides: synthesis ? synthesis.overrides : null,
  tokens: synthesis ? synthesis.tokens : null,
  boardReport,
  svgPath: SVG_OUT,
}
