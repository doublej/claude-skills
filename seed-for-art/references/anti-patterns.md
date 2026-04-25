# Anti-patterns

The AI-slop failure modes this skill exists to close off. Read once per session, before stage 1.

## The largest failure mode — melancholy by default

Condensation is structurally elegiac. When you strip names, dates, and argument from any source, the surviving grammar is "object + condition", which reads as *what remains* and *what does not arrive*. Without active counter-pressure, every seed drifts into lament — even on neutral, light, or technical source material.

**The canonical ORAC run is not a model of "always be elegiac".** It is a model of *elegiac source rendered into a warm brief*. The lift from dirge to wit happened because stage 3 actively pushed back. This skill is structured so that the pushback starts at stage 1.

Counter-pressure rules:

| Rule | Why |
|------|-----|
| Pick the register in step 1 of the workflow, before any drafting. | Drift sets in within the first three fragments. |
| Default to `warm`. Choose `elegiac` only when the work IS a lament. | The default of any condensation engine is mournful; you have to opt out actively. |
| Presence/absence split: ≥40 % of fragments inventory what is *here*. | Single-mode lists of losses are how seeds collapse into elegy. |
| Use the verb whitelist for the chosen register. | Verbs do most of the affect work. *Decays / drifts / removes* lock in mourning regardless of subject. |
| Banned vocabulary by default: ghost, lament, mourn, void, decay, ruin, hollow, withered, fading, all that remains. | These words feel literary; they do the dour-default's lifting. Replace with concrete observation in the chosen register. |
| Form encodes affect. A liturgy IS funereal-pattern; missing-persons IS elegy-form. Pick the cassette before drafting. | You cannot save a liturgy with cheerful words; the form will dominate. |

If a seed comes back depressing despite a non-elegiac register, the failure is almost always one of: (1) absence-fragments dominate, (2) banned vocabulary leaked through, or (3) a stage-2 form was inherited from the elegiac cassette by accident.

## Slop in fragments and motifs

| Avoid | Why | Instead |
|-------|-----|---------|
| "Moody and atmospheric." | Adjectives that describe nothing. Image models invent generic dusk. | Named artist + hex palette: *Tom Gauld linework on `#F4EFE4` ground, `#E30613` accent.* |
| "A figure stands in shadow." | Anonymous human archetype. Reads as stock illustration every time. | Posture + prop + action: *a civil-servant silhouette walks away with a manila folder; one page flutters loose.* |
| Adjective-stacked motifs ("the lonely sad container"). | Adjectives are decoration. Image models lock onto nouns and verbs. | Concrete object + abstract framing: *the container as metronome — bureaucracy's rhythm section.* |
| Fragments that argue. | Argument belongs in the letter, not the seed. The seed remains; the letter wins. | Condensation: *I am not the client. I am its nervous system.* |
| Names, dates, addresses inside fragments. | Locks the seed to one case. Future re-use breaks. | Strip proper nouns; keep institutional roles (the committee, the resident, the file). |

## Slop in the brief

| Avoid | Why | Instead |
|-------|-----|---------|
| Colour names ("ochre", "warm cream"). | Drift across tools and prints. | Hex codes (`#E3B43B`, `#F4EFE4`). |
| "Minimalist editorial style." | Does not discriminate. Half the internet is "minimalist editorial". | Named artists with weighting: *Gauld before Gorey, Favre before Le Tan.* |
| Generic NOT-list ("no clichés, no AI look"). | Closes nothing. Lazy paths remain open. | Domain-specific NOT-list: *no Utrecht skyline, no Dom tower, no heraldic shield, no anthropomorphised containers.* |
| Single mega-prompt for all N images. | Image models compress the joke; the illustrator picks one. | Per-image specs — concept, caption, thumbnail test. |
| Five images that each try to say everything. | The set becomes one redundant image, repeated. | One thesis per image. The set is the argument; each image is one beat. |
| Captions only in source language *or* only in English. | Source-language only locks out wider audience. English only loses case-specific weight. | Bilingual when domain-relevant; declare register explicitly. |
| Tone tags as parallel list ("warm, witty, critical"). | No priority. Image models average the list. | Hierarchy: *warm first, witty second, critical third.* |
| No caption per image. | Composition floats. Reader has no anchor. | Each image carries a caption in serif italic with a literary point. |
| No thumbnail test. | Image that needs full size to read fails on web. | Each spec includes silhouette test + reward-detail test. |
| Brief with no permission to refuse. | Illustrator follows literally; output is the brief in pictures, not a piece of art. | Closing note: *treat this as grammar, not instruction. Any image may be refused and replaced.* |

## Slop in the variations

| Avoid | Why | Instead |
|-------|-----|---------|
| Nine variations that read alike. | Defeats the point. The register-shift IS the work. | Genuinely distinct voices. Inventory ≠ liturgy ≠ instructions ≠ glossary. |
| Variations that retell the source. | Repeats the letter. | Re-form the seed *through* the register. The source is in the air; only the form changes. |
| Glossary with single definitions. | Loses the joke. | Stacked definitions: 1. formal. 2. sardonic, lived. |
| Instructions that name the case. | Specific to one user. Not reusable as art. | Generic *role* (the citizen, the patient, the resident, the maintainer) — the second person carries the case without naming it. |
| Diary entries with full dates. | Dates lock to a calendar. | Italic month/year only. Or no date — *"the day after"*. |

## The single largest failure mode

Going `data → image` directly. Skipping stages 1 and 2 to "save time" is what produces AI slop. The two intermediate distillations are not ceremonial — they are the value. Every stage is a literalism filter.

If a user asks to skip stages, push back once: the result will be visibly worse. If they insist, comply and note in the output that stages were skipped.
