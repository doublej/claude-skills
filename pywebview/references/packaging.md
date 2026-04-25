# Packaging pywebview apps

## Choosing the tool

| Platform | Recommended | Alternative |
|---|---|---|
| macOS | py2app | briefcase |
| Windows | PyInstaller | nuitka, briefcase |
| Linux | PyInstaller | nuitka |
| Android | buildozer + python-for-android | — |

## PyInstaller (Windows / Linux)

### Project layout

```
app/
  main.py
  gui/                # built frontend assets
    index.html
    assets/...
  requirements.txt
```

### One-folder build (recommended)

```bash
pyinstaller main.py \
  --name MyApp \
  --noconsole \
  --add-data "gui:gui" \
  --icon icon.ico
```

Note: `--add-data` separator differs by OS — `:` on macOS/Linux, `;` on Windows.

### One-file build (slow startup, simple distribution)

```bash
pyinstaller main.py --onefile --noconsole --add-data "gui;gui"
```

Avoid `--onefile` on macOS — unpacks to /tmp on every launch and breaks .app bundle metadata. Use py2app instead.

### Loading bundled assets at runtime

Frozen apps run from a different cwd. Resolve paths relative to the executable:

```python
import sys, os, webview

def resource_path(rel):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)

webview.create_window('App', resource_path('gui/index.html'))
webview.start(http_server=True)
```

### Reducing bundle size

Edit `MyApp.spec` and add to the `Analysis(...)`:

```python
excludes=['tkinter', 'unittest', 'pytest', 'numpy.testing'],
```

Then rebuild with `pyinstaller MyApp.spec`.

### Windows-specific gotchas

- WebView2 Runtime must be installed on the target machine. Bundle the Evergreen Bootstrapper installer alongside your app, or use `MicrosoftEdgeWebview2Setup.exe /silent /install` in your installer script.
- pythonnet requires the .NET Framework 4.0+ — present on Win7 SP1 and later.
- For code signing use `signtool sign /fd sha256 /tr http://timestamp.digicert.com /td sha256 /a MyApp.exe`.

### Linux-specific gotchas

- If you see `cannot find python3.xx.so`, add it manually:

  ```bash
  pyinstaller main.py --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:."
  ```

- GTK build needs `libwebkit2gtk-4.1-0` runtime on the target system. Document as a system dependency in your install instructions; PyInstaller cannot bundle it portably.
- For AppImage, layer PyInstaller output inside the AppDir.

## py2app (macOS)

### setup.py

```python
from setuptools import setup

APP = ['main.py']
DATA_FILES = [('gui', ['gui/index.html']), ('gui/assets', [...])]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'MyApp',
        'CFBundleIdentifier': 'com.example.myapp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '11.0',
    },
    'packages': ['webview'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

### Build

```bash
python setup.py py2app -A      # development build (alias mode, fast)
python setup.py py2app         # production
```

The dev alias build is critical — full builds are slow.

### Code signing & notarization

```bash
codesign --deep --force --options runtime \
  --sign "Developer ID Application: Your Name (TEAMID)" \
  dist/MyApp.app

ditto -c -k --keepParent dist/MyApp.app MyApp.zip
xcrun notarytool submit MyApp.zip --keychain-profile NotaryProfile --wait
xcrun stapler staple dist/MyApp.app
```

Required `Info.plist` keys when using hardened runtime:

```xml
<key>NSAppleEventsUsageDescription</key>
<string>This app uses AppleEvents.</string>
<key>com.apple.security.cs.allow-unsigned-executable-memory</key>
<true/>
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

## briefcase (cross-platform)

```bash
pip install briefcase
briefcase new
briefcase create
briefcase build
briefcase package
```

Briefcase produces native installers (msi/dmg/deb) and handles signing scaffolding. Heavier learning curve than PyInstaller.

## nuitka (compiles to C)

```bash
nuitka --standalone --enable-plugin=tk-inter \
  --include-data-dir=gui=gui \
  --macos-app-bundle main.py
```

Smaller and faster than PyInstaller, but builds take longer and some pywebview backends need plugin hints.

## Frontend build integration

If you use Vite/Webpack/etc., build the frontend before packaging:

```bash
cd frontend && npm run build && cd ..
pyinstaller main.py --add-data "frontend/dist:gui"
```

Vite tip: change `build.outDir` away from `./dist` because PyInstaller also creates `./dist/`. E.g. `build: { outDir: '../app/gui' }` in `vite.config.js`.

## Auto-update

pywebview has no built-in updater. Common options:

- **Sparkle** (macOS) via PyObjC
- **WinSparkle** (Windows) via ctypes
- **pyu** / **PyUpdater** for cross-platform
- **Custom**: check a versioned JSON manifest, download, replace, restart

## Smoke test after packaging

```python
# Inside the app, on first launch:
print('frozen:', getattr(sys, 'frozen', False))
print('meipass:', getattr(sys, '_MEIPASS', None))
print('cwd:', os.getcwd())
print('argv:', sys.argv)
```

Confirm all asset paths resolve and the WebView2/WebKit runtime loads. Most packaging bugs surface as a blank window.
