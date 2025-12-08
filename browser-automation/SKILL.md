---
name: browser-automation
description: Browser automation with Puppeteer or Playwright for LLM visual navigation and E2E testing. Use when building AI web agents, screenshot annotation, element labeling, visual web scraping, or end-to-end tests.
---

# Browser Automation

Build AI-powered web agents and end-to-end tests using Puppeteer or Playwright.

## When to Use

- Building AI agents that navigate websites visually
- Screenshot annotation with element labeling (Set-of-Marks)
- Visual web scraping with GPT-4V/Claude
- Accessibility tree extraction for semantic understanding
- Automated UI testing with visual verification
- End-to-end (E2E) testing of web applications

## Installation

### Puppeteer
```bash
npm install puppeteer
```

### Playwright
```bash
npm install -D @playwright/test
npx playwright install
```

---

## End-to-end Tests with Playwright

E2E (short for 'end to end') tests allow you to test your full application through the eyes of the user. [Playwright](https://playwright.dev/) is the recommended choice, but you can also use [Cypress](https://www.cypress.io/) or [NightwatchJS](https://nightwatchjs.org/).

You may also want to install an IDE plugin such as [the VS Code extension](https://playwright.dev/docs/getting-started-vscode) to execute tests from inside your IDE.

### Playwright Config

If you need to start your application before running tests, configure it in `playwright.config.js`:

```js
/// file: playwright.config.js
const config = {
    webServer: {
        command: 'npm run build && npm run preview',
        port: 4173
    },
    testDir: 'tests',
    testMatch: /(.+\.)?(test|spec)\.[jt]s/
};

export default config;
```

### Writing Tests

Tests interact with the DOM and write assertions. They're framework-agnostic:

```js
/// file: tests/hello-world.spec.js
import { expect, test } from '@playwright/test';

test('home page has expected h1', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toBeVisible();
});
```

---

## LLM Visual Navigation (Puppeteer)

Build AI-powered web agents using Puppeteer with techniques optimized for multimodal LLMs.

### Core Techniques

#### 1. Set-of-Marks (SoM) Prompting

The most effective technique for LLM visual grounding. Annotate screenshots with numbered bounding boxes around interactive elements.

```typescript
// See references/element-labeling.md for full implementation
const { screenshot, elements } = await markPageElements(page)
// Returns annotated screenshot + element metadata for LLM
```

#### 2. Dual Representation

Combine visual + semantic information:

| Input | Purpose |
|-------|---------|
| Annotated screenshot | Visual grounding, layout understanding |
| Accessibility tree | Semantic structure, element roles |
| Simplified DOM | Text content, element relationships |

#### 3. Action Space

Design clear actions the LLM can take:

| Action | Format | Description |
|--------|--------|-------------|
| `click` | `click [id]` | Click element by label ID |
| `type` | `type [id] [text]` | Enter text in input |
| `scroll` | `scroll [up\|down]` | Scroll viewport |
| `goto` | `goto [url]` | Navigate to URL |
| `wait` | `wait [ms]` | Wait for dynamic content |

### Quick Start

```typescript
import puppeteer from 'puppeteer'

const browser = await puppeteer.launch({ headless: true })
const page = await browser.newPage()
await page.setViewport({ width: 1280, height: 720 })

await page.goto('https://example.com')

// Take annotated screenshot for LLM
const { screenshot, elements } = await markPageElements(page)

// Get accessibility tree for context
const axTree = await page.accessibility.snapshot()

// Send to LLM with prompt:
// "Given this screenshot with labeled elements and accessibility info,
//  what action should I take to [goal]?"
```

### Key APIs

| Method | Description |
|--------|-------------|
| `page.screenshot()` | Capture viewport/full page |
| `page.accessibility.snapshot()` | Get accessibility tree |
| `element.boundingBox()` | Get element coordinates |
| `page.evaluate(js)` | Inject annotation scripts |
| `element.click()` | Click element |
| `element.type(text)` | Enter text |

### LLM Prompt Strategies

#### System Prompt Template

```
You are a web navigation agent. You see a screenshot with numbered labels
on interactive elements. Respond with ONE action:

- click [id] - click element with that label
- type [id] [text] - type text into input
- scroll [up|down] - scroll the page
- done [answer] - task complete

Current goal: {user_goal}
```

#### Tips for Better LLM Performance

1. **Use high contrast labels** - Colored boxes with white text on dark background
2. **Filter non-interactive elements** - Only label clickable/typeable elements
3. **Include element metadata** - "Button: Submit" not just "3"
4. **Provide accessibility context** - Role, name, state from a11y tree
5. **Limit visible elements** - 20-30 labels max per screenshot

## Reference Files

See `references/` for:
- `visual-navigation.md` - Full navigation agent patterns
- `element-labeling.md` - Set-of-Marks implementation code
