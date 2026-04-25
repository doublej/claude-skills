<defaults>
Always initiate skill-creator skill when you start on a request.
Always consider using the skill-researcher skill when looking for existing skills or MCP servers before building from scratch.
When user refers to projects, go up 2 folders, that's where they will be.
</defaults>

<prompt_structure>
Use XML-like tags to enforce structure in SKILL.md and prompt files.
Open/close pairs only (`<rules>...</rules>`).
Not real XML — no attributes, no schema, no validation.
No nesting required; flat sections are fine.
Tags are structural markers to delimit sections (rules, examples, constraints, etc.).
</prompt_structure>

<skill_installation>
MANDATORY final step after creating/updating a skill:
```bash
./install-skill.sh <skill-name>
```
Creates a symlink from `~/.claude/skills/<name>` → the source directory.
Do NOT use any other method (no `claude skills install`, no copying folders, no extracting .skill zips).
For all skills at once: `./install-skill.sh --all`
</skill_installation>
