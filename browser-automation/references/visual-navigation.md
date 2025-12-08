# Visual Navigation Patterns for LLM Agents

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Puppeteer  │────▶│  Annotated   │────▶│  LLM (GPT-4V│
│  Browser    │     │  Screenshot  │     │  / Claude)  │
└─────────────┘     └──────────────┘     └──────────────┘
       ▲                                        │
       │                                        │
       └────────────── Action ──────────────────┘
```

## ReAct Loop Implementation

```typescript
import puppeteer, { Page } from 'puppeteer'

interface Action {
  type: 'click' | 'type' | 'scroll' | 'goto' | 'done'
  elementId?: number
  text?: string
  direction?: 'up' | 'down'
  url?: string
  answer?: string
}

async function navigateWithLLM(
  page: Page,
  goal: string,
  llm: (screenshot: string, elements: Element[], goal: string) => Promise<Action>
): Promise<string> {
  const maxSteps = 15

  for (let step = 0; step < maxSteps; step++) {
    // 1. Observe: capture annotated screenshot
    const { screenshot, elements } = await markPageElements(page)

    // 2. Think: ask LLM for next action
    const action = await llm(screenshot, elements, goal)

    // 3. Act: execute the action
    if (action.type === 'done') {
      return action.answer || 'Task completed'
    }

    await executeAction(page, action, elements)

    // 4. Wait for page to settle
    await page.waitForNetworkIdle({ timeout: 5000 }).catch(() => {})
  }

  throw new Error('Max steps exceeded')
}

async function executeAction(page: Page, action: Action, elements: Element[]) {
  switch (action.type) {
    case 'click':
      const clickEl = elements.find(e => e.id === action.elementId)
      if (clickEl) {
        await page.mouse.click(clickEl.centerX, clickEl.centerY)
      }
      break

    case 'type':
      const typeEl = elements.find(e => e.id === action.elementId)
      if (typeEl && action.text) {
        await page.mouse.click(typeEl.centerX, typeEl.centerY)
        await page.keyboard.type(action.text)
      }
      break

    case 'scroll':
      const delta = action.direction === 'up' ? -300 : 300
      await page.mouse.wheel({ deltaY: delta })
      break

    case 'goto':
      if (action.url) await page.goto(action.url)
      break
  }
}
```

## Accessibility Tree for Context

Combine visual with semantic information:

```typescript
interface SemanticContext {
  screenshot: string        // Base64 annotated image
  elements: Element[]       // Labeled interactive elements
  accessibilityTree: string // Simplified a11y tree
  pageTitle: string
  currentUrl: string
}

async function getPageContext(page: Page): Promise<SemanticContext> {
  const { screenshot, elements } = await markPageElements(page)

  // Get accessibility tree
  const axTree = await page.accessibility.snapshot({ interestingOnly: true })
  const simplifiedTree = simplifyAxTree(axTree)

  return {
    screenshot,
    elements,
    accessibilityTree: simplifiedTree,
    pageTitle: await page.title(),
    currentUrl: page.url()
  }
}

function simplifyAxTree(node: any, depth = 0): string {
  if (!node || depth > 4) return ''

  const indent = '  '.repeat(depth)
  const role = node.role || 'unknown'
  const name = node.name ? `: "${node.name}"` : ''

  let result = `${indent}[${role}${name}]\n`

  if (node.children) {
    for (const child of node.children) {
      result += simplifyAxTree(child, depth + 1)
    }
  }

  return result
}
```

## Handling Dynamic Content

```typescript
async function waitForStableContent(page: Page, timeout = 5000) {
  // Wait for network idle
  await page.waitForNetworkIdle({ idleTime: 500, timeout }).catch(() => {})

  // Wait for DOM to stabilize
  await page.evaluate(() => {
    return new Promise<void>(resolve => {
      let mutations = 0
      const observer = new MutationObserver(() => mutations++)
      observer.observe(document.body, { childList: true, subtree: true })

      const check = () => {
        const prev = mutations
        setTimeout(() => {
          if (mutations === prev) {
            observer.disconnect()
            resolve()
          } else {
            check()
          }
        }, 200)
      }
      check()
    })
  })
}
```

## Error Recovery

```typescript
async function robustClick(page: Page, element: Element, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      // Scroll element into view
      await page.evaluate((x, y) => {
        window.scrollTo({
          left: x - window.innerWidth / 2,
          top: y - window.innerHeight / 2,
          behavior: 'smooth'
        })
      }, element.centerX, element.centerY)

      await new Promise(r => setTimeout(r, 300))

      // Verify element still at expected position
      const currentElements = await markPageElements(page)
      const current = currentElements.elements.find(e => e.id === element.id)

      if (current) {
        await page.mouse.click(current.centerX, current.centerY)
        return true
      }
    } catch (e) {
      if (i === retries - 1) throw e
      await new Promise(r => setTimeout(r, 500))
    }
  }
  return false
}
```

## Prompt Engineering for Navigation

### Effective System Prompt

```
You are a precise web navigation agent. You will receive:
1. A screenshot with numbered labels on interactive elements
2. A list of elements: [id, type, text, role]
3. The accessibility tree summary
4. Current URL and page title

Your goal: {goal}

Rules:
- Output exactly ONE action per turn
- Use element IDs from the labeled screenshot
- If unsure, scroll to reveal more content
- Explain your reasoning briefly before the action

Actions:
- click [id] - Click the element
- type [id] "text" - Type into input field
- scroll up/down - Scroll page
- goto [url] - Navigate to URL
- done "answer" - Task complete with answer

Response format:
Reasoning: <brief explanation>
Action: <action>
```

### Common Failure Modes

| Problem | Solution |
|---------|----------|
| Clicks wrong element | Increase label contrast, reduce overlapping boxes |
| Misses hidden elements | Scroll before re-annotating |
| Slow response | Limit elements to 25, compress screenshot |
| Loops on same action | Track action history, detect repeats |
| Fails on popups/modals | Detect overlays, prioritize modal elements |

## Performance Optimization

```typescript
// Compress screenshots for faster LLM processing
async function captureOptimizedScreenshot(page: Page): Promise<string> {
  const screenshot = await page.screenshot({
    type: 'jpeg',
    quality: 80,  // Good balance of quality/size
    encoding: 'base64'
  })
  return screenshot
}

// Limit elements to most relevant
function filterElements(elements: Element[], maxCount = 25): Element[] {
  // Prioritize by visibility and interactivity
  return elements
    .filter(e => e.visible && e.area > 100)  // Minimum size
    .sort((a, b) => {
      // Prioritize: inputs > buttons > links
      const priority = { INPUT: 3, BUTTON: 2, A: 1 }
      return (priority[b.tag] || 0) - (priority[a.tag] || 0)
    })
    .slice(0, maxCount)
}
```
