---
name: raycast-snippets
description: Create Raycast snippets for code expansion and text templates. Use when the user wants to create keyboard shortcuts, code snippets, boilerplate expansions, or text macros for Raycast. Outputs importable JSON files.
---

<output_format>

Create importable snippet collections for Raycast's text expansion feature.

<json_format>

```json
[
  {
    "name": "Console Log",
    "text": "console.log({cursor})",
    "keyword": "!clog"
  }
]
```

Fields:
- `name`: Display name in Raycast
- `text`: Content to expand (supports dynamic placeholders)
- `keyword`: Trigger prefix (optional, e.g., `!clog`, `@@`, `;;js`)

</json_format>

<placeholders>

See [references/placeholders.md](references/placeholders.md) for full reference.

**Most useful for code:**
- `{cursor}` - Cursor position after expansion
- `{clipboard}` - Last copied text
- `{argument}` - Prompt for input (max 3)
- `{argument name="var"}` - Named/reusable argument

**Date/time:**
- `{date format="yyyy-MM-dd"}` - Custom format
- `{datetime}` - Full timestamp
- `{date offset="+1d"}` - Relative dates

</placeholders>

<patterns>

## Logging
```json
{"name": "Console Log", "text": "console.log({cursor})", "keyword": "!clog"}
{"name": "Console Log Variable", "text": "console.log('{clipboard}:', {clipboard})", "keyword": "!clogv"}
```

## Functions
```json
{"name": "Arrow Function", "text": "const {argument name=\"fn\"} = ({argument name=\"params\"}) => {\n  {cursor}\n}", "keyword": "!afn"}
{"name": "Async Function", "text": "async function {argument}() {\n  {cursor}\n}", "keyword": "!afunc"}
```

## React Hooks
```json
{"name": "useState", "text": "const [{argument name=\"state\"}, set{argument name=\"state\"}] = useState({cursor})", "keyword": "!us"}
{"name": "useEffect", "text": "useEffect(() => {\n  {cursor}\n}, [])", "keyword": "!ue"}
```

## Comments/Headers
```json
{"name": "TODO", "text": "// TODO: {cursor}", "keyword": "!todo"}
{"name": "File Header", "text": "/**\n * {argument name=\"description\"}\n * @author {argument name=\"author\"}\n * Created: {date format=\"yyyy-MM-dd\"}\n */", "keyword": "!header"}
```

</patterns>

<workflow>

1. Gather requirements: what snippets does user need?
2. Build JSON array with appropriate keywords
3. Save as `.json` file
4. User imports via Raycast "Import Snippets" command

</workflow>

<conventions>

- `!` prefix for code: `!clog`, `!fn`, `!todo`
- `;;` prefix for language: `;;js`, `;;py`, `;;css`
- `@@` for personal info: `@@email`, `@@phone`
- `//` for comments: `//todo`, `//fix`

</conventions>

</output_format>
