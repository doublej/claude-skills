---
name: code-map
description: "Importance-ranked repo maps via Tree-sitter parsing and PageRank"
---

# Codebase Mapper

Generate a structural map of any codebase ranked by importance. Uses Tree-sitter for code parsing and PageRank for ranking file/symbol significance.

<setup>
Auto-installs on first run. All code is bundled in `scripts/repomap/`.
</setup>

<usage>

Run from any directory. The wrapper handles venv setup and activation.

### Quick map of current project

```bash
bash {SKILL_DIR}/scripts/repomap.sh . --root .
```

### Focused map (specific files/dirs)

```bash
bash {SKILL_DIR}/scripts/repomap.sh src/ --root . --map-tokens 4096
```

### With focus files (files being actively investigated)

```bash
bash {SKILL_DIR}/scripts/repomap.sh . --root . --focus-files main.py utils.py
```

### Exclude noise

```bash
bash {SKILL_DIR}/scripts/repomap.sh . --root . --exclude-extensions .json .css .svg --exclude-unranked
```

</usage>

<key_options>

| Flag | Default | Purpose |
|------|---------|---------|
| `--root` | `.` | Repository root directory |
| `--map-tokens` | `65536` | Max tokens in output |
| `--focus-files` | — | Files being actively worked on (20x boost) |
| `--mentioned-files` | — | Files mentioned in conversation (5x boost) |
| `--mentioned-idents` | — | Identifiers to trace across codebase (10x) |
| `--context-files` | — | Additional files to include in map |
| `--exclude-unranked` | off | Skip PageRank=0 files |
| `--exclude-extensions` | — | Skip file types (e.g. `.json .css`) |
| `--exclude-dirs` | — | Skip directories (e.g. `build dist sketches`) |
| `--no-gitignore` | off | Include .gitignore'd files (default: respect .gitignore) |
| `--force-refresh` | off | Clear cache and recompute |
| `--verbose` | off | Show debug info |

</key_options>

<output_format>

```
Analysed 147 files · ranked 89 · ~4052 tokens

src/core/engine.py:
(Rank value: 100.0000)
  46: class Engine:
  49:     def __init__(...):
  93:     def process(self):

src/utils.py:
(Rank value: 56.2391)
  18: Tag = namedtuple(...)
  21: def count_tokens(...):
```

Files sorted by PageRank score (0–100 scale, highest first). Each entry shows key definitions with line numbers. Respects `.gitignore` by default.

</output_format>

<workflows>

## Explore a New Codebase

1. Run a broad map: `bash {SKILL_DIR}/scripts/repomap.sh . --root . --map-tokens 8192 --exclude-unranked`
2. Read the top-ranked files to understand architecture
3. For deeper dive, re-run with `--focus-files` pointing to the files you're investigating
4. Use `--mentioned-idents` to boost specific classes/functions you're tracing

## Prepare Context for Refactoring

1. Map the target area: `bash {SKILL_DIR}/scripts/repomap.sh src/module/ --root . --map-tokens 4096`
2. Identify high-rank files (most referenced/depended upon)
3. Read those files to understand coupling before making changes

## Full Codebase Audit (with related skills)

1. **Map** — Generate structural overview with this skill
2. **Detect** — Run repomap-analyzer for automated quality findings (deprecated patterns, dead code, duplicates)
3. **Analyse** — Run dev-refactor for deeper multi-dimensional analysis and task generation

</workflows>

<supported_languages>
47+ languages including Python, JavaScript, TypeScript, Rust, Go, Java, C/C++, Swift, Ruby, Kotlin, Dart, Elixir, and more.
</supported_languages>

<cache>
Results are cached in `.repomap.tags.cache.v1/` in the working directory. Use `--force-refresh` to clear.
</cache>

<related_skills>

| Skill | Relationship |
|-------|-------------|
| **repomap-analyzer** | Uses this skill's repomap output to detect code quality issues |
| **dev-refactor** | Uses this skill for structural mapping in Step 2 of its workflow |

</related_skills>
