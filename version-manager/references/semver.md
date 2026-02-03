# Semantic Versioning Reference

Quick reference for Semantic Versioning (SemVer) 2.0.0.

Full spec: https://semver.org/

## Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

Examples:
- `1.0.0`
- `2.3.5`
- `1.0.0-alpha.1`
- `1.0.0-beta.2+20250204`

## Version Components

### MAJOR (X.0.0)
Increment when making incompatible API changes.

**Examples:**
- Removing features
- Changing function signatures
- Removing deprecated code
- Breaking changes to public API

### MINOR (x.X.0)
Increment when adding functionality in a backwards-compatible manner.

**Examples:**
- Adding new features
- Adding new functions/methods
- Deprecating functionality (without removing)
- Substantial internal improvements

### PATCH (x.x.X)
Increment when making backwards-compatible bug fixes.

**Examples:**
- Bug fixes
- Security patches
- Documentation fixes
- Performance improvements (if no API change)

## Pre-release Versions

Format: `1.0.0-<identifier>.<number>`

**Common identifiers:**
- `alpha` - Early development, unstable
- `beta` - Feature complete, but unstable
- `rc` (release candidate) - Stable, ready for release

**Examples:**
```
1.0.0-alpha.1
1.0.0-alpha.2
1.0.0-beta.1
1.0.0-beta.2
1.0.0-rc.1
1.0.0-rc.2
1.0.0
```

**Ordering:**
`1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0`

## Build Metadata

Format: `1.0.0+<metadata>`

**Examples:**
```
1.0.0+20250204
1.0.0+build.123
1.0.0-beta.1+exp.sha.5114f85
```

Build metadata does NOT affect version precedence.

## Version Precedence

Compare from left to right:

1. `1.0.0 < 2.0.0` (MAJOR)
2. `1.1.0 < 1.2.0` (MINOR)
3. `1.1.1 < 1.1.2` (PATCH)
4. `1.0.0-alpha < 1.0.0` (pre-release < release)
5. `1.0.0-alpha < 1.0.0-beta` (alphabetical)
6. `1.0.0-beta.1 < 1.0.0-beta.2` (numeric)

## Initial Development

### 0.y.z Versions
For initial development, before public API is stable:
- Start with `0.1.0`
- Increment MINOR for features
- Increment PATCH for fixes
- Breaking changes allowed at any time

**When to move to 1.0.0:**
- Public API is stable
- Production-ready
- Backwards compatibility commitment

## Decision Tree

```
Did you break backwards compatibility?
├─ YES: MAJOR (X.0.0)
└─ NO: Did you add new features?
    ├─ YES: MINOR (x.X.0)
    └─ NO: Did you fix bugs or make improvements?
        ├─ YES: PATCH (x.x.X)
        └─ NO: No version change needed
```

## Best Practices

### DO:
✅ Start at `0.1.0` for new projects
✅ Release `1.0.0` when production-ready
✅ Increment MAJOR for breaking changes
✅ Tag releases in git: `v1.0.0`
✅ Document breaking changes
✅ Use pre-release versions for testing

### DON'T:
❌ Use `0.0.1` (use `0.1.0`)
❌ Skip versions (`1.0.0` → `1.2.0`)
❌ Decrement versions
❌ Reuse version numbers
❌ Change released versions
❌ Use non-numeric identifiers for MAJOR/MINOR/PATCH

## Examples by Scenario

### New Project
```
0.1.0 - Initial development
0.2.0 - Add features
0.3.0 - Add more features
1.0.0 - First stable release
```

### Adding Features
```
1.0.0 - Current
1.1.0 - Add feature A
1.2.0 - Add feature B
1.2.1 - Fix bug in feature B
```

### Breaking Changes
```
1.5.0 - Current
2.0.0 - Remove deprecated API
2.1.0 - Add new feature
3.0.0 - Another breaking change
```

### Pre-release Workflow
```
1.0.0       - Current stable
1.1.0-alpha.1 - Early testing
1.1.0-alpha.2 - More testing
1.1.0-beta.1  - Feature complete
1.1.0-rc.1    - Release candidate
1.1.0         - Stable release
```

### Security Patches
```
1.2.3 - Current
1.2.4 - Security fix (PATCH)
```

## FAQ

**Q: When do I increment MAJOR for 0.x.x versions?**
A: You don't have to. 0.x.x is inherently unstable. Move to 1.0.0 when stable.

**Q: Can I have v0.0.1?**
A: Technically yes, but start with 0.1.0 for initial development.

**Q: What if I make a breaking change by accident?**
A: Release a new MAJOR version immediately with the fix.

**Q: Do build numbers affect versioning?**
A: No. `1.0.0+build.1` and `1.0.0+build.2` are the same version.

**Q: How do I version internal/private APIs?**
A: Only public API affects versioning. Internal changes can be any bump type.

**Q: Should I version documentation separately?**
A: No. Documentation is part of the release, same version.

**Q: What about git commit hashes?**
A: Add to build metadata: `1.0.0+sha.5114f85`

## Common Patterns

### Libraries/Packages
```
0.1.0  - Initial
1.0.0  - Stable public API
2.0.0  - Breaking changes
```

### Applications/Tools
```
0.1.0  - First working version
1.0.0  - Feature complete, production-ready
2.0.0  - Major redesign
```

### Services/APIs
```
1.0.0  - Initial public release
1.x.x  - Backwards-compatible changes
2.0.0  - API v2 (breaking)
```

## Version Ranges (for dependencies)

Common notation:
- `1.2.3` - Exact version
- `^1.2.3` - Compatible (>= 1.2.3, < 2.0.0)
- `~1.2.3` - Patch updates (>= 1.2.3, < 1.3.0)
- `>=1.2.3` - Greater or equal
- `1.x` or `1.*` - Any 1.x.x version

## Regex Pattern

Valid SemVer regex:
```regex
^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?(\+([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?$
```

Simplified (without pre-release/build):
```regex
^\d+\.\d+\.\d+$
```
