# pywebview API cheatsheet

## `webview.create_window(title, ...)`

Returns a `Window` instance. Can be called before or after `webview.start()`.

| Param | Default | Notes |
|---|---|---|
| `title` | required | Window title |
| `url` | `None` | URL string, relative file path, or WSGI/ASGI app object |
| `html` | `None` | HTML string (overrides `url`) |
| `js_api` | `None` | Python object — methods exposed as `pywebview.api.*` |
| `width` | `800` | Logical pixels |
| `height` | `600` | Logical pixels |
| `x`, `y` | `None` | Window position; `None` = center on screen |
| `screen` | `None` | A `Screen` from `webview.screens` for multi-monitor |
| `resizable` | `True` | |
| `fullscreen` | `False` | |
| `min_size` | `(200, 100)` | |
| `hidden` | `False` | Create hidden, call `show()` later |
| `frameless` | `False` | No title bar / chrome |
| `easy_drag` | `True` | Whole frameless window is draggable |
| `shadow` | `False` | Windows-only drop shadow on frameless |
| `focus` | `True` | Focusable on creation |
| `minimized` | `False` | |
| `maximized` | `False` | |
| `menu` | `[]` | Per-window menu (list of `Menu`) |
| `on_top` | `False` | Always on top |
| `confirm_close` | `False` | Native "are you sure" dialog |
| `background_color` | `'#FFFFFF'` | Hex color shown before content loads |
| `transparent` | `False` | Transparent background |
| `text_select` | `False` | Allow user to select text outside `<input>` |
| `zoomable` | `False` | Allow ctrl+wheel zoom |
| `draggable` | `False` | Allow dragging images/links out |
| `vibrancy` | `False` | macOS blur effect |
| `server` | `BottleServer` | Custom WSGI server class |
| `server_args` | `{}` | Passed to server constructor |
| `localization` | `None` | Per-window string overrides |

## `webview.start(func=None, args=None, ...)`

Blocks. Spawns the GUI loop. `func` runs in a background thread.

| Param | Default | Notes |
|---|---|---|
| `func` | `None` | Callable invoked after windows are shown |
| `args` | `None` | Positional args for `func` (single value or tuple) |
| `localization` | `{}` | Global string overrides |
| `gui` | `None` | Force `'cef'`, `'qt'`, or `'gtk'` (Linux/Windows only) |
| `debug` | `False` | Devtools + right-click context menu |
| `http_server` | `False` | Auto-spin built-in server for relative paths |
| `http_port` | `None` | Pin port (else random) |
| `user_agent` | `None` | Override UA string |
| `private_mode` | `True` | `True` = no cookies/storage between runs |
| `storage_path` | `None` | Where cookies/localStorage live when `private_mode=False` |
| `menu` | `[]` | Application-level menu |
| `server` | `BottleServer` | Custom WSGI server |
| `ssl` | `False` | HTTPS for built-in server |
| `server_args` | `{}` | |
| `icon` | `None` | Path to icon file (Linux/Windows only — macOS uses bundle) |

## `Window` properties

- `title` — get/set
- `on_top` — get/set
- `x`, `y`, `width`, `height` — geometry
- `state` — observable shared state object
- `dom` — DOM API root
- `events` — event bus
- `native` — backend-specific native handle (NSWindow / HWND / GtkWindow)

## `Window` methods

| Method | Returns | Notes |
|---|---|---|
| `load_url(url)` | — | Navigate |
| `load_html(content, base_uri=None)` | — | Replace document |
| `load_css(css)` | — | Inject stylesheet |
| `evaluate_js(script, callback=None)` | value | Sync (or async via callback) |
| `run_js(code)` | — | Fire-and-forget; works with strict CSP |
| `expose(*funcs)` | — | Add functions to `pywebview.api.*` at runtime |
| `get_current_url()` | str | |
| `get_cookies()` | list | |
| `clear_cookies()` | — | |
| `create_file_dialog(dialog_type, directory='', allow_multiple=False, save_filename='', file_types=())` | tuple\|None | `webview.FileDialog.OPEN/SAVE/FOLDER` |
| `create_confirmation_dialog(title, message)` | bool | |
| `show()`, `hide()` | — | |
| `minimize()`, `maximize()`, `restore()` | — | |
| `toggle_fullscreen()` | — | |
| `move(x, y)` | — | |
| `resize(width, height, fix_point=FixPoint.NORTH \| WEST)` | — | |
| `set_title(title)` | — | |
| `destroy()` | — | Close window |

## Window events (`window.events`)

Subscribe with `+=`, unsubscribe with `-=`:

```python
def handler(window): ...
window.events.loaded += handler
window.events.loaded -= handler
```

| Event | Args | Notes |
|---|---|---|
| `before_show` | `(window,)` | Native window exists, content not loaded |
| `before_load` | `(window,)` | Each navigation |
| `loaded` | `(window,)` | DOM ready |
| `shown` | `()` | |
| `closing` | `()` | Return `False` to cancel close |
| `closed` | `()` | After destruction |
| `initialized` | `(renderer,)` | `renderer` is the backend name; return `False` to abort |
| `minimized`, `maximized`, `restored`, `shown` | `()` | |
| `resized` | `(width, height)` | |
| `moved` | `(x, y)` | |
| `request_sent`, `response_received` | network events | |

Pass `window` as first arg only if your handler signature accepts it — pywebview detects it.

## DOM API (`window.dom`)

```python
el = window.dom.get_element('#root')         # one
els = window.dom.get_elements('.row')        # many
new = window.dom.create_element('<div/>', parent=el, mode='LAST_CHILD')
window.dom.body                              # <body>
window.dom.document                          # document
```

`Element` API:

```python
el.events.click += lambda e: print(e)        # any DOM event
el.style['color'] = 'red'                    # CSSStyleDeclaration-like
el.classes.add('active')                     # also: remove, toggle, contains
el.attributes = {'disabled': True}           # set; None removes
el.tag                                       # tag name
el.value                                     # form value
el.text                                      # innerText
el.html                                      # innerHTML
el.children                                  # list[Element]
el.parent                                    # Element
el.visible                                   # bool, get/set
el.focused                                   # bool, get/set
el.append(child) / .prepend / .move(parent) / .copy() / .remove() / .empty()
el.toggle()                                  # show/hide
```

## Shared state

Python:

```python
window.state.foo = 1               # set
val = window.state.foo             # get
window.state += handler            # subscribe
window.state -= handler            # unsubscribe
del window.state.foo               # delete
```

Handler signature: `handler(event_type, key, value)` where `event_type` is `'create' | 'change' | 'delete'`.

JavaScript:

```js
pywebview.state.foo = 1
console.log(pywebview.state.foo)
pywebview.state.addEventListener('change', e => {
  // e.key, e.value, e.type
});
```

Top-level mutations propagate. Nested object mutations do NOT — replace the whole object.

## Menu API

```python
from webview.menu import Menu, MenuAction, MenuSeparator

app_menu = [
  Menu('File', [
    MenuAction('Open', lambda: ...),
    MenuSeparator(),
    MenuAction('Quit', lambda: ...),
  ]),
  Menu('__app__', [           # macOS-only: items inside the app menu
    MenuAction('Preferences…', open_prefs),
  ]),
]

webview.start(menu=app_menu)
# OR per-window:
webview.create_window('W', menu=app_menu)
```

## File dialogs

```python
import webview

# Open one file
files = window.create_file_dialog(
    webview.FileDialog.OPEN,
    directory='/Users/me',
    allow_multiple=False,
    file_types=('Image Files (*.bmp;*.jpg;*.png)', 'All files (*.*)'),
)

# Save as
path = window.create_file_dialog(
    webview.FileDialog.SAVE,
    save_filename='untitled.txt',
)

# Pick a folder
folders = window.create_file_dialog(webview.FileDialog.FOLDER)
```

Returns a tuple of paths or `None` when cancelled.

## Constants

```python
webview.FileDialog.OPEN | SAVE | FOLDER
webview.FixPoint.NORTH | SOUTH | EAST | WEST     # for resize anchor
webview.token                                     # per-session CSRF token
webview.windows                                   # list[Window]
webview.active_window()                           # Window | None
webview.screens                                   # list[Screen]
```

## Settings

```python
webview.settings = {
  'ALLOW_DOWNLOADS': True,
  'ALLOW_FILE_URLS': True,
  'OPEN_EXTERNAL_LINKS_IN_BROWSER': True,
  'OPEN_DEVTOOLS_IN_DEBUG': True,
  'REMOTE_DEBUGGING_PORT': 9222,
  'IGNORE_SSL_ERRORS': False,
}
```

Set BEFORE `webview.start()`.
