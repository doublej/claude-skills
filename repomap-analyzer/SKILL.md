---
name: repomap-analyzer
description: Analyze repository for deprecated patterns, mixed conventions, dead code, and duplicate methods using repomap call graph
allowed-tools:
  - Bash
  - Read
  - Write
---

# Repomap Analyzer Skill

Analyze repositories for code quality issues using repomap call graph.

## When to Use

- Auditing code quality
- Finding deprecated patterns or dead code
- Identifying mixed conventions or duplicates
- Generating quality reports

## Usage

```bash
python analyze.py <path-to-repo>
```

## Files

- `analyze.py` - Main analysis script
- `report_generator.py` - Report generation
- `detectors/` - Issue detection modules
- `requirements.txt` - Dependencies
