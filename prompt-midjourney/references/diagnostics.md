# Scoring, gap analysis, and failure modes

Use after a generation, when the user shares output images or describes what came back wrong.

<scoring>

Score every image on the same seven dimensions. Score all seven every time — give 1.0 to any that
genuinely does not apply, rather than dropping it, so scores stay comparable across iterations.

| Dimension | Question |
|---|---|
| Subject | Is the right thing depicted, doing the right thing? |
| Lighting | Does the light setup match intent? |
| Colour | Is the palette right in hue and saturation? |
| Mood | Does it feel the way it should? |
| Composition | Framing, placement, negative space, crop |
| Material | Surfaces, texture, finish, wear |
| Spatial | Depth, scale relationships, perspective |

Score 0–1 per dimension. The overall score is the mean, but **act on the lowest dimension, not the mean** —
a 0.90 mean hiding a 0.55 on composition is a composition problem, not a good image.

Two rules that keep this honest:
- **Scores are preliminary until the user validates them.** State them as readings, not verdicts.
- **Say when a dimension can't be judged** from what was shared (e.g. material at low resolution) rather than inventing a number.

</scoring>

<gap_to_action>

The most valuable decision in the loop: given the gap, what do you actually change?

| Gap | Action | Why |
|---|---|---|
| Everything roughly right, one small flaw | **Vary Subtle** | Preserves the equilibrium that already works |
| Right idea, wrong execution across the frame | **Vary Strong** | Same prompt, meaningfully different draw |
| One dimension badly wrong, rest good | **Targeted prompt edit** — change only the words for that dimension | Isolates cause from effect |
| Wrong subject or wrong concept | **Rewrite the prompt** | The prompt is the problem, not the sample |
| Unwanted element keeps appearing | **`--no`** it | Cheaper than rewording around it |
| Look is right but style is off, and words aren't getting there | **Add `--sref`** | Some qualities (grain character, colour grade) resist description |
| Style bleeding too hard into subject | **Lower `--sw`** or add explicit subject detail | Reference is outweighing the prompt |
| Likeness drifting on a referenced subject | **Raise `--ow`** toward 300+ | Stylization is overwriting identity |
| Output too "Midjourney", too beautified | **`--raw`**, lower `--s` | House aesthetic is asserting itself |
| Output flat and generic | **Raise `--s`**, or `--exp 10–25` | Under-stylized |
| Only one region is wrong | **Edit / Vary Region** on that region | Preserves everything already correct |
| Frame is too tight | **Zoom Out / Pan** | Cheaper than re-prompting composition |
| No idea what look is wanted | **`--draft` + `--sref random`** | 24 different styles in one job |
| Grid is too samey | **Raise `--chaos`** | Widens the spread between the four |

Note: Pan, Zoom Out, and Edit/Vary Region **downscale an HD image to SD** — re-upscale afterwards.

</gap_to_action>

<iteration_discipline>

- **Change one aspect at a time.** Two simultaneous changes make the result uninterpretable.
- **Above ~0.85 overall, prefer Vary Subtle to rewriting.** High-scoring prompts are fragile equilibria; a rewrite usually trades one strong dimension for another.
- **Some dimensions genuinely trade against each other.** Heavy grain fights flat lighting; high stylize fights likeness. When two iterations in opposite directions both lose ground, stop optimising and name the tradeoff to the user — accepting a balanced result is a legitimate outcome.
- **Sub-object placement is not reliably promptable.** For "logo on the left side of the mug", generate a batch and select rather than iterating on wording.
- **Log what changed and what moved.** Even within one session, "we already tried that and it cost us lighting" is the most useful thing you can say.

</iteration_discipline>

<failure_modes>

Symptom → cause → fix. Check here before rewriting a prompt from scratch.

**Subject**

| Symptom | Cause | Fix |
|---|---|---|
| Wrong subject entirely | Subject buried mid-prompt | Front-load it |
| Key element missing | Too many concepts competing | Cut to essentials, add back one at a time |
| Extra unwanted elements | No exclusions | `--no` |
| Subject rendered in the wrong style | Style bleeding | `--raw`, or separate style words from subject words |
| Face drifts across the grid | No identity anchor | `--oref` + `--ow 300+` |

**Composition**

| Symptom | Cause | Fix |
|---|---|---|
| Subject in the wrong place | No position language | State it: "subject at the far right" |
| No room for type | "negative space" read as an art term | Describe the empty area physically |
| Too zoomed in | No framing guidance | "wide shot", "extreme wide angle" |
| Too zoomed out | Subject described too thinly | Add details that demand a closer frame |
| Collage / arranged layout instead of one scene | An aesthetic keyword ("zine", "collage", "moodboard") is driving layout | Remove it, use material words instead |
| Three-quarter angle when frontal wanted | MJ's default perspective bias | "flat frontal view", "orthographic" |
| Continuous pattern fills the frame | Pattern/swirl words | "scattered discrete forms floating in a dark void" |
| Gradient runs the wrong way | No direction given | "from [colour] at the top to [colour] at the bottom" — avoid bare "vertical", it triggers stripes |

**Light, colour, mood**

| Symptom | Cause | Fix |
|---|---|---|
| Too bright / cheerful | Generic lighting words | Name the setup; add "moody", "low-key" |
| Too dark | No warmth | "warm", "inviting", raise ambient |
| Flat and lifeless | Low stylize, no atmosphere | Raise `--s`, add atmospheric detail (haze, dust, rain) |
| Wrong palette | Not specified | State 2–3 colours explicitly |
| Oversaturated | MJ beautification | `--raw`, "muted", "desaturated" |
| Colours clash | Too many colour mentions | Limit to 2–3 |
| Plastic, airbrushed skin | Quality-spam words | Delete them; add film stock + a physical skin detail (pores, freckles, stubble) |

**Text**

| Symptom | Cause | Fix |
|---|---|---|
| Garbled letters | String too long | 1–4 words, in quotes |
| Text ignored | Not quoted | `a sign reading "OPEN"` |
| Right text, wrong style | No treatment described | "hand-painted serif", "vinyl-cut sans" |

**Parameters**

| Symptom | Cause | Fix |
|---|---|---|
| Flag appears as literal text in the image | Em dash instead of `--`, or flag mid-prompt | Run `scripts/lint_prompt.py` |
| Aspect ratio ignored | Ratio beyond the cap | 14:1 max, 4:1 in HD |
| Style reference has no effect | `--sw` too low, or old code needing `--sv 4`/`--sv 6` | Raise `--sw`; set the matching `--sv` |
| Output inexplicably off-brief | A Personalization profile is silently applied | Check `--p`; try without |

</failure_modes>

<attribution>

Diagnostic tables and the seven-dimension rubric adapted from JustinPerea/midjourney-cc-skill (MIT), whose entries were extracted from logged generation sessions. Actions updated for the V8 family.

</attribution>
