# Reddit / Forum Message Rules

## Structure
- Lead with the answer or solution. People scan for the useful part.
- Plain prose, short paragraphs. No headers unless the post is long.
- One point per paragraph. Break walls of text into 2-3 sentence chunks.
- Context belongs after the answer, not before it.

## Disclosure (non-negotiable)
- If the post mentions your own product, project, or company, say so plainly: "I built this", "disclosure: it's mine".
- Mention the product only when it genuinely answers the question. If a free or non-yours option fits better, name it too.
- Never lead with the product. Lead with the solution; the product is a footnote.

## Tone
- Casual-informative. Helpful peer, not a brand account.
- Lead with empathy when replying to a problem — acknowledge it before solving.
- No marketing voice, no superlatives, no call-to-action language.
- Contractions natural. Sentence fragments fine.

## What kills a post
- Sales pitch energy — instantly downvoted and flagged as spam.
- Undisclosed self-promotion — bannable, and readers notice.
- Over-formatting (bold everywhere, emoji, headers on a short reply).
- Restating the question back before answering.

## Length
- Quick reply: 1-3 sentences with the answer.
- Detailed reply: a short paragraph or two, plus a code block / link if it helps.
- If it needs more than ~4 paragraphs, it probably wants its own post.

## Formatting
- Markdown: `code` for technical references, ```fenced``` for snippets, > for quotes.
- One link, inline, only if it adds value. Bare promotional links read as spam.
- Lists only when there are genuinely multiple items.

## Common Patterns

**Helpful answer with disclosure:**
```
Had this exact problem. The fix is to set `connection_timeout` higher — the default
of 5s is too aggressive for cold starts.

Disclosure: I maintain a small tool that automates this, but honestly for one service
you don't need it, the config change above is enough.
```

**Empathy-first reply:**
```
Yeah, that error message is genuinely unhelpful, took me a while too.

It's almost always a stale lockfile. Delete it, reinstall, and it goes away.
```
