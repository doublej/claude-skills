---
name: claude-md-optimizer
description: Review and optimize the global CLAUDE.md file with latest best practices. Use when user wants to update their CLAUDE.md, check if it follows current recommendations, or ensure configuration is aligned with latest Claude Code capabilities.
metadata:
  version: 1.2.0
  created: 2026-02-04
  updated: 2026-05-25
  models: Claude Opus 4.7, Sonnet 4.6, Haiku 4.5
---

# CLAUDE.md Optimizer

Analyze and improve the user's global CLAUDE.md file using current best practices.

<age_awareness>
Run the age check script first and show results to the user:

```bash
python3 scripts/check_age.py
```

If >6 weeks old, warn that recommendations may be outdated and suggest requesting an updated skill.
</age_awareness>

<workflow>
1. Run `scripts/check_age.py` and show results
2. Read `~/.claude/CLAUDE.md` using the Read tool
3. Read `references/best_practices_2026_05.md` (phrasing/content) and `references/formatting-examples.md` (structure/shape)
4. Compare current file against best practices
5. Present prioritized recommendations (max 5 High, 3 Medium, 2 Low)
6. On user approval: apply changes using Edit tool
7. Stop after changes are confirmed
</workflow>

<analysis_focus_areas>

Work through the "High-impact CLAUDE.md review checklist" in the references file first — it
captures the 4.6/4.7 behavior shifts that most often make an older CLAUDE.md mis-steer the model
(aggressive ALL-CAPS/MUST/NEVER → overtriggering, negative phrasing, missing rationale, stale
model IDs). Then cover the areas below.

### Phrasing for current models
- No pervasive ALL-CAPS / MUST / ALWAYS / NEVER / CRITICAL (overtriggers 4.6/4.7)
- Positive instructions over prohibitions ("do X" not "don't do Y")
- Rules carry a short rationale; broad rules state their scope explicitly
- Current model names/IDs (Opus 4.7 / Sonnet 4.6 / Haiku 4.5, `claude-opus-4-7`)

### Structure
- Clear precedence rules defined
- Logical grouping of related instructions
- XML tags used appropriately for sections
- Progressive disclosure where applicable
- Formatting follows `references/formatting-examples.md` (flat sections, one instruction per line,
  no noisy tables / over-nested tags / dense blobs / emphasis overload / fake config / tiny sections)

### Tool Usage
- consult-user-mcp integration documented
- Parallel tool call guidance present
- Specialized tool preferences over bash commands
- Task agent usage for exploration documented

### Code Standards
- Size targets specified (functions, params, nesting, files)
- KISS + YAGNI principles included
- SRP and explicit-over-clever guidance
- Error handling philosophy stated

### Workflow Guidance
- Git commit discipline defined
- Quality gate approach specified
- Change policy articulated
- Output format standardized

### Completeness
- All critical areas covered
- No redundant or outdated guidance
- Model-specific capabilities mentioned
- Version/date tracking if applicable
</analysis_focus_areas>

<recommendation_format>

For each improvement:

1. **Category**: Which focus area
2. **Current state**: What the file has (or lacks)
3. **Recommended change**: Specific addition/modification
4. **Rationale**: Why this helps (1 sentence)
5. **Priority**: High / Medium / Low

Cap: 5 High, 3 Medium, 2 Low. Group by priority.
</recommendation_format>

<making_changes>
On user approval:
- Use Edit tool for targeted changes; preserve style and formatting
- Preserve existing customizations
- Suggest only what adds clear value; explain tradeoffs where recommendations conflict
</making_changes>

<version_tracking>
After changes, optionally add version metadata to CLAUDE.md:

```xml
<!-- Updated: YYYY-MM-DD | Based on Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5 -->
```
</version_tracking>
