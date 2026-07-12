---
name: code-audit
description: "Audit code quality via code-map's PageRank call graph: dead code, duplicate methods, deprecated patterns, naming inconsistencies. Use when auditing codebase health or hunting dead/duplicate code; owns the smells dimension for code-optimize. Triggers on 'code audit', 'find dead code', 'duplicate code', 'code smells'."
---

<intro>

Automated code quality analysis powered by code-map's PageRank call graph. Detects deprecated patterns, naming inconsistencies, dead code, and duplicate methods.

</intro>

<prerequisites>

Requires the **code-map** skill installed alongside this skill (uses its bundled repomap).

</prerequisites>

<usage>

```bash
python3 {SKILL_DIR}/analyze.py <path-to-repo>
```

### With custom output and token limit

```bash
python3 {SKILL_DIR}/analyze.py <path-to-repo> --output report.md --map-tokens 16384
```

## Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--output` | `repomap-analysis.md` | Output report file path |
| `--map-tokens` | `32768` | Token limit for repomap generation |

</usage>

<detectors>

| Detector | What It Finds |
|----------|---------------|
| `deprecated` | Deprecated markers (`@deprecated`, `# TODO...remove`), naming inconsistencies between old/new conventions |
| `conventions` | Mixed naming styles (snake_case vs camelCase), import order violations, mixed quote styles |
| `deadcode` | PageRank=0 definitions (unreferenced), commented-out code, unused imports |
| `duplicates` | Duplicate function signatures across files, similar function bodies |

</detectors>

<output_format>

```markdown
# Repository Analysis Report

**Generated**: 2025-06-15 14:30:00
**Repository**: `/path/to/repo`

## Summary

- **Total Issues**: 23
- **Deprecated Patterns**: 4
- **Mixed Conventions**: 6
- **Dead Code Paths**: 8
- **Duplicate Methods**: 5

## Deprecated Patterns (4 issues)

- `src/utils.py:15` - Deprecated marker found: # deprecated: use new_func
- `src/old.py:0` - Old convention 'getData' used alongside new 'get_data'

## Dead Code Paths (8 issues)

- `src/legacy.py:42` - 'old_handler' has PageRank 0 (unreferenced)
- `src/helpers.py:8` - Unused import: collections
```

Findings are sorted by severity (critical > high > medium > low), then by file and line number.

</output_format>

<workflows>

1. Run analysis: `python3 {SKILL_DIR}/analyze.py /path/to/project`
2. Review `repomap-analysis.md` for issues
3. Address high-severity findings first

## Workflow: Feed into Refactoring

1. Run structural map first: `bash code-map/scripts/repomap.sh . --root . --exclude-unranked`
2. Run analysis: `python3 {SKILL_DIR}/analyze.py .`
3. Use findings as input for code-optimize to generate actionable tasks

</workflows>

<related_skills>

| Skill | Relationship |
|-------|-------------|
| **code-map** | Provides the repomap engine (required dependency) |
| **code-optimize** | Consumes analysis output to generate refactoring tasks (owns the `smells` dimension) |

</related_skills>
