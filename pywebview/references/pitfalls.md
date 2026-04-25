# pywebview pitfalls — diagnosis + fix

## Bridge

### `pywebview is not defined` / `Cannot read property 'api' of undefined`

JS ran before the bridge was injected. Wait for the event:

```js
// WRONG
window.onload = () => pywebview.api.foo();

// RIGHT
window.addEventListener('pywebviewready', () => pywebview.api.foo());
```

### Python method exists but JS sees `undefined`

- Method name starts with `_` → hidden by design.
- Method is on a non-callable nested attribute → check `_serializable = False` and dunder-attrs.
- Method was added AFTER `start()` but you used `js_api=` instead of `expose()`.

Fix: call `window.expose(func)` for runtime additions.

### Long-running Python call blocks the UI

Each `pywebview.api.*` call already runs on a worker thread, but if the JS Promise is chained synchronously the user sees a frozen button. Show a progress state in JS BEFORE awaiting the call. For cancellable work, expose a separate `cancel()` method that flips a flag.

### Returning a non-JSON-serializable value

Methods must return JSON-serializable types (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`). Datetime, Decimal, custom objects → convert to dict/string first.

### `evaluate_js` returns `None` when it shouldn't

The expression must produce a value — wrap multi-statement code in an IIFE:

```python
window.evaluate_js('(() => { const x = 1 + 1; return x })()')
```

## Window lifecycle

### `webview.create_window` returns immediately but window is blank for seconds

Native window appears before content. Use `events.before_show` to inject loading indicators or set a dark `background_color` to mask the white flash.

### Code after `webview.start()` never runs

`start()` blocks until the last window closes. Move post-start logic into the start function:

```python
webview.start(my_main, window)   # runs in background thread
```

### `webview.windows[0]` is empty at module load

Indexing happens before `start()`. Pass the window reference explicitly:

```python
window = webview.create_window(...)
webview.start(my_func, window)
```

## State

### State changes don't fire listeners

Top-level only. `state.user.name = 'X'` won't fire — replace the whole object:

```python
# Won't fire:
window.state.user['name'] = 'Alice'

# Fires:
window.state.user = {**window.state.user, 'name': 'Alice'}
```

### State init throws at startup

Init `window.state.foo = 1` BEFORE `webview.start()`. After start, init from the start-func or from `events.loaded`.

## Platform-specific

### Windows: `Microsoft Edge WebView2 Runtime not found`

Install the Evergreen Bootstrapper. For installers, run silently:

```
MicrosoftEdgeWebview2Setup.exe /silent /install
```

### Windows: pythonnet build fails

Use `pip install pywebview --no-binary :all:` only as a last resort. Prefer Python 3.11+ where pythonnet ships wheels.

### Linux: `webkit2gtk` not found

```bash
sudo apt install libwebkit2gtk-4.1-0          # Ubuntu 24+
sudo apt install libwebkit2gtk-4.0-37         # older Ubuntu
pip install pywebview[gtk]
```

### Linux: QT looks fine in dev but blank in PyInstaller

`pyinstaller --collect-all PyQt5` (or PyQt6) — webengine resources are not auto-collected.

### macOS: app icon is generic Python rocket

`webview.start(icon=...)` is ignored on macOS. Set `CFBundleIconFile` in the py2app `plist`.

### macOS: window is too small on Retina

`width=800` is logical pixels. Backend scales correctly — if it looks small, your CSS is using physical pixels somewhere.

### macOS: `webview.start(gui='qt')` crashes

`gui=` only accepts `'qt'` or `'gtk'` on Linux, `'cef'` on Windows. macOS is locked to Cocoa+WebKit.

## File / asset loading

### `index.html` shows but assets are 404

Built-in server serves relative to the cwd, not the script directory. Either `cd` first or use absolute paths:

```python
import os
here = os.path.dirname(os.path.abspath(__file__))
webview.create_window('App', os.path.join(here, 'gui/index.html'))
webview.start(http_server=True)
```

### `file://` works in dev, breaks in production

CORS and absolute paths flake under `file://`. Always use the built-in server (`http_server=True`) or a Flask/FastAPI app. Frozen apps must resolve via `sys._MEIPASS` (PyInstaller) or `Resources/` (py2app).

### CSP blocks inline scripts after `evaluate_js`

Some sites have CSPs that forbid `eval`. Use `run_js` instead — pywebview runs it without `eval`.

## Threading

### "RuntimeError: There is no current event loop in thread"

You ran an asyncio coroutine on a non-main thread without a loop. Wrap with `asyncio.run()` inside a sync `js_api` method, or create a loop manually:

```python
def my_method(self):
    return asyncio.new_event_loop().run_until_complete(my_coro())
```

### Calling `window.load_url` from a `js_api` method hangs

Don't block the JS Promise on a window operation that requires the GUI thread. Defer:

```python
def navigate(self, url):
    threading.Thread(target=lambda: webview.windows[0].load_url(url)).start()
    return {'ok': True}
```

## DevTools

### Right-click context menu is missing

`debug=True` is required to enable it. In production builds, expose a hidden shortcut:

```js
document.addEventListener('keydown', e => {
  if (e.shiftKey && e.metaKey && e.key === 'I') pywebview.api.toggle_devtools();
});
```

```python
class Api:
    def toggle_devtools(self):
        # No public API — set REMOTE_DEBUGGING_PORT and connect Chrome
        pass
```

### Console.log doesn't appear anywhere

In `debug=False`, console output is silenced on most backends. Either enable debug mode, or pipe logs back to Python:

```js
console.log = (...args) => pywebview.api._log(args.join(' '));
```

## Packaging

See `packaging.md` — the most common cause of "works in dev, broken when frozen" is missing `--add-data` for the `gui/` directory.

## Security

### Anyone on localhost can hit the Flask routes

When using server mode, generate the per-session token and verify on every route:

```python
@app.route('/api/whatever')
def handler():
    if request.headers.get('X-Token') != webview.token:
        return 'forbidden', 403
```

The frontend reads `webview.token` from a template variable rendered into a `<meta>` tag.

### XSS via `load_html` of user content

`load_html` injects raw HTML. Sanitize first or use `evaluate_js` with parameters via JSON.

### Allow-listing external domains

```python
webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = True
```

Or intercept navigation in `events.before_load` and call `window.run_js('window.stop()')` if disallowed.
