# Animation Patterns

Entrance animation patterns for GitHub Pages documentation sites, following animation-easing skill best practices.

## Overview

All animations use a consistent `fadeSlideUp` pattern with staggered delays. Animations are subtle, purposeful, and respect user preferences.

## Core Animation

### fadeSlideUp Keyframes

```css
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Properties:**
- Opacity: 0 → 1 (fade in)
- TranslateY: 20px → 0 (slide up)
- Distance: 20px (subtle, not jarring)

### Default Animation Application

```css
.animated {
  animation: fadeSlideUp 0.5s ease-out forwards;
  opacity: 0; /* Start invisible */
}
```

**Timing:**
- Duration: `0.5s` (500ms) - smooth but not slow
- Easing: `ease-out` - starts fast, ends slow (natural feel)
- Fill mode: `forwards` - maintains final state

## Staggered Delays

### Sequential Elements

For lists, grids, or sequential content, stagger delays by 200ms:

```svelte
{#each items as item, i}
  <div class="item" style="animation-delay: {i * 200}ms">
    {item.content}
  </div>
{/each}
```

**Pattern:**
- Item 0: 0ms delay
- Item 1: 200ms delay
- Item 2: 400ms delay
- Item 3: 600ms delay
- Item 4: 800ms delay
- Item 5: 1000ms delay

**Max delay:** Cap at 1000ms (1 second) to avoid waiting too long

### Section-Level Delays

For page sections, use larger intervals:

```css
.hero { animation-delay: 0ms; }
.install { animation-delay: 200ms; }
.features { animation-delay: 400ms; }
.getting-started { animation-delay: 600ms; }
.footer { animation-delay: 1000ms; }
```

**Then stagger children within each section:**

```svelte
<!-- Features section starts at 400ms -->
<section class="features" style="animation-delay: 400ms">
  <!-- First card appears at 400ms -->
  <div class="card" style="animation-delay: 0ms">...</div>
  <!-- Second card appears at 600ms (400 + 200) -->
  <div class="card" style="animation-delay: 200ms">...</div>
  <!-- Third card appears at 800ms (400 + 400) -->
  <div class="card" style="animation-delay: 400ms">...</div>
</section>
```

## Animation Timing Function Guide

Based on animation-easing skill decision tree:

### Entrance Animations (Use: ease-out)

```css
animation-timing-function: ease-out;
/* or cubic-bezier(0, 0, 0.2, 1) for custom control */
```

**Why ease-out:**
- Elements entering viewport should start fast and decelerate
- Feels natural, like objects settling into place
- Aligns with user's attention pattern

### Hover Animations (Use: ease-in-out)

```css
transition: all 0.2s ease-in-out;
```

**Why ease-in-out:**
- Smooth acceleration and deceleration
- Short duration (200ms) for immediate feedback

### Exit Animations (Rare, Use: ease-in)

```css
animation-timing-function: ease-in;
```

**Why ease-in:**
- Elements leaving should accelerate
- Opposite of entrance

## Duration Guidelines

### Based on Animation-Easing Skill

**Entrance animations:**
- Duration: 400-500ms
- Too fast (<300ms): Jarring, hard to track
- Too slow (>600ms): Sluggish, boring

**Hover effects:**
- Duration: 150-200ms
- Fast response to user interaction

**Large movements:**
- Duration: 500-600ms
- More distance needs more time

**Our choice: 500ms**
- Sweet spot for subtlety and visibility
- Works well with 20px translateY

## Complete Example

### Hero Section

```svelte
<section class="hero">
  <div class="container">
    <h1>Project Name</h1>
    <p class="description">Project description...</p>
  </div>
</section>

<style>
  .hero {
    animation: fadeSlideUp 0.5s ease-out forwards;
    opacity: 0;
  }

  @keyframes fadeSlideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
```

### Feature Grid with Stagger

```svelte
<section class="features">
  <div class="container">
    <h2>Features</h2>
    <div class="grid">
      {#each features as feature, i}
        <div class="feature-card" style="animation-delay: {i * 200}ms">
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .features {
    animation: fadeSlideUp 0.5s ease-out forwards;
    animation-delay: 400ms;
    opacity: 0;
  }

  .feature-card {
    animation: fadeSlideUp 0.5s ease-out forwards;
    opacity: 0;
  }

  @keyframes fadeSlideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
```

### Install Section with Delay

```svelte
<section class="install">
  <div class="container">
    <div class="install-box">
      <code>{installCommand}</code>
      <button onclick={copyToClipboard}>Copy</button>
    </div>
  </div>
</section>

<style>
  .install {
    animation: fadeSlideUp 0.5s ease-out forwards;
    animation-delay: 200ms;
    opacity: 0;
  }

  @keyframes fadeSlideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
```

## Accessibility: Reduced Motion

### Media Query

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

**What this does:**
- Disables ALL animations
- Disables ALL transitions
- Elements appear instantly
- Respects user preference

### Alternative Approach (Fade Only)

If you want to keep fades but remove motion:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01s !important;
    animation-delay: 0s !important;
  }

  @keyframes fadeSlideUp {
    from {
      opacity: 0;
      transform: translateY(0); /* No movement */
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
```

**Our recommendation:** Disable completely (first approach)

## Global Styles Setup

### In global.css

```css
/* Keyframes */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    animation: none !important;
    transition: none !important;
  }
}
```

### In Components

```svelte
<style>
  .element {
    animation: fadeSlideUp 0.5s ease-out forwards;
    opacity: 0;
  }

  /* Delay is set inline via style attribute for dynamic values */
</style>
```

## Performance Considerations

### Use Transform Over Top/Left

**Good (GPU-accelerated):**
```css
transform: translateY(20px);
```

**Bad (CPU-bound):**
```css
top: 20px;
```

**Why:**
- `transform` is GPU-accelerated
- Doesn't trigger layout recalculation
- Smoother, better performance

### Use Opacity

**Good:**
```css
opacity: 0;
```

**Also good:**
```css
visibility: hidden;
```

Both are performant. We use opacity for smooth fading.

### Avoid Animating These Properties

- width/height
- margin/padding
- border
- top/left/right/bottom (use transform instead)

## Testing Animations

### Manual Tests

1. **Normal viewing:**
   - Reload page
   - Observe smooth fade and slide
   - Elements should appear sequentially

2. **Reduced motion:**
   - Enable in System Preferences > Accessibility > Display
   - Reload page
   - Elements should appear instantly, no animation

3. **Mobile:**
   - Test on actual device or simulator
   - Animations should be smooth (60fps)
   - No janky movement

### Browser DevTools

**Chrome DevTools:**
1. Open DevTools
2. Cmd+Shift+P → "Animations"
3. Reload page
4. Inspect animation timeline

**Emulate reduced motion:**
1. Cmd+Shift+P → "reduced motion"
2. Select "Emulate CSS prefers-reduced-motion: reduce"

## Animation Checklist

For each documentation site:

- [ ] fadeSlideUp keyframes defined in global.css
- [ ] Sections have base animation (500ms ease-out)
- [ ] Sections have staggered delays (0ms, 200ms, 400ms, etc.)
- [ ] Grid items stagger by 200ms intervals
- [ ] Max delay is 1000ms
- [ ] Initial opacity is 0
- [ ] animation fill-mode is forwards
- [ ] Reduced motion media query disables all animations
- [ ] Transform (not top/left) used for movement
- [ ] Animations tested on desktop and mobile

## Common Mistakes

**WRONG: Forgetting opacity: 0**
```css
.element {
  animation: fadeSlideUp 0.5s ease-out;
  /* Missing opacity: 0 - element is visible before animation */
}
```

**CORRECT:**
```css
.element {
  animation: fadeSlideUp 0.5s ease-out forwards;
  opacity: 0; /* Starts invisible */
}
```

**WRONG: Using ease-in for entrance**
```css
animation: fadeSlideUp 0.5s ease-in forwards;
/* Feels sluggish, starts slow */
```

**CORRECT:**
```css
animation: fadeSlideUp 0.5s ease-out forwards;
/* Feels natural, decelerates smoothly */
```

**WRONG: Forgetting forwards**
```css
animation: fadeSlideUp 0.5s ease-out;
/* Animation reverses after completion */
```

**CORRECT:**
```css
animation: fadeSlideUp 0.5s ease-out forwards;
/* Maintains final state */
```

**WRONG: Too much stagger**
```css
style="animation-delay: {i * 500}ms"
/* 5 items = 2.5 second wait, too slow */
```

**CORRECT:**
```css
style="animation-delay: {Math.min(i * 200, 1000)}ms"
/* Cap at 1 second */
```

## Summary

**Default animation:**
```css
animation: fadeSlideUp 0.5s ease-out forwards;
opacity: 0;
```

**Staggered delays:**
- Sections: 0ms, 200ms, 400ms, 600ms, 1000ms
- Grid items: i * 200ms (capped at 1000ms)

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
}
```

**Timing function:**
- Entrance: `ease-out`
- Hover: `ease-in-out`
- Duration: 400-500ms
