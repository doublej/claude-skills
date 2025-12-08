# Easing Functions Guide

## Core Easing Families (Ranked by Ease & Impact)

### Tier 1: Essential Easing (Start Here)

#### Ease-Out
**CSS:** `cubic-bezier(0, 0, 0.58, 1)`
**JavaScript:** `easeOutQuad`, `easeOutCubic`, `easeOutQuart`

**What it does:** Starts fast and slows down toward completion.

**Why it matters:** Creates responsive, courteous feel. Elements enter the screen quickly then settle gently. This is Material Design's recommended default for most UI animations.

**Key characteristics:**
- Fast initial acceleration
- Smooth deceleration at end
- Feels natural and polished
- Duration: 200-500ms for UI elements

**When to use:**
- Elements entering the screen (modals, dropdowns, notifications)
- UI transitions that need to feel responsive
- Any element that needs to "arrive" smoothly
- Default choice for 80% of animations

**Real-world analogy:** Opening a door—quick initial push, gentle slow as it settles.

---

#### Ease-In-Out
**CSS:** `cubic-bezier(0.42, 0, 0.58, 1)`
**JavaScript:** `easeInOutQuad`, `easeInOutCubic`

**What it does:** Slow start, acceleration in middle, slow end. Symmetric S-curve.

**Why it matters:** Balanced curve feels natural for position changes. Both ends ease, creating smooth transitions.

**Key characteristics:**
- Easing on both start and end
- Symmetrical acceleration
- Works well for movements between on-screen positions
- Duration: 300-500ms

**When to use:**
- Elements moving between on-screen positions
- Property changes (size, color, opacity)
- When start and end points both need emphasis
- Less responsive than ease-out, more balanced

**Real-world analogy:** Sliding a drawer in and out—slow at both ends.

---

#### Linear
**CSS:** `linear`
**JavaScript:** `none` (constant rate)

**What it does:** Constant rate of speed throughout animation.

**Why it matters:** Baseline for mechanical effects. Most human movements aren't linear, so this only works for specific cases.

**Key characteristics:**
- Uniform speed (no acceleration)
- Feels mechanical and cold
- Best for continuous effects
- Duration: Any (effect-dependent)

**When to use:**
- Loading spinners and progress indicators
- Continuous rotation (watch hands, fan blades)
- Mechanical animations
- Scrolling indicators

**When NOT to use:** For most UI transitions (feels unnatural). Users respond better to non-linear motion.

---

### Tier 2: Personality & Emphasis (Use With Intent)

#### Back Easing (Anticipation + Overshoot)
**JavaScript:** `easeOutBack`, `easeInBack`, `easeInOutBack`

**What it does:** Movement goes beyond target then returns (easeOutBack), or pulls back before moving forward (easeInBack).

**Why it matters:** Creates anticipatory "wind-up" effects. Adds playful, energetic feel. Makes movements feel more intentional.

**Key characteristics:**
- Harmonic oscillation (like a spring or pendulum)
- Based on mathematical curves with controllable overshoot
- Default overshoot: 1.70158 (can be tuned)
- Settles in 1-2 oscillations
- Duration: 400-600ms

**Variants:**
- **BackIn:** Pulls back before moving forward (anticipation)
- **BackOut:** Overshoots target before settling (bounce-back)
- **BackInOut:** Both effects

**When to use:**
- Playful, energetic interfaces
- Button presses that "wind up"
- Elements that need anticipatory motion
- Success states or delightful interactions

**When NOT to use:**
- Professional/corporate interfaces
- Conservative designs
- Frequent animations (novelty wears off)

**Real-world analogy:** Pulling back a slingshot then releasing.

---

#### Bounce Easing
**JavaScript:** `easeOutBounce`, `easeInBounce`

**What it does:** Simulates physics of ball bouncing on a surface. Series of parabolas with decreasing amplitude.

**Why it matters:** Creates realistic gravity-based collision effects. Very satisfying for drop/landing animations.

**Key characteristics:**
- Multiple bounces (typically 3-4)
- Energy loss affects both amplitude AND frequency
- Bounces accelerate in frequency over time
- Duration: 800-1200ms minimum (needs time to settle)
- More realistic than elastic for physical collisions

**When to use:**
- Drop/landing animations
- Ball physics simulations
- Playful loading sequences
- Emphasis animations for important events

**When NOT to use:**
- Professional interfaces
- Frequent animations
- Short durations (bounce won't settle)

**Different from Elastic:** Bounce models surface collision (decreasing frequency), while Elastic models spring oscillation (constant frequency).

---

#### Elastic Easing
**JavaScript:** `easeOutElastic`, `easeInElastic`

**What it does:** Oscillates back and forth multiple times like a rubber band or spring.

**Why it matters:** Creates springy, playful motion that strongly attracts attention.

**Key characteristics:**
- Multiple oscillations (configurable bounciness)
- Looks like object tied to target with rubber band
- Bounciness parameter controls number of wiggles
- Constant frequency, exponentially decaying amplitude
- Duration: 800-1200ms minimum

**When to use:**
- Attention-grabbing animations
- Playful, fun projects
- When personality is priority
- Loading animations in casual apps

**When NOT to use:**
- Professional/serious interfaces
- Frequent animations
- Accessibility-focused designs
- Short durations

**Real-world analogy:** Rubber band pulling object to target point.

---

### Mathematical Easing Families

#### Power Curves (Quad, Cubic, Quart, Quint)
**Pattern:** Power of 2, 3, 4, 5 mathematical functions

**Quad (x²):** Gentle easing
**Cubic (x³):** Moderate easing
**Quart (x⁴):** Strong easing
**Quint (x⁵):** Very aggressive easing

**When to use:** Quint ease-out provides extremely smooth UI transitions. Higher powers create more dramatic acceleration (useful when you need pronounced effects).

#### Sine Easing
**Pattern:** Based on sine wave mathematics

**Characteristics:** Gentle, flowing curves. Softer than power curves.

**When to use:** When standard power curves don't provide the exact smoothness you need.

#### Circular Easing
**Pattern:** Based on circular arc mathematics

**Characteristics:** Mid-range smoothness between Sine and Power curves.

#### Exponential Easing
**Pattern:** Based on exponential growth/decay

**Characteristics:** Very dramatic acceleration/deceleration. Use sparingly.

---

## Disney's 12 Animation Principles (Relevant Ones)

### Timing
Controls duration of actions (number of frames between poses).

**Why it matters:** Grounds animation in physics-based realism and conveys weight.

- Heavier objects = more frames (slower movement)
- Lighter objects = fewer frames (quicker reactions)
- Target: 60fps (16.7ms per frame) for smooth web animations

### Spacing
Controls distance between frames (distribution of movement).

**Why it matters:** Creates rhythm and makes performance readable.

- Wider spacing = rapid movement
- Closer spacing = gradual motion
- Works with timing to sell weight

### Ease In and Ease Out (Slow In/Slow Out)
Reflects real-world acceleration and deceleration.

**Why it matters:** Objects don't move at constant speed in nature.

- More frames at beginning = ease in
- More frames at end = ease out
- Creates realistic acceleration/deceleration

### Anticipation
Preparatory movement before main action.

**Why it matters:** Prepares audience for upcoming action. Adds realism and clarity.

- Character steadies before action
- Pull-back before forward motion
- Examples: Football steadying before kick, golfer swing-back before hit

---

## CSS Cubic-Bezier Explained

Cubic-bezier curves use four control points: `cubic-bezier(x1, y1, x2, y2)`

**Axes:**
- **X-axis:** Time/progress (0 = start, 1 = end)
- **Y-axis:** Value change (0 = start value, 1 = end value)

**Creating Easing:**
- Points at (0, 0) and (1, 1) are endpoints
- Middle control points shape the curve

**Overshoot (Y values > 1):** Creates easing that goes past target then returns.

**Bounce (Multiple curves):** Creates oscillating effect (not native to cubic-bezier, requires multiple segments).

**Common Curves:**
- Linear: `cubic-bezier(0, 0, 1, 1)`
- Ease: `cubic-bezier(0.25, 0.1, 0.25, 1.0)`
- Ease-out: `cubic-bezier(0, 0, 0.58, 1.0)`
- Ease-in: `cubic-bezier(0.42, 0, 1.0, 1.0)`
- Ease-in-out: `cubic-bezier(0.42, 0, 0.58, 1.0)`

---

## Spring Physics (Advanced)

Spring animations simulate actual spring physics with three parameters:

**Stiffness:** Higher = more sudden, snappy movement
**Damping:** Strength of opposing force (0 = infinite oscillation, 1 = no oscillation)
**Mass:** Higher = more lethargic, slower response

**Damping Ratio Sweet Spots:**
- 0.7-0.8: Pleasant bounce with gentle overshoot
- 0.85-0.95: Stiff, quick movement
- Near 1.0: Minimal overshoot

**Advantages:**
- Velocity-aware (incorporates existing motion)
- Natural feel for gesture-based interactions
- Settles automatically based on physics

**Disadvantages:**
- Duration is variable (physics-based, not time-based)
- Less predictable timing
- Harder to control precise moments

---

## When to Use What: Decision Tree

```
Starting a UI animation?
├─ Element entering screen?
│  └─ Use EASE-OUT (default choice)
├─ Element moving between positions?
│  └─ Use EASE-IN-OUT (symmetric)
├─ Element leaving screen?
│  └─ Use EASE-IN (get moving quick)
└─ Mechanical effect?
   └─ Use LINEAR (spinner, progress)

Want to add personality?
├─ Professional interface?
│  └─ Stick with Ease-Out/Ease-In-Out
├─ Playful/Fun project?
│  ├─ Want snappy overshoot?
│  │  └─ Use BACK easing
│  ├─ Want physics-like collision?
│  │  └─ Use BOUNCE easing
│  └─ Want spring/rubber band?
│     └─ Use ELASTIC easing
└─ Game/Interactive?
   └─ Consider SPRING physics
```

---

## Key Takeaways

1. **Ease-Out is your default** - Works for 80% of UI animations
2. **Match the emotion to the interface** - Professional ≠ Playful
3. **Respect the settling time** - Bounce/Elastic need 800-1200ms
4. **Timing matters more than easing** - Duration conveys weight
5. **Test with your specific duration** - 200ms ease-out ≠ 800ms ease-out
6. **Use sparingly** - Novelty wears off fast on repeated animations
