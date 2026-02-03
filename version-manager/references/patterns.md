# Versioning Pattern Selection Guide

Choose the right versioning pattern based on project characteristics and team workflow.

## Decision Matrix

| Criteria | Simple | Standard | Advanced | Automated |
|----------|--------|----------|----------|-----------|
| **Project Type** | Go, scripts, single binaries | Python, Node, Rust packages | Multi-component systems | High-velocity releases |
| **Team Size** | 1-2 developers | 2-10 developers | 3+ developers | Any size |
| **Release Frequency** | Infrequent (monthly+) | Regular (weekly-monthly) | Regular (weekly-monthly) | Continuous (daily+) |
| **Automation Need** | Low | Medium | Medium-High | High |
| **CI/CD Maturity** | Basic or none | Basic | Intermediate | Advanced |
| **Complexity Tolerance** | Low | Medium | Medium-High | High |
| **Manual Control** | High | Medium | Medium | Low |

## Pattern Details

### Pattern 1: Simple

**Best for:**
- Go projects without package managers
- Shell scripts and utilities
- Single-binary tools
- Projects with infrequent releases
- Solo developers or small teams

**What you get:**
- Plain text `VERSION` file
- Manual `CHANGELOG.md` updates
- Git hooks for validation
- Manual tagging: `git tag v$(cat VERSION)`

**Pros:**
- Zero dependencies
- Maximum simplicity
- Full manual control
- Easy to understand

**Cons:**
- Manual changelog updates
- No automation
- Easy to forget steps
- More prone to human error

**When to avoid:**
- Package manager projects (use Standard instead)
- Need automated changelog
- High release frequency

---

### Pattern 2: Standard

**Best for:**
- Python packages (PyPI)
- Node packages (npm)
- Rust crates (crates.io)
- Projects with conventional commit workflow
- Teams with basic CI/CD

**What you get:**
- Version in package manifest (package.json, pyproject.toml, Cargo.toml)
- Automated changelog from conventional commits
- Git hooks for validation + commit enforcement
- Tools: bumpp (Node), python-semantic-release (Python), cargo-release (Rust)

**Pros:**
- Industry-standard approach
- Automated changelog generation
- Conventional commit benefits (structured history)
- Good tooling support

**Cons:**
- Requires commit discipline
- Tool-specific learning curve
- Changelog may lack user focus

**When to avoid:**
- Team doesn't want commit conventions
- Multi-component projects (use Advanced)
- Need full automation (use Automated)

---

### Pattern 3: Advanced (Multi-component)

**Best for:**
- Projects with multiple versioned components
- Systems with independent module versions
- Teams wanting user-focused changelogs
- Projects needing component tracking

**What you get:**
- `releases.json` as single source of truth
- JSON schema validation
- Component-specific version tracking
- User-focused change descriptions
- Automated `CHANGELOG.md` generation
- CI validation scripts

**Pros:**
- Fine-grained component control
- User-focused change descriptions
- Schema validation prevents errors
- Flexible for complex projects
- Clear separation: tech (git) vs. user (changelog)

**Cons:**
- More manual work (editing releases.json)
- Higher complexity
- Overkill for simple projects
- Requires discipline to maintain

**When to avoid:**
- Single-component projects (use Standard)
- Need full automation (use Automated)
- Small team, simple workflow (use Simple)

**Example projects:**
- consult-user-mcp (macOS app + base prompt versions)
- Multi-platform tools (CLI + web UI + mobile)
- Plugin systems with core + extensions

---

### Pattern 4: Automated (Full semantic-release)

**Best for:**
- High-velocity CI/CD workflows
- Teams with strict conventional commits
- Projects needing automatic publishing
- Mature DevOps practices

**What you get:**
- Full automation via semantic-release
- GitHub Actions for tag-triggered releases
- Auto-generated changelog and GitHub releases
- Automatic publishing to npm/PyPI/crates.io
- PR validation and CI integration

**Pros:**
- Zero manual intervention
- Impossible to forget steps
- Consistent, repeatable releases
- Perfect for high velocity

**Cons:**
- Highest complexity
- Less manual control
- Requires CI/CD infrastructure
- Debugging can be challenging
- Commit format strictly enforced

**When to avoid:**
- Team wants manual release control
- CI/CD infrastructure not ready
- Infrequent releases (overhead not worth it)
- Learning curve too steep

---

## Migration Paths

### Simple → Standard
1. Create package manifest (package.json, pyproject.toml, etc.)
2. Move version from VERSION to manifest
3. Enable conventional commits (optional)
4. Install standard pattern tools

### Standard → Advanced
1. Create releases.json
2. Migrate changelog entries to releases.json
3. Set up schema validation
4. Configure component tracking
5. Switch changelog generation to releases.json source

### Standard → Automated
1. Ensure strict conventional commits
2. Set up semantic-release config
3. Configure CI/CD workflows
4. Test on staging branch
5. Roll out to main branch

### Advanced → Automated
1. Generate conventional commits from releases.json
2. Set up semantic-release
3. Configure to read from releases.json
4. Automate releases.json updates (custom tooling)

---

## Quick Selection Flowchart

```
Is this a package manager project (npm, PyPI, crates.io)?
├─ YES: Do you want full automation?
│   ├─ YES: Pattern 4 (Automated)
│   └─ NO: Pattern 2 (Standard)
└─ NO: Do you have multiple versioned components?
    ├─ YES: Pattern 3 (Advanced)
    └─ NO: Pattern 1 (Simple)
```

---

## Real-World Examples

**Pattern 1: Simple**
- CLI tools written in Go
- Shell script utilities
- Single-file programs
- Internal tools

**Pattern 2: Standard**
- Most npm packages
- Python libraries on PyPI
- Rust crates
- Single-component web apps

**Pattern 3: Advanced**
- consult-user-mcp (macOS app 1.9.3 + base-prompt 1.3.1)
- Electron apps (main + renderer versions)
- Monorepos with independent releases
- Multi-platform SDKs

**Pattern 4: Automated**
- High-frequency npm packages
- SaaS products with daily deploys
- Large open-source projects
- Enterprise CI/CD pipelines
