---
name: blog-writer
description: Write authentic, no-nonsense blog posts with Dutch directness and zero AI slop. Use when writing a blog post, article, technical post, opinion piece, tutorial, or case study.
---

# Blog Writer

Write blog posts that say something real, say it clearly, and respect the reader's time.

## Workflow

```
1. BRIEF    → Gather topic, audience, voice, constraints
2. RESEARCH → Verify claims, gather examples and data
3. OUTLINE  → Structure by reader value, get approval
4. DRAFT    → Write with banned-words enforcement
5. REVIEW   → Quality checklist
6. DELIVER  → Markdown with frontmatter
```

## Step 1: Brief

Gather before writing:
- **Topic**: What specifically are we writing about?
- **Type**: Technical post, opinion piece, tutorial, case study, or update? (see `references/blog-types.md`)
- **Audience**: Who reads this? What do they already know?
- **Thesis**: One sentence — what's the point?
- **Voice sample**: Link to an existing post by the author (triggers voice calibration)
- **Target length**: Default 800–1200 words unless specified

If the user provides a voice sample, run Voice Calibration before drafting.

## Step 2: Research

Before writing a single word:
- Verify every factual claim. If you can't verify it, flag it.
- Gather concrete examples: code snippets, data points, real tool names
- Find counterarguments to the thesis — address them or adjust
- No claim without evidence. No example without specifics.

## Step 3: Outline

Structure rules:
1. **Lead with the point.** The reader should know the thesis within the first two paragraphs.
2. **Order by reader value.** Most useful content first. Background later (or never).
3. **Each section earns its place.** If removing a section doesn't hurt the post, remove it.

Use the structural template from `references/blog-types.md` for the chosen type.

Present the outline for approval before drafting. Format:

```
## Outline: [Title]

**Thesis:** [one sentence]
**Type:** [post type]
**Est. length:** [word count]

1. [Section] — [what it covers and why]
2. [Section] — [what it covers and why]
3. ...
```

## Step 4: Draft

### Writing Rules

1. **Lead with the point.** Don't build up to it. State it, then support it.
2. **One idea per paragraph.** If a paragraph covers two things, split it.
3. **Show, don't tell.** Code > description. Example > explanation. Data > opinion.
4. **Short paragraphs.** 1–4 sentences. Wall of text = reader gone.
5. **Active voice.** "We removed the cache" not "The cache was removed by us."
6. **Specific > vague.** "Reduced response time from 800ms to 120ms" not "significantly improved performance."
7. **Cut filler.** Every word earns its place or gets deleted.

### Banned Words Enforcement

Check every sentence against `references/banned-words.md`. Quick inline list of the worst offenders:

> dive, delve, unlock, unleash, harness, leverage, robust, comprehensive, holistic, synergy, pivotal, transformative, cutting-edge, game-changer, deep dive, "in today's fast-paced world", "let's explore", "excited to announce"

If you catch yourself using any: stop, delete, rewrite with plain language.

### Paragraph Flow

- First sentence of each paragraph: states the point
- Remaining sentences: support with evidence or example
- Last paragraph of each section: bridges to the next or delivers a conclusion
- No orphan paragraphs that don't connect to anything

## Step 5: Review

Check the draft against every item:

### Content
- [ ] Thesis is clear within the first two paragraphs
- [ ] Every claim is supported with evidence, code, or data
- [ ] No unsupported superlatives ("best", "fastest", "revolutionary")
- [ ] Counterarguments are addressed, not ignored

### Voice
- [ ] Zero words from the banned list
- [ ] Zero phrases from the banned list
- [ ] Reads like a human wrote it — read it aloud
- [ ] Matches the author's voice (if sample provided)

### Structure
- [ ] Every section earns its place
- [ ] Paragraphs are 1–4 sentences
- [ ] Code examples are complete and runnable (if technical)
- [ ] Intro doesn't waste time — gets to the point fast

### Anti-Clickbait
- [ ] Title is honest about what the post delivers
- [ ] No "You Won't Believe" / "X Things You Need to Know" patterns
- [ ] Title matches content — no bait and switch

## Step 6: Deliver

Output as markdown with frontmatter:

```markdown
---
title: "Exact Post Title"
description: "One-sentence summary for SEO/social"
tags: [tag1, tag2, tag3]
date: YYYY-MM-DD
draft: true
---

[Post body in markdown]
```

Always set `draft: true`. The author publishes when ready.

## Voice Calibration

When the user provides an existing post or writing sample:

1. **Read the sample** and extract:
   - Sentence length patterns (short/mixed/long)
   - Paragraph length patterns
   - Use of first person (I/we/you)
   - Humor style (dry, none, self-deprecating)
   - Technical depth (surface, detailed, deep)
   - Contractions (uses them or doesn't)
   - How they open posts
   - How they handle transitions

2. **Summarize the voice** in 3–4 bullets before drafting:
   ```
   Voice profile:
   - Short, punchy sentences. Mixes in longer ones for rhythm.
   - Heavy use of "you" — talks directly to the reader.
   - Dry humor, no exclamation marks.
   - Opens with a provocative statement, not a question.
   ```

3. **Match the voice** throughout the draft. If unsure, lean toward shorter and more direct.

## Dutch Directness Principles

These apply to every post:

1. **Say what you mean.** No hedging, no weasel words, no "it could be argued that."
2. **Respect the reader's time.** If it can be said in fewer words, use fewer words.
3. **Substance over style.** A plain sentence with a real insight beats a polished sentence with nothing to say.
4. **Opinions are fine.** State them clearly, support them, and acknowledge the other side.
5. **No false modesty.** Don't undersell good work. Don't oversell mediocre work.

### Before / After

**Before (AI slop):**
> In today's rapidly evolving technological landscape, it's becoming increasingly important for developers to harness the power of modern frameworks to build robust and comprehensive solutions that can truly transform the way we think about web development.

**After (Dutch direct):**
> Most web frameworks add complexity without solving real problems. Here's one that doesn't.

## Vault Integration

When writing a blog post for a project, check for a promotion vault folder:

**Path:** `_management/promotion-vault/projects/{project-name}/`

If the vault folder exists:
- Read `index.md` frontmatter for project context (description, tags, status, links)
- Write the blog post body to `blog-post.md` in the vault folder (markdown-only, no frontmatter)
- Add an `article` entry to `posts.yaml` with `body_file: blog-post.md` and metadata (`subject`, `subtitle`, `hero_image`, `status: draft`)

If no vault folder exists, create content in the conversation and suggest:
```
Run: bun run _management/promotion-vault/scripts/promote.ts {project} init
```
