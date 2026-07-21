---
name: ui-type-lint
description: "Pixel-analysis linter for typography in UI screenshots — no OCR, no DOM. Detects the classic agent-design failures: font sizes too similar (weak hierarchy), body text too small, lines too wide, plus low contrast, tight/loose leading, ragged alignment, wide tracking, and type-scale sprawl. Use after generating or restyling any UI to verify the result from a screenshot, when a design 'looks off', or when the user says 'check the typography', 'fonts too similar/small/wide', 'lint this screenshot', 'verify the design'. Pairs with design-frontend / ui-readable for the fix."
---

# ui-type-lint

<overview>
Screenshot in, findings out. The script binarizes the image, groups glyph
components into text lines, estimates per-line font size, stroke weight, line
measure, letter-spacing, and leading, clusters the sizes, and flags problems
with locations. It judges what was actually rendered — not what the CSS claims.
</overview>

<usage>
```bash
uv run ~/.claude/skills/ui-type-lint/scripts/typelint.py <screenshot.png> [flags]
```

| Flag | Meaning |
|---|---|
| `--scale N` | Device pixel ratio of the capture. **Retina/macOS screenshots need `--scale 2`**, headless Chrome at default DPR needs nothing. All px in findings are CSS px = device px / scale. |
| `--annotate out.png` | Write overlay: line boxes colored by size cluster, flagged regions in red (high) / orange (warn) with the finding id. Show this to the user. |
| `--json` | Machine-readable output (image, clusters, findings with bboxes). |
| `--fail-on warn\|high` | Exit 2 when findings at/above that severity exist — for loops and CI. |
| `--min-body` / `--min-heading-ratio` / `--max-cpl` | Threshold overrides (defaults 14px, 1.4×, 80cpl). |

Capturing input: any real screenshot works. For local HTML:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --screenshot=/tmp/shot.png --window-size=1440,900 \
  --hide-scrollbars "file:///path/page.html"
```
</usage>

<findings>
| id | Fires when | Typical fix |
|---|---|---|
| `body-too-small` | Dominant text cluster < 14 CSS px (findings within ~7% of the floor are marked borderline and capped at warn) | Raise body to 14–16px |
| `tiny-text` | Secondary cluster < 10px with real usage | Raise captions/labels to ≥11px |
| `weak-hierarchy` | Largest heading < 1.4× body (a ≥1.15× weight step relaxes this to 1.25×), or no cluster ≥1.25× body at all ("flat typography") | Push headings to ≥1.4× body or add weight contrast |
| `no-weight-contrast` | Heading/body differ by neither size (<1.5×) nor stroke weight | Bold the headings |
| `muddy-scale` | Two well-used sizes < 1.15× apart at/above body (conventional 12/14-style caption pairs below body are not flagged) | Merge them, or separate roles by size/weight |
| `too-many-sizes` | > 6 well-used sizes | Consolidate to a 4–5 step scale |
| `long-lines` | Body runs > 80 chars per line (high above 100) | Constrain measure to 60–75ch |
| `wide-measure` | Body text runs > 75% of viewport width | Wrap earlier; don't fill containers edge to edge |
| `wide-tracking` | Letter-spacing > 0.3em on running text | Reserve tracking for small caps labels |
| `tight-leading` | Paragraph line-height < 1.3 (blocks <1.0 discarded as mis-segmentation) | Body line-height ~1.4–1.6 |
| `loose-leading` | Wrapped prose at line-height > 1.9 (link lists / settings rows exempt — only blocks whose lines fill the measure count) | Bring body back under ~1.8 |
| `low-contrast` | ≥3 lines below WCAG (4.5:1 text, 3:1 ≥24px); gradient/photo backgrounds and sub-1.3:1 noise skipped | Darken/lighten the text color |
| `ragged-alignment` | Left edges in one column drift ~0.3–0.6em, scattered (two clean edges ≥0.4em apart = intentional hanging indent, skipped) | Snap lines to one axis |

Severities: `high` = fix before showing anyone, `warn` = should fix, `info` =
context (e.g. retina-scale hint). The cluster table always prints — use it to
sanity-check even when there are zero findings.
</findings>

<workflow>
1. Screenshot the UI (real browser, real widths — both desktop and narrow if responsive).
2. Run the linter; on retina captures pass `--scale 2`.
3. Fix findings in the source (tokens from **ui-readable**, direction from **design-frontend**), re-screenshot, re-run until clean at `--fail-on warn`.
4. When reporting to the user, show the annotated overlay and quote the finding messages — they contain measured values, not opinions.
</workflow>

<limitations>
- Estimates: font size from glyph heights (±10%), advance from ink widths — CPL is approximate, which is why `wide-measure` exists as a geometry-based backstop. Body is chosen by paragraph mass (multi-line aligned blocks), falling back to raw char count on pages with no prose blocks.
- Cannot identify typefaces, so "these two fonts look alike" (family-level similarity) is out of scope; size/weight similarity is what it measures.
- Latin-tuned: cap-ratio, advance clamps, and mixed-case detection assume proportional Latin text. CJK, Arabic, condensed/display faces, and code blocks will misestimate.
- Measures ink, not typographic axes: leading uses ink-top pitch (not baselines), alignment uses first-glyph ink edges, "tracking" is raw inter-component gap — conservative thresholds absorb most of this, but treat single warns near a threshold as borderline.
- Very stylized text (gradients on gradients, outlines, < ~8px, heavy blur) may be missed; photos and illustrations are filtered but can leak noise lines.
- Single-image analysis; it knows nothing about breakpoints it hasn't seen.
</limitations>
