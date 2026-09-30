---
name: skill-overview
description: "Display a compact table of all available skills and descriptions"
---

# Skill Overview

Display all SKILL.md files in a compact table format.

## Presentation

Open with the banner, then wrap the script's table in the report.

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   SKILL OVERVIEW                                             ║
║   Compact table of every installed skill                     ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

SKILL OVERVIEW  ──  <skills dir>   skills: <n>

SKILL                     DESCRIPTION
──────────────────────────────────────────────────────────────
<skill-name>              <truncated description|—>

github.com/doublej
```

## Usage

Run the script with the skills directory as argument:

```bash
python3 scripts/list_skills.py /path/to/skills
```

Output shows skill name and truncated description in aligned columns.
