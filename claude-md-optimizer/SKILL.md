---
name: claude-md-optimizer
description: Review and optimize the global CLAUDE.md file with latest best practices. Use when user wants to update their CLAUDE.md, check if it follows current recommendations, or ensure configuration is aligned with latest Claude Code capabilities.
metadata:
  version: 1.0.0
  created: 2026-02-04
  models: Claude Opus 4.5, Sonnet 4.5
---

# CLAUDE.md Optimizer

Analyze and improve the user's global CLAUDE.md file using current best practices.

## Age Awareness

**CRITICAL**: Always run the age check script first and display the results to the user:

```bash
python3 scripts/check_age.py
```

If the information is >6 weeks old, warn the user that recommendations may be outdated and suggest they request an updated version of this skill.

## Workflow

1. **Check skill age**: Run `scripts/check_age.py` and show results
2. **Read current CLAUDE.md**: Load from `~/.claude/CLAUDE.md`
3. **Load best practices**: Read `references/best_practices_2026_02.md`
4. **Analyze alignment**: Compare current file against best practices
5. **Provide recommendations**: Suggest specific, actionable improvements

## Analysis Focus Areas

### Structure
- Clear precedence rules defined
- Logical grouping of related instructions
- XML tags used appropriately for sections
- Progressive disclosure where applicable

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

## Recommendation Format

For each improvement, provide:

1. **Category**: Which focus area
2. **Current state**: What file currently has (or lacks)
3. **Recommended change**: Specific addition/modification
4. **Rationale**: Why this improves the file (1 sentence)
5. **Priority**: High/Medium/Low

Group recommendations by priority.

## Making Changes

If user approves recommendations:
1. Use Edit tool for surgical changes to existing content
2. Preserve user's existing style and formatting
3. Keep changes minimal and targeted
4. Don't rewrite sections unnecessarily

## Version Tracking

After making changes, optionally suggest adding version metadata to the CLAUDE.md:

```xml
<!-- Updated: YYYY-MM-DD | Based on Claude Opus 4.5 / Sonnet 4.5 -->
```

## Important Notes

- **Respect user preferences**: Don't remove customizations
- **Match existing style**: Follow tone and formatting patterns
- **Minimal changes**: Only suggest what adds clear value
- **Explain tradeoffs**: If recommendations conflict with existing approaches
- **Age awareness**: Always show skill age before recommendations

## Example Usage

User: "Review my CLAUDE.md file"

Response:
1. Run age check script, show results
2. Read ~/.claude/CLAUDE.md
3. Analyze against best practices
4. Present prioritized recommendations
5. Offer to implement approved changes
