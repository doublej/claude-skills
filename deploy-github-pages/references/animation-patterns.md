# Animation patterns

The site has one moving thing: the terminal. Everything else is still, so the demo is where the eye goes.

<motion>
| Motion | Where | How |
|---|---|---|
| Line print | `Terminal.svelte` | Each direct child of the body is hidden, then shown at 0.35s, 0.45s, 0.55s … (capped at 0.95s from line 8). Instant, like real output; no fades or slides. |
| Cursor | `Terminal.svelte` | Plate-coloured block after the last line, blinking with `steps(1)` every 1.1s. |
| Replay | Home demo | `{#key step}` around `<Terminal>` remounts it, so switching steps prints the new output again. |
| Interaction feedback | Toggles, step list, nav, copy button | 0.15s colour/background transitions only. Copy button text changes to "Copied" for 2s. |
</motion>

<rules>
- Do not add entrance animations to sections, cards or headings. No fade-and-slide on scroll.
- Do not add hover lifts or shadows to feature items.
- To replay a terminal when its content changes, wrap it in `{#key value}`; do not animate individual spans.
- Keep a terminal demo to about 8 lines per frame. Past line 8, lines share the last delay.
- The demo terminal has `min-height: 11em` so switching steps does not shift the page; raise it if the longest step is taller.
</rules>

<reduced_motion>
`global.css` ends with:

```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

With animations off, every terminal line is visible at once and the cursor is a static block. Nothing depends on an animation finishing, so keep it that way: never hide content with an animation that has no end state.
</reduced_motion>
