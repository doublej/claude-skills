# Slack Message Rules

## Structure
- **Line 1 is the message.** Lead with the point, context after.
- Use line breaks to separate concerns — don't write paragraphs.
- Bold key info: names, deadlines, decisions.
- Use bullet lists for multiple items, never numbered lists for casual updates.

## Threading
- If the message is a reply or follow-up, assume thread context — skip re-explaining.
- For channel posts that need discussion: end with a clear prompt or question.
- Keep top-level messages scannable — details go in thread replies.

## Formatting
- `code` for technical terms, commands, file names.
- *italic* for emphasis (sparingly).
- **bold** for action items and key info.
- > blockquote for quoting others or highlighting a decision.
- Emoji: functional only (:white_check_mark:, :warning:, :eyes:). Never decorative.

## Tone
- Professional but not stiff. Write like a competent colleague.
- No "Hi team," opener unless the channel is large or formal.
- No sign-off. Slack messages don't end with "Thanks," or "Best,".
- Contractions are fine. "We're" not "We are".

## Length
- Status updates: 1-3 lines.
- Requests: state what you need + why + deadline in under 5 lines.
- Announcements: short paragraph + bullet points for details.
- If it needs more than ~8 lines, it should be a doc with a Slack summary linking to it.

## Common Patterns

**Request:**
```
Can you review the PR for auth changes? Need it merged before EOD — blocks the release.
```

**Update:**
```
Shipped the dashboard fix. Monitoring for the next hour, will update in thread.
```

**Decision needed:**
```
We need to pick a direction on the API versioning:
• Option A: URL path versioning (`/v2/users`)
• Option B: Header-based versioning

Leaning toward A for simplicity. Thoughts?
```
