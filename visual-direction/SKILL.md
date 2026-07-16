---
name: visual-direction
description: >
  Compartmentalized visual-direction fan-out: 7 isolated subagents each decide
  ONE design domain (typography, color, signature element, layout, motion,
  texture, copy) from an identical context packet with zero shared context,
  then a synthesis judge measures direction convergence, resolves conflicts,
  and a blind build agent implements the page. Use when the user wants a fresh,
  bias-free visual direction for a page or product, wants to test what
  direction a brief "forces", or asks for the fan-out/compartmentalized design
  process. Triggers on "/visual-direction", "visual direction", "design
  fan-out", "isolated design decisions", "what direction does this brief
  imply". For single-context design work use design-frontend instead.
---

# Visual Direction

Runs a compartmentalized design process: independent deciders that cannot
anchor on each other, judged for convergence, reconciled, then built blind.
The convergence verdict doubles as a diagnostic — a sharp packet forces
agreement; a vague one exposes ambiguity in the brief.

<architecture>
- 7 deciders (fable, medium effort), each sees ONLY the context packet and its
  single domain: typography · color · signature/visual hook · layout+structure ·
  motion · texture/background · copy. Each also reports a `direction_word` —
  the aesthetic direction it infers from the packet alone.
- 1 synthesis judge (fable, high effort): compares direction_words, resolves
  cross-domain conflicts with minimal overrides, emits a reconciled token system.
- 1 build agent (fable, high effort): sees only packet + tokens, writes one
  self-contained HTML file.
</architecture>

<workflow>
1. **Write the context packet.** Product facts, audience, page job, available
   real content, constraints — nothing else. Rules:
   - NO aesthetic direction, tone words, or references to existing styling.
     The deciders must infer direction; pre-naming it invalidates the experiment
     and biases the output. If the user wants continuity with an existing
     design system, this is the wrong skill — use design-frontend.
   - Name one concrete subject, its audience, and the page's single job.
   - Include only content that is real; mark everything else as to-be-decided.
   - Be aware the packet's framing steers convergence: strong positioning
     language ("measured, not marketed") collapses the direction space. That
     can be the goal — or flatten the language to test genuine divergence.
   - Packet text must not contain backticks or `${` (it is interpolated into a
     JS template literal).
2. **Fill the template.** Read `~/.claude/skills/visual-direction/assets/workflow-template.js`,
   substitute `__PACKET__` (the packet text) and `__OUT_PATH__` (an absolute
   scratchpad path for the HTML deliverable), and write the result to the
   scratchpad. Do NOT pass the packet via Workflow `args` — args interpolation
   has silently arrived as `undefined` before; hardcoding via placeholders is
   the reliable path.
3. **Launch.** `Workflow({scriptPath: <filled copy>})`. Runs in background;
   9 agents, roughly 330k tokens and 10 minutes.
4. **Report.** Lead with the convergence verdict (the per-domain
   direction_words and whether the packet forced agreement), then conflicts
   and overrides the judge made, then send the built HTML to the user
   (SendUserFile, display render). Offer the reconciled token system as the
   reusable artifact — it outlives the mockup.
</workflow>

<failure_modes>
- Deciders receiving an empty/undefined packet refuse to fabricate and return
  explicit pipeline-fault responses. If any decision reads "no context / blocked",
  the packet substitution failed — fix the filled script and resume with
  `Workflow({scriptPath, resumeFromRunId})` (changed prompts re-run; unchanged
  ones replay from cache).
- If the synthesis judge reports weak convergence, surface that to the user as
  a finding about the brief, not a failure of the run — offer to sharpen the
  packet and re-run, or to pick among the divergent directions.
</failure_modes>
