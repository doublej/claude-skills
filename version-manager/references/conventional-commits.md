# Conventional Commits Specification

Quick reference for conventional commit format used in Pattern 2 (Standard) and Pattern 4 (Automated).

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Description | Semver Impact |
|------|-------------|---------------|
| `feat` | New feature | MINOR bump |
| `fix` | Bug fix | PATCH bump |
| `docs` | Documentation only | No bump |
| `style` | Code style (formatting, missing semicolons, etc.) | No bump |
| `refactor` | Code refactoring (neither adds feature nor fixes bug) | No bump |
| `perf` | Performance improvement | PATCH bump |
| `test` | Adding or updating tests | No bump |
| `chore` | Maintenance tasks (dependency updates, etc.) | No bump |
| `build` | Build system changes | No bump |
| `ci` | CI/CD configuration changes | No bump |
| `revert` | Revert previous commit | Depends on reverted commit |

## Breaking Changes

Add `!` after type/scope OR `BREAKING CHANGE:` in footer:

```
feat!: remove deprecated API
```

```
feat: add new authentication method

BREAKING CHANGE: Old auth tokens are no longer supported
```

Breaking changes trigger a MAJOR version bump.

## Examples

### Feature
```
feat: add user authentication
```

```
feat(api): add GraphQL endpoint for user queries
```

### Bug Fix
```
fix: resolve memory leak in image processor
```

```
fix(ui): correct button alignment on mobile
```

### Documentation
```
docs: update README with installation instructions
```

### Chore
```
chore: update dependencies
```

```
chore(deps): bump lodash from 4.17.20 to 4.17.21
```

### Breaking Change
```
feat!: migrate to API v2

BREAKING CHANGE: API v1 endpoints are removed. See migration guide.
```

## Scope

Optional, indicates which part of codebase is affected:

- `api` - API changes
- `ui` - UI changes
- `cli` - CLI changes
- `core` - Core functionality
- `deps` - Dependencies
- `config` - Configuration

Examples:
```
feat(api): add rate limiting
fix(ui): correct form validation
chore(deps): update TypeScript to 5.0
```

## Body and Footer

### Body
Detailed description of changes:

```
feat: add email notification system

Implemented asynchronous email notifications using SendGrid.
Supports HTML templates and batch sending.
```

### Footer
For breaking changes, issue references:

```
fix: correct date formatting bug

Fixes #123
Closes #456
```

```
feat!: redesign user settings

BREAKING CHANGE: User settings schema has changed.
Old settings must be migrated using migration script.

Refs: #789
```

## Automation Benefits

Conventional commits enable:
1. **Automatic versioning** - Type determines semver bump
2. **Changelog generation** - Commits grouped by type
3. **Release notes** - Formatted for users
4. **CI/CD triggers** - Different actions based on type

## Enforcement

Enable commit-msg hook to enforce format:

```bash
# Create .conventional-commits file to enable
touch .conventional-commits
```

Hook will validate commit messages and reject invalid format.

## Tools

- **commitizen** - CLI tool for guided conventional commits
- **commitlint** - Validate commit messages
- **semantic-release** - Automate versioning and releases (Pattern 4)
- **changelogithub** - Generate changelog from commits (Node)
- **python-semantic-release** - Python version of semantic-release

## Best Practices

1. **Use imperative mood** - "add feature" not "added feature"
2. **Lowercase type** - `feat:` not `Feat:`
3. **No period at end** - "add feature" not "add feature."
4. **Scope is optional** - Only use if it adds clarity
5. **Body explains "why"** - Description is "what"
6. **Breaking changes are explicit** - Use `!` or `BREAKING CHANGE:`
7. **Reference issues** - Add issue numbers in footer

## Bad Examples (Avoid)

```
Update stuff
```
❌ No type, vague description

```
Feat: Added new feature
```
❌ Capitalized type

```
feat: Added user authentication.
```
❌ Past tense, period at end

```
fix lots of bugs
```
❌ No colon after type

```
feat(api): add new endpoint, fix bug, update docs
```
❌ Multiple changes in one commit (split into 3)

## Good Examples

```
feat: add user authentication

Implemented JWT-based authentication with refresh tokens.
Includes login, logout, and token refresh endpoints.
```

```
fix(api): handle null values in user profile

Prevents 500 error when profile fields are missing.
Defaults to empty string for nullable fields.

Fixes #234
```

```
docs: add API documentation for authentication

Includes examples for login, logout, and token refresh.
```

```
chore(deps): update dependencies

- axios: 0.27.2 → 1.2.0
- typescript: 4.9.4 → 5.0.0
```

```
feat!: migrate to API v2

BREAKING CHANGE: API v1 endpoints removed. All clients must migrate to v2.

Migration guide: docs/MIGRATION.md
Closes #567
```
