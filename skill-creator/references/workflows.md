# Workflow Patterns

## Sequential Workflows

For complex tasks that need ordered steps, provide an overview early in documentation:

```markdown
## PDF Form Filling Workflow

1. Analyze the form (run analyze_form.py)
2. Extract field information
3. Validate input data
4. Fill form fields
5. Verify output (run verify_output.py)
```

## Conditional Workflows

Handle branching logic by presenting decision points:

```markdown
## Document Modification

Determine the modification type:

**Creating new content:**
1. Use template from assets/
2. Apply formatting rules
3. Save to output location

**Editing existing content:**
1. Parse existing document
2. Locate target sections
3. Apply modifications
4. Preserve formatting
```

Both patterns emphasize clarity through structure, helping Claude understand task progression and make appropriate choices at branch points.
