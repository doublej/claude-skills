# Design System Patterns

Complete design system specification extracted from consult-user-mcp and beads-kanban documentation sites.

## Typography

### Font Families

```css
/* Primary font for all text */
font-family: 'Instrument Sans', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;

/* Monospace font for code */
font-family: 'DM Mono', 'Courier New', monospace;
```

**Loading (in app.html):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

### Font Sizes

```css
/* Headings */
h1 { font-size: 2.5rem; }    /* 40px */
h2 { font-size: 2rem; }      /* 32px */
h3 { font-size: 1.5rem; }    /* 24px */
h4 { font-size: 1.25rem; }   /* 20px */

/* Body text */
body { font-size: 1.1rem; }  /* 17.6px */
p { font-size: 1.1rem; }

/* Small text */
small { font-size: 0.9rem; }     /* 14.4px */
.secondary { font-size: 0.95rem; } /* 15.2px */

/* Code */
code { font-size: 0.9rem; }
pre code { font-size: 0.85rem; }
```

### Font Weights

```css
/* Instrument Sans weights */
h1, h2 { font-weight: 600; }     /* Semibold for main headings */
h3 { font-weight: 500; }         /* Medium for subheadings */
body { font-weight: 400; }       /* Regular for body text */
strong { font-weight: 500; }     /* Medium for emphasis */

/* DM Mono weights */
code { font-weight: 400; }       /* Regular for code */
```

### Line Heights

```css
h1, h2, h3 { line-height: 1.2; }
body, p { line-height: 1.6; }
code { line-height: 1.4; }
```

### Letter Spacing

```css
h1 { letter-spacing: -0.03em; }  /* Tighter for large headings */
h2 { letter-spacing: -0.02em; }
body { letter-spacing: normal; }
```

## Color Palette

### Light Theme (Only)

```css
:root {
  /* Backgrounds */
  --bg-primary: #fafafa;       /* Main page background */
  --bg-secondary: #fff;        /* Card backgrounds */
  --bg-tertiary: #f5f5f5;      /* Subtle backgrounds */
  --bg-code: #f0f0f0;          /* Code block backgrounds */

  /* Text colors */
  --text-primary: #1a1a1a;     /* Main text */
  --text-secondary: #404040;   /* Secondary text */
  --text-tertiary: #606060;    /* Tertiary text */
  --text-quaternary: #808080;  /* Subtle text */

  /* Borders */
  --border: #e0e0e0;           /* Default borders */
  --border-subtle: #d0d0d0;    /* Hover/focus borders */

  /* Accent */
  --accent: #1a1a1a;           /* Buttons, links, emphasis */
  --accent-hover: #404040;     /* Hover state */
}
```

### Usage Guidelines

**Backgrounds:**
- Page: `var(--bg-primary)` (#fafafa)
- Cards/panels: `var(--bg-secondary)` (#fff)
- Code blocks: `var(--bg-code)` (#f0f0f0)

**Text:**
- Headings: `var(--text-primary)` (#1a1a1a)
- Body text: `var(--text-secondary)` (#404040)
- Captions/metadata: `var(--text-tertiary)` (#606060)
- Disabled/placeholder: `var(--text-quaternary)` (#808080)

**Borders:**
- Default: `1px solid var(--border)` (#e0e0e0)
- Hover: `1px solid var(--border-subtle)` (#d0d0d0)

## Spacing System

### CSS Variables

```css
:root {
  /* Section spacing */
  --section-padding: 60px;

  /* Container */
  --container-max-width: 1200px;
  --container-padding: 24px;

  /* Grid */
  --grid-gap: 24px;

  /* Component spacing */
  --spacing-xs: 8px;
  --spacing-sm: 12px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}
```

### Section Padding

```css
section {
  padding: var(--section-padding) var(--container-padding);
  /* 60px top/bottom, 24px left/right */
}
```

### Container

```css
.container {
  max-width: var(--container-max-width); /* 1200px */
  margin: 0 auto;
  padding: 0 var(--container-padding);   /* 24px */
}
```

### Grid Gaps

```css
.grid {
  display: grid;
  gap: var(--grid-gap); /* 24px */
}
```

## Layout Patterns

### Hero Section

```css
.hero {
  padding: var(--section-padding) var(--container-padding);
  text-align: center;
  background: var(--bg-primary);
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 600;
  letter-spacing: -0.03em;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.hero .description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}
```

### Feature Grid

```css
.features {
  padding: var(--section-padding) var(--container-padding);
}

.features .grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--grid-gap);
}

.feature-card {
  background: var(--bg-secondary);
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: 8px;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}
```

### Code Block

```css
.install-box {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: 'DM Mono', monospace;
  font-size: 0.9rem;
  max-width: 600px;
  margin: 0 auto;
}

.install-box button {
  background: var(--accent);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
}

.install-box button:hover {
  background: var(--accent-hover);
}
```

## Responsive Breakpoints

### Breakpoint Values

```css
/* Mobile: < 700px */
/* Tablet: 700px - 999px */
/* Desktop: 1000px+ */
```

### Media Queries

```css
/* Desktop first (default styles for desktop) */

/* Tablet */
@media (max-width: 1000px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile */
@media (max-width: 700px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .container {
    padding: 0 16px;
  }

  h1 {
    font-size: 2rem; /* 32px */
  }

  h2 {
    font-size: 1.75rem; /* 28px */
  }
}
```

### Responsive Typography

```css
@media (max-width: 700px) {
  html {
    font-size: 14px; /* Base font size scales down */
  }

  h1 { font-size: 2rem; }
  h2 { font-size: 1.5rem; }
  h3 { font-size: 1.25rem; }
}
```

## Border Radius

```css
/* Cards */
.card { border-radius: 8px; }

/* Buttons */
button { border-radius: 6px; }

/* Small elements */
.badge { border-radius: 4px; }

/* Circular */
.avatar { border-radius: 50%; }
```

## Shadows (Minimal)

```css
/* Subtle shadow for cards */
.card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* Hover state */
.card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}
```

**Note:** Use shadows sparingly. Borders are preferred over shadows in this design system.

## Buttons

### Primary Button

```css
.button-primary {
  background: var(--accent);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.button-primary:hover {
  background: var(--accent-hover);
}
```

### Secondary Button

```css
.button-secondary {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--border);
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button-secondary:hover {
  border-color: var(--accent);
  background: var(--bg-tertiary);
}
```

## Links

```css
a {
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s;
}

a:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}
```

## Footer

```css
footer {
  padding: var(--section-padding) var(--container-padding);
  text-align: center;
  border-top: 1px solid var(--border);
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

footer a {
  color: var(--text-secondary);
}

footer a:hover {
  color: var(--text-primary);
}
```

## Accessibility

### Color Contrast

All color combinations meet WCAG AA standards:
- `#1a1a1a` on `#fafafa`: 14.8:1 (AAA)
- `#404040` on `#fafafa`: 9.4:1 (AAA)
- `#606060` on `#fafafa`: 6.1:1 (AA)
- White on `#1a1a1a`: 17.4:1 (AAA)

### Focus States

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

button:focus-visible,
a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Anti-Patterns (Avoid)

Based on frontend-design skill:

**Don't use:**
- Inter font (use Instrument Sans instead)
- Generic gradient backgrounds
- Excessive shadows
- Too many colors (stick to the defined palette)
- Overly complex animations
- Dark mode toggle (light theme only for consistency)

**Do use:**
- Instrument Sans + DM Mono
- Minimal, subtle design
- Defined color palette
- Simple, purposeful animations
- Light theme consistently
