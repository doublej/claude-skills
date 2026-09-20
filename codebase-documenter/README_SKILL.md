# Codebase Documenter Skill

A comprehensive skill for generating technical documentation from source code.

## What It Does

Analyzes codebases to generate:
- **Architecture documentation** (system design, component diagrams)
- **API references** (endpoints, functions, schemas)
- **Onboarding guides** (setup, workflows, conventions)
- **Project READMEs** (quick start, tech stack)

## Key Features

### 1. Smart Framework Detection
- Detects languages (Python, TypeScript, Go, Rust, Swift, etc.)
- Identifies frameworks (FastAPI, React, Next.js, Django, Express, etc.)
- Fetches framework-specific best practices via Context7 integration

### 2. Automated Analysis
- `analyze_project.py` - Scans project structure, detects technologies
- `extract_api.py` - Extracts API endpoints/functions (planned)
- `generate_mermaid.py` - Creates architecture diagrams (planned)

### 3. Template-Based Generation
- Pre-built templates for ARCHITECTURE.md, API.md, CONTRIBUTING.md
- Mermaid diagram snippets (C4, sequence, ER diagrams, etc.)
- Framework-specific patterns reference

### 4. Hybrid Pattern Lookup
- Uses Context7 for framework documentation
- References built-in patterns for common stacks
- Generates docs informed by best practices

## Usage

```bash
# Trigger the skill
/codebase-documenter

# Or ask naturally
"Document this codebase"
"Create architecture docs for this project"
"Generate API reference"
```

## Components

### SKILL.md
Main skill instructions with:
- When to use this skill
- 4-phase workflow (Discovery → Pattern Lookup → Generation → Quality Check)
- Decision framework for what docs to generate
- Integration with Context7 for framework patterns

### Scripts

**`scripts/analyze_project.py`**
- Detects languages, frameworks, entry points, dependencies
- Builds project structure tree
- Outputs JSON analysis report
- Handles monorepos and multi-package projects

### References

**`references/framework_patterns.md`**
- Architectural patterns for FastAPI, Next.js, React, Django, Express, Go, Rust
- Standard project structures
- Key concepts and patterns

**`references/doc_templates.md`**
- Templates for ARCHITECTURE.md, API.md, CONTRIBUTING.md, README.md
- Variable placeholders and usage notes
- Length guidelines

### Assets

**`assets/mermaid_snippets.md`**
- 12+ reusable Mermaid diagram patterns
- C4 diagrams, sequence flows, ER diagrams, state machines
- Usage tips and customization guide

## Example Workflow

```
User: "Document this FastAPI codebase"

1. Run analyze_project.py
   → Detects: FastAPI + SQLAlchemy + Pydantic

2. Query Context7
   → "FastAPI project structure best practices"

3. Generate docs:
   - ARCHITECTURE.md (layered architecture diagram)
   - API.md (endpoints with request/response schemas)
   - CONTRIBUTING.md (setup with poetry, pytest)

4. Create Mermaid diagrams
   → Request flow: routes → services → models → database
```

## Supported Frameworks

- **Backend**: FastAPI, Django, Flask, Express, NestJS, Gin, Actix, Spring
- **Frontend**: React, Next.js, Vue, Svelte
- **Languages**: Python, TypeScript, JavaScript, Go, Rust, Java, Swift, Kotlin

## Output Structure

```
project/
├── docs/
│   ├── ARCHITECTURE.md    # System design + diagrams
│   ├── API.md             # Endpoint/function reference
│   └── CONTRIBUTING.md    # Onboarding guide
├── README.md              # Updated/created if needed
└── ...existing code...
```

## Quality Standards

- **Concise**: Architecture docs 200-500 lines
- **Accurate**: All code examples from actual codebase
- **Clear**: Explains "why" not just "what"
- **Traceable**: Links to source files with line numbers
- **Current**: Notes framework versions

## Integration Points

### Context7 MCP
- Resolves library IDs for detected frameworks
- Queries architectural best practices
- Ensures docs align with official patterns

### Future Integrations
- Tree-sitter for AST-based API extraction
- Custom MCP servers for company-specific patterns
- Git history analysis for change documentation

## Roadmap

### Phase 1 (Current)
- ✅ Project structure analysis
- ✅ Framework detection
- ✅ Template-based documentation
- ✅ Mermaid diagram snippets

### Phase 2 (Planned)
- ⏳ `extract_api.py` - Tree-sitter based API extraction
- ⏳ `generate_mermaid.py` - Automated diagram generation
- ⏳ Monorepo support improvements

### Phase 3 (Future)
- 📋 Git history analysis for changelog
- 📋 Dependency graph visualization
- 📋 Interactive documentation browser

## Notes

- **Never invents code** - only documents what exists
- **Validates examples** - ensures code snippets are from codebase
- **Prefers docs/ directory** - keeps documentation close to code
- **Detects frameworks automatically** - no manual configuration
- **Integrates with existing tools** - works with Context7, Mermaid

## Installation

The skill is already packaged as `codebase-documenter.skill` and ready for use.

For manual testing:
```bash
python3 scripts/analyze_project.py /path/to/project --output analysis.json
```

## Created By

Generated via skill-researcher + skill-creator workflow
Date: 2026-02-03
Research: Documentation generation tools, framework patterns, AST analysis
