# List available recipes
default:
    @just --list
    @echo ''
    @echo "branch: $(git branch --show-current 2>/dev/null || echo 'n/a')"

# Install one skill to Claude Code
[group('setup')]
install-one skill:
    ./install-skill.sh {{ skill }}

# Install all skills to Claude Code
[group('setup')]
install-all:
    ./install-skill.sh --all

# List all installable skills
[group('setup')]
list-skills:
    ./install-skill.sh --list

# Repair broken skill symlinks
[group('setup')]
sync-fix *ARGS:
    python3 sync-skills.py fix {{ ARGS }}

# Show file/line stats for one skill (or all)
[group('develop')]
stats *ARGS:
    ./skill-stats.sh {{ ARGS }}

# Show skill usage report (last 30 days)
[group('develop')]
usage:
    python3 skill-usage-tracker/scripts/generate_stats.py

# Open the local usage dashboard (nominate skills for removal)
[group('develop')]
usage-dashboard:
    python3 skill-usage-tracker/scripts/web_ui.py

# Summary of Claude <-> Codex skill sync status
[group('develop')]
sync-status:
    python3 sync-skills.py status

# Per-skill Claude <-> Codex sync status
[group('develop')]
sync-list:
    python3 sync-skills.py list

# Validate skill descriptions (frontmatter, naming)
[group('quality')]
validate:
    ./install-skill.sh --validate --all

# Check aggregate token budget for skill descriptions
[group('quality')]
budget *ARGS:
    python3 validate-context-budget.py {{ ARGS }}

# Validate Claude <-> Codex sync integrity
[group('quality')]
sync-validate:
    python3 sync-skills.py validate

# Run all quality checks
[group('quality')]
check:
    @echo '→ Validating skill descriptions...'
    just validate
    @echo '→ Checking context budget...'
    just budget
    @echo '→ Validating Codex sync...'
    just sync-validate

# Push local skill symlinks to Codex CLI
[group('deploy')]
sync:
    python3 sync-skills.py sync

# Remove Python cache artifacts
[group('cleanup')]
clean:
    find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
    find . -type f -name '*.pyc' -delete
