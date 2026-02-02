---
name: note-refiner
description: Scan folders of messy notes/documents and organize them at two levels — file system (rename, move, merge, split) and file content (restructure into clean markdown). Uses consult-user-mcp for decisions. Use when organizing notes, cleaning up docs, restructuring project files, or tidying braindumps.
---

# Note Refiner

Organize messy note folders into clean, structured markdown — both the file system and the content within each file.

## Workflow

```
1. SCAN      → Inventory files, detect types, gather context
2. ANALYZE   → Map themes, find duplicates, detect gaps
3. CHECK-IN  → Present reorganization plan, get approval
4. ORGANIZE  → Rename/move/merge/split files
5. REFINE    → Clean up content within each file
6. DELIVER   → Summary of changes, notify completion
```

## Step 1: SCAN

Accept a folder path from the user, or default to the current working directory.

Inventory every file in the folder:
- File name, extension, size, modification date
- Read each file's content to understand what it contains
- Note the writing style: fragments, stream-of-consciousness, structured, mixed

Ask the user via `ask_multiple_choice`:
- "What kind of notes are these?" — options: Client notes, Project documentation, Meeting notes, Research/braindump, Mixed/unsure

Ask via `ask_text_input`:
- "Any context I should know? (project name, client, date range, etc.)"

## Step 2: ANALYZE

### File system level
- Detect naming inconsistencies (mixed case, no dates, cryptic names)
- Identify orphan files that don't fit any theme
- Group files by theme/topic based on content similarity
- Flag duplicates and near-duplicates
- Identify files that should be merged (small fragments on same topic)
- Identify files that should be split (multiple unrelated topics)

### File level
For each file, identify:
- Primary theme and sub-themes
- Action items and todos
- Decisions made
- Open questions
- Content gaps or incomplete sections

Propose a target folder structure with semantic grouping.

## Step 3: CHECK-IN

Present the reorganization plan to the user. This is the critical decision point.

Use `ask_confirmation` to present the proposed folder structure:
- List files to rename with old → new names
- List files to move with target folders
- List files to merge with rationale
- List files to split with rationale

For any ambiguous files, use `ask_text_input`:
- "I'm unsure about [filename]. What is this about?"

Use `ask_multiple_choice` for refinement level:
- "How much content cleanup?" — options:
  - Structure only (add headers, frontmatter, no text changes)
  - Light cleanup (fix formatting, add structure, minor edits)
  - Full rewrite (restructure, clean grammar, complete sentences)

Wait for approval before proceeding. Do not modify any files until the user confirms.

## Step 4: ORGANIZE

Execute only what the user approved in step 3.

Create the target folder structure first, then:
- Rename files to consistent, descriptive names (kebab-case, with dates where relevant)
- Move files into their thematic folders
- Merge related fragments: combine content into a single file, preserving all information
- Split oversized files: create separate files with clear names for each topic

Naming convention: `YYYY-MM-DD-descriptive-name.md` when dates are relevant, otherwise `descriptive-name.md`.

## Step 5: REFINE

Apply the approved refinement level to each file.

### Structure only
- Add YAML frontmatter: title, date, tags, type, status
- Add H2/H3 headers to create semantic sections
- Move action items into a dedicated `## Action Items` section
- Move open questions into a dedicated `## Open Questions` section

### Light cleanup (includes structure only)
- Fix markdown formatting (lists, code blocks, links)
- Deduplicate content within file
- Normalize heading levels
- Fix obvious typos

### Full rewrite (includes light cleanup)
- Rewrite incomplete sentences into clear prose
- Improve paragraph flow and readability
- Add transitional text between sections
- Ensure consistent tone throughout

Preserve all original information. Never delete content the user wrote — restructure and clarify it.

## Step 6: DELIVER

Output a summary of all changes:
- Files renamed (count and examples)
- Files moved (count and target folders)
- Files merged (count and what was combined)
- Files split (count and what was separated)
- Files refined (count and refinement level applied)

If the folder is inside a git repo, use `ask_confirmation`:
- "These files are in a git repo. Want me to commit the changes?"

If confirmed, commit with message: `refactor: reorganize and clean up notes`

Use `notify_user` to signal completion.

## Rules

- Never delete files — only rename, move, merge, or restructure
- Always preserve original content when merging or restructuring
- Always get user approval before modifying files (step 3)
- Use kebab-case for file names, lowercase
- Use `.md` extension for all text files unless the original format matters
- Keep folder nesting shallow: max 2 levels deep
- When merging, add a comment at the top noting which files were combined
- When splitting, add cross-references between the resulting files
