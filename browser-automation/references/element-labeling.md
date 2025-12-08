# Element Labeling (Set-of-Marks) Implementation

## Overview

Set-of-Marks (SoM) prompting annotates screenshots with numbered bounding boxes around interactive elements, enabling LLMs to reference specific UI elements by ID.

## Core Implementation

```typescript
import { Page } from 'puppeteer'

interface Element {
  id: number
  tag: string
  text: string
  role: string
  x: number
  y: number
  width: number
  height: number
  centerX: number
  centerY: number
  visible: boolean
  area: number
}

interface MarkResult {
  screenshot: string   // Base64 encoded annotated image
  elements: Element[]  // Metadata for each labeled element
}

async function markPageElements(page: Page): Promise<MarkResult> {
  // Inject marking script and get element data
  const elements = await page.evaluate(markPageScript)

  // Take screenshot with overlays visible
  const screenshot = await page.screenshot({
    type: 'jpeg',
    quality: 85,
    encoding: 'base64'
  })

  // Remove overlays
  await page.evaluate(unmarkPageScript)

  return { screenshot, elements }
}
```

## Mark Page Script (Inject into Browser)

```typescript
const markPageScript = () => {
  // Remove any existing marks
  document.querySelectorAll('[data-som-mark]').forEach(el => el.remove())

  const elements: Element[] = []
  const viewport = {
    width: window.innerWidth,
    height: window.innerHeight
  }

  // Selectors for interactive elements
  const selectors = [
    'a[href]',
    'button',
    'input:not([type="hidden"])',
    'select',
    'textarea',
    '[role="button"]',
    '[role="link"]',
    '[role="checkbox"]',
    '[role="menuitem"]',
    '[role="tab"]',
    '[onclick]',
    '[tabindex]:not([tabindex="-1"])'
  ]

  const candidates = document.querySelectorAll(selectors.join(','))
  let id = 0

  candidates.forEach(el => {
    const rect = el.getBoundingClientRect()

    // Skip if outside viewport or too small
    if (rect.width < 10 || rect.height < 10) return
    if (rect.bottom < 0 || rect.top > viewport.height) return
    if (rect.right < 0 || rect.left > viewport.width) return

    // Check if element is actually visible (not behind another element)
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2
    const topElement = document.elementFromPoint(centerX, centerY)

    if (!topElement || !el.contains(topElement) && !topElement.contains(el)) {
      return // Element is obscured
    }

    // Clamp to viewport bounds
    const x = Math.max(0, rect.left)
    const y = Math.max(0, rect.top)
    const width = Math.min(rect.right, viewport.width) - x
    const height = Math.min(rect.bottom, viewport.height) - y

    if (width < 10 || height < 10) return

    // Get element metadata
    const tag = el.tagName
    const text = (el.textContent || '').trim().slice(0, 50)
    const role = el.getAttribute('role') ||
                 el.getAttribute('aria-label') ||
                 (tag === 'A' ? 'link' : tag === 'BUTTON' ? 'button' : tag.toLowerCase())

    // Create visual overlay
    const overlay = document.createElement('div')
    overlay.setAttribute('data-som-mark', String(id))
    overlay.style.cssText = `
      position: fixed;
      left: ${x}px;
      top: ${y}px;
      width: ${width}px;
      height: ${height}px;
      border: 2px dashed rgba(255, 0, 0, 0.8);
      background: rgba(255, 0, 0, 0.1);
      pointer-events: none;
      z-index: 999999;
      box-sizing: border-box;
    `

    // Create label badge
    const label = document.createElement('div')
    label.style.cssText = `
      position: absolute;
      top: -1px;
      left: -1px;
      background: #e11d48;
      color: white;
      font-size: 11px;
      font-weight: bold;
      font-family: monospace;
      padding: 1px 4px;
      border-radius: 0 0 4px 0;
      line-height: 1.2;
    `
    label.textContent = String(id)
    overlay.appendChild(label)

    document.body.appendChild(overlay)

    elements.push({
      id,
      tag,
      text,
      role,
      x,
      y,
      width,
      height,
      centerX: x + width / 2,
      centerY: y + height / 2,
      visible: true,
      area: width * height
    })

    id++
  })

  return elements
}
```

## Unmark Page Script

```typescript
const unmarkPageScript = () => {
  document.querySelectorAll('[data-som-mark]').forEach(el => el.remove())
}
```

## Enhanced Labeling with Color Coding

```typescript
const markPageWithColors = () => {
  // Color by element type
  const colors: Record<string, string> = {
    A: '#3b82f6',       // blue - links
    BUTTON: '#22c55e',  // green - buttons
    INPUT: '#f59e0b',   // amber - inputs
    SELECT: '#8b5cf6',  // purple - dropdowns
    TEXTAREA: '#f59e0b',// amber - text areas
    DEFAULT: '#e11d48'  // red - other
  }

  // ... same logic as above, but use:
  const color = colors[tag] || colors.DEFAULT
  overlay.style.border = `2px solid ${color}`
  overlay.style.background = `${color}20`
  label.style.background = color
}
```

## Generating Element Description for LLM

```typescript
function formatElementsForLLM(elements: Element[]): string {
  return elements.map(e => {
    const desc = e.text || e.role
    return `[${e.id}] ${e.tag}: "${desc.slice(0, 40)}"`
  }).join('\n')
}

// Example output:
// [0] A: "Home"
// [1] BUTTON: "Sign In"
// [2] INPUT: "Search..."
// [3] A: "Products"
```

## Handling Scroll Position

```typescript
async function markVisibleElements(page: Page): Promise<MarkResult> {
  // First scroll through page to build complete map
  const allElements: Element[] = []
  const scrollHeight = await page.evaluate(() => document.body.scrollHeight)
  const viewportHeight = await page.evaluate(() => window.innerHeight)

  let scrollY = 0
  let globalId = 0

  while (scrollY < scrollHeight) {
    await page.evaluate(y => window.scrollTo(0, y), scrollY)
    await new Promise(r => setTimeout(r, 200))

    const elements = await page.evaluate(markPageScript)

    // Adjust IDs and coordinates for scroll offset
    elements.forEach(e => {
      e.id = globalId++
      e.y += scrollY
      e.centerY += scrollY
    })

    allElements.push(...elements)
    scrollY += viewportHeight * 0.8
  }

  // Scroll back to top and mark only visible
  await page.evaluate(() => window.scrollTo(0, 0))
  return markPageElements(page)
}
```

## Performance Tips

### 1. Limit Element Count

```typescript
function pruneElements(elements: Element[], max = 25): Element[] {
  // Sort by priority: larger, higher on page, interactive types
  return elements
    .sort((a, b) => {
      const typePriority: Record<string, number> = {
        INPUT: 10, BUTTON: 8, SELECT: 7, TEXTAREA: 6, A: 4
      }
      const scoreA = (typePriority[a.tag] || 1) + (a.area / 10000) - (a.y / 1000)
      const scoreB = (typePriority[b.tag] || 1) + (b.area / 10000) - (b.y / 1000)
      return scoreB - scoreA
    })
    .slice(0, max)
    .sort((a, b) => a.id - b.id)  // Restore visual order
}
```

### 2. Reduce Label Overlap

```typescript
function adjustOverlappingLabels(elements: Element[]): Element[] {
  // Detect overlapping labels and offset them
  for (let i = 0; i < elements.length; i++) {
    for (let j = i + 1; j < elements.length; j++) {
      const a = elements[i]
      const b = elements[j]

      // If labels would overlap (within 20px)
      if (Math.abs(a.x - b.x) < 20 && Math.abs(a.y - b.y) < 15) {
        // Offset the second label
        b.labelOffsetY = 15
      }
    }
  }
  return elements
}
```

### 3. Skip Decorative Elements

```typescript
const skipSelectors = [
  '[aria-hidden="true"]',
  '[role="presentation"]',
  '[role="img"]:not([aria-label])',
  'svg:not([role="button"])',
  '.icon:not([role])',
  '[data-decorative]'
]
```

## Using with CDP Directly

For better performance, use Chrome DevTools Protocol:

```typescript
import { CDPSession } from 'puppeteer'

async function getElementsViaCDP(client: CDPSession) {
  // Get full accessibility tree
  const { nodes } = await client.send('Accessibility.getFullAXTree')

  // Filter for interactive nodes
  return nodes.filter(node =>
    ['button', 'link', 'textbox', 'combobox', 'checkbox']
      .includes(node.role?.value)
  )
}
```
