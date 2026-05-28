# Animation Best Practices & Timing Guidelines

## Duration Guidelines by Context

### Micro-interactions
- Simple property changes: **100-200ms**
- Button hover/focus: **150-300ms**
- Loading indicators: **Continuous** (not time-based)
- Tooltips: **100-200ms**

### Standard UI Transitions
- Modal/dialog entry: **300-500ms**
- Drawer/sidebar entry: **300-600ms**
- Dropdown/menu opening: **200-300ms**
- Form field focus: **150-250ms**
- Page transitions: **300-500ms**

### Complex Animations
- Multi-element stagger: **400-600ms** (individual elements) + stagger offset
- Loading sequences: **600-1000ms**
- Success states: **400-800ms**
- Error animations: **300-500ms** (keep brief to avoid frustration)

### Playful/Elastic Animations
- Bounce effects: **800-1200ms minimum** (must allow settling)
- Elastic animations: **800-1200ms minimum**
- Back overshoot: **400-600ms**

### Rule: Don't Exceed 700ms
- Animations longer than 700ms feel slow and laggy
- Exception: Explicitly dramatic effects or loading sequences
- Mobile users are impatient: Keep durations tight

---

## Platform-Specific Adjustments

### Mobile
- **Baseline duration:** 300ms
- **Why:** Smaller screens, less complex movements
- **Adjust for:** Simple, snappy interactions
- **Touch feedback:** Respond within 100ms for tactile feel

### Tablet
- **Baseline duration:** 390ms (30% longer than mobile)
- **Why:** Larger screens, more space to traverse
- **Adjust for:** Gesture-based interactions
- **Desktop scaling:** Also works for large desktop displays

### Desktop
- **Baseline duration:** 150-200ms
- **Why:** Faster, more predictable interactions
- **Adjust for:** Keyboard navigation, precise mouse movements
- **Exception:** Complex visualizations may need longer

### Wearables (Watch, AR)
- **Baseline duration:** 210ms (30% shorter than mobile)
- **Why:** Minimal screen real estate
- **Adjust for:** Quick glances, fast feedback
- **Critical:** Keep animations brief to avoid missing information

---

## Material Design Motion Standards

### Standard Curve
**Easing:** `cubic-bezier(0.4, 0.0, 0.2, 1)` (easeOutCubic)

**Usage:**
- Material growth and shrinkage
- Property changes (color, opacity, size)
- Persistent element transitions
- Default for most animations

**Duration:**
- Mobile: 300ms
- Tablet: 390ms (30% longer)
- Desktop: 150-200ms

---

### Deceleration Curve
**Easing:** `cubic-bezier(0.0, 0.0, 0.2, 1)` (pure ease-out, no ease-in)

**Usage:**
- Elements entering at full velocity
- Rapid screen transitions
- Responsive appearance

**Duration:** 225ms for mobile entries

---

### Acceleration Curve
**Easing:** `cubic-bezier(0.4, 0.0, 1, 1)` (pure ease-in, no ease-out)

**Usage:**
- Elements leaving screen at full velocity
- Exit animations to appear obedient
- Removes focus-taking "deceleration"

**Duration:** 195ms for mobile exits (20% shorter than entry)

---

### Sharp Curve
**Easing:** `cubic-bezier(0.4, 0.0, 0.6, 1)`

**Usage:**
- Elements that may return to screen
- Transitions within a page
- Less dramatic than deceleration curve

---

## The "Courteous Squire" Rule

This is Material Design's golden rule for responsive interfaces:

### Entering (Arriving)
- **Easing:** Ease-out
- **Duration:** Baseline (e.g., 300ms mobile, 200ms desktop)
- **Effect:** Arrive quickly, slow into place
- **Psychology:** Fast response = perceived responsiveness

### Exiting (Departing)
- **Easing:** Ease-in
- **Duration:** 20% shorter (e.g., 240ms if entry was 300ms)
- **Effect:** Get moving quickly, depart at speed
- **Psychology:** Obedient, doesn't linger

**Why it works:** Asymmetry feels natural. Entering needs a gentle landing. Exiting should be quick and courteous.

---

## Staggered Animation Patterns

### List Entry Pattern
- **Individual animation duration:** 200-300ms ease-out
- **Stagger offset:** 50-100ms between items
- **Total duration:** 300ms + (n × stagger)
- **Direction:** Top-to-bottom (natural reading flow)
- **Effect:** Guides attention and prevents overwhelming

**Example:**
```
Item 1: 0-300ms fade-in
Item 2: 50-350ms fade-in
Item 3: 100-400ms fade-in
Item 4: 150-450ms fade-in
```

### Grid Entry Pattern
- **Stagger:** 30-50ms between items
- **Start direction:** Top-left, move right then down
- **Alternative:** Spiral outward from center

### Cascade Animations
- **For dependent items:** 100-150ms stagger
- **Less jarring than linear stagger**
- **Creates hierarchical flow**

---

## Easing + Duration Combinations

### Fast Response (Professional Interfaces)
- Easing: **Ease-out**
- Duration: **150-250ms**
- Effect: Quick, responsive, trustworthy
- Use: Banking, healthcare, enterprise tools

### Balanced Feel (Startup/Web Apps)
- Easing: **Ease-in-out**
- Duration: **300-400ms**
- Effect: Smooth, natural, polished
- Use: Consumer apps, SaaS, design tools

### Playful Feel (Creative/Gaming)
- Easing: **Back-out or Bounce**
- Duration: **400-800ms**
- Effect: Fun, energetic, memorable
- Use: Games, creative tools, entertainment

### Calm/Meditative (Content-Heavy)
- Easing: **Ease-in-out**
- Duration: **400-600ms**
- Effect: Slow, deliberate, thoughtful
- Use: Reading apps, meditation, educational content

---

## Animation Selection by Purpose

### Communicating State Change
- Primary animation: **Ease-out** (grabs attention)
- Duration: **200-300ms**
- Use: Active/inactive, success/error, expanded/collapsed
- Pair with: Color change, icon swap

### Guiding Attention
- Primary animation: **Ease-out** or **Back-out**
- Duration: **300-500ms**
- Use: Modals, alerts, important messages
- Technique: Scale up from center, slide in from top

### Acknowledging User Action
- Primary animation: **Ease-out**
- Duration: **150-200ms**
- Use: Button press, form validation
- Technique: Scale, color change, or subtle slide

### Creating Delight
- Primary animation: **Bounce** or **Elastic**
- Duration: **800-1200ms**
- Use: Success state, unexpected rewards, easter eggs
- Caution: Use sparingly (novelty wears off fast)

### Loading/Waiting
- Type: **Continuous** (spinner) or **Progressive** (bar)
- Easing: **Linear** (mechanical feel appropriate)
- Duration: Variable, based on actual load time
- Psychology: Fast spinner looks like it's working hard

---

## Accessibility Considerations

### Respecting Reduced Motion
Use the `prefers-reduced-motion` media query:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Who Needs Reduced Motion
- Vestibular disorders (motion triggers dizziness)
- Photosensitive epilepsy (flashing animations trigger seizures)
- Cognitive overload from rapid motion
- Older users (motion harder to track)

### Best Practice
- Provide option in settings
- Simplify animations, don't eliminate (opacity fades over 100ms still work)
- Test animations with reduced-motion enabled

---

## Common Pitfalls to Avoid

### Too Long
- Animation longer than 700ms feels slow
- Users will learn to wait, reducing perceived responsiveness
- Exception: Explicitly dramatic effects with user consent

### Too Short
- Under 100ms may not register as animation
- Users may miss the transition
- Feels janky and incomplete

### Too Many at Once
- Multiple simultaneous animations create chaos
- Use stagger or sequence instead
- Maximum 3-4 elements animating simultaneously

### Wrong Easing for Duration
- 200ms bounce (won't settle)
- 800ms ease-out (feels slow)
- 100ms ease-in-out (feels abrupt)

### Animating Wrong Properties
- `left`, `top`, `width`, `height` cause reflows (janky)
- Better: `transform` (GPU-accelerated), `opacity` (free)
- Always animate: `transform`, `opacity`, `filter`

### Ignoring Accessibility
- No `prefers-reduced-motion` support
- Animations too fast to understand
- Flashing animations (seizure risk)

### Over-Using Personality
- Elastic animations every time feel annoying
- Use sparingly for emphasis
- Professional interfaces should avoid novelty easing

---

## Quick Reference: When to Use Each Easing

| Easing | Duration | Use Case | Industry |
|--------|----------|----------|----------|
| **Ease-Out** | 200-500ms | UI appearing, default | All |
| **Ease-In-Out** | 300-500ms | Position changes | All |
| **Ease-In** | 150-300ms | UI disappearing | All |
| **Linear** | Variable | Spinners, loaders | All |
| **Back** | 400-600ms | Playful interaction | Gaming, Creative |
| **Bounce** | 800-1200ms | Landing, dropping | Gaming, Playful |
| **Elastic** | 800-1200ms | Attention, spring | Gaming, Creative |
| **Spring** | Variable | Gesture response | iOS, Interactive |

---

## Implementation Checklist

- [ ] Choose easing based on purpose (ease-out default)
- [ ] Set duration for platform (300ms mobile, 200ms desktop)
- [ ] Verify settling time for bounce/elastic (800ms+)
- [ ] Animate only `transform` and `opacity`
- [ ] Stagger multi-element animations (50-100ms offset)
- [ ] Test with `prefers-reduced-motion`
- [ ] Verify smooth 60fps performance
- [ ] Get stakeholder feedback on feel
- [ ] Document chosen easing + duration for consistency
- [ ] Consider platform-specific adjustments
