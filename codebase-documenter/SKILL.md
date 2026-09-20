---
name: codebase-documenter
description: "Generate architecture docs, API references, onboarding guides from code"
---

# Codebase Documenter

Generate comprehensive technical documentation from source code by analyzing project structure, detecting frameworks, and creating architecture guides, API references, and onboarding documentation.

## When to Use

Trigger this skill when:
- User asks to "document this codebase/project"
- Creating architecture diagrams or system design docs
- Generating API/SDK reference documentation
- Building onboarding guides for contributors
- Analyzing project structure for new team members

## Workflow

### 1. Discovery Phase

**Analyze project structure:**
```bash
scripts/analyze_project.py <project_path>
```

This script detects:
- Languages and frameworks used
- Project structure (monorepo, multi-package, single app)
- Entry points (main files, API routes, CLI commands)
- Dependencies and external integrations
- Build tools and configuration files

**Output:** `analysis_report.json` with detected technologies and structure.

### 2. Framework Pattern Lookup (Hybrid Approach)

For detected frameworks, fetch relevant patterns:
- Use `mcp__plugin_context7_context7__resolve-library-id` to find framework documentation
- Query architectural patterns for detected stack
- Reference `references/framework_patterns.md` for common patterns

**Example:**
```
Detected: FastAPI + SQLAlchemy + React
→ Lookup: FastAPI project structure best practices
→ Lookup: React component organization patterns
```

### 3. Documentation Generation

Generate documentation sections in this order:

#### A. Architecture Overview (`docs/ARCHITECTURE.md`)
- System design diagram (use Mermaid)
- Component responsibilities
- Data flow between layers
- External dependencies and integrations
- Technology stack justification

#### B. API Reference (`docs/API.md`)
- Endpoints/functions with signatures
- Request/response schemas
- Authentication/authorization
- Error codes and handling
- Rate limits (if applicable)

#### C. Onboarding Guide (`docs/CONTRIBUTING.md`)
- Setup instructions
- Development workflow
- Code organization conventions
- Testing strategy
- Deployment process

#### D. Project README (`README.md`)
Only generate if missing or severely outdated:
- Project purpose (1-2 sentences)
- Quick start (installation + first run)
- Link to detailed docs
- License and contribution info

### 4. Quality Standards

**Conciseness:**
- Architecture docs: 200-500 lines
- API reference: 1 page per major component
- Onboarding: < 300 lines

**Accuracy:**
- Verify all code paths exist
- Validate imports and dependencies
- Check configuration examples work

**Clarity:**
- Use code examples from the actual codebase
- Explain "why" not just "what"
- Link to external framework docs where appropriate

## Scripts

### `scripts/analyze_project.py`
Analyzes project structure and detects technologies.

**Usage:**
```bash
python3 scripts/analyze_project.py <project_path> [--output analysis.json]
```

**Output:** JSON file with:
- Languages detected (by file extensions)
- Frameworks (by imports, config files)
- Entry points (main.py, index.ts, package.json scripts)
- Dependencies (requirements.txt, package.json, go.mod)
- Project structure tree

### `scripts/extract_api.py`
Extracts API endpoints/functions from code using tree-sitter.

**Usage:**
```bash
python3 scripts/extract_api.py <project_path> --language python [--output api.json]
```

**Supported languages:** Python, TypeScript, JavaScript, Go, Rust

**Output:** JSON with:
- Function signatures
- Docstrings/comments
- Parameters and return types
- File locations

### `scripts/generate_mermaid.py`
Generates Mermaid diagrams from analysis data.

**Usage:**
```bash
python3 scripts/generate_mermaid.py <analysis.json> --type architecture
```

**Types:**
- `architecture` - System component diagram
- `flow` - Data flow between components
- `sequence` - Request/response sequences

## References

### `references/framework_patterns.md`
Common architectural patterns for popular frameworks. Loaded when specific frameworks detected.

### `references/doc_templates.md`
Templates for different documentation sections. Use as starting structure.

## Assets

### `assets/mermaid_snippets.md`
Reusable Mermaid diagram patterns (C4 diagrams, sequence flows, etc.).

## Examples

### Example 1: FastAPI Backend
```
User: "Document this FastAPI codebase"

Steps:
1. Run analyze_project.py → detects FastAPI, SQLAlchemy, Pydantic
2. Query Context7 for FastAPI architectural patterns
3. Extract API endpoints with extract_api.py
4. Generate:
   - ARCHITECTURE.md (layered architecture: routes → services → models)
   - API.md (all endpoints with request/response schemas)
   - CONTRIBUTING.md (setup with poetry, testing with pytest)
5. Create Mermaid diagram showing request flow
```

### Example 2: React/TypeScript Frontend
```
User: "Create onboarding docs for this React project"

Steps:
1. Run analyze_project.py → detects React, Vite, TanStack Query
2. Reference framework_patterns.md for React component organization
3. Extract component tree and props
4. Generate:
   - ARCHITECTURE.md (component hierarchy, state management)
   - CONTRIBUTING.md (setup, component patterns, styling conventions)
5. Skip API.md (no backend in this repo)
```

### Example 3: Monorepo
```
User: "Document this monorepo"

Steps:
1. Detect workspace structure (packages/apps separation)
2. Run analyze_project.py per package
3. Generate root ARCHITECTURE.md showing package relationships
4. Generate per-package docs in each subdirectory
5. Create root README with package overview
```

## Decision Framework

**When to generate which docs:**
- Always: ARCHITECTURE.md (high-level overview)
- If API exists: API.md (endpoints/functions)
- If complex setup: CONTRIBUTING.md (onboarding)
- If README missing/bad: README.md (project summary)

**When to skip:**
- Documentation already comprehensive (validate with user)
- Codebase < 500 lines (inline comments sufficient)
- Legacy project with no maintenance (low value)

## Integration with Context7

When frameworks detected:
1. Use `resolve-library-id` to find framework documentation
2. Query architectural best practices:
   ```
   "What is the recommended project structure for [framework] applications?"
   "What are common patterns for [framework] dependency management?"
   ```
3. Reference official patterns in generated docs

## Output Format

Generate documentation as Markdown files in `docs/` directory:
```
project/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── CONTRIBUTING.md
├── README.md (updated or created)
└── ...existing code...
```

Each document includes:
- Auto-generated notice with timestamp
- Table of contents (if > 100 lines)
- Code examples from actual codebase
- Links to official framework docs
- Mermaid diagrams where helpful

## Notes

- **Never invent code patterns** - only document what exists
- **Validate examples** - ensure all code snippets are from the codebase
- **Link to sources** - reference files/line numbers for traceability
- **Version awareness** - note framework versions in docs
- **Keep docs close to code** - prefer `docs/` directory over wiki/external sites
