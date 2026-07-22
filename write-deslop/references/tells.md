# AI Copywriting Tells — Catalog & Fix Strategies

Researched July 2026 across corpus studies (Science Advances, COLING), detector data (GPTZero, Originality.ai, Pangram), Wikipedia WP:AITELLS, and 20+ practitioner sources. scan.py detects the mechanical subset; the judgment tells (sections 7–9) only a reading pass catches.

<meta_rules>
1. **Density convicts, presence doesn't.** Every tell occurs in human writing. 4+ co-occurring tells is the AI signature. Never nuke a single em-dash and call it fixed.
2. **Tells are era-stamped.** Word lists decay as models get patched; structure and substance tells survive. Weight the reading pass over the word hits.
3. **The tell migrated:** vocabulary (2024) → structure (2025) → substance (2026: "confident vagueness" — copy that explains instead of asserts).
</meta_rules>

<lexical>
## 1. Lexical (scan.py: word findings)

Delve-cluster at 10–30x human baseline: delve (28x), underscore (13.8x), showcase (10.7x), boast, intricate, meticulous, tapestry, testament, pivotal, realm, seamless, robust, leverage, foster, elevate, unlock, unleash, game-changer, ever-evolving, landscape, journey, ecosystem.

Quantified phrases: "play a significant role in shaping" (182x), "today's fast-paced world" (107x), "aims to explore" (50x).

**Fix:** replace with the plain word (use, help, show, is) or — better — with the specific fact the hype word papered over. "Seamless integration" → "connects to Stripe in one click". Copula avoidance ("serves as", "stands as", "boasts") → plain "is/has".
</lexical>

<rhetorical>
## 2. Rhetorical templates (scan.py: phrase/rhetoric findings)

- **Negative parallelism** "It's not X, it's Y" + variants ("isn't just", "less about X, more about Y") — the #1 cited tell; Fortune 500 filings 50→200+ (2023→2025)
- "Not just X, but also Y" — means "both", pure cadence
- **Rule of three** — adjective triplets, three bullets, three benefits at every level
- Staccato triplet — "No fluff. No filler. No B.S."
- "From X to Y" fake-breadth sweep
- "Whether you're A or B" false-inclusivity
- Rhetorical-question transitions — "The result?", "But here's the thing:"
- Participial riders — ", highlighting the importance of", ", underscoring the need for" (2–5x human rate)
- Elegant variation — synonym rotation ("the artist… the painter… the creator") where a human repeats the noun

**Fix:** state Y directly and cut the negated strawman. Break triads: keep the strongest item, or make it two or four. Answer the rhetorical question before it's asked. Delete the -ing rider or promote it to its own sentence with a subject. These are legitimate devices — allow at most ONE deliberate use per piece.
</rhetorical>

<punctuation>
## 3. Punctuation & typography (scan.py: structure findings)

- Em-dash saturation (>3/1k words suspect, >8 strong) — the tell is density, not presence
- Curly quotes mixed into straight-quote text (the mix is the tell)
- 100%-consistent Oxford comma (humans drift)
- Paragraph-initial "However,/Moreover,/Additionally," at machine rates
- Emoji as formatting (🚀✅💡 on headings/bullets)

**Fix:** em-dashes → comma, colon, period, or parentheses depending on the joint. Normalize quotes to the document's style. Cut connective openers — paragraphs rarely need them; the logic should be in the content. Writer skill's `clean.py` handles the Unicode/mechanical layer.
</punctuation>

<rhythm>
## 4. Rhythm (scan.py: low burstiness metric)

- Sentence-length CV < 0.35 = uniform rhythm (human prose alternates long/short in bursts)
- Uniform paragraph mass — every paragraph 3–4 sentences doing claim → elaboration → mini-summary
- Near-constant SVO order

**Fix:** rewrite for variance, not average. Add a 3-word sentence. Let one run long. Merge two uniform paragraphs, split another mid-thought. Read aloud — flat rhythm is audible.
</rhythm>

<discourse>
## 5. Discourse structure (reading pass)

- Five-paragraph-essay skeleton regardless of genre
- "In conclusion" restating what was just said
- Hedging blanket — "generally", "typically", "can vary", "it's worth noting"
- Both-sidesism — every viewpoint one balanced paragraph, no position taken
- Sycophantic openers ("Great question!") and wrap-up moralizing ("Ultimately, X reminds us…")
- "Challenges and Future Prospects" formula

**Fix:** delete the conclusion if it adds nothing (it usually adds nothing). Take a position — copy that refuses to commit converts nothing. Cut every hedge that isn't legally required; where nuance matters, state the specific condition instead of "typically".
</discourse>

<formatting>
## 6. Formatting (scan.py: structure findings)

- Bullet reflex — lists where prose belongs
- "**Term:** explanation" lead-in down an entire list
- Boldface saturation; heading every 80 words; Title Case Headers in sentence-case house style
- Tables for trivial content; three same-shaped bullets per group
- Markdown artifacts bleeding into published copy (asterisks, # headings in email)

**Fix:** convert list-shaped prose back to prose when items connect causally. One bolded phrase per section max. Match the destination's header case.
</formatting>

<substance>
## 7. Substance (reading pass — most durable tier, scan.py can't catch these)

- **Zero concrete specifics** — no numbers, names, dates, prices; examples are "a small business owner", "a recent study"
- **Confident vagueness** — explains instead of asserts, restates instead of decides. Audit: what changed? for whom? compared to what? why now?
- **No first-hand texture** — nothing only a practitioner would know; no failure stories, no scars
- **Vague authority** — "experts argue", "industry reports suggest"
- **Significance inflation** — "stands as a testament", "nestled in the heart of"
- **No falsifiable claim anywhere**

**Fix (the highest-value pass):** demand specifics from the source material — real numbers, named customers, actual dates, prices, the concrete mechanism. If the source has none, ASK the user for them rather than inventing. One verifiable claim beats three superlatives.
</substance>

<copy_specific>
## 8. Sales-copy specific (reading pass)

- **Swap test** — replace the brand with a competitor; if the copy still works, it says nothing
- No villain, no enemy, no risk taken — relentless corporate-cheerful
- Fake urgency with no real deadline or offer mechanics
- Generic CTAs — "Learn More", "Get Started", "Submit" (no one wants to submit)
- Grade 10+ prose — real direct-response copy runs grade 5–7
- Writes ABOUT emotions ("You are frustrated") not FROM them (scene-level specificity)
- Headline formula regression — "X: The Ultimate Guide to Y"

**Fix:** name the enemy (the old way, the competitor category, the tax). CTA = the object of desire ("Get my teardown", not "Submit"). Shorten words and sentences until it reads at grade 6–7. Urgency only when a real mechanic backs it.
</copy_specific>

<channel_specific>
## 9. Channel tells (scan.py catches the phrases; register is a reading pass)

**Email:** "I hope this finds you well", "just circling back", fake-personalization openers ("I was impressed by [Company]"), three dense paragraphs instead of short lines + one ask, Title Case colon subjects. Fix: write like texting a colleague who happens to be a VP; lowercase specific subject lines outperform.

**LinkedIn/social:** hook → restate → listicle → moral arc; emoji-bullets on every line; "Let that sink in", "Here's the kicker", "Gone are the days"; metronomic one-line broetry; "thrilled/honored to announce". Fix: 1–2 emoji max, one concrete story beat instead of the moral.
</channel_specific>

<sources>
## Sources

- Wikipedia WP:AITELLS: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Science Advances excess vocabulary: https://www.science.org/doi/10.1126/sciadv.adt3813
- "Why Does ChatGPT Delve" (COLING 2025): https://arxiv.org/html/2412.11385v1
- GPTZero multipliers: https://gptzero.me/news/most-common-ai-vocabulary/
- Pangram pattern guide: https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns
- Negative parallelism tracking: https://ruben.substack.com/p/its-not-x-its-y
- 32-sign audit checklist: https://copyadscontent.com/signs-of-ai-writing/
- DR-copy economics: https://robpalmer.com/blog/direct-response-copywriting-ai
- Human expert detection: https://arxiv.org/abs/2501.15654
</sources>
