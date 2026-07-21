---
name: ui-align
description: "Measurement-first audit and fix of text/icon alignment in a LIVE rendered web UI — baselines via the strut trick, optical (cap-mid) centres, SVG ink centres, DOM-enlarged proof images. Requires a page you can run JS against (claude-in-chrome, playwright, devtools). Use when asked to 'fix alignment', 'text looks off', 'icons sit low', 'measure the baseline', or to audit a top bar / toolbar / pill / chip / row. For screenshot-only typography linting (no DOM) use ui-type-lint instead."
---

# ui-align

<overview>
Box alignment and optical alignment are two different problems, and box alignment
is almost never the bug. In the originating audit every element of the bar centred
at exactly 24.00 — flexbox was flawless — yet the bar read as misaligned; the whole
defect was typographic. This skill measures the live DOM (CSS alone cannot find
these defects — the numbers only exist after layout), applies an alignment contract
to decide which deltas are real, and proves fixes with re-rasterized enlargements.

Provenance: claims below marked [judgment] are heuristics calibrated in one audit
(one font, one 2× display) — treat as defaults, not law. Everything else was
observed live.
</overview>

<diagnostic_order>
Diagnose in this order. Skipping ahead produces nudge-hacks that paper over real
layout bugs.

1. **Box centres.** If they disagree → layout bug (padding, `line-height`,
   `align-items`, fixed heights). Fix there and stop.
2. **Baselines.** Boxes agree but it still reads wrong → text runs that should
   share a baseline don't.
3. **Optical centres (cap-mid).** Baselines fine within each container, but
   containers disagree with each other, or icons disagree with text.
</diagnostic_order>

<alignment_contract>
Most "fix alignment" requests fail because the wrong pairs get compared. This
table is the rulebook:

| Relationship | Aligns by | Notes |
|---|---|---|
| Text runs on one visual line, same container | **Shared baseline** | A split here is always a defect. |
| Text in *separate* bordered containers (pills, `kbd` chips, badges, buttons) | **Box centre** | Different baselines here are correct and conventional. Do NOT flag. |
| Icon vs adjacent text | Icon **ink** centre vs text **cap-mid** | Not box centre, not baseline. |
| Icon vs icon in one row | Ink centres | Box centres lie when artwork is off-centre in its viewBox. |
| Sibling containers of equal height | **Cap-mid offset from box centre** | Normalizes across font size and family. |

The pill/chip exception matters most: flagging separate bordered boxes for
"different baselines" is noise, not a finding. The audit report's `boxed` field is
a hint for this rule — verify it before trusting it.
</alignment_contract>

<measurement>
Evaluate the whole bundled script in the target page (paste its contents into the
JS-eval tool; it returns `"ui-align loaded"`):

```
~/.claude/skills/ui-align/scripts/ui-align.js
```

Then:

```js
__uiAlign.audit('header')   // or any selector for the component under audit
```

Returns per-text-node rows (baselineY, capMidY, boxCenterY, capMidMinusBoxCenter,
font info, `boxed` hint), per-SVG rows (inkCenterY, inkMinusBoxCenter), and a
summary: `capMidSpread` (headline metric), `boxCenterSpread`, grouped `baselines`.

The script already encodes the gotchas that produce false positives — do not
re-derive these by hand:

- **Strut in flex/grid parents**: a baseline strut becomes a flex item and returns
  garbage; the script wraps the text node in an inline-block first.
- **`getBBox()` is in viewBox user units**: `viewBox.y` must be subtracted before
  scaling to screen (forgetting it manufactured a phantom 6px defect), and it
  **excludes stroke** — stroked art extends `strokeWidth/2` past the geometry.

Sanity rule: a well-drawn icon has ink centre ≈ viewBox centre. If the delta is
large, suspect your arithmetic before the artwork.
</measurement>

<bug_catalog>
**The `align-items:center` baseline split — the headline bug.** It centres
*boxes*; two text runs of different `font-size` in one flex row get their boxes
centred but their baselines split, because the baseline sits asymmetrically in the
em box. A 0.5px font-size delta produced a 0.65px baseline split in JetBrains Mono
— the break is larger than the size difference causing it (~1.3×, tracks the
font's ascent ratio [judgment, single font]). Fixes, in preference order:

1. **One font-size for the whole row** — take emphasis from colour or weight. Best fix.
2. `align-items: baseline` — often unavailable: it wrecks non-text flex children
   (dots, icons, avatars, separators).
3. Per-item `translateY` nudge — last resort, breaks on font or size change.

When unifying font-size, choose the value by its effect on the *surrounding*
context, not just the local container — the right choice can fix the internal
split and the cross-container cap-mid mismatch in one change.

**Mono vs sans at equal box height.** Different typefaces at the same nominal size
don't share an optical centre; mono faces have deeper descenders and ride high in
a centred box. Compare via cap-mid offset from box centre.

**Icon artwork off-centre in its own viewBox.** Ink centre ≠ viewBox centre.
Fixing means editing shared icon paths — app-wide blast radius. Usually report and
leave alone unless the delta clears the act threshold on its own.
</bug_catalog>

<tolerances>
[judgment] Calibrated on a 2× DPR display; scale accordingly.

| Delta | Action |
|---|---|
| ≤ 0.25px | Ignore — below perception. |
| 0.25–0.5px | Note it. Fix only if cheap and local. |
| ≥ 0.5px | Real. Act. (0.65px ≈ 1.3 device px at 2× — plainly visible.) |

Headline metric for a component: cap-mid **spread** (max − min) across all its
text. Under ~0.25px spread reads as coherent.
</tolerances>

<verification_protocol>
1. **Never zoom a screenshot to verify.** Screenshot zoom crops and upsamples an
   already-downscaled capture — sub-pixel detail is destroyed before you zoom
   (two lines 0.65px apart collapse into one smear). Instead:
   `__uiAlign.enlarge(sel, 6, [{y: 27.30, label: 'baseline A'}, ...])` builds a
   `transform:scale()` clone the browser re-rasterizes, with measured values drawn
   as guide lines. Screenshot `#__uiAlignStage` — that image is the proof.
   `__uiAlign.clearStage()` when done.
2. **Test the fix in-page before touching files**: `__uiAlign.tryFix(css)`,
   re-run `audit()`, confirm the numbers move as predicted. Only then edit source.
3. **Re-measure shipped CSS clean**: after editing, reload, re-evaluate the
   script, and check `__uiAlign.assertClean()` is `true` so you know you're
   measuring real CSS, not your own injection. Easy to fool yourself here.
4. **Images cross-check arithmetic, not replace it.** Measurement code has bugs;
   the phantom 6px defect was caught because the enlargement *looked fine*,
   contradicting the number. Discovery comes from measurement; the image is the
   independent check. Run both.
</verification_protocol>

<reporting>
- Lead with the defect in plain language, then the numbers.
- State deltas against a **named reference line** ("baseline 27.30 shared by A, B, C").
- Headline result: **before → after cap-mid spread**.
- Explicitly list what was **not** fixed and why (cost, blast radius,
  below-threshold). Silence reads as "everything was fine".
- Separate "boxes were correct" from "type was wrong" so the reader learns the
  mechanism.
</reporting>

<anti_patterns>
- Comparing baselines across bordered pills and reporting a "defect" — they align by box centre.
- `translateY` nudges before checking whether one font-size fixes the row.
- `align-items: baseline` on a flex row containing dots, icons, avatars or separators.
- Trusting `getBBox()` as ink bounds on stroked artwork.
- Forgetting `viewBox.y` when mapping user units to screen.
- Zooming a downscaled screenshot and believing the result.
- Editing CSS before confirming the fix numerically in-page.
- "Fixing" a sub-0.25px delta — churn with no perceptible gain.
</anti_patterns>
