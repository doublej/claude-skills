---
name: social-promotion
description: Write social promotion content for apps, tools, and products across X.com, Threads, and Substack. Use when creating launch posts, product updates, feature announcements, or ongoing social content campaigns.
---

# Social Promotion

Write promotional social content for applications, tools, and products across X.com (Twitter), Threads, and Substack.

## Workflow

```
1. BRIEF → Gather product context and promotion goal
2. ANGLE → Choose content angle and hook strategy
3. DRAFT → Write platform-specific content
4. REFINE → Humanize, tighten, remove AI patterns
5. DELIVER → Output all variants with posting notes
```

## Step 1: Brief

Gather before writing:
- **What** is being promoted (product/feature/update)
- **Who** is the audience (developers, designers, founders, general)
- **Why** should they care (pain point solved, benefit unlocked)
- **Proof** — any metrics, testimonials, demos, screenshots available?
- **Tone** — the user's voice (default: direct, confident, no hype)

## Step 2: Angle

Pick ONE angle per post. Never combine.

| Angle | Works for | Example hook |
|-------|-----------|-------------|
| Pain → solution | Feature launches | "Tired of X? Built Y." |
| Show, don't tell | Demos, screenshots | "Here's what happens when..." |
| Contrarian | Thought leadership | "Everyone says X. They're wrong." |
| Behind the scenes | Build-in-public | "Spent 3 weeks on this one feature." |
| Social proof | Traction updates | "500 devs shipped with this last week." |
| Curiosity gap | Any | "The trick to X that nobody talks about." |
| Direct value | Tutorials, tips | "How to do X in 30 seconds:" |

## Step 3: Draft

Write for each requested platform. See `references/` for platform-specific rules:
- `references/x-writing.md` — X.com posts and threads
- `references/threads-writing.md` — Threads posts
- `references/substack-writing.md` — Substack articles

### Cross-Platform Rules

1. **First line is everything.** If the hook doesn't stop the scroll, nothing else matters.
2. **One idea per post.** Split multi-idea content into a thread or series.
3. **Concrete > abstract.** Numbers, specifics, examples beat vague claims.
4. **No AI slop.** Avoid: "game-changer", "revolutionary", "excited to announce", "I'm thrilled", "comprehensive", "robust", "leverage", "harness the power". If it sounds like a press release, rewrite it.
5. **No emoji spam.** Zero or one emoji per post maximum.
6. **Links suppress reach** on X and Threads. Put links in replies or at the end.
7. **End with a pull.** Question, CTA, or open loop — give people a reason to engage.

## Step 4: Refine

Check every draft against these filters:

- [ ] Would a real human post this? Read it aloud.
- [ ] Is the hook specific enough to stop someone mid-scroll?
- [ ] Does it avoid all AI-typical phrases from the banned list above?
- [ ] Is there exactly ONE clear idea?
- [ ] Is there a reason to engage (reply, share, click)?
- [ ] Is it the right length for the platform?

Cut ruthlessly. If a sentence doesn't earn its place, delete it.

## Step 5: Deliver

Output format per platform:

```
## X.com
[post text]
> Posting note: [any tactical advice — time, thread strategy, media]

## Threads
[post text]
> Posting note: [tactical advice]

## Substack
**Subject:** [subject line]
**Subtitle:** [preview text]
[article body or outline]
> Posting note: [tactical advice]
```

If promoting the same thing across all platforms, adapt — never copy-paste between platforms.

## Content Campaign Mode

When asked for a campaign (multiple posts over time), plan a sequence:

| Day | Platform | Angle | Content type |
|-----|----------|-------|-------------|
| D-1 | X | Curiosity gap | Teaser |
| D0 | All | Show don't tell | Launch post |
| D+1 | Threads | Behind the scenes | Build story |
| D+3 | Substack | Direct value | Deep dive article |
| D+7 | X | Social proof | Traction update |

Adapt the cadence to the user's actual posting rhythm.

## Vault Integration

When working on promotion for a project, check for a promotion vault folder:

**Path:** `_management/promotion-vault/projects/{project-name}/`

If the vault folder exists:
- Read `index.md` frontmatter for project context (description, tags, status, links)
- Write creative/strategy content to markdown files:
  - `social-x.md` — X.com strategy, specs, posting rules, creative notes
  - `social-threads.md` — Threads strategy, specs, posting rules, creative notes
  - `social-substack.md` — Substack article body (referenced by posts.yaml `body_file`)
- When posts are finalized, write structured entries to `posts.yaml`:
  - Each post gets an `id`, `platform`, `format`, `status`, `text`/`thread`, `images`, `reply`, `note`
  - Formats: `single`, `thread`, `carousel`, `note`, `article`
  - Status: `draft` (default for new posts)
- Reference screenshots from `assets/` subdirectories

If no vault folder exists, create content in the conversation and suggest:
```
Run: bun run _management/promotion-vault/scripts/promote.ts {project} init
```
