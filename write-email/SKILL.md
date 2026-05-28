---
name: write-email
description: "Write emails that read human, not AI. Strips em-dashes, zero-width watermarks, RTF/HTML residue, and slop phrases before output. Triggers on \"write an email\", \"draft an email\", \"reply to this email\", or pasted email text the user wants rewritten."
---

# Human Email Writer

Draft emails that read like a person wrote them. Run every draft through `scripts/clean.py` before outputting.

<workflow>

1. **Brief** — get the four facts (recipient, point, desired outcome, tone). Ask at most 2 questions if any are missing. Skip when obvious.
2. **Draft** — apply email rules + anti-slop (`references/email-anti-slop.md`).
3. **Filter** — pipe the draft through `scripts/clean.py`. Use the cleaned output.
4. **Output** — subject line on its own, then the body in a fenced block. No commentary unless asked.

</workflow>

<filter_step>

The filter strips AI watermarks the user pastes around all day. Always run it — even on drafts you wrote yourself, since em-dashes sneak in.

```bash
echo "$DRAFT" | python3 scripts/clean.py
```

What it removes:
- Em-dashes: ` —` → `,` and bare `—` → `, ` (matches the user's raycast clean-watermark exactly)
- Zero-width chars: `​`, `‌`, `‍`, `﻿`, `⁠`, NBSP, all U+2000–U+200A spaces, line/paragraph separators, BiDi controls
- Non-printable control bytes
- RTF residue (`\rtf1`, `\fonttbl`, `\par`, etc.)
- HTML font/style/class/span/div/p/meta tags and inline `font-family:`, `color:`, `background:` declarations
- GUIDs (8-4-4-4-12 hex)
- Trailing whitespace, runs of 3+ blank lines, double spaces
- NFKC-normalizes the whole thing first

What it does NOT remove (use the LLM, not the filter):
- Slop phrases ("I hope this email finds you well")
- Slop words ("delve", "leverage", "robust")
- Bad rhythm or AI-shaped paragraphs

So: filter strips mechanical tells, the writing pass strips lexical tells. Both required.

</filter_step>

<email_rules>

### Subject

- Specific and scannable. No "Quick question", "Following up", "Hello".
- Action type when relevant: "Review needed:", "FYI:", "Decision by Friday:".
- Under 8 words.

### Structure

- **Line 1**: state what this email is about and what you need. No "I hope this finds you well."
- **Body**: 1–3 short paragraphs. One idea per paragraph.
- **Close**: clear next step. Who does what by when. Not "let me know your thoughts."
- **Sign-off**: match the relationship. "Cheers," / "Thanks," / "Best,". Never "Warm regards", "Kind regards", "Kindly".

### Length

- Reply emails are shorter than the original.
- Mobile-screen-readable without scrolling when possible.
- More than 3 short paragraphs → ask if it should be a doc or call instead.

### Tone register

| Register | Use for | Cues |
|----------|---------|------|
| internal | team, peers | direct, skip pleasantries, contractions ok |
| client | external, professional warmth | brief greeting, courteous close, no jargon |
| upward | execs, decision-makers | bottom line first, context after, respect their time |

</email_rules>

<difficult_messages>

For rejections, bad news, complaints, escalations:

- Lead with the decision. Don't bury the "no".
- One sentence of context, not a paragraph of justification.
- One "sorry" max. Over-apologising sounds insincere.
- Don't soften so much the message becomes ambiguous.
- End with a concrete next step, not "let me know."

</difficult_messages>

<sentence_variety>

AI emails alternate short-long-short-long like a metronome. Real writing is irregular.

- Vary sentence length unpredictably. Three short in a row is fine.
- Don't start consecutive sentences the same way.
- Mix statements, fragments, occasional questions. Not every sentence needs subject-verb-object.
- Read it aloud before delivering. If it sounds like a speech, rewrite.

</sentence_variety>

<voice_calibration>

If `references/voice-samples.md` has filled-in samples, read them before drafting. Extract: greeting/sign-off habits, contraction use, formality level, paragraph length, how the user opens.

No samples? Default to direct and natural.

</voice_calibration>

<output_format>

```
Subject: [subject line]
~~~
[Body, after running through clean.py]
~~~
```

After output, mention what the filter removed if it removed anything (one line, e.g. "Filter: 2 em-dashes, 1 zero-width"). If it removed nothing, say nothing.

</output_format>

<self_check>

Before output, verify:
- [ ] Ran `scripts/clean.py` on the draft
- [ ] Zero phrases from `references/email-anti-slop.md`
- [ ] Subject is specific (not "Quick question")
- [ ] Line 1 states the point
- [ ] Close has a concrete next step
- [ ] No em-dashes survived (filter handles, but spot-check)
- [ ] Sign-off matches relationship register

Any unchecked → fix before outputting.

</self_check>
