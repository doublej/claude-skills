# cmux browser automation

cmux ships a headless browser surface addressable with the same
`--workspace` / `--surface` model as panes. Verbs group into seven clusters.
One canonical example per cluster — reach for `cmux browser <verb> --help`
for the rest.

> **Refs invalidate on navigation.** Every node ref returned by `find`,
> `snapshot`, or `query` is only valid until the next `goto`, `back`,
> `forward`, `reload`, or document replacement. Re-find after navigation.
> Storing refs across awaits is the #1 source of "node detached" errors.

## 1. Lifecycle

| Verb | Use |
|------|-----|
| `new-browser` | Spawn browser surface, returns `surface` id |
| `close-surface` | Same close verb as pane surfaces |
| `list-pane-surfaces --kind browser --json` | Enumerate live browsers |

```bash
BS=$(cmux new-browser --workspace "$WS" --tab "app:browser" --json | jq -r .id)
```

## 2. Navigation

| Verb | Use |
|------|-----|
| `browser goto --surface <id> <url>` | Load URL |
| `browser back`/`forward`/`reload` | History |
| `browser wait-for-load --surface <id>` | Block until document is ready |

```bash
cmux browser goto --surface "$BS" https://example.com
cmux browser wait-for-load --surface "$BS" --timeout 10
```

## 3. Snapshot & find

| Verb | Use |
|------|-----|
| `browser snapshot --surface <id> --json` | Whole accessibility tree |
| `browser find --surface <id> --role button --name "Save" --json` | Targeted |
| `browser query --surface <id> --css '.row'` | CSS selector (returns refs) |

Prefer `find` by role + accessible name over CSS — survives DOM reshuffles.

```bash
REF=$(cmux browser find --surface "$BS" --role textbox --name "Email" --json \
      | jq -r .ref)
```

## 4. Interact

| Verb | Use |
|------|-----|
| `browser click --surface <id> --ref <ref>` | Click element |
| `browser fill --surface <id> --ref <ref> --value "..."` | Replace value |
| `browser type --surface <id> --ref <ref> --text "..."` | Append keystrokes |
| `browser hover --surface <id> --ref <ref>` | Hover |
| `browser press --surface <id> --key Enter` | Send key |
| `browser scroll --surface <id> --ref <ref> --direction down` | Scroll into view |

`fill` replaces the field; `type` appends. Use `fill` for login forms,
`type` for search-as-you-type widgets.

```bash
cmux browser fill --surface "$BS" --ref "$REF" --value "alice@example.com"
cmux browser press --surface "$BS" --key Enter
```

## 5. Read & assert

| Verb | Use |
|------|-----|
| `browser get-text --surface <id> --ref <ref>` | Visible text |
| `browser get-attr --surface <id> --ref <ref> --name href` | HTML attr |
| `browser get-value --surface <id> --ref <ref>` | Input value |
| `browser get-url --surface <id>` | Current URL |
| `browser get-title --surface <id>` | `<title>` |
| `browser is-visible --surface <id> --ref <ref>` | Bool |
| `browser is-enabled --surface <id> --ref <ref>` | Bool |
| `browser screenshot --surface <id> --out path.png` | Full-page PNG |

## 6. Wait

| Verb | Use |
|------|-----|
| `browser wait-for-ref --surface <id> --ref <ref> [--state visible\|hidden\|enabled]` | Until state |
| `browser wait-for-url --surface <id> --pattern '.*/dashboard'` | URL regex |
| `browser wait-for-text --surface <id> --text "Welcome"` | Text appears |
| `browser wait-idle --surface <id>` | Network + DOM idle |

Every wait takes `--timeout <seconds>` (default 5). Prefer `wait-for-ref`
over `sleep` — the surface reports live state.

## 7. Evaluate, frames, dialogs

| Verb | Use |
|------|-----|
| `browser eval --surface <id> --script 'document.title'` | Run JS in page |
| `browser eval-on --surface <id> --ref <ref> --script 'el.scrollTop'` | JS on node |
| `browser frame --surface <id> --name main` | Scope subsequent calls |
| `browser frame-reset --surface <id>` | Back to top document |
| `browser dialog accept --surface <id>` | Accept JS alert/confirm |
| `browser dialog dismiss --surface <id>` | Dismiss |
| `browser dialog prompt --surface <id> --text "..."` | Fill prompt |

**Dialog trap**: a JS `alert()` blocks the page thread. Install
`browser dialog accept` *before* triggering the action, not after.

```bash
cmux browser dialog accept --surface "$BS" --once &
cmux browser click --surface "$BS" --ref "$DELETE_BTN"
```

## Canonical end-to-end example

Log into a page, wait for the dashboard, screenshot it:

```bash
BS=$(cmux new-browser --workspace "$WS" --tab "app:browser" --json | jq -r .id)
cmux browser goto --surface "$BS" https://example.com/login
cmux browser wait-for-load --surface "$BS"

EMAIL=$(cmux browser find --surface "$BS" --role textbox --name Email --json | jq -r .ref)
PASS=$( cmux browser find --surface "$BS" --role textbox --name Password --json | jq -r .ref)
cmux browser fill --surface "$BS" --ref "$EMAIL" --value "alice@example.com"
cmux browser fill --surface "$BS" --ref "$PASS"  --value "$PASSWORD"

SUBMIT=$(cmux browser find --surface "$BS" --role button --name "Sign in" --json | jq -r .ref)
cmux browser click --surface "$BS" --ref "$SUBMIT"

cmux browser wait-for-url --surface "$BS" --pattern '.*/dashboard' --timeout 20
cmux browser screenshot --surface "$BS" --out /tmp/dashboard.png
```

## Picking a strategy

- Action has a label → `find` by role+name, then `click`/`fill`.
- Action has only CSS → `query`, but budget for breakage on redesign.
- Page has dynamic content → wait for the *outcome* (URL change, text
  appears, node visible), not for a fixed `sleep`.
- Need a value from a deep property → `eval-on` beats DOM-scraping text.
- Subframes (OAuth popups, stripe.js) → always `frame` before interacting.
