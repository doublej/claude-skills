# Animation Easing Reference

## Easing Families

### Tier 1: Essential (Start Here)

**Ease-Out** -- `cubic-bezier(0, 0, 0.58, 1)`
Fast start, slow end. Responsive, courteous feel. Default for 80% of UI animations.
Duration: 200-500ms. Use for elements entering screen.

**Ease-In-Out** -- `cubic-bezier(0.42, 0, 0.58, 1)`
Symmetric S-curve. Balanced for position changes.
Duration: 300-500ms. Use for elements moving between on-screen positions.

**Ease-In** -- `cubic-bezier(0.42, 0, 1.0, 1.0)`
Slow start, fast end. Quick departure.
Duration: 150-300ms. Use for elements leaving screen. 20% shorter than entry.

**Linear** -- `linear`
Constant speed. Mechanical feel.
Duration: variable. Use for spinners, progress bars, continuous rotation.

### Tier 2: Personality (Use With Intent)

**Back** -- Overshoot / anticipation. Pulls back before forward (BackIn) or overshoots target (BackOut). Default overshoot: 1.70158.
Duration: 400-600ms. Playful/creative interfaces only.

**Bounce** -- Multiple parabolas with decreasing amplitude. Simulates ball drop.
Duration: 800-1200ms minimum. Needs time to settle.

**Elastic** -- Spring-like oscillation. Constant frequency, decaying amplitude.
Duration: 800-1200ms minimum. Very attention-grabbing, use sparingly.

**Spring Physics** -- Stiffness, damping, mass. Velocity-aware, inherits gesture motion.
Duration: variable (physics-based). Best for gesture-driven interactions.
- Damping 0.7-0.8: pleasant bounce
- Damping 0.85-0.95: stiff, quick
- Damping ~1.0: minimal overshoot

### Power Curves

| Family | Strength | CSS Example |
|--------|----------|-------------|
| Quad (x^2) | Gentle | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` |
| Cubic (x^3) | Moderate | `cubic-bezier(0.215, 0.61, 0.355, 1)` |
| Quart (x^4) | Strong | `cubic-bezier(0.165, 0.84, 0.44, 1)` |
| Quint (x^5) | Very aggressive | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Sine | Gentle, flowing | `cubic-bezier(0.39, 0.575, 0.565, 1)` |
| Expo | Very dramatic | `cubic-bezier(0.19, 1, 0.22, 1)` |

## Decision Tree

```
What type of animation?
|
+-- Element appearing?
|   -> EASE-OUT, 200-500ms
|
+-- Moving between positions?
|   -> EASE-IN-OUT, 300-500ms
|
+-- Element disappearing?
|   -> EASE-IN, 150-300ms (20% shorter than entry)
|
+-- Mechanical/continuous?
|   -> LINEAR, variable
|
+-- Playful/personality?
    +-- Snappy anticipation?  -> BACK, 400-600ms
    +-- Physics collision?    -> BOUNCE, 800-1200ms
    +-- Spring rubber band?   -> ELASTIC, 800-1200ms
```

## Platform Timing Guidelines

| Platform | Baseline | Notes |
|----------|----------|-------|
| Desktop | 150-200ms | Faster, mouse precision |
| Mobile | 300ms | Touch feedback within 100ms |
| Tablet | 390ms | 30% longer than mobile |
| Wearable | 210ms | 30% shorter than mobile |

Larger distances/screens = longer durations.

## Duration Guidelines by Context

| Context | Duration | Easing |
|---------|----------|--------|
| Button hover/focus | 150-300ms | Ease-out |
| Tooltip | 100-200ms | Ease-out |
| Dropdown/menu | 200-300ms | Ease-out |
| Modal entry | 300-500ms | Ease-out |
| Drawer/sidebar | 300-600ms | Ease-out |
| Page transition | 300-500ms | Ease-in-out |
| Stagger item | 200-300ms each | Ease-out + 50-100ms offset |
| Success state | 400-800ms | Ease-out or Bounce |
| Error shake | 300-500ms | Custom |
| Bounce/elastic | 800-1200ms min | Must settle |

**Hard limits:** Under 100ms = glitch (too fast). Over 700ms = sluggish (exception: dramatic/bounce).

## Material Design Standards

**Standard:** `cubic-bezier(0.4, 0.0, 0.2, 1)` -- growth, property changes. 300ms mobile / 200ms desktop.

**Deceleration:** `cubic-bezier(0.0, 0.0, 0.2, 1)` -- elements entering. 225ms.

**Acceleration:** `cubic-bezier(0.4, 0.0, 1, 1)` -- elements leaving. 195ms (20% shorter).

**Courteous Squire Rule:** Enter fast + land gently (ease-out). Exit quickly (ease-in). Asymmetry feels natural.

## Stagger Patterns

### List Entry

```
Item 1: 0-300ms   (ease-out)
Item 2: 50-350ms  (ease-out, +50ms offset)
Item 3: 100-400ms (ease-out, +100ms)
Item 4: 150-450ms (ease-out, +150ms)
```

- Individual duration: 200-300ms
- Offset: 50-100ms between items
- Direction: top-to-bottom (reading flow)

### Grid Entry

- Offset: 30-50ms between items
- Direction: top-left, then right + down (or spiral from center)

## Performance Rules

**GPU-accelerated (smooth):** `transform`, `opacity`, `filter`

**Causes reflows (janky):** `left`, `top`, `width`, `height`, `margin`, `padding`

Always animate transform/opacity. Never animate layout properties.

## Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Simplify animations, don't eliminate. Opacity fade over 100ms still works.

## Three.js Animation Patterns

### Clock-Based Animation

```ts
const clock = new THREE.Clock();

function animate() {
  const dt = clock.getDelta();
  const elapsed = clock.getElapsedTime();

  // Continuous rotation
  mesh.rotation.y += dt * speed;

  // Sine wave bob
  mesh.position.y = Math.sin(elapsed * 2) * 0.5;

  // Eased interpolation
  mesh.position.lerp(targetPos, 1 - Math.pow(0.01, dt));
}
```

### AnimationMixer (glTF Animations)

```ts
const mixer = new THREE.AnimationMixer(model);
const clips = gltf.animations;

const action = mixer.clipAction(clips[0]);
action.play();

// In render loop
mixer.update(dt);

// Crossfade between animations
const walk = mixer.clipAction(clips[0]);
const run = mixer.clipAction(clips[1]);
walk.play();
run.play();
walk.crossFadeTo(run, 0.5, false);
```

### Tween with Easing (manual)

```ts
function easeOutCubic(t: number) { return 1 - Math.pow(1 - t, 3); }

let progress = 0;
const duration = 0.5; // seconds
const startPos = mesh.position.clone();
const endPos = new THREE.Vector3(5, 0, 0);

function animate(dt: number) {
  if (progress < 1) {
    progress = Math.min(progress + dt / duration, 1);
    const t = easeOutCubic(progress);
    mesh.position.lerpVectors(startPos, endPos, t);
  }
}
```

## Easing Combinations by Mood

| Mood | Easing | Duration | Use |
|------|--------|----------|-----|
| Professional | Ease-out | 150-250ms | Banking, enterprise |
| Balanced | Ease-in-out | 300-400ms | SaaS, consumer apps |
| Playful | Back-out / Bounce | 400-800ms | Games, creative |
| Calm | Ease-in-out | 400-600ms | Reading, meditation |

## Common Pitfalls

- Same easing on all properties = monotone feel
- 200ms bounce = won't settle (needs 800ms+)
- Using elastic for professional interfaces
- No `prefers-reduced-motion` support
- Animating layout properties instead of transform/opacity

## Real-World Patterns

| Company | Technique | Key Insight |
|---------|-----------|-------------|
| Apple iOS | Spring physics, damping 0.7-0.9 | Inherit gesture velocity |
| Google | Staggered list entry, 50-100ms offset | Prevents cognitive overload |
| Stripe | Custom cubic-bezier error shake | Custom easing = brand |
| Figma | Ease-in-back overshoot on entry | Anticipation adds clarity |
| Framer Motion | Spring physics for hover/drag | Physics > duration for gestures |
