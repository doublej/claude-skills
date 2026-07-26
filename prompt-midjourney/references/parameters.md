# Midjourney parameters — V8 family

<freshness>

Verified against Midjourney changelog and practitioner docs on **2026-07-27**. Current default: **V8.2** (since 2026-07-24).

Midjourney shipped V8.0 → V8.1 → V8.2 in four months. Treat this file as a cache, not as truth.
Before relying on any parameter in a high-stakes job, check <https://updates.midjourney.com>.
`docs.midjourney.com` blocks automated fetching — use the changelog host or ask the user to paste the doc page.

</freshness>

<version_timeline>

| Version | Status | Notes |
|---|---|---|
| V8.2 | **default since 2026-07-24** | Aesthetics, image quality, Personalization. Bolder, edgier, more sophisticated output |
| V8.1 | selectable (was default 2026-06-10 → 07-23) | Fastest V8 variant. Draft Mode. Aesthetic closest to V7 |
| V8.0 | deprecated | Alpha, 2026-03-17. Retired shortly after V8.1 |
| V7 | selectable | Still the only model with native `--oref` and `--q` |
| Niji 7 | selectable via `--niji 7` | Anime/manga. Supports Personalization and Moodboards |

Style references, Personalization profiles, and aesthetics carry over between V7 and V8.x — a V7 profile still works.

</version_timeline>

<resolution>

HD is the headline V8 change. It renders natively at 2K — no separate upscale step.

| Flag | Effect | Cost | Speed |
|---|---|---|---|
| `--hd` | native 2048px | ~1.3 GPU min | ~12s |
| `--sd` | standard definition | ~0.8 GPU min | ~4s |

Two constraints that bite:
- **HD caps aspect ratio at 4:1.** Outside HD the cap is 14:1.
- **Pan, Zoom Out, and Edit/Vary Region downscale an HD image to SD.** Re-upscale afterwards to get back to HD.

Working pattern: explore in SD (or Draft), then rerun the keeper seed-locked as HD.

</resolution>

<core_parameters>

| Flag | Range | Default | Use |
|---|---|---|---|
| `--ar W:H` | up to 14:1 (4:1 in HD) | 1:1 | aspect ratio |
| `--s`, `--stylize` | 0–1000 | 100 | MJ aesthetic push. 0–50 literal/photoreal, 100–300 balanced, 300+ artistic |
| `--chaos`, `--c` | 0–100 | 0 | spread between the four images in a grid |
| `--weird` | 0–3000 | 0 | unconventional aesthetics. 100–500 subtle, 1000–2000 strange, 2000+ maximum |
| `--exp` | 0–100 | 0 | experimental detail and dynamics. **10–25 is the sweet spot**; higher overwhelms stylize and personalization |
| `--raw` | — | off | strip MJ's house aesthetic, interpret the prompt literally. V7 spelling was `--style raw` |
| `--no x, y` | — | — | exclude elements |
| `--seed N` | — | random | reproducibility. V8 is ~99% identical on reseed, not byte-exact |
| `--iw` | 0–2 | 1 | weight of an image prompt (a bare image URL at the start), not of `--sref`/`--oref` |
| `--stop` | 10–100 | 100 | halt generation early for a softer, less resolved image |
| `--draft` | — | off | 24 images per job at half cost; click Vary to render one at full res |
| `--tile` | — | off | seamlessly tiling texture |
| `--motion low\|high` | — | low | video only |

</core_parameters>

<reference_systems>

Three separate systems. Picking the wrong one is the most common structural mistake.

| Want to transfer | Use | Weight flag |
|---|---|---|
| Aesthetic — palette, light quality, grain, rendering | `--sref <url\|code>` | `--sw 0–1000` (default 100) |
| A subject — this face, this jacket, this product | `--oref <url>` | `--ow 0–1000` (default 100) |
| Your own accumulated taste | `--p` / moodboard | — |
| Composition/content of a whole image | bare image URL at prompt start | `--iw 0–2` |

**Style reference `--sref`**
- Accepts an image URL, a numeric style code, or several blended: `--sref 1234 5678`.
- Weight per reference with `::`-free syntax by repeating: MJ blends multiple srefs; bias by listing weights in the UI or splitting jobs.
- `--sw` guidance: 0–50 subtle · 100–150 inspired-by · 200–250 same style, new subject · 300+ dominant, near-copy.
- `--sref random` (V8.1+, Draft Mode) gives each of the 24 draft images a different random style. This is the fastest style-discovery tool that exists — use it when the user cannot describe the look they want.
- `--sv` selects sref algorithm version. `--sv 7` is current (4x faster and cheaper, supports `--hd`, `--p`, `--stylize`, `--exp`). `--sv 4` / `--sv 6` reproduce pre-2026 style codes; old codes need them.
- V7 srefs drifted badly across a grid. V8.1 fixed this — a sref now holds across all four images.

**Omni reference `--oref`**
- Replaced `--cref` (dead since V6). Transfers identity: face, body, clothing, an object.
- **`--oref` still routes through V7 even when V8 is selected** — the V8-native version is in training. Expect V7 aesthetics on referenced subjects, and expect that this is the parameter most likely to change next.
- `--ow` guidance: 0–30 loose inspiration · 60–100 clear resemblance · 300+ maximum fidelity.
- Raise `--ow` when running high `--s` or `--exp`, or the stylization overwrites the likeness.

**Personalization `--p`**
- `--p` applies the default profile; `--p <mID>` or `--profile <mID>` selects a specific moodboard.
- Stability tiers: 40 ratings minimum to activate, ~200 for fairly stable, ~2000 for maximum refinement.
- A profile is a persistent taste bias. When output is inexplicably off-brief, check whether a profile is silently applied.

</reference_systems>

<dead_parameters>

Do not emit these. `scripts/lint_prompt.py` catches them.

| Flag | Status |
|---|---|
| `--cref`, `--cw` | dead after V6. Use `--oref` + `--ow` |
| `--q`, `--quality` | V7-only. V8 has no quality flag — use `--hd` / `--sd` |
| `--turbo` | gone on V8. Use `--draft` for speed |
| `--style raw` | V7 spelling. V8 uses `--raw` |
| `::` multi-prompt weighting | unsupported since V7 |
| `--uplight`, `--upbeta`, `--test`, `--testp` | V4 era |

`--fast` / `--relax` are account modes, not prompt parameters.

</dead_parameters>

<prompt_structure>

V8 has strong natural-language understanding. Short prompts beat long ones, and the front of the prompt carries the most weight.

```
[subject] [subject details] [environment] [style/mood] [technical: camera, light, stock] [--flags]
```

Rules that hold up in practice:
- **Front-load the subject.** Word position is weight.
- **Under ~40 words.** Past that, terms start competing and diluting. Start short, add back only what the output is missing.
- **Abstract concepts work directly** on V7+ — "ethereal nostalgia", "institutional dread" land as written. This was not true on V6.
- **Quote text you want rendered**: `a neon sign reading "OPEN"`. Keep it to 1–4 words; longer strings garble.
- **Parameters go at the very end.** A flag in the middle breaks the parser.
- **Two ASCII hyphens.** An em dash from a formatted document silently turns the flag into prose.

</prompt_structure>

<attribution>

Parameter ranges and reference-system guidance cross-checked against the Midjourney changelog (updates.midjourney.com), practitioner guides (blakecrosley.com/guides/midjourney, ud.hk V8.1 guide), and JustinPerea/midjourney-cc-skill (MIT) — whose V7 material was corrected against V8 where the two disagree.

</attribution>
