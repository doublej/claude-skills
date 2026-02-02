---
name: message-rewriter
description: Rewrite rough notes or existing text into natural, platform-native messages for Slack, Email, WhatsApp, and Telegram in the user's voice. Use when drafting or rewriting messages for a specific platform.
---

# Message Rewriter

Rewrite text into natural, platform-native messages. Two modes: quick (default) and guided.

## Mode Routing

**Quick Mode** — User provides content + target platform. Rewrite immediately, no questions.
- "Rewrite this for Slack: ..."
- "Make this a WhatsApp message: ..."
- "Email version of: ..."

**Guided Mode** — Input is very rough, ambiguous, or user asks for help shaping the message.
- "Help me write a message to my team about..."
- Bullet points with no clear structure
- User explicitly asks for guidance

When in doubt, default to Quick Mode.

## Quick Mode

1. Detect target platform
2. Read `references/voice-samples.md` — if samples exist for this platform, extract voice profile
3. Apply platform rules (see Platform Rules below + `references/platform-{name}.md`)
4. Check against `references/banned-words.md`
5. Output the rewritten message, ready to copy

## Guided Mode

### BRIEF
Gather what's missing:
- **To whom?** — Recipient/audience (team, client, friend, manager)
- **About what?** — Core point in one sentence
- **Desired outcome?** — What should the reader do/feel/know after reading?
- **Platform** — Slack, Email, WhatsApp, or Telegram

Ask at most 2 questions. Infer the rest.

### DRAFT
Write the message applying voice + platform rules.

### REFINE (optional)
Only if user requests changes. Apply tone modifiers and iterate.

## Voice Calibration

Read `references/voice-samples.md`. If samples exist for the target platform, extract:
- Sentence length (short bursts / mixed / longer)
- Greeting and sign-off patterns
- Formality level
- Emoji usage (none / functional / expressive)
- Paragraph rhythm (single lines / short blocks)
- Directness vs softening
- First person style (I / we / avoided)

Summarize as 3-4 bullet voice profile before drafting:

```
Voice profile:
- Short sentences, direct. No fluff.
- Opens with "Hey" for Slack, no greeting for WhatsApp.
- Rare emoji, only thumbs-up or checkmark.
- Signs off emails with "Cheers," — never "Best regards."
```

When no samples exist: default to direct and natural. No corporate tone.

## Platform Rules

| Platform | Register | Key trait | Reference |
|----------|----------|-----------|-----------|
| Slack | Professional-casual | Point on line 1, thread-aware | `references/platform-slack.md` |
| Email | Formal spectrum | Subject line matters, paragraph discipline | `references/platform-email.md` |
| WhatsApp | Very casual | Speech-like bursts, can split messages | `references/platform-whatsapp.md` |
| Telegram | Medium-casual | Rich formatting ok, longer messages fine | `references/platform-telegram.md` |

Read the relevant platform reference file before drafting.

## Cross-Platform Rules

### Banned Words
Check every sentence against `references/banned-words.md`. Worst offenders:

> leverage, synergy, comprehensive, robust, "I hope this email finds you well", "please do not hesitate to", "at your earliest convenience", "just wanted to reach out", "I'm thrilled", "excited to share", "as per my last"

If you catch any: delete and rewrite in plain language.

### Anti-Slop
- No corporate buzzwords in casual messages
- No filler phrases that add zero information
- No hedging where directness works ("I was just wondering if maybe..." -> "Can you...")
- No AI-typical sentence patterns (see AI Giveaways below)

### AI Giveaways — Hard Rules
These are dead tells that text was AI-generated. Catch and fix every one.

**Punctuation:**
- Never use em-dashes (—). Use a comma, period, or rewrite the sentence.
- Never use semicolons in casual messages (Slack, WhatsApp, Telegram). Rare in email.

**Structure:**
- No "Not only X, but also Y" constructions
- No "Whether it's X or Y, Z" openers
- No triple-adjective lists ("fast, reliable, and scalable")
- No mirrored sentence pairs ("X is great. But Y is even better.")
- No "This means..." or "What this means is..." transitions
- No sentences starting with "Interestingly," "Importantly," "Notably," or "Crucially"

**Tone:**
- No over-enthusiasm that the user didn't put in the source text
- No false empathy ("I completely understand...")
- No summarizing what someone just said back to them
- No "Great question!" or "That's a great point!" energy

**Word patterns:**
- Check `references/banned-words.md` — includes AI slop words and dead phrases
- If a word feels like it belongs in a LinkedIn post, cut it

### Length Discipline
- Slack: 1-4 lines for status updates, up to a short paragraph for context
- Email: as short as possible while being complete
- WhatsApp: 1-3 short bursts, never a wall of text
- Telegram: can be longer but stay focused

## Input Handling

**Rough notes / bullet points:** Construct a coherent message from fragments. Fill gaps with reasonable assumptions. Don't ask about every missing detail.

**Existing text (too formal, wrong platform, needs rewriting):** Reshape to match target platform. Preserve the core message. Strip what doesn't belong.

**Platform conversion:** When converting between platforms (e.g., email -> Slack), don't just shorten — restructure for how people read on that platform.

## Tone Modifiers

User can request these on top of platform defaults:

| Modifier | Effect |
|----------|--------|
| softer | Add courtesy, soften directives, more "would you mind" |
| firmer | Remove hedging, stronger language, clear expectations |
| urgent | Front-load the ask, add time pressure, trim context |
| formal | Full sentences, proper structure, no contractions |
| casual | Contractions, shorter sentences, conversational |

Modifiers stack on platform rules, they don't replace them.

## Output Format

Present the rewritten message in a code block, ready to copy:

~~~
[The rewritten message here]
~~~

For email, include subject line above the code block:

**Subject:** [subject line]
~~~
[Email body here]
~~~

If the message could reasonably be split (WhatsApp), show the split:

~~~
Message 1:
[first part]

Message 2:
[second part]
~~~

No commentary after the output unless the user asks for explanation.
