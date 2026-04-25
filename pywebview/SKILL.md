---
name: pywebview
description: Build native desktop apps with Python backend + HTML/CSS/JS frontend using pywebview. Covers window creation, two-way Python↔JS interop (js_api, expose, evaluate_js, run_js, shared state), Flask/FastAPI integration, DOM manipulation from Python, native file dialogs and menus, multi-window apps, debug mode, and freezing with PyInstaller/py2app. Use when writing pywebview code, debugging window or interop issues, choosing between js_api vs HTTP-server architectures, packaging desktop apps with web UIs in Python, or migrating from Electron/Tauri to a Python-native stack.
---

# pywebview

<overview>
pywebview wraps a native webview (WinForms+WebView2 / Cocoa+WebKit / GTK+WebKit2 / QT+QtWebEngine) and gives Python full control over the window. No bundled Chromium — small executables. Two-way bridge: call Python from JS, JS from Python, share state.

Use this skill when building or debugging Python desktop apps with web UIs (`webview.create_window`, `webview.start`, `pywebview.api.*`, `js_api`, `expose`, `evaluate_js`, Flask/FastAPI + pywebview).
</overview>

<contract>
## Agent behavior contract

1. **One blocking entry point.** `webview.start()` blocks until the last window closes. Run background work via `webview.start(func, *args)` — never put work after `start()`.
2. **Never touch the GUI thread directly.** Window methods (`load_url`, `evaluate_js`, `resize`, ...) are safe to call from any thread; pywebview marshals them. But blocking work in `js_api` methods blocks the JS caller — use threads for long ops.
3. **Wait for `pywebviewready`.** `pywebview.api` is NOT guaranteed at `window.onload`. JS must subscribe to `window.addEventListener('pywebviewready', ...)` before calling Python.
4. **`js_api` exposes class methods.** Pass an instance to `create_window(js_api=api)`. All public callable methods become `pywebview.api.method_name(...)` returning Promises. Methods starting with `_` are hidden. Set `_serializable = False` on a nested object to hide it.
5. **Names are camelCased on the JS side automatically.** Python `say_hello_to` → JS `pywebview.api.sayHelloTo` (since v5). Do not rename manually.
6. **Promises always.** Every `pywebview.api.*` call returns a Promise. Python exceptions reject the Promise with a JS `Error`.
7. **`expose()` for runtime additions.** Use `window.expose(func1, func2)` after `create_window`, or call inside the start-func. Takes precedence over `js_api` on name conflict.
8. **`evaluate_js` returns a value, `run_js` does not.** Use `evaluate_js(code, callback=None)` when you need the JS result. Use `run_js(code)` when CSP forbids `unsafe-eval` or you don't care about the return.
9. **Shared state.** `window.state.foo = 1` (Python) ↔ `pywebview.state.foo` (JS). Top-level mutations propagate. Subscribe with `window.state += handler` (Python) or `pywebview.state.addEventListener('change', handler)` (JS). Initialize state BEFORE `start()`.
10. **HTTP server choice.**
    - Static files / no backend: built-in bottle server, pass `html=` or relative path as `url=`.
    - Flask/FastAPI/Django: pass the WSGI/ASGI app object as `url=` argument: `create_window('App', flask_app)`.
    - Verify `webview.token` on every server route to block external requests (see `flask_app` example).
11. **Window dimensions are logical pixels.** `width=800` means 800 CSS pixels — backend handles DPI scaling.
12. **`debug=True` enables devtools.** `webview.start(debug=True)` opens dev tools and the right-click context menu. Always off in production.
13. **Multi-window:** `webview.create_window(...)` returns a `Window`. All windows are in `webview.windows`. `webview.active_window()` is the focused one. Spawn additional windows from the start-func.
14. **File dialogs require a window.** `window.create_file_dialog(webview.FileDialog.OPEN | SAVE | FOLDER, ...)` — returns tuple of paths or `None`. Always call from a non-GUI thread (i.e., inside a `js_api` method or the start-func), not at module top-level.
15. **DOM API mirrors the browser.** `window.dom.get_element('#id')`, `.events.click += handler`, `.style['color'] = 'red'`, `.classes.toggle('active')`, `.attributes = {'disabled': True}`. Subscribe to events from Python directly.
16. **Linux requires a backend choice.** `pip install pywebview[qt]` or `pip install pywebview[gtk]`. GTK needs WebKit2 ≥ 2.22.
17. **Windows requires WebView2 Runtime.** Ships with Win11; on Win10 the installer must include the Evergreen bootstrapper.
18. **Frozen apps need data.** PyInstaller: `--add-data "gui:gui"`. py2app on macOS (recommended over PyInstaller). Vite/webpack: build first, point `--add-data` at the dist folder.
19. **Single-file is a trap on macOS.** `--onefile` works but unpacks to /tmp on every launch — slow startup, breaks native menu bundle metadata. Use `--onedir` + a .app wrapper, or py2app.
20. **Closing != destroying.** `confirm_close=True` shows a native confirm dialog before close. `events.closing` can return `False` to cancel; `events.closed` runs after destruction.
</contract>

<quick_start>
```python
import webview
webview.create_window('Hello', html='<h1>Hello</h1>')
webview.start()
```

Load a URL:

```python
webview.create_window('Docs', 'https://example.com')
webview.start()
```

Load local files (built-in HTTP server):

```python
webview.create_window('App', 'index.html')  # relative to cwd
webview.start(http_server=True)
```

## Two-way bridge (the core pattern)

### Pattern A — `js_api` class (no HTTP server)

```python
import webview

class Api:
    def greet(self, name):
        return {'message': f'Hello {name}!'}

    def _hidden(self):  # underscore = not exposed
        pass

if __name__ == '__main__':
    window = webview.create_window('App', html=HTML, js_api=Api())
    webview.start()
```

```html
<script>
  window.addEventListener('pywebviewready', () => {
    pywebview.api.greet('World').then(r => console.log(r.message));
  });
</script>
```

### Pattern B — `expose()` for free functions

```python
def echo(a, b): return a + b

window = webview.create_window('App', html=HTML)
window.expose(echo)              # before start
webview.start()
# OR inside the start function for runtime expose
```

### Pattern C — Python calls JS

```python
def main(window):
    result = window.evaluate_js('document.title')   # returns str
    window.run_js('document.body.style.background = "red"')  # no return
webview.start(main, window)
```

### Pattern D — shared reactive state

```python
window = webview.create_window('S', html=HTML)
window.state.counter = 0           # init BEFORE start

def on_change(event_type, key, value):
    print(f'{key} = {value}')

def on_loaded(w):
    w.state += on_change

window.events.loaded += on_loaded
webview.start()
```

```js
window.addEventListener('pywebviewready', () => {
  pywebview.state.addEventListener('change', e => console.log(e));
  pywebview.state.counter++;       // triggers Python listener
});
```

## Flask/FastAPI integration

Pass the app object as the URL parameter — pywebview runs it on a background thread:

```python
from flask import Flask
import webview

flask_app = Flask(__name__, static_folder='gui', template_folder='gui')

@flask_app.route('/')
def index(): return render_template('index.html', token=webview.token)

webview.create_window('App', flask_app)
webview.start()
```

**Always verify `webview.token`** on every route — pywebview generates a CSRF-style token per session and the frontend reads it from a template variable. This blocks external browsers from hitting localhost:port.

## When to use which architecture

| Scenario | Pick |
|---|---|
| Static SPA (React/Vue/Svelte) bundled assets | Pattern A `js_api` + `http_server=True` |
| Existing Flask/FastAPI app | Server mode, pass app to `create_window` |
| Heavy Python computation called from UI | Pattern A, run work in threads inside api methods |
| Lots of small DOM updates from Python | DOM API (`window.dom.*`) — no JS round-trip |
| Reactive shared state | Pattern D `window.state` |
| Existing website you're embedding | Just pass URL string |

## Detailed references

- **API cheatsheet** — every parameter and method: `references/api-cheatsheet.md`
- **Cookbook** — copy-paste recipes for menus, dialogs, multi-window, drag regions, frameless windows, DOM events, downloads, cookies: `references/cookbook.md`
- **Packaging** — PyInstaller, py2app, signing, code-signing identifiers: `references/packaging.md`
- **Pitfalls** — every common bug, with fix: `references/pitfalls.md`

## Pitfall self-check (read before declaring done)

- [ ] Did I wait for `pywebviewready` before calling `pywebview.api`?
- [ ] Are long-running Python ops in a thread (not blocking the JS Promise)?
- [ ] Did I init `window.state` BEFORE `webview.start()`?
- [ ] Linux: did I install `pywebview[qt]` or `pywebview[gtk]`?
- [ ] Windows: is WebView2 Runtime present?
- [ ] Production: `debug=False`?
- [ ] Server mode: are routes verifying `webview.token`?
- [ ] Did I name camelCase / snake_case correctly across the bridge?

</quick_start>
