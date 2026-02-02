# Content Extraction Strategy

Patterns and strategies for extracting content from project files to populate documentation sites.

## Overview

The goal is to extract all necessary information from existing project files without asking the user questions. Make intelligent defaults when information is missing.

## Source Files Priority

1. **README.md** - Primary source for content
2. **package.json** - Metadata, dependencies, repository URL
3. **pyproject.toml** - Python project metadata
4. **Cargo.toml** - Rust project metadata
5. **Project files** - Fallback analysis if README is minimal

## README.md Extraction

### Project Title

**Strategy:**
1. First H1 heading: `# Project Name`
2. If no H1, use package.json `name` field
3. Convert kebab-case to Title Case: `my-project` → `My Project`

**Regex:**
```regex
^#\s+(.+)$
```

**Example:**
```markdown
# Consult User MCP

Claude Code MCP server that provides beautiful native macOS dialogs...
```

Extract: `"Consult User MCP"`

### Project Description

**Strategy:**
1. First paragraph after title (1-3 sentences)
2. If no clear paragraph, use package.json `description`
3. If neither exists, generate from project name: `"A [type] for [purpose]"`

**Pattern:**
- Skip H1 title
- Skip any images/badges
- Take first paragraph (1-3 sentences, usually 100-200 characters)

**Example:**
```markdown
# My Project

![Badge](...)

Claude Code MCP server that provides beautiful native macOS dialogs for user input, replacing basic text prompts with rich, accessible UI components.

More content...
```

Extract: `"Claude Code MCP server that provides beautiful native macOS dialogs for user input, replacing basic text prompts with rich, accessible UI components."`

### Features

**Strategy:**
1. Look for sections titled: "Features", "Why [Project]", "What it does", "Highlights"
2. Parse bullet points under that section
3. If no features section, extract key points from description
4. Generate 3-6 features minimum

**Section headers to search:**
```regex
^##\s+(Features|Why .+|What it does|Highlights|Key Features)
```

**Bullet point formats:**
```markdown
- **Feature name**: Description
- **Feature name** - Description
* Feature name: Description
- Feature name - Description
```

**Parsing regex:**
```regex
^[\-\*]\s+\*\*(.+?)\*\*[\:\-]\s*(.+)$
^[\-\*]\s+(.+?)[\:\-]\s*(.+)$
```

**Example:**
```markdown
## Features

- **Native dialogs**: Beautiful macOS-native input dialogs
- **Type-safe**: Full TypeScript support with type inference
- **Accessible**: Keyboard navigation and screen reader support
```

Extract:
```javascript
[
  {
    title: "Native dialogs",
    description: "Beautiful macOS-native input dialogs"
  },
  {
    title: "Type-safe",
    description: "Full TypeScript support with type inference"
  },
  {
    title: "Accessible",
    description: "Keyboard navigation and screen reader support"
  }
]
```

**Fallback (if no features section):**
Generate from project type:
- CLI Tool: "Simple CLI", "Fast execution", "Cross-platform"
- Library: "Easy to use", "Well documented", "Actively maintained"
- MCP Server: "Claude integration", "Native UI", "Type-safe"

### Installation Command

**Strategy:**
1. Search for code blocks containing install commands
2. Look for sections titled: "Installation", "Install", "Getting Started", "Quick Start"
3. Extract first command that installs the package

**Command patterns:**
```bash
npm install package-name
npm i package-name
bun add package-name
pip install package-name
cargo install package-name
brew install package-name
```

**Regex:**
```regex
(npm|bun|pip|cargo|brew)\s+(install|add|i)\s+([\w\-@/]+)
```

**Example:**
```markdown
## Installation

```bash
npm install @jjverlaan/consult-user-mcp
```
```

Extract: `"npm install @jjverlaan/consult-user-mcp"`

**Fallback:**
Generate from package.json:
- Node.js: `npm install ${packageName}`
- Python: `pip install ${packageName}`
- Rust: `cargo install ${packageName}`

### Getting Started Steps

**Strategy:**
1. Look for sections: "Getting Started", "Quick Start", "Usage", "How to use"
2. Extract numbered or bulleted steps
3. Include code examples if present
4. Generate 3-5 steps

**Section headers:**
```regex
^##\s+(Getting Started|Quick Start|Usage|How to use|Quickstart)
```

**Step patterns:**
```markdown
1. First step
2. Second step

- Step one
- Step two

**Step 1**: Description
```

**Example:**
```markdown
## Getting Started

1. Install the package
   ```bash
   npm install my-package
   ```

2. Import and use
   ```javascript
   import { myFunction } from 'my-package';
   ```

3. Configure options
   ```javascript
   myFunction({ option: 'value' });
   ```
```

Extract:
```javascript
[
  {
    title: "Install the package",
    description: "Add to your project dependencies",
    code: "npm install my-package"
  },
  {
    title: "Import and use",
    description: "Import the main function",
    code: "import { myFunction } from 'my-package';"
  },
  {
    title: "Configure options",
    description: "Customize behavior with options",
    code: "myFunction({ option: 'value' });"
  }
]
```

**Fallback:**
Generate basic steps from project type:
1. Installation step (from install command)
2. Basic usage step
3. Configuration step (if applicable)

### Architecture/Diagram

**Strategy:**
1. Look for architecture diagrams (Mermaid, images)
2. If found, extract and render
3. If not found, skip section (optional)

**Indicators:**
```markdown
```mermaid
![Architecture](...)
## Architecture
```

## package.json Extraction

### Fields to Extract

```json
{
  "name": "package-name",           // Project name
  "version": "1.0.0",               // Version
  "description": "...",             // Description (fallback)
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "homepage": "https://...",        // Homepage URL
  "license": "MIT",                 // License
  "keywords": ["..."],              // Keywords (for features)
  "dependencies": { ... },          // Tech stack
  "bin": { ... }                    // Indicates CLI tool
}
```

### Repository URL Parsing

**From repository.url:**
```javascript
// Input: "git+https://github.com/user/repo.git"
// Extract: "https://github.com/user/repo"

const url = repoUrl
  .replace('git+', '')
  .replace('.git', '');
```

**GitHub username and repo name:**
```javascript
// Input: "https://github.com/user/repo"
// Extract: user="user", repo="repo"

const match = url.match(/github\.com\/([^\/]+)\/([^\/]+)/);
const [_, user, repo] = match;
```

### Tech Stack from Dependencies

**Strategy:**
1. Extract dependency names from `dependencies` and `devDependencies`
2. Categorize by type
3. Create tech stack showcase

**Categorization:**
```javascript
const categories = {
  frontend: ['svelte', 'react', 'vue', 'solid'],
  backend: ['express', 'fastify', 'hono', 'elysia'],
  database: ['prisma', 'drizzle', 'mongodb', 'postgres'],
  testing: ['vitest', 'jest', 'playwright', 'cypress'],
  build: ['vite', 'webpack', 'rollup', 'esbuild'],
  language: ['typescript', 'javascript']
};
```

**Example:**
```json
{
  "dependencies": {
    "@sveltejs/kit": "^2.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

Extract:
```javascript
[
  { name: "SvelteKit", category: "frontend" },
  { name: "TypeScript", category: "language" },
  { name: "Vite", category: "build" }
]
```

## Project Type Detection

### CLI Tool Detection

**Indicators:**
- `bin` field in package.json
- `scripts.start` includes CLI commands
- Dependencies: `commander`, `yargs`, `cac`, `oclif`
- README mentions CLI usage

**Example:**
```json
{
  "bin": {
    "my-cli": "./dist/cli.js"
  }
}
```

Type: `"CLI Tool"`

### Library Detection

**Indicators:**
- `main` or `exports` field
- No `bin` field
- README has "Installation" and "API" sections

Type: `"Library"`

### MCP Server Detection

**Indicators:**
- Package name contains "mcp"
- Dependencies include MCP-related packages
- README mentions "Claude" or "MCP"

Type: `"MCP Server"`

### Web App Detection

**Indicators:**
- Dependencies include framework (react, svelte, vue)
- `scripts.dev` or `scripts.start` exists
- README mentions "development server"

Type: `"Web Application"`

## Intelligent Defaults

### When README is Minimal

If README is missing or very short (< 200 characters):

1. **Title:** Use package.json name (Title Case)
2. **Description:** Use package.json description or generate
3. **Features:** Generate from project type and dependencies
4. **Installation:** Generate from package.json name
5. **Getting Started:** Generate basic 3-step guide

### Generated Features by Type

**CLI Tool:**
```javascript
[
  { title: "Simple CLI", description: "Easy-to-use command-line interface" },
  { title: "Fast", description: "Optimized for performance" },
  { title: "Cross-platform", description: "Works on macOS, Linux, and Windows" }
]
```

**Library:**
```javascript
[
  { title: "Easy to use", description: "Simple, intuitive API" },
  { title: "Well documented", description: "Comprehensive documentation and examples" },
  { title: "Type-safe", description: "Full TypeScript support" }
]
```

**MCP Server:**
```javascript
[
  { title: "Claude integration", description: "Seamless integration with Claude" },
  { title: "Native UI", description: "Beautiful native user interfaces" },
  { title: "Type-safe", description: "Full TypeScript support with type inference" }
]
```

### Generated Getting Started

**CLI Tool:**
```javascript
[
  {
    title: "Install globally",
    code: "npm install -g ${packageName}"
  },
  {
    title: "Run the CLI",
    code: "${binName} --help"
  },
  {
    title: "Use in your project",
    code: "${binName} [command] [options]"
  }
]
```

**Library:**
```javascript
[
  {
    title: "Install the package",
    code: "npm install ${packageName}"
  },
  {
    title: "Import and use",
    code: "import { ${mainExport} } from '${packageName}';"
  },
  {
    title: "Start building",
    description: "Check the API documentation for available methods"
  }
]
```

## Content Validation

### Required Fields

Ensure these fields are populated (with fallbacks):
- Project title
- Description (1-3 sentences)
- Installation command
- At least 3 features
- At least 3 getting started steps
- Repository URL
- License (or "MIT" default)

### Quality Checks

- Description is 100-300 characters
- Each feature has title + description
- Installation command is valid for package manager
- Getting started steps are sequential and logical
- Repository URL is valid GitHub URL

## Example: Complete Extraction

**Input (README.md):**
```markdown
# Consult User MCP

![npm version](...)

Claude Code MCP server that provides beautiful native macOS dialogs for user input, replacing basic text prompts with rich, accessible UI components.

## Features

- **Native dialogs**: Beautiful macOS-native input dialogs
- **Multiple input types**: Confirmation, multiple choice, text input, multi-question flows
- **Type-safe**: Full TypeScript support with type inference

## Installation

```bash
npm install @jjverlaan/consult-user-mcp
```

## Quick Start

1. Install the package
2. Add to your Claude Code MCP servers configuration
3. Use in your prompts
```

**Input (package.json):**
```json
{
  "name": "@jjverlaan/consult-user-mcp",
  "version": "1.0.0",
  "description": "Beautiful native macOS dialogs for Claude Code",
  "repository": {
    "url": "https://github.com/jjverlaan/consult-user-mcp"
  },
  "license": "MIT"
}
```

**Extracted Output:**
```javascript
{
  title: "Consult User MCP",
  description: "Claude Code MCP server that provides beautiful native macOS dialogs for user input, replacing basic text prompts with rich, accessible UI components.",
  installCommand: "npm install @jjverlaan/consult-user-mcp",
  repoUrl: "https://github.com/jjverlaan/consult-user-mcp",
  license: "MIT",
  features: [
    {
      title: "Native dialogs",
      description: "Beautiful macOS-native input dialogs"
    },
    {
      title: "Multiple input types",
      description: "Confirmation, multiple choice, text input, multi-question flows"
    },
    {
      title: "Type-safe",
      description: "Full TypeScript support with type inference"
    }
  ],
  gettingStarted: [
    {
      title: "Install the package",
      code: "npm install @jjverlaan/consult-user-mcp"
    },
    {
      title: "Add to your Claude Code MCP servers configuration",
      description: "Configure in your settings"
    },
    {
      title: "Use in your prompts",
      description: "Start asking questions with beautiful dialogs"
    }
  ],
  projectType: "MCP Server"
}
```
