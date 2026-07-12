# Reference/Documentation Template

Use this template for skills that provide information lookups, documentation, API references, or command guides.

---

## Template Structure

```markdown
---
name: your-reference-skill
description: Brief description of what documentation/reference this provides
---

# Your Reference Skill

[Brief explanation of what this reference covers]

## Quick Reference

[Concise table or list of most common items]

## Categories

### Category 1
[Documentation for first category]

### Category 2
[Documentation for second category]

---

## Detailed Reference

### Command/Topic 1

**Description:** [What it does]

**Usage:**
```
[code example]
```

**Parameters:**
- `param1` - [description]
- `param2` - [description]

**Examples:**
```
[example 1]
[example 2]
```

**See also:** [Related topics]

---

### Command/Topic 2

[Same structure as above]

---

## Common Patterns

[Frequently used combinations or workflows]

## Troubleshooting

[Common issues and solutions]
```

---

## Key Elements

### 1. Quick Reference Section
Put most common items at the top:

```markdown
## Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init`  | Initialize  | `tool init --type=web` |
| `build` | Build       | `tool build --prod` |
| `test`  | Run tests   | `tool test --watch` |
```

### 2. Structured Tables
Use consistent table formats:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value    | Value    | Value    |
```

Align for readability:
```markdown
| Left-aligned | Center | Right-aligned |
|:-------------|:------:|--------------:|
| Text         | Text   | 123           |
```

### 3. Code Examples
Always include practical examples:

```markdown
**Basic usage:**
\`\`\`bash
command --option value
\`\`\`

**Advanced usage:**
\`\`\`bash
command --option1 value1 --option2 value2
\`\`\`
```

### 4. Cross-References
Link related topics:

```markdown
**See also:**
- [Related Topic 1](#related-topic-1)
- [Related Topic 2](#related-topic-2)
- External: https://docs.example.com
```

### 5. Searchable Structure
Use consistent heading hierarchy:

```markdown
## Main Category
### Subtopic 1
#### Detail 1
### Subtopic 2
#### Detail 2
```

---

## Example: Git Commands Reference

```markdown
---
name: git-reference
description: Quick reference for common git commands and workflows
---

# Git Commands Reference

Essential git commands for daily development workflow.

## Quick Reference

| Command | Description |
|---------|-------------|
| `git status` | Show working tree status |
| `git add <file>` | Stage changes |
| `git commit -m "msg"` | Commit staged changes |
| `git push` | Push to remote |
| `git pull` | Pull from remote |
| `git branch` | List branches |
| `git checkout <branch>` | Switch branches |
| `git merge <branch>` | Merge branch |

---

## Basic Workflow

### 1. Check Status
View current changes:
```bash
git status
```

### 2. Stage Changes
Stage specific files:
```bash
git add file1.js file2.js
```

Stage all changes:
```bash
git add .
```

### 3. Commit
```bash
git commit -m "feat: add user authentication"
```

### 4. Push
```bash
git push
```

---

## Branching

### Create Branch
```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Or in two steps
git branch feature/new-feature
git checkout feature/new-feature
```

### List Branches
```bash
# Local branches
git branch

# All branches (including remote)
git branch -a
```

### Delete Branch
```bash
# Delete local branch (safe)
git branch -d feature/old-feature

# Force delete (careful!)
git branch -D feature/old-feature
```

---

## History and Diffs

### View Commit History
```bash
# Recent commits
git log --oneline -10

# Detailed history
git log --graph --decorate --all
```

### View Changes
```bash
# Unstaged changes
git diff

# Staged changes
git diff --staged

# Changes in specific file
git diff path/to/file.js
```

---

## Undoing Changes

| Scenario | Command |
|----------|---------|
| Discard unstaged changes | `git checkout -- <file>` |
| Unstage file | `git reset HEAD <file>` |
| Amend last commit | `git commit --amend` |
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Undo last commit (discard changes) | `git reset --hard HEAD~1` |

---

## Remote Operations

### View Remotes
```bash
git remote -v
```

### Add Remote
```bash
git remote add origin https://github.com/user/repo.git
```

### Fetch and Pull
```bash
# Fetch (download without merging)
git fetch origin

# Pull (fetch + merge)
git pull origin main
```

### Push
```bash
# Push current branch
git push

# Push and set upstream
git push -u origin feature/new-feature

# Force push (careful!)
git push --force
```

---

## Common Patterns

### Feature Branch Workflow
```bash
# Start new feature
git checkout -b feature/new-feature

# Make changes, commit
git add .
git commit -m "feat: implement feature"

# Push to remote
git push -u origin feature/new-feature

# After review, merge to main
git checkout main
git merge feature/new-feature

# Delete feature branch
git branch -d feature/new-feature
```

### Stashing Changes
```bash
# Stash current changes
git stash

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

---

## Troubleshooting

### Merge Conflicts
```bash
# After conflict occurs:
# 1. View conflicted files
git status

# 2. Edit files to resolve conflicts
# 3. Stage resolved files
git add <resolved-file>

# 4. Complete merge
git commit
```

### Accidentally Committed to Wrong Branch
```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Switch to correct branch
git checkout correct-branch

# Commit changes
git add .
git commit -m "your message"
```

### Detached HEAD State
```bash
# Create branch from current state
git checkout -b recovery-branch

# Or discard and return to branch
git checkout main
```

---

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book)
- [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/)
```

---

## Customization Tips

### Add Search/Filter Capability
For large references, add category navigation:

```markdown
## Categories
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
```

### Add Visual Indicators
Use icons or symbols for importance:

```markdown
| Command | Type | Description |
|---------|------|-------------|
| `init` | ⚡ Essential | Initialize project |
| `config` | ⚙️ Advanced | Configure settings |
| `debug` | 🐛 Debug | Debug mode |
```

### Add Comparison Tables
Compare similar options:

```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Speed | Fast | Slow |
| Memory | Low | High |
| Use case | Production | Development |
```

### Add Decision Trees
Help users choose right option:

```markdown
## Which Command Should I Use?

- Need to [scenario 1]? → Use `command1`
- Need to [scenario 2]? → Use `command2`
- Not sure? → Start with `command-help`
```

---

## When to Use This Template

**Good fit:**
- API documentation skills
- Command reference guides
- Configuration lookups
- Standards/best practices guides
- Troubleshooting references

**Not a good fit:**
- Interactive workflows → use `simple-workflow.md` or `multi-phase.md`
- Code generation → use execution-focused template
- Decision-making tools → consider decision tree pattern

---

## Table Style Guidelines

### Simple Reference
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value A  | Value B  |
```

### With Status Indicators
```markdown
| Item | Status |
|------|--------|
| Feature A | ✓ Available |
| Feature B | ⚠ Beta |
| Feature C | ✗ Deprecated |
```

### Multi-column with Alignment
```markdown
| Name | Type | Default | Description |
|:-----|:----:|:-------:|:------------|
| timeout | number | 5000 | Request timeout in ms |
| retries | number | 3 | Number of retry attempts |
```

### Nested Information
```markdown
| Component | Details |
|-----------|---------|
| **Authentication** | |
| ↳ Methods | OAuth, JWT, API Key |
| ↳ Endpoints | `/auth/login`, `/auth/logout` |
| **Authorization** | |
| ↳ Roles | admin, user, guest |
| ↳ Permissions | read, write, delete |
```

---

## See Also

- [OUTPUT_FRAMEWORK.md](../OUTPUT_FRAMEWORK.md) - Full framework documentation
- [simple-workflow.md](./simple-workflow.md) - Template for action-based skills
- [components.md](./components.md) - Reusable formatting snippets
