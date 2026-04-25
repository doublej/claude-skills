# pywebview cookbook

Copy-paste recipes. Each one is a complete runnable script unless noted.

## 1. Background work in a `js_api` method (don't freeze the UI)

```python
import threading, time, webview

class Api:
    def __init__(self):
        self._cancel = False

    def heavy(self):
        # Runs on a worker thread already (each pywebview.api.* call gets one),
        # but if you spawn more, do it explicitly.
        self._cancel = False
        for i in range(1_000_000):
            if self._cancel:
                return {'message': 'cancelled'}
            _ = i * i
        return {'message': 'done'}

    def cancel(self):
        self._cancel = True

webview.create_window('Heavy', html='<button onclick="pywebview.api.heavy().then(r=>document.body.innerText=r.message)">Go</button>', js_api=Api())
webview.start()
```

## 2. Frameless draggable window (custom titlebar)

```python
import webview

HTML = """
<style>
  body { margin:0; font-family:system-ui }
  .titlebar { background:#222; color:white; padding:8px; user-select:none; -webkit-app-region: drag }
  .titlebar button { -webkit-app-region: no-drag }
</style>
<div class="titlebar pywebview-drag-region">
  My App <button onclick="pywebview.api.close()">×</button>
</div>
<main style="padding:1rem">Content</main>
"""

class Api:
    def close(self):
        webview.windows[0].destroy()

webview.create_window('Frameless', html=HTML, frameless=True, easy_drag=False, js_api=Api())
webview.start()
```

`easy_drag=False` + add class `pywebview-drag-region` to specific elements you want draggable. With `easy_drag=True`, the entire window is a drag region (clicks on buttons may misfire).

## 3. Multi-window, opened from JS

```python
import webview

class Api:
    def open_settings(self):
        webview.create_window('Settings', html='<h1>Settings</h1>', width=400, height=300)

webview.create_window('Main', html='<button onclick="pywebview.api.open_settings()">Settings</button>', js_api=Api())
webview.start()
```

## 4. Native menu with keyboard shortcuts

```python
import webview
from webview.menu import Menu, MenuAction, MenuSeparator

def new_doc():    webview.active_window().load_html('<h1>New</h1>')
def open_doc():
    paths = webview.active_window().create_file_dialog(webview.FileDialog.OPEN)
    if paths: print(paths[0])

menu = [
    Menu('File', [
        MenuAction('New', new_doc),
        MenuAction('Open…', open_doc),
        MenuSeparator(),
        MenuAction('Quit', lambda: webview.active_window().destroy()),
    ]),
]

webview.create_window('App', html='<h1>Menu app</h1>')
webview.start(menu=menu)
```

Keyboard shortcuts are not first-class — bind via JS and call back, or use a backend-specific accelerator on `window.native`.

## 5. Save text from a textarea

```python
import webview

class Api:
    def save(self, text):
        path = webview.windows[0].create_file_dialog(
            webview.FileDialog.SAVE, save_filename='note.txt')
        if not path: return {'ok': False}
        with open(path, 'w') as f: f.write(text)
        return {'ok': True, 'path': path}

webview.create_window('Notes', html="""
  <textarea id="t" style="width:100%;height:80vh"></textarea>
  <button onclick="pywebview.api.save(document.getElementById('t').value).then(r=>alert(r.path||'cancelled'))">Save</button>
""", js_api=Api())
webview.start()
```

## 6. Manipulate DOM from Python (no JS round-trip)

```python
import webview

def bind(window):
    btn = window.dom.get_element('#btn')
    out = window.dom.get_element('#out')

    def click(e):
        out.text = 'Clicked!'
        out.style['color'] = 'crimson'

    btn.events.click += click

webview.create_window('DOM', html='<button id="btn">Hi</button><p id="out"></p>')
webview.start(bind, webview.windows[0])
```

Cheaper than `evaluate_js` for many small updates.

## 7. Long-poll style streaming Python → JS

```python
import threading, time, webview

def stream(window):
    n = 0
    while True:
        time.sleep(1)
        window.evaluate_js(f'document.getElementById("counter").innerText = {n}')
        n += 1

webview.create_window('Stream', html='<h1>Tick: <span id="counter">0</span></h1>')
webview.start(stream, webview.windows[0])
```

For high-frequency updates use `window.dom.get_element(...)` directly — fewer JS bridges.

## 8. Confirm-before-close

```python
import webview

def on_closing():
    if not webview.windows[0].create_confirmation_dialog('Quit?', 'Unsaved changes will be lost.'):
        return False  # cancel close

w = webview.create_window('App', html='<h1>Hi</h1>')
w.events.closing += on_closing
webview.start()
```

Or pass `confirm_close=True` for the default native dialog.

## 9. Embed a Vite/React app (built assets)

Project layout:

```
app/
  main.py
  gui/                  # vite build output
    index.html
    assets/...
```

```python
# main.py
import webview
webview.create_window('App', 'gui/index.html', width=1200, height=800)
webview.start(http_server=True, debug=True)
```

Vite config tip: set `base: './'` so assets resolve relatively when served from `gui/`.

## 10. Flask app inside pywebview, with token auth

```python
from flask import Flask, request, jsonify, render_template
import webview

app = Flask(__name__, template_folder='gui', static_folder='gui')

def auth():
    return request.headers.get('X-Token') == webview.token

@app.route('/')
def index(): return render_template('index.html', token=webview.token)

@app.post('/api/echo')
def echo():
    if not auth(): return 'forbidden', 403
    return jsonify(request.json)

webview.create_window('App', app)
webview.start()
```

Frontend reads the token from a meta tag rendered by the template and sends it in `X-Token` on every fetch.

## 11. FastAPI + uvicorn

```python
import threading, uvicorn, webview
from fastapi import FastAPI

api = FastAPI()
@api.get('/')
def root(): return {'hello': 'world'}

def serve():
    uvicorn.run(api, host='127.0.0.1', port=8765, log_level='warning')

threading.Thread(target=serve, daemon=True).start()
webview.create_window('FastAPI', 'http://127.0.0.1:8765')
webview.start()
```

Pywebview can also accept a WSGI/ASGI app directly via `create_window('T', api)` for built-in serving — simpler, no port pinning.

## 12. System tray icon (via pystray)

pywebview ships an example using pystray. Run pystray on the main thread, pywebview on a background thread:

```python
import threading, webview, pystray
from PIL import Image

def show():    webview.windows[0].show()
def quit_app(icon): icon.stop(); webview.windows[0].destroy()

def run_webview():
    webview.create_window('Tray', html='<h1>Hi</h1>', hidden=True)
    webview.start()

threading.Thread(target=run_webview, daemon=True).start()
icon = pystray.Icon('app', Image.open('icon.png'), menu=pystray.Menu(
    pystray.MenuItem('Show', show),
    pystray.MenuItem('Quit', quit_app),
))
icon.run()
```

## 13. Cookies and persistence

```python
webview.start(private_mode=False, storage_path='./userdata')
# now cookies + localStorage persist across runs

cookies = webview.windows[0].get_cookies()
webview.windows[0].clear_cookies()
```

`private_mode=True` (default) is incognito.

## 14. Open external links in the system browser

```python
webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = True
```

Or intercept in JS:

```js
document.addEventListener('click', e => {
  const a = e.target.closest('a[target="_blank"]');
  if (a) { e.preventDefault(); pywebview.api.open_external(a.href); }
});
```

```python
import webbrowser
class Api:
    def open_external(self, url): webbrowser.open(url)
```

## 15. Drag-and-drop files into the window

JS-side standard HTML5 drop:

```js
document.body.addEventListener('drop', async e => {
  e.preventDefault();
  for (const f of e.dataTransfer.files) {
    // f.path is non-standard — use FileReader, or pass name + bytes via base64
    const buf = await f.arrayBuffer();
    pywebview.api.handle_drop(f.name, Array.from(new Uint8Array(buf)));
  }
});
document.body.addEventListener('dragover', e => e.preventDefault());
```

```python
class Api:
    def handle_drop(self, name, bytes_list):
        with open(f'/tmp/{name}', 'wb') as f:
            f.write(bytes(bytes_list))
```

Native file paths from drag events are not exposed by all backends — round-trip the bytes.

## 16. Keyboard shortcuts (in-page)

```js
document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key === 's') {
    e.preventDefault();
    pywebview.api.save();
  }
});
```

## 17. Devtools in production (debugging field issues)

```python
import os
if os.environ.get('APP_DEBUG'):
    webview.start(debug=True)
else:
    webview.start()
```

Or expose remote debugging:

```python
webview.settings['REMOTE_DEBUGGING_PORT'] = 9222
# then connect from Chrome → chrome://inspect
```

## 18. Multiple monitors

```python
import webview
def main():
    s = webview.screens
    print(s)  # [Screen(width, height, x, y), ...]
    webview.create_window('Right monitor', html='<h1>Hi</h1>', screen=s[1])
webview.start(main)
```
