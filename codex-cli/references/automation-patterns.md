# Automation Patterns

Comprehensive patterns for integrating Codex CLI into scripts, CI/CD pipelines, and automated workflows.

## Table of Contents

- [Quiet Mode Basics](#quiet-mode-basics)
- [Output Handling](#output-handling)
- [CI/CD Integration](#cicd-integration)
- [Batch Processing](#batch-processing)
- [Approval Mode Patterns](#approval-mode-patterns)
- [Error Handling](#error-handling)

## Quiet Mode Basics

### Non-Interactive Execution

```bash
# Quiet mode flag
codex -q "explain utils.ts"

# Environment variable
CODEX_QUIET_MODE=1 codex "explain utils.ts"

# Exec subcommand
codex exec "explain utils.ts"
```

### JSON Output

```bash
# Get structured output
codex -q --json "analyze code quality" > report.json

# Parse with jq
codex -q --json "find bugs" | jq '.issues[]'
```

### Capture Output

```bash
# To variable
RESULT=$(codex -q "summarize changes")
echo "$RESULT"

# To file
codex -q "generate docs" > DOCS.md

# With timestamp
codex -q "status report" > "reports/$(date +%Y%m%d).md"
```

## Output Handling

### JSON Structure

```bash
codex -q --json "task"
```

Output structure:

```json
{
  "result": "...",
  "files_modified": ["path/to/file.ts"],
  "commands_executed": ["npm test"],
  "errors": []
}
```

### Parsing Examples

```bash
# Get result text
codex -q --json "query" | jq -r '.result'

# List modified files
codex -q --json "refactor" | jq -r '.files_modified[]'

# Check for errors
if codex -q --json "task" | jq -e '.errors | length > 0' > /dev/null; then
    echo "Errors occurred"
fi
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/codex-review.yml
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Codex
        run: npm install -g @openai/codex

      - name: Review PR
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          git diff origin/main...HEAD > changes.diff
          cat changes.diff | codex -q -a suggest \
            "Review these changes for bugs and security issues" \
            > review.md

      - name: Post Review
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

### GitHub Actions - Auto-fix

```yaml
name: Auto-fix Lint
on:
  push:
    branches: [main]

jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Codex
        run: npm install -g @openai/codex

      - name: Fix Lint Issues
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex -q -a auto-edit "fix all ESLint errors"

      - name: Commit Changes
        run: |
          git config user.name "Codex Bot"
          git config user.email "codex@example.com"
          git add -A
          git diff --cached --quiet || git commit -m "fix: auto-fix lint errors"
          git push
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - review
  - fix

code-review:
  stage: review
  image: node:20
  before_script:
    - npm install -g @openai/codex
  script:
    - git diff $CI_MERGE_REQUEST_DIFF_BASE_SHA..HEAD |
        codex -q -a suggest "Review for issues" > review.md
    - cat review.md
  artifacts:
    paths:
      - review.md
  only:
    - merge_requests

auto-fix:
  stage: fix
  image: node:20
  before_script:
    - npm install -g @openai/codex
  script:
    - codex -q -a auto-edit "fix TypeScript errors"
  only:
    - main
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Skip if no staged changes
STAGED=$(git diff --cached --name-only --diff-filter=ACM)
if [ -z "$STAGED" ]; then
    exit 0
fi

echo "Running Codex pre-commit check..."

# Review staged changes
ISSUES=$(git diff --cached | codex -q -a suggest \
    "List critical bugs only. Say 'none' if clean.")

if [[ "$ISSUES" != *"none"* ]]; then
    echo "Codex found issues:"
    echo "$ISSUES"
    echo ""
    read -p "Commit anyway? [y/N] " confirm
    [[ $confirm != [yY] ]] && exit 1
fi

exit 0
```

## Batch Processing

### Process Multiple Files

```bash
#!/bin/bash
# review-all.sh

for file in src/*.ts; do
    echo "Reviewing $file..."
    codex -q -a suggest "review $file for issues" > "reviews/$(basename $file .ts).md"
done
```

### Parallel Processing

```bash
#!/bin/bash
# parallel-review.sh

# Using GNU parallel
find src -name "*.ts" | parallel -j4 \
    'codex -q -a suggest "review {}" > reviews/{/.}.md'

# Using xargs
ls src/*.ts | xargs -P4 -I{} sh -c \
    'codex -q -a suggest "review {}" > reviews/$(basename {} .ts).md'
```

### Directory Traversal

```bash
#!/bin/bash
# review-tree.sh

find . -name "*.ts" -type f | while read file; do
    dir=$(dirname "$file")
    mkdir -p "docs/$dir"
    codex -q -a suggest "document $file" > "docs/${file%.ts}.md"
done
```

## Approval Mode Patterns

### Safe Analysis (suggest)

```bash
# Read-only operations
codex -q -a suggest "analyze code quality"
codex -q -a suggest "find security vulnerabilities"
codex -q -a suggest "explain architecture"
```

### Controlled Editing (auto-edit)

```bash
# File modifications only
codex -q -a auto-edit "fix TypeScript errors"
codex -q -a auto-edit "add JSDoc comments"
codex -q -a auto-edit "refactor to use async/await"
```

### Full Automation (full-auto)

```bash
# Complete automation (sandboxed)
codex -q -a full-auto "generate tests and run them"
codex -q -a full-auto "fix lint errors and verify"
codex -q -a full-auto "update dependencies and test"
```

### Multi-Directory Operations

```bash
# Monorepo patterns
codex -q --cd apps/frontend --add-dir ../shared \
    -a auto-edit "update shared imports"

codex -q --cd packages/core --add-dir ../utils --add-dir ../types \
    -a full-auto "refactor and test"
```

## Error Handling

### Basic Error Handling

```bash
#!/bin/bash
set -euo pipefail

if ! codex -q -a suggest "analyze" > result.md 2>&1; then
    echo "Codex failed"
    exit 1
fi
```

### Retry Logic

```bash
#!/bin/bash
# codex-retry.sh

retry() {
    local n=0
    local max=3
    local delay=5

    until [ $n -ge $max ]; do
        "$@" && return 0
        n=$((n+1))
        echo "Attempt $n failed. Retrying in ${delay}s..."
        sleep $delay
        delay=$((delay * 2))
    done

    echo "All $max attempts failed"
    return 1
}

retry codex -q -a suggest "task"
```

### Timeout Handling

```bash
#!/bin/bash
# With timeout
timeout 300 codex -q -a full-auto "complex task" || {
    echo "Codex timed out after 5 minutes"
    exit 1
}
```

### Full-Auto Error Mode

In config:

```yaml
# Ask user on errors (interactive)
fullAutoErrorMode: ask-user

# Continue on errors (CI/CD)
fullAutoErrorMode: ignore-and-continue
```

### Wrapper Script

```bash
#!/bin/bash
# codex-safe.sh - Production wrapper

LOG_DIR="${CODEX_LOG_DIR:-/var/log/codex}"
TIMEOUT="${CODEX_TIMEOUT:-300}"

log() {
    echo "[$(date -Iseconds)] $*" >> "$LOG_DIR/codex.log"
}

safe_codex() {
    local mode="${1:-suggest}"
    local task="$2"

    log "START: mode=$mode task=$task"

    local start_time=$(date +%s)
    local result

    if result=$(timeout "$TIMEOUT" codex -q -a "$mode" "$task" 2>&1); then
        local duration=$(($(date +%s) - start_time))
        log "SUCCESS: duration=${duration}s"
        echo "$result"
        return 0
    else
        log "FAILED: $result"
        return 1
    fi
}

# Usage: ./codex-safe.sh suggest "analyze code"
safe_codex "$@"
```

### JSON Error Checking

```bash
#!/bin/bash
# Check JSON output for errors

result=$(codex -q --json "task")

if echo "$result" | jq -e '.errors | length > 0' > /dev/null; then
    echo "Errors found:"
    echo "$result" | jq -r '.errors[]'
    exit 1
fi

echo "$result" | jq -r '.result'
```
