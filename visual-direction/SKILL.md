---
name: visual-direction
description: >
  Compartmentalized visual-direction fan-out: 8 isolated subagents each decide
  ONE design domain (typography, color, signature element, layout, motion,
  texture, shape, copy) from an identical context packet with zero shared context,
  then a synthesis judge measures direction convergence, resolves conflicts,
  and emits a reconciled token system — a medium-agnostic brand/visual
  direction usable for any deliverable. Always renders the direction as an
  image from a prebuilt SVG board. Use when the user wants a fresh, bias-free
  visual direction, wants to test what direction a brief "forces", or asks for
  the fan-out/compartmentalized design process. Triggers on
  "/visual-direction", "visual direction", "design fan-out", "isolated design
  decisions", "what direction does this brief imply". For single-context
  design work use design-frontend instead.
---

# Visual Direction

Runs a compartmentalized design process: independent deciders that cannot
anchor on each other, judged for convergence, then reconciled into a token
system. The deliverable is the direction itself — tokens usable in any
medium (site, deck, packaging, app) — presented as a rendered direction
board. The convergence verdict doubles as a diagnostic: a sharp packet
forces agreement; a vague one exposes ambiguity in the brief.

<architecture>
- 8 deciders (chosen model, medium effort), each sees ONLY the context packet
  and its single domain: typography · color · signature/visual hook ·
  layout+structure · motion · texture/background · shape/form language · copy.
  Each also reports a
  `direction_word` — the aesthetic direction it infers from the packet alone.
- 1 synthesis judge (chosen model, high effort): compares direction_words,
  resolves cross-domain conflicts with minimal overrides, emits the reconciled
  token system — the primary output.
- 1 board agent (chosen model, medium effort): fills the prebuilt SVG
  direction-board template (`assets/direction-board.svg`) with the tokens.
  It substitutes placeholders only — it designs nothing and must keep the
  small credits line (github.com/doublej) at the bottom.
</architecture>

<workflow>
1. **Ask which model.** Via consult-user `ask` (type `pick`): options
   `fable (recommended)`, `opus (recommended)`, `sonnet`, `haiku`, with
   "Other" free text allowed for any model string. Strip any
   " (recommended)" suffix before use. One model powers all 10 agents;
   effort tiers (medium/high) stay the same regardless of model. If the
   ask is cancelled or AFK, default to `fable`.
2. **Write the context packet.** Product facts, audience, page/product job,
   available real content, constraints — nothing else. Rules:
   - NO aesthetic direction, tone words, or references to existing styling.
     The deciders must infer direction; pre-naming it invalidates the experiment
     and biases the output. If the user wants continuity with an existing
     design system, this is the wrong skill — use design-frontend.
   - Name one concrete subject, its audience, and the single job the design
     must do.
   - Include only content that is real; mark everything else as to-be-decided.
   - Be aware the packet's framing steers convergence: strong positioning
     language ("measured, not marketed") collapses the direction space. That
     can be the goal — or flatten the language to test genuine divergence.
   - Packet text must not contain backticks or `${` (it is interpolated into a
     JS template literal).
3. **Fill the template.** Read `~/.claude/skills/visual-direction/assets/workflow-template.js`,
   substitute `__PACKET__` (the packet text), `__MODEL__` (the chosen model),
   and `__SVG_OUT__` (an absolute scratchpad path ending in `.svg`), and write
   the result to the scratchpad. Do NOT pass the packet via Workflow `args` —
   args interpolation has silently arrived as `undefined` before; hardcoding
   via placeholders is the reliable path.
4. **Launch.** `Workflow({scriptPath: <filled copy>})`. Runs in background;
   10 agents, roughly 330k tokens and 10 minutes.
5. **Render the board image.** Always — the image is the standing artifact:
   ```bash
   rsvg-convert --zoom 2 -o <scratchpad>/direction-board.png <svg_out>
   ```
   (Fallback if rsvg-convert is missing: `magick <svg_out> <png>`.) View the
   PNG once to check nothing overflows; if a line overflows, shorten that
   text in the filled SVG directly and re-render. Also write the reconciled
   token system to `<scratchpad>/direction-tokens.json`.
6. **Report.** Lead with the convergence verdict (the per-domain
   direction_words and whether the packet forced agreement), then conflicts
   and overrides the judge made. Send the board PNG (SendUserFile, display
   render) together with `direction-tokens.json`. Frame the token system as
   the reusable brand direction — it applies to any medium, not just a page.
   If the user wants the direction applied (a page, deck, etc.), hand the
   tokens to design-frontend or the relevant build path as a follow-up.
</workflow>

<failure_modes>
- Deciders receiving an empty/undefined packet refuse to fabricate and return
  explicit pipeline-fault responses. If any decision reads "no context / blocked",
  the packet substitution failed — fix the filled script and resume with
  `Workflow({scriptPath, resumeFromRunId})` (changed prompts re-run; unchanged
  ones replay from cache).
- If `rsvg-convert` errors, the board agent produced invalid XML — fix the
  filled SVG in place (usually an unescaped `&`) and re-render; the workflow
  does not need to re-run.
- If the synthesis judge reports weak convergence, surface that to the user as
  a finding about the brief, not a failure of the run — offer to sharpen the
  packet and re-run, or to pick among the divergent directions.
</failure_modes>
