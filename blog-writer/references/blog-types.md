# Blog Post Types

Each type has a structural template. Use as a starting point — adapt to the content, not the other way around.

## Technical Post

When you solved a problem, built something, or found a better approach.

```
1. The Problem     — What broke, what was slow, what was missing
2. Context         — Why it matters, who hits this
3. Solution        — What you did, with code
4. Code / Config   — Complete, runnable examples
5. Results         — Measurable outcomes (before/after numbers)
6. Lessons         — What surprised you, what you'd do differently
```

**Open with the problem, not the technology.** "Our API response times hit 3 seconds under load" beats "In this post we'll explore Redis caching."

**Code rules:**
- Complete enough to run or adapt
- Include language identifiers in code blocks
- Comment only what isn't obvious
- Show the final version, not every iteration

## Opinion Piece

When you have a position and can defend it.

```
1. Thesis          — State your position in 1–2 sentences
2. Evidence        — Support with examples, data, experience
3. Counterargument — Steel-man the opposing view
4. Rebuttal        — Why your position holds despite the counter
5. Conclusion      — Restate thesis with nuance gained from the argument
```

**Rules:**
- State the thesis immediately. Don't sneak up on it.
- The counterargument section is mandatory. If you can't argue the other side, your position is too weak or too obvious to write about.
- Use "I think" / "In my experience" — own your opinions.
- End with something actionable, not "time will tell."

## Tutorial

When you're teaching someone to build or do something specific.

```
1. What We Build   — Show the end result upfront (screenshot, demo, output)
2. Prerequisites   — What the reader needs before starting (be specific)
3. Steps           — Numbered, each one independently verifiable
4. Complete Code   — Full working example at the end
5. Next Steps      — What to try next, where to go deeper
```

**Rules:**
- Show the finished product first. Let the reader decide if it's worth their time.
- Each step produces a visible result the reader can verify.
- Don't explain concepts inline — link to resources or add a brief aside.
- Prerequisites must be specific: "Node.js 18+" not "Node.js installed."
- Test every code example. If it doesn't run, don't publish it.

## Case Study

When you're sharing a real-world project, migration, or decision.

```
1. Situation       — Where things stood before
2. Challenge       — The specific problem or constraint
3. Approach        — What you chose and why (include rejected alternatives)
4. Results         — Measurable outcomes, honest about tradeoffs
5. Retrospective   — What you'd do differently with hindsight
```

**Rules:**
- Include numbers. "Improved performance" means nothing. "P95 latency dropped from 450ms to 80ms" means something.
- Mention what you considered and rejected — the decision process matters.
- The retrospective must be honest. If you'd make the same choices, say so and say why. If not, say what changed.
- Name real tools, frameworks, and services. Vague case studies help nobody.

## Update Post

When something changed in your product, project, or approach.

```
1. What Changed    — The change in one paragraph
2. Why             — The reason behind the change
3. How to Use It   — Concrete instructions, migration steps, or examples
4. What's Next     — Upcoming related changes (if any)
```

**Rules:**
- Lead with what changed, not the backstory.
- If there's a migration path, include it with code.
- Keep it short. Updates don't need 2000 words.
- Link to docs for full reference — the post covers the "what" and "why."
