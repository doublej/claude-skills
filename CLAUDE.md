Always initiate skill-creator skill when you start on a request.
Always consider using the skill-researcher skill when looking for existing skills or MCP servers before building from scratch.
When user refers to projects, go up 2 folders, that's where they will be.

## Skill installation (MANDATORY final step)

After creating/updating a skill, you MUST install it by running:
```bash
./install-skill.sh <skill-name>
```
This creates a symlink from `~/.claude/skills/<name>` → the source directory.
Do NOT use any other method (no `claude skills install`, no copying folders, no extracting .skill zips).
For all skills at once: `./install-skill.sh --all`