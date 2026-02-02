# Capture Methods by Project Type

## macOS / iOS Swift Apps

### Running iOS Simulator
```bash
# List booted simulators
xcrun simctl list devices booted

# Screenshot specific simulator
xcrun simctl io <device-udid> screenshot output.png

# Or capture all booted simulators
xcrun simctl io booted screenshot output.png
```

Set simulator to the right device type before capturing (e.g., iPhone 16 Pro Max for App Store screenshots).

### Running macOS App
```bash
# Capture specific window by name (exact match)
screencapture -l $(osascript -e 'tell app "AppName" to id of window 1') output.png

# Interactive window capture (click to select)
screencapture -w output.png

# Capture without shadow
screencapture -o -w output.png
```

Use `scripts/capture.sh` for common patterns.

### No Build Available — Faux HTML Fallback
When the app can't be run, recreate the UI in HTML:
- Match fonts, colors, spacing from design files or screenshots
- Use SF Pro (or system font stack) for iOS/macOS fidelity
- Wrap in appropriate device bezel

## Web Apps (SvelteKit, Next.js, etc.)

### Playwright Device Emulation
```javascript
const { chromium, devices } = require('playwright');

const browser = await chromium.launch();
const context = await browser.newContext({
  ...devices['iPhone 14 Pro Max'],
  deviceScaleFactor: 3,
});
const page = await context.newPage();
await page.goto('http://localhost:5173');
await page.screenshot({ path: 'output.png' });
await browser.close();
```

Start the dev server first, then capture against localhost.

### Browser Chrome via Playwright
For desktop screenshots with browser chrome, capture the full page and composite into a browser frame in the compose step.

## Electron / Tauri Apps

Two approaches:
1. **Playwright against localhost** — if the app exposes a web server
2. **screencapture** — if the app is running as a desktop window

Prefer Playwright for reproducibility.

## CLI Tools

### ANSI-to-HTML Terminal Render
```bash
# Run command and capture ANSI output
script -q /dev/null <command> | ansi2html > terminal.html

# Or use a terminal CSS theme
```

If `ansi2html` isn't available, use a minimal HTML wrapper:
```html
<pre style="background:#1e1e2e;color:#cdd6f4;font-family:'SF Mono',monospace;
  font-size:14px;padding:20px;border-radius:8px;line-height:1.5;">
<!-- paste terminal output here, with ANSI codes converted to spans -->
</pre>
```

Then capture with Playwright at desired dimensions.

## API / Library (No UI)

Render a representative code snippet:
- Use Shiki or highlight.js for syntax highlighting
- Pick a compelling code example (setup, key API call, or output)
- Wrap in a styled HTML page with the project's branding

```html
<div style="background:#1e1e2e;padding:40px;border-radius:12px;">
  <!-- Shiki-highlighted code block -->
</div>
```

Capture with Playwright.
