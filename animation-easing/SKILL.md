---
name: animation-easing
description: Comprehensive guide to animation easing functions, timing principles, and best practices for creating smooth, responsive animations. Learn when and how to use ease-out, ease-in-out, bounce, elastic, and spring animations. Use this skill when explaining animation techniques, helping choose the right easing for a project, designing animation timings for UI transitions, or teaching animation principles to designers and developers.
---

# Animation Easing: Theory & Practice

## Overview

This skill teaches animation easing functions—the mathematical curves that control how objects accelerate and decelerate during animations. Whether you're building a UI transition, designing a game animation, or creating an interactive experience, choosing the right easing function dramatically impacts how your animation feels to the user.

The skill covers:
- **Easing families** (ease-out, ease-in-out, bounce, elastic, spring, and more)
- **Timing guidelines** by platform and context
- **Real-world examples** from production interfaces (Apple, Google, Stripe, Figma)
- **Best practices** for responsive, accessible animations
- **Decision trees** to help choose the right easing for your specific use case

## Quick Start: Choose Your Easing

Most animations fall into these categories:

### 1. UI Element Appearing (Modal, Button, Alert)
**Use:** Ease-out
**Duration:** 200-500ms
**Why:** Fast start (responsive), slow end (polished landing)
**CSS:** `cubic-bezier(0, 0, 0.58, 1)`

### 2. Element Moving Between Positions
**Use:** Ease-in-out
**Duration:** 300-500ms
**Why:** Symmetric curve feels balanced
**CSS:** `cubic-bezier(0.42, 0, 0.58, 1)`

### 3. Element Disappearing
**Use:** Ease-in
**Duration:** 150-300ms
**Why:** Quick departure feels obedient
**CSS:** `cubic-bezier(0.42, 0, 1.0, 1.0)`

### 4. Loading/Continuous Effect
**Use:** Linear
**Duration:** Continuous
**Why:** Mechanical feel appropriate for process
**CSS:** `linear`

### 5. Playful/Gaming Interface (Bounce, Spring)
**Use:** Bounce or Elastic
**Duration:** 800-1200ms minimum
**Why:** Personality and delight
**Caution:** Only for casual/gaming interfaces

## Core Easing Functions Explained

See **[EASING GUIDE](references/easing-guide.md)** for comprehensive coverage of all easing families:

- **Ease-Out:** Fast start, slow end (responsive, polished)
- **Ease-In-Out:** Symmetric S-curve (balanced)
- **Ease-In:** Slow start, fast end (obedient exit)
- **Linear:** Constant speed (mechanical)
- **Back:** Anticipatory overshoot (playful)
- **Bounce:** Physics-based collision (realistic)
- **Elastic:** Spring-like oscillation (fun)
- **Spring Physics:** Velocity-aware, damping-based (responsive)

Each has specific use cases, duration requirements, and personality traits.

## Platform-Specific Timing

Choose your base duration by platform:

### Mobile
- **Baseline:** 300ms
- **Adjust for:** Responsive feel on small screens
- **Touch feedback:** Respond within 100ms

### Desktop
- **Baseline:** 150-200ms
- **Adjust for:** Faster, more predictable interactions
- **Mouse precision:** Quicker feedback expected

### Tablet
- **Baseline:** 390ms (30% longer than mobile)
- **Adjust for:** Larger screens, more space to traverse

### Wearables
- **Baseline:** 210ms (30% shorter than mobile)
- **Adjust for:** Minimal screen real estate, quick glances

**Principle:** Longer distances and larger screens = longer durations. Mobile users are more impatient than desktop users.

## Animation Selection Decision Tree

```
What type of animation are you creating?

├─ UI element appearing?
│  └─ Use EASE-OUT (responsive, lands gently)
│     Example: Modal fade-in, button appearance, notification entry
│
├─ Element moving between positions?
│  └─ Use EASE-IN-OUT (symmetric, balanced)
│     Example: Expanding accordion, sliding drawer, position shift
│
├─ Element disappearing?
│  └─ Use EASE-IN (quick departure)
│     Example: Modal close, notification dismiss, menu exit
│
├─ Mechanical/continuous effect?
│  └─ Use LINEAR (constant speed)
│     Example: Spinner, progress bar, rotating loader
│
└─ Playful/Personality-focused?
   ├─ Want snappy anticipation?
   │  └─ Use BACK (wind-up effect)
   │     Duration: 400-600ms
   │     Example: Button press, playful reveal
   │
   ├─ Want physics-like bounce?
   │  └─ Use BOUNCE (realistic collision)
   │     Duration: 800-1200ms minimum
   │     Example: Drop animation, landing effect
   │
   └─ Want springy rubber band?
      └─ Use ELASTIC (spring oscillation)
         Duration: 800-1200ms minimum
         Example: Attention-grabbing, fun interactions
```

## Material Design Motion Standards

Google's Material Design defines standard motion for professional interfaces:

**Standard Curve:** `cubic-bezier(0.4, 0.0, 0.2, 1)`
- Use for: Material growth, property changes, persistent transitions
- Duration mobile: 300ms
- Duration desktop: 200ms

**Deceleration:** `cubic-bezier(0.0, 0.0, 0.2, 1)` (pure ease-out)
- Use for: Elements entering screen
- Duration: 225ms

**Acceleration:** `cubic-bezier(0.4, 0.0, 1, 1)` (pure ease-in)
- Use for: Elements leaving screen
- Duration: 195ms (20% shorter than entry)

**The Courteous Squire Rule:**
- **Entering:** Fast arrival (ease-out), slow landing
- **Exiting:** Quick departure (ease-in)
- **Psychology:** Asymmetry feels natural. Entering needs gentle landing; exiting should be swift and courteous.

See **[BEST PRACTICES](references/best-practices.md)** for detailed timing guidelines, stagger patterns, and implementation checklists.

## Real-World Examples from Production

Learn from how leading companies implement animations:

### Apple iOS
Uses spring physics with damping 0.7-0.9. Animations inherit gesture velocity, creating responsive feel.
**Key learning:** Physics-based animations feel more responsive than duration-based.

### Google Material Design
Uses staggered list entry animations (50-100ms offset between items) to prevent cognitive overload.
**Key learning:** Stagger is powerful for visual flow.

### Stripe
Uses custom cubic-bezier curves for payment form animations (error shake).
**Key learning:** Custom easing creates memorable brand moments.

### Figma
Uses ease-in-back (overshoot on entry) to signal intentional state changes.
**Key learning:** Anticipatory motion adds clarity.

See **[REAL-WORLD EXAMPLES](references/real-world-examples.md)** for 10 detailed case studies and implementation patterns you can directly apply.

## Staggered Animation Pattern

When animating multiple elements (lists, grids):

```
Item 1: 0-300ms (animate in)
Item 2: 50-350ms (animate in)  <- 50ms offset
Item 3: 100-400ms (animate in) <- 100ms offset total
Item 4: 150-450ms (animate in) <- 150ms offset total
```

**Timing rules:**
- Individual item duration: 200-300ms each
- Stagger offset: 50-100ms between items
- Direction: Top-to-bottom (natural reading flow)

**Why it works:**
- Prevents overwhelming users with simultaneous motion
- Guides attention in natural reading direction
- Makes loading feel intentional and controlled

## Common Pitfalls

### Duration Mistakes
- ❌ Under 100ms: Animation feels like a glitch (too fast to register)
- ❌ Over 700ms: Animation feels slow and sluggish
- ❌ 200ms bounce: Bounce won't settle (needs 800ms+)

### Easing Mistakes
- ❌ Using elastic for professional interface (inappropriate personality)
- ❌ Same easing for all properties (monotone feel)
- ❌ No easing support for reduced-motion preference (accessibility fail)

### Animation Property Mistakes
- ❌ Animating `left`, `top`, `width`, `height` (causes reflows, janky)
- ✅ Animate `transform`, `opacity`, `filter` (GPU-accelerated, smooth)

## Accessibility: Respecting Reduced Motion

Always implement `prefers-reduced-motion` support:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Who needs this:**
- Vestibular disorders (motion triggers dizziness)
- Photosensitive epilepsy (flashing/rapid motion)
- Cognitive overload from animation
- Older users (motion harder to track)

**Best practice:** Simplify animations, don't eliminate. Opacity fade over 100ms still works without motion.

## Recommended Resources

### For Learning Easing Theory
- **[EASING GUIDE](references/easing-guide.md)** - Complete reference on all easing families, Disney's 12 animation principles, cubic-bezier math
- [Easings.net](https://easings.net/) - Interactive easing visualization (30+ presets)
- [Robert Penner's Easing Functions](https://robertpenner.com/easing/) - Gold standard easing library

### For Implementation Guidance
- **[BEST PRACTICES](references/best-practices.md)** - Timing guidelines, platform adjustments, stagger patterns, implementation checklist
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function) - CSS easing reference
- [Material Design Motion](https://m1.material.io/motion/duration-easing.html) - Google's motion standards

### For Inspiration & Real-World Examples
- **[REAL-WORLD EXAMPLES](references/real-world-examples.md)** - 10 production animation case studies (Apple, Google, Stripe, Figma, etc.)
- [CodePen Animation Examples](https://codepen.io) - Working examples of animations
- Browser DevTools - Inspect animations on live websites (Chrome DevTools → Animations tab)

## Quick Decision: Should You Add an Animation?

**Animate if:**
- State is changing and users might miss it
- You want to guide user attention
- The motion conveys meaning
- Platform conventions use animation

**Don't animate if:**
- Users see this interaction repeatedly (novelty wears off)
- Duration would exceed 700ms
- You're using animation as visual filler (no purpose)
- It conflicts with reduced-motion preference

## Implementation Workflow

1. **Identify the purpose** - State change? Attention? Feedback?
2. **Choose easing** - Use decision tree above
3. **Set duration** - Based on platform + context
4. **Test settling** - For bounce/elastic, verify 800ms+ settling
5. **Verify performance** - Target 60fps (animate transform/opacity only)
6. **Test accessibility** - Verify `prefers-reduced-motion` support
7. **Get feedback** - Does it feel right? Does it serve the purpose?

## Key Takeaways

1. **Ease-out is your default** - Works for ~80% of UI animations
2. **Match emotion to interface** - Professional ≠ Playful
3. **Timing communicates weight** - Longer = heavier
4. **Respect settling time** - Bounce/Elastic need 800-1200ms
5. **Stagger prevents chaos** - Use 50-100ms offset for multiple items
6. **Animate only transform/opacity** - GPU-accelerated, smooth
7. **Platform matters** - Mobile 300ms, Desktop 200ms baseline
8. **Accessibility matters** - Always support `prefers-reduced-motion`
9. **Test with real users** - Perception matters more than theory
10. **Use sparingly** - Personality easing loses impact if overused
