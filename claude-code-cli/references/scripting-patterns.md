# Scripting Patterns

Comprehensive automation patterns for integrating Claude Code CLI into scripts, CI/CD pipelines, and workflows.

## Table of Contents

- [Pipe Patterns](#pipe-patterns)
- [Output Capture](#output-capture)
- [File Processing](#file-processing)
- [Git Integration](#git-integration)
- [CI/CD Patterns](#cicd-patterns)
- [Safety & Best Practices](#safety--best-practices)

## Pipe Patterns

### File Analysis

```bash
# Single file review
cat src/main.py | claude -p "review this code for bugs"

# With specific focus
cat api.py | claude -p "check for security vulnerabilities"

# Explain complex code
cat algorithm.py | claude -p "explain this algorithm step by step"
```

### Git Diffs

```bash
# Staged changes
git diff --cached | claude -p "review these changes"

# Specific file changes
git diff HEAD~1 src/auth.py | claude -p "summarize changes"

# Branch comparison
git diff main..feature | claude -p "create release notes"
```

### Log Analysis

```bash
# Recent errors
tail -100 app.log | claude -p "identify errors and suggest fixes"

# Filter and analyze
grep ERROR logs/*.log | claude -p "categorize these errors"

# System logs
journalctl -u myservice --since "1 hour ago" | claude -p "diagnose issues"
```

### Multiple Files

```bash
# Concatenate files
cat src/*.py | claude -p "find common patterns"

# With file markers
for f in src/*.py; do
    echo "=== $f ===" && cat "$f"
done | claude -p "review all files"

# Specific files
cat package.json tsconfig.json | claude -p "check for version conflicts"
```

### Command Output

```bash
# Test failures
pytest 2>&1 | claude -p "explain why tests failed"

# Lint output
eslint src/ 2>&1 | claude -p "prioritize these issues"

# Build errors
npm run build 2>&1 | claude -p "fix these build errors"
```

## Output Capture

### To Variables

```bash
# Capture response
REVIEW=$(cat code.py | claude -p "brief code review")
echo "Review: $REVIEW"

# Use in conditionals
QUALITY=$(claude -p --output-format json "rate this code 1-10" | jq -r '.rating')
if [ "$QUALITY" -lt 5 ]; then
    echo "Code needs improvement"
fi
```

### To Files

```bash
# Simple redirect
claude -p "document this codebase" > DOCS.md

# Append mode
claude -p "add API section" >> DOCS.md

# With timestamp
claude -p "status report" > "reports/$(date +%Y%m%d).md"
```

### JSON Output Parsing

```bash
# Get specific field with jq
claude -p --output-format json "analyze" | jq -r '.result'

# Extract array
claude -p --output-format json "list issues" | jq -r '.issues[]'

# Transform output
claude -p --output-format json "categorize errors" | jq '.categories | keys[]'
```

### Structured Extraction

```bash
# With JSON schema
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "bugs": {"type": "array", "items": {"type": "string"}},
    "severity": {"type": "string", "enum": ["low", "medium", "high"]}
  },
  "required": ["bugs", "severity"]
}' "analyze for bugs" | jq '.bugs[]'
```

## File Processing

### Batch Processing

```bash
# Process all Python files
for f in src/*.py; do
    echo "Processing $f..."
    claude -p "review: $(cat $f)" > "reviews/$(basename $f .py).md"
done

# With error handling
for f in *.py; do
    if output=$(cat "$f" | claude -p "analyze" 2>&1); then
        echo "$output" > "analysis/${f%.py}.md"
    else
        echo "Failed: $f" >> errors.log
    fi
done
```

### Parallel Processing

```bash
# Using GNU parallel
find src -name "*.py" | parallel -j4 \
    'cat {} | claude -p "review" > reviews/{/.}.md'

# Using xargs
ls *.py | xargs -P4 -I{} sh -c \
    'cat {} | claude -p "analyze" > analysis/{}.md'
```

### Directory Traversal

```bash
# Recursive processing
find . -name "*.ts" -type f | while read f; do
    dir=$(dirname "$f")
    mkdir -p "docs/$dir"
    cat "$f" | claude -p "document" > "docs/${f%.ts}.md"
done
```

### Transform Files

```bash
# Add type annotations
for f in src/*.py; do
    TYPED=$(cat "$f" | claude -p "add type hints, output only code")
    echo "$TYPED" > "${f%.py}_typed.py"
done

# Convert format
cat data.csv | claude -p "convert to JSON array" > data.json
```

## Git Integration

### Commit Messages

```bash
#!/bin/bash
# generate-commit.sh - Generate commit message from staged changes

DIFF=$(git diff --cached)
if [ -z "$DIFF" ]; then
    echo "No staged changes"
    exit 1
fi

MSG=$(echo "$DIFF" | claude -p "Write a conventional commit message. Format: type(scope): description. Output only the message.")

echo "Proposed: $MSG"
read -p "Use this message? [y/N] " confirm
[[ $confirm == [yY] ]] && git commit -m "$MSG"
```

### PR Descriptions

```bash
#!/bin/bash
# generate-pr.sh - Generate PR description

BASE=${1:-main}
COMMITS=$(git log $BASE..HEAD --oneline)
DIFF=$(git diff $BASE...HEAD --stat)

cat <<EOF | claude -p "Write a PR description with Summary and Changes sections"
Commits:
$COMMITS

Changed files:
$DIFF
EOF
```

### Code Review

```bash
#!/bin/bash
# review-pr.sh - Review PR changes

PR_NUM=$1
gh pr diff $PR_NUM | claude -p "Review this PR for:
- Bugs and edge cases
- Security issues
- Performance concerns
- Code style
Output as markdown checklist."
```

### Changelog Generation

```bash
#!/bin/bash
# changelog.sh - Generate changelog from commits

SINCE=${1:-$(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~20")}

git log $SINCE..HEAD --pretty=format:"%s" | claude -p "Generate a changelog grouped by:
- Features
- Bug Fixes
- Breaking Changes
- Other"
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts)$')

if [ -n "$STAGED" ]; then
    for file in $STAGED; do
        ISSUES=$(cat "$file" | claude -p --max-turns 1 "List critical bugs only. Say 'none' if clean.")
        if [[ "$ISSUES" != *"none"* ]]; then
            echo "Issues in $file:"
            echo "$ISSUES"
            exit 1
        fi
    done
fi
```

## CI/CD Patterns

### GitHub Actions

```yaml
# .github/workflows/review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get diff
        run: |
          git diff origin/main...HEAD > changes.diff

      - name: Review changes
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cat changes.diff | claude -p --max-turns 1 \
            "Review for bugs and security issues. Be concise." \
            > review.md

      - name: Post comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review
            });
```

### GitLab CI

```yaml
# .gitlab-ci.yml
code-review:
  stage: review
  script:
    - git diff $CI_MERGE_REQUEST_DIFF_BASE_SHA..HEAD |
        claude -p --max-turns 1 "Review for issues" > review.md
    - cat review.md
  artifacts:
    paths:
      - review.md
  only:
    - merge_requests
```

### Pre-deployment Check

```bash
#!/bin/bash
# check-deploy.sh

echo "Running pre-deploy analysis..."

# Check for secrets
SECRETS=$(grep -r "API_KEY\|PASSWORD\|SECRET" src/ 2>/dev/null)
if [ -n "$SECRETS" ]; then
    echo "$SECRETS" | claude -p "Are any of these actual secrets? Answer yes/no with explanation."
fi

# Check migrations
if [ -d "migrations" ]; then
    cat migrations/*.sql | claude -p "Check for dangerous operations (DROP, TRUNCATE, data loss)"
fi
```

## Safety & Best Practices

### Permission Handling

```bash
# Skip permissions for non-destructive operations
claude -p --dangerously-skip-permissions --tools "Read,Grep" "find TODOs"

# Never skip for destructive operations
claude -p --tools "Read" "analyze"  # Safe, read-only
```

### Timeout and Limits

```bash
# Limit autonomous turns
claude -p --max-turns 3 "refactor this"

# Shell timeout
timeout 120 claude -p "complex task" || echo "Timed out"
```

### Error Handling

```bash
#!/bin/bash
set -euo pipefail

# With retries
retry() {
    local n=0
    local max=3
    until [ $n -ge $max ]; do
        "$@" && return 0
        n=$((n+1))
        sleep $((n * 2))
    done
    return 1
}

retry claude -p "task"
```

### Input Sanitization

```bash
# Limit input size
head -1000 large_file.log | claude -p "analyze"

# Filter sensitive data
cat config.json | sed 's/"password":.*/PASSWORD_REDACTED/g' | claude -p "review config"
```

### Logging

```bash
#!/bin/bash
# With logging

LOG_FILE="claude_$(date +%Y%m%d_%H%M%S).log"

{
    echo "=== $(date) ==="
    echo "Query: $1"
    claude -p "$1" 2>&1
    echo "=== End ==="
} | tee -a "$LOG_FILE"
```
