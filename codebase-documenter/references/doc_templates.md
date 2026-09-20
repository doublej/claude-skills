# Documentation Templates

Templates for different documentation sections. Use as starting structure.

## ARCHITECTURE.md Template

```markdown
# Architecture Overview

> Auto-generated on [DATE] by Claude Code codebase-documenter skill

## System Design

[Mermaid diagram showing components and relationships]

## Technology Stack

- **Language**: [Primary language + version]
- **Framework**: [Main framework + version]
- **Database**: [If applicable]
- **Key Libraries**: [Top 3-5 dependencies]

## Project Structure

[Brief explanation of directory organization]

\`\`\`
project/
├── [directory]/  # Purpose
├── [directory]/  # Purpose
└── ...
\`\`\`

## Component Responsibilities

### [Component Name]
**Purpose**: [What it does]
**Location**: [Files/directories]
**Dependencies**: [What it depends on]

[Repeat for main components]

## Data Flow

[Explanation of how data moves through the system]

\`\`\`mermaid
sequenceDiagram
    [Example sequence]
\`\`\`

## External Dependencies

| Dependency | Purpose | Documentation |
|------------|---------|---------------|
| [Name] | [Why used] | [Link] |

## Configuration

Key configuration files:
- \`[file]\`: [Purpose]

## Build & Deployment

[Brief overview of build process and deployment]
```

---

## API.md Template

```markdown
# API Reference

> Auto-generated on [DATE] from codebase analysis

## Overview

[Brief description of API purpose and authentication]

## Base URL

\`\`\`
[Environment]: [URL]
\`\`\`

## Authentication

[How to authenticate, if applicable]

## Endpoints

### [Method] /path/to/endpoint

**Description**: [What this endpoint does]

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| [param] | [type] | Yes/No | [desc] |

**Request Example**:
\`\`\`json
{
  "example": "request"
}
\`\`\`

**Response Example**:
\`\`\`json
{
  "example": "response"
}
\`\`\`

**Errors**:
| Code | Description |
|------|-------------|
| 400 | Bad request |
| 404 | Not found |

**Source**: \`[file:line]\`

[Repeat for each endpoint]

---

## Data Models

### [Model Name]

\`\`\`typescript
{
  field: type  // description
}
\`\`\`

**Source**: \`[file:line]\`
```

---

## CONTRIBUTING.md Template

```markdown
# Contributing Guide

> Auto-generated on [DATE] by Claude Code codebase-documenter skill

## Getting Started

### Prerequisites

- [Tool] version [X.Y.Z]
- [Other requirements]

### Setup

1. Clone the repository:
   \`\`\`bash
   git clone [repo-url]
   cd [project-name]
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   [install command]
   \`\`\`

3. Configure environment:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your settings
   \`\`\`

4. Run the application:
   \`\`\`bash
   [run command]
   \`\`\`

## Development Workflow

### Code Organization

[Explanation of how code is organized]

### Making Changes

1. Create a feature branch:
   \`\`\`bash
   git checkout -b feature/your-feature
   \`\`\`

2. Make your changes following our [conventions](#conventions)

3. Test your changes:
   \`\`\`bash
   [test command]
   \`\`\`

4. Commit with a clear message:
   \`\`\`bash
   git commit -m "feat: description"
   \`\`\`

## Conventions

### Code Style

[Language-specific style guide or linter]

### Commit Messages

Follow [conventional commits](https://www.conventionalcommits.org/):
- \`feat:\` New feature
- \`fix:\` Bug fix
- \`docs:\` Documentation
- \`refactor:\` Code refactoring
- \`test:\` Testing

### File Naming

[Project-specific naming conventions]

## Testing

### Running Tests

\`\`\`bash
[test command]
\`\`\`

### Writing Tests

[Where to put tests, naming conventions, example]

## Deployment

[Deployment process or link to deployment docs]

## Questions?

[How to get help - Slack, Discord, Issues, etc.]
```

---

## README.md Template (if missing)

```markdown
# [Project Name]

[One-sentence description of what this project does]

## Quick Start

\`\`\`bash
# Install
[install command]

# Run
[run command]
\`\`\`

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Contributing Guide](docs/CONTRIBUTING.md)

## Tech Stack

[Brief list of main technologies]

## License

[License info if available]
```

---

## Usage Notes

### Template Variables

Replace bracketed placeholders:
- `[DATE]` → Current date
- `[file:line]` → Source reference
- `[Component Name]` → Actual component name
- `[Description]` → Context-specific text

### Mermaid Diagrams

Use appropriate diagram types:
- **Architecture**: C4 diagram or component diagram
- **Data flow**: Sequence diagram
- **State**: State diagram
- **Dependencies**: Graph diagram

### Length Guidelines

- **ARCHITECTURE.md**: 200-500 lines
- **API.md**: 1 page per major component
- **CONTRIBUTING.md**: < 300 lines
- **README.md**: < 150 lines

### Table of Contents

Add TOC for documents > 100 lines:
```markdown
## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
```
