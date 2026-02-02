---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. **Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

- **High freedom**: Multiple approaches valid, context-dependent decisions
- **Medium freedom**: Preferred pattern exists, some variation acceptable
- **Low freedom**: Operations fragile/error-prone, consistency critical

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/     - Executable code
    ├── references/  - Documentation loaded as needed
    └── assets/      - Files used in output (templates, etc.)
```

#### Scripts (`scripts/`)
- When the same code is being rewritten repeatedly
- Token efficient, deterministic, may be executed without loading into context

#### References (`references/`)
- Documentation loaded as needed into context
- Keeps SKILL.md lean
- If files are large (>10k words), include grep search patterns in SKILL.md

#### Assets (`assets/`)
- Files used in output (templates, images, fonts, boilerplate)
- NOT loaded into context, used within output Claude produces

#### What NOT to Include
- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.
- Only include what an AI agent needs to do the job

### Progressive Disclosure

1. **Metadata** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude

Keep SKILL.md under 500 lines. Split content into separate files when approaching this limit.

## Skill Creation Process

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources and write SKILL.md)
5. Package the skill (run package_skill.py)
6. Iterate based on real usage

### Step 1: Understanding with Concrete Examples

Ask questions like:
- "What functionality should the skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

### Step 2: Planning Reusable Contents

For each example, identify what scripts, references, and assets would be helpful:
- Repetitive code → `scripts/`
- Schema/API docs → `references/`
- Templates/boilerplate → `assets/`

### Step 3: Initializing the Skill

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates skill directory with SKILL.md template and example resource directories.

### Step 4: Edit the Skill

#### Learn Proven Design Patterns
- **Multi-step processes**: See references/workflows.md
- **Output formats/quality standards**: See references/output-patterns.md

#### Update SKILL.md

**Frontmatter:**
- `name`: The skill name (hyphen-case)
- `description`: Primary triggering mechanism. Include what the skill does AND when to use it.

**Body:** Instructions for using the skill and its bundled resources. Use imperative/infinitive form.

### Step 5: Packaging a Skill

```bash
scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Validates and packages skill into distributable .skill file.

### Step 6: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or bundled resources
4. Test again
