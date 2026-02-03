---
name: version-manager
description: Set up versioning, bump versions, create releases, manage git tags, and generate changelogs across Python, Node, Rust, Go, Swift, and multi-component projects. Supports four progressive patterns from simple (VERSION file) to fully automated (semantic-release). Use when initializing version tracking, bumping version numbers, creating release tags, or automating changelog generation.
---

# Version Manager

Comprehensive versioning for all project types with four progressive patterns: simple (VERSION file), standard (package manager + automation), advanced (multi-component tracking), and automated (full CI/CD).

## Quick Start

**Initialize versioning in a project:**
```bash
python3 scripts/init_versioning.py
```

**Bump version interactively:**
```bash
python3 scripts/bump_version.py
```

**Validate version consistency:**
```bash
python3 scripts/validate_version.py
```

## Four Versioning Patterns

### Pattern 1: Simple
**Use for:** Go projects, shell scripts, simple tools

- Plain text `VERSION` file
- Manual `CHANGELOG.md` (Keep a Changelog format)
- Git hooks for validation
- Manual tags: `git tag v$(cat VERSION)`

**Setup:** `init_versioning.py` detects and creates `VERSION`, `CHANGELOG.md`, installs hooks

### Pattern 2: Standard
**Use for:** Python (pyproject.toml), Node (package.json), Rust (Cargo.toml)

- Version in package manifest
- Automated changelog from conventional commits
- Git hooks for validation + commit-msg enforcement
- Tools: bumpp (Node), python-semantic-release (Python), cargo-release (Rust)

**Setup:** `init_versioning.py` detects package type, configures tools, installs hooks

### Pattern 3: Advanced (Multi-component)
**Use for:** Projects with multiple versioned components (like consult-user-mcp)

- `releases.json` as single source of truth (with JSON schema validation)
- Component-specific version tracking
- User-focused change descriptions
- CI validation scripts
- Automated `CHANGELOG.md` generation from releases.json

**Setup:** `init_versioning.py --pattern advanced` creates releases.json structure

### Pattern 4: Automated (Full semantic-release)
**Use for:** High-velocity CI/CD workflows

- Full automation via semantic-release
- GitHub Actions for tag-triggered releases
- Auto-generated changelog and GitHub releases
- Automatic publishing to npm/PyPI/crates.io

**Setup:** `init_versioning.py --pattern automated` configures semantic-release

See `references/patterns.md` for decision matrix.

## Core Scripts

### init_versioning.py
Detect project type and initialize versioning:

```bash
# Auto-detect project type and pattern
python3 scripts/init_versioning.py

# Force specific pattern
python3 scripts/init_versioning.py --pattern advanced

# Skip git hooks installation
python3 scripts/init_versioning.py --no-hooks
```

**What it does:**
1. Detects project type (package.json, pyproject.toml, Cargo.toml, go.mod, VERSION)
2. Prompts for pattern selection if ambiguous
3. Creates appropriate version files
4. Installs git hooks
5. Adds versioning section to CLAUDE.md
6. Initializes git tag v1.0.0 (or current version)

### bump_version.py
Interactive version bumping with validation:

```bash
# Interactive prompt (major/minor/patch)
python3 scripts/bump_version.py

# Non-interactive
python3 scripts/bump_version.py --patch
python3 scripts/bump_version.py --minor
python3 scripts/bump_version.py --major

# Skip tag creation
python3 scripts/bump_version.py --no-tag
```

**Pre-release checks:**
- Clean working directory
- All version files in sync
- No existing tag for new version

**Actions:**
1. Updates all version files
2. Generates/updates changelog entry
3. Creates git tag
4. Shows next steps (push, publish)

### validate_version.py
Check version consistency (for CI/hooks):

```bash
# Validate current state
python3 scripts/validate_version.py

# Validate staged changes only (for pre-commit hook)
python3 scripts/validate_version.py --staged

# Validate specific version
python3 scripts/validate_version.py --version 1.2.3
```

**Checks:**
- Version format is valid semver (X.Y.Z)
- All version files contain same version
- Changelog has entry for current version
- Git tag matches current version (if exists)
- Working directory clean (for releases)

Exits with error code 1 on failure (CI-friendly).

### generate_changelog.py
Generate CHANGELOG.md from structured data:

```bash
# From releases.json (Pattern 3: Advanced)
python3 scripts/generate_changelog.py --from-releases

# From conventional commits (Pattern 2: Standard)
python3 scripts/generate_changelog.py --from-commits

# Custom range
python3 scripts/generate_changelog.py --from-commits --since v1.0.0
```

**Output:** Keep a Changelog format with grouped changes (Added, Changed, Fixed, Removed)

### sync_versions.py
Multi-file version synchronization:

```bash
# Sync all configured files
python3 scripts/sync_versions.py

# Dry run (show what would change)
python3 scripts/sync_versions.py --dry-run
```

**Example:** pyproject.toml → src/package/__init__.py (__version__ = "X.Y.Z")

Configure targets in `.version-sync.json`:
```json
{
  "source": "VERSION",
  "targets": [
    {
      "file": "src/mypackage/__init__.py",
      "pattern": "__version__ = \"{{VERSION}}\""
    }
  ]
}
```

## Git Hooks

Installed to `.git/hooks/` (not tracked in repo).

### pre-commit
Validates version consistency before commit:
- If VERSION, package.json, pyproject.toml, Cargo.toml, or releases.json changed
- Runs `validate_version.py --staged`
- Blocks commit on failure

### commit-msg (opt-in for Pattern 2+)
Enforces conventional commit format:
- feat: new feature
- fix: bug fix
- docs: documentation
- chore: maintenance
- etc.

### pre-push
Validates tag format before push:
- Tags must match `v*` pattern
- Version must be valid semver
- No duplicate tags

**Install hooks:**
```bash
bash scripts/install_hooks.sh
```

## Multi-Component Versioning (Pattern 3)

Based on consult-user-mcp's approach.

### releases.json Structure

```json
{
  "$schema": "./assets/schema/releases.schema.json",
  "releases": [
    {
      "version": "1.2.0",
      "date": "2025-02-04",
      "highlight": "Multi-platform support",
      "changes": [
        {
          "text": "Added Windows compatibility",
          "type": "added"
        },
        {
          "text": "Fixed race condition in async handler",
          "type": "fixed"
        }
      ]
    }
  ],
  "components": {
    "base-prompt": "1.5.0",
    "macos-app": "1.2.0",
    "cli-tool": "2.0.1"
  }
}
```

### Workflow
1. Edit `releases.json` to add changes
2. Run `generate_changelog.py --from-releases`
3. Run `bump_version.py` (syncs all files)
4. Commit, tag, push

## Cookiecutter Templates

Pre-configured project templates with versioning baked in.

### python-versioned
```bash
cookiecutter cookiecutters/python-versioned/
```

**Includes:**
- pyproject.toml with version field
- src/package/__init__.py with __version__
- CHANGELOG.md
- Git hooks installed
- Release script
- CLAUDE.md versioning section

### node-versioned
```bash
cookiecutter cookiecutters/node-versioned/
```

**Includes:**
- package.json with version and release scripts
- bumpp and changelogithub in devDependencies
- simple-git-hooks configuration
- Release workflow

### multi-component
```bash
cookiecutter cookiecutters/multi-component/
```

**Includes:**
- releases.json with schema
- Multiple component tracking
- Automated changelog generation script
- CI validation workflows

## Integration with CLAUDE.md

`init_versioning.py` adds a versioning section to project CLAUDE.md:

```markdown
## Versioning

Current version: 1.0.0 (in VERSION file)

### Release Process
1. Update CHANGELOG.md with changes
2. Run: python3 scripts/bump_version.py
3. Select version bump type (major/minor/patch)
4. Review and confirm changes
5. Push: git push && git push --tags

### Commit Conventions
Use conventional commit format:
- feat: new feature
- fix: bug fix
- docs: documentation
- chore: maintenance

### Version Files
- Primary: VERSION
- Synced to: src/package/__init__.py

### Git Tags
Format: vX.Y.Z (e.g., v1.0.0)
```

## Common Workflows

### Initial Setup
```bash
cd my-project
python3 /path/to/version-manager/scripts/init_versioning.py
git add .
git commit -m "chore: initialize versioning"
```

### Release New Version
```bash
# Make changes, commit normally
git commit -m "feat: add new feature"

# When ready to release
python3 scripts/bump_version.py --minor
# Review changelog, version files, tag

git push origin main
git push origin v1.1.0
```

### CI Validation
```yaml
# .github/workflows/validate-version.yml
name: Validate Version
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: python3 scripts/validate_version.py
```

### Multi-Component Release
```bash
# 1. Update releases.json
{
  "version": "2.0.0",
  "date": "2025-02-04",
  "highlight": "Major refactor",
  "components": {
    "core": "2.0.0",
    "plugin": "1.5.0"
  }
}

# 2. Generate changelog
python3 scripts/generate_changelog.py --from-releases

# 3. Bump version (syncs all files)
python3 scripts/bump_version.py --major

# 4. Push
git push && git push --tags
```

## Version Format

All patterns use semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards-compatible
- **PATCH**: Bug fixes, backwards-compatible

Pre-release: `1.0.0-alpha.1`, `1.0.0-beta.2`, `1.0.0-rc.1`

See `references/semver.md` for full specification.

## Troubleshooting

**Version files out of sync:**
```bash
python3 scripts/validate_version.py  # Shows which files differ
python3 scripts/sync_versions.py     # Fix sync issues
```

**Git hooks not working:**
```bash
bash scripts/install_hooks.sh        # Reinstall hooks
chmod +x .git/hooks/*                # Ensure executable
```

**Changelog generation fails:**
```bash
# Check commit format
git log --oneline | head -20

# Ensure conventional commits
# See references/conventional-commits.md
```

**Tag already exists:**
```bash
git tag -d v1.0.0                    # Delete local tag
git push origin :refs/tags/v1.0.0   # Delete remote tag
```

## References

- `references/patterns.md` - Pattern selection decision matrix
- `references/conventional-commits.md` - Commit message specification
- `references/semver.md` - Semantic versioning reference
- `assets/schema/releases.schema.json` - JSON schema for releases.json
