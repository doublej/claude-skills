# Output Patterns

## Template Pattern

Use structured formats tailored to your strictness requirements:

**Strict contexts** (APIs, data formats):
```markdown
ALWAYS use this exact template structure:
- Executive Summary
- Key Findings
- Recommendations
```

**Flexible contexts:**
```markdown
Use your best judgment and adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For situations where output quality depends on demonstration, provide input/output pairs:

**Commit message example:**

Input scenario:
- Fixed null pointer exception in user authentication
- Updated error handling in login flow

Output:
```
fix(auth): handle null user in login validation

- Add null check before accessing user properties
- Improve error message for failed authentication
```

**Key principle:** Examples often communicate intent more effectively than descriptions alone, helping Claude understand nuanced expectations about tone, depth, and structure.
