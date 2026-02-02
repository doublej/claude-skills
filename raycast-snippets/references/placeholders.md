# Dynamic Placeholders Reference

## Core Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{clipboard}` | Last copied text |
| `{cursor}` | Cursor position after paste |
| `{argument}` | Input prompt (max 3) |
| `{selection}` | Selected text (AI Commands only) |
| `{uuid}` | Random UUID |

## Date/Time

| Placeholder | Output Example |
|-------------|----------------|
| `{date}` | 1 Jun 2022 |
| `{time}` | 3:05 pm |
| `{datetime}` | 1 Jun 2022 at 6:45 pm |
| `{day}` | Monday |

### Custom Date Formats

`{date format="FORMAT_STRING"}`

| Format | Output |
|--------|--------|
| `yyyy-MM-dd` | 2022-06-15 |
| `MM/dd/yyyy` | 06/15/2022 |
| `EEEE, MMM d, yyyy` | Wednesday, Jun 15, 2022 |
| `HH:mm:ss` | 13:44:39 |
| `yyyy-MM-dd'T'HH:mm:ssZ` | 2022-06-15T13:44:39+0000 |

### Date Offsets

`{date offset="+2d"}` - 2 days ahead
`{date offset="-1M"}` - 1 month ago
`{datetime offset="+1h +30m"}` - 1.5 hours from now

Units: `m` (minutes), `h` (hours), `d` (days), `M` (months), `y` (years)

## Modifiers

Apply to any placeholder: `{clipboard | modifier}`

| Modifier | Effect |
|----------|--------|
| `uppercase` | FOO |
| `lowercase` | foo |
| `trim` | Remove whitespace |
| `percent-encode` | URL encode |
| `json-stringify` | Escape for JSON |
| `raw` | No auto-formatting |

Chain modifiers: `{clipboard | trim | uppercase}`

## Arguments

### Named Arguments (reusable)
```
{argument name="tone"}
```
Same name = same value throughout snippet.

### Default Values (optional)
```
{argument default="happy"}
{argument name="sport" default="skiing"}
```

### Options (dropdown)
```
{argument name="tone" options="happy, sad, professional"}
```

## Clipboard Offset

`{clipboard offset=1}` - 2nd-to-last copied
`{clipboard offset=2}` - 3rd-to-last copied

Requires Clipboard History enabled.

## Snippet References

`{snippet name="email-signature"}` - Insert another snippet's content.
Only non-referencing snippets can be inserted.
