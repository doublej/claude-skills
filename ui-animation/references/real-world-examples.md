# Real-World Animation Examples from Production Interfaces

Learn from how leading companies implement animations in their products.

## 1. Apple iOS - Spring Animations with Damping

**Company:** Apple
**Feature:** App launch animations, icon bounces, view controller transitions

**What they do:**
Apps launch with a spring animation that overshoots slightly, then settles. This gives tactile feedback without feeling chaotic.

**Technique:** Physics-based spring with damping ratio 0.7-0.9

**Why it works:**
- Natural, responsive feel mimicking real-world physics
- Subtle overshoot signals the animation is complete
- Damping prevents infinite oscillation

**Timing:**
- Duration: Variable (300-600ms based on gesture velocity)
- Damping: 0.8 is typical sweet spot
- Modern approach: 2-parameter spring (duration + bounce) instead of mass/stiffness/damping

**Implementation:** `UIView.animate(withDuration:delay:options:animations:completion:)` with spring options

**Key Learning:**
Spring animations feel more responsive than duration-based tweens because they inherit gesture velocity. The same gesture on different devices settles at slightly different times based on physics—users don't notice because it "feels right."

---

## 2. Stripe Payment Forms - Error Shake with Custom Easing

**Company:** Stripe
**Feature:** Payment form validation and error indication

**What they do:**
When payment field validation fails, the input field shakes horizontally with a custom cubic-bezier easing. The shake has personality while clearly communicating error.

**Technique:** Custom cubic-bezier easing (not a standard preset)

**Why it works:**
- Shake gets immediate attention without being aggressive
- Custom curve adds personality that sets Stripe apart
- Fast (under 500ms) maintains professional feel
- Horizontal only (doesn't interfere with form layout)

**Timing:**
- Duration: 350-500ms
- Number of shakes: 3-4 horizontal oscillations
- Easing: Custom curve optimized for their brand feel

**Key Learning:**
Custom cubic-bezier curves create memorable brand moments. Stripe invests in tiny animations because they're micro-moments customers experience repeatedly. The right easing curve feels trustworthy and professional.

---

## 3. Figma - Overshoot with Anticipatory Motion (Ease-In-Back)

**Company:** Figma
**Feature:** UI element entry, component transitions

**What they do:**
Elements go slightly past their final position before settling into place, creating anticipatory motion. This "wind-up" prepares users for the main action.

**Technique:** Ease-in-back (overshoot on entry)

**Why it works:**
- Anticipation signals that something intentional is happening
- Overshoot amount is visually obvious and satisfying
- Short duration (300-400ms) prevents feeling sluggish
- Figma's design system makes this tool-specific tuning

**Implementation:** Figma lets designers adjust overshoot amount via a vertical handle in the spring editor

**Key Learning:**
Overshoot can add delight without sacrificing professionalism when duration is short. Figma's design team discovered that anticipatory motion helps users understand when they've triggered a state change.

---

## 4. Google Material Design - Staggered List Entry

**Company:** Google
**Feature:** Lists, cards, grid layouts loading data

**What they do:**
When a list of items loads, each item fades or slides in sequentially rather than all at once. This prevents overwhelming users and establishes visual hierarchy.

**Technique:** Sequential animation with 50-100ms stagger offset

**Why it works:**
- Stagger prevents cognitive overload (processing all at once is overwhelming)
- Sequential animation establishes reading direction (top-to-bottom)
- Manageable pace helps users understand layout
- Creates dynamic feeling without chaos

**Timing:**
- Individual item duration: 200-300ms ease-out
- Stagger offset: 50-100ms between items
- Total sequence: 300ms + (n × stagger)

**Pattern:**
```
Item 1: 0-300ms (fade in)
Item 2: 50-350ms (fade in)
Item 3: 100-400ms (fade in)
Item 4: 150-450ms (fade in)
```

**Key Learning:**
Stagger is one of the most underrated animation techniques. It makes loading feel intentional and under control, improving perceived performance and user confidence.

---

## 5. Navigation Drawers - Ease-Out-Quart (Strong Deceleration)

**Company:** Android Material Design, many apps
**Feature:** Side navigation, drawer menus

**What they do:**
Navigation drawers slide in from the left/right edge with strong deceleration. They start at full velocity then slow dramatically.

**Technique:** Cubic-bezier easeOutQuart: `cubic-bezier(0.165, 0.84, 0.44, 1)`

**Why it works:**
- Mimics opening a physical drawer (quick pull, slows as it extends)
- Fast initial motion feels responsive
- Dramatic deceleration feels intentional (not coasting)
- Matches user's gesture velocity expectations

**Timing:**
- Duration: 400-600ms for full drawer
- Easing: easeOutQuart (strong deceleration)

**Real-world analogy:** Opening a filing cabinet—quick initial pull, gradual slow as drawer fully extends

**Key Learning:**
Different animations should use different easings to match physical expectations. A drawer should feel like opening a drawer, not like opacity fading.

---

## 6. Modal Dialogs - Scale + Backdrop Fade

**Company:** Most modern web apps (Bootstrap, Material-UI, etc.)
**Feature:** Modal dialogs, alert boxes, confirmation dialogs

**What they do:**
Modals scale up from center (or slide from top) with ease-out while backdrop fades in (linear opacity change).

**Technique:**
- Modal: `cubic-bezier(0, 0, 0.58, 1)` easeOut on scale
- Backdrop: Linear on opacity

**Why it works:**
- Scale from center grabs attention (rapid initial movement)
- Ease-out settling feels polished
- Backdrop fade separate from modal prevents visual conflict
- Different easings for different properties prevents monotone feel

**Timing:**
- Modal scale: 300-400ms ease-out
- Backdrop fade: 250-300ms linear (slightly faster)
- Overlap animations for visual fluidity

**Key Learning:**
Complex animations use multiple properties with different easings. Modal + backdrop isn't one animation—it's a choreographed pair. Stagger them by 50-100ms for polish.

---

## 7. Framer Motion / React Springs - Button Hover with Spring Physics

**Company:** Web developers using Framer Motion
**Feature:** Button hover effects, interactive feedback

**What they do:**
Buttons scale or lift on hover using spring physics. The movement feels responsive and has natural settling based on physics, not fixed duration.

**Technique:** Spring animation with configurable stiffness and damping

**Example parameters:**
```
stiffness: 400    // Snappier movement
damping: 10       // Allows overshoot
mass: 0.75        // Lighter feel
```

**Why it works:**
- Spring physics feel more responsive than duration-based tweens
- Inherits gesture velocity (interactive feedback feels natural)
- Settles automatically based on physics
- Different stiffness values create different personality

**Key Learning:**
Spring physics and duration-based animations solve different problems. Springs are better for gesture-based interactions (hover, drag), while duration-based are better for timed sequences (loading, transitions).

---

## 8. iOS UIKit - Damped Spring for View Transitions

**Company:** Apple (UIKit framework)
**Feature:** View controller transitions, interactive animations

**What they do:**
View controller transitions and gesture responses use `usingSpringWithDamping` parameter with damping ratio between 0.7 and 0.9.

**Typical values:**
- Damping 0.7-0.8: Pleasant bounce
- Damping 0.85-0.95: Stiff, quick movement
- Damping near 1.0: Minimal overshoot

**Why it works:**
- Values near 0.7 create satisfying bounce without excessive motion
- Variable duration based on gesture velocity (feels responsive)
- Modern parameter (damping ratio) more intuitive than mass/stiffness

**Key Learning:**
iOS has spent years perfecting spring parameter ranges. Damping ratio 0.7-0.8 is universally pleasant. This is a starting point for any spring animation project.

---

## 9. Notion AI Assistant - Performance-Optimized Animations

**Company:** Notion (using Lottie)
**Feature:** AI assistant character animation

**What they do:**
AI assistant character with smooth, personality-filled animations that maintain responsiveness. Uses JSON-based Lottie animations instead of live rendering.

**Technique:** Lottie (JSON animation format) for complex motion without performance impact

**Why it works:**
- Creates strong personality while maintaining 60fps performance
- Pre-rendered JSON animations don't block interactive elements
- Complex easing and choreography baked into JSON
- No performance penalty compared to simpler animations

**Timing:**
- Interactive elements: Under 300ms (maintains responsiveness perception)
- Character animations: 500-2000ms (more complex, less frequent)

**Key Learning:**
For complex animated characters or mascots, consider pre-baked animation formats (Lottie, SVG). Live-rendered complex animations can impact performance. Trade-offs: less flexible but much more performant.

---

## 10. Google Photos - Grid Reflow with Cross-Fade

**Company:** Google
**Feature:** Photo grid deletion and reflow

**What they do:**
When deleting photos, the grid slides left and uses quick cross-fade on transitioning images. Maintains spatial awareness while smoothly handling multiple simultaneous changes.

**Technique:** Slide + cross-fade (two properties with different easing/timing)

**Why it works:**
- Grid slide (~300ms) guides attention
- Cross-fade (~150ms, faster than slide) for subtlety
- Different timings prevent visual conflict
- Spatial continuity maintained (users understand photos moved)

**Timing pattern:**
```
Grid slide: 300ms ease-out
Cross-fade: 150ms linear (overlapped by 100ms)
```

**Key Learning:**
Complex state changes use multiple coordinated animations. Each animation has a purpose (slide for spatial change, fade for content change). Different timings prevent visual chaos.

---

## Pattern Observations Across Companies

### Timing Sweet Spots
- **Micro-interactions:** 150-300ms (button hover, focus)
- **UI transitions:** 300-500ms (modal entry, drawer slide)
- **Complex animations:** 400-600ms
- **Playful effects:** 800-1200ms (rarely used)

### Easing Preferences
- **Professional interfaces:** 95% ease-out + ease-in-out
- **Playful interfaces:** Mix in back/bounce (5-20% of animations)
- **Physical interactions:** Spring physics (iOS, Framer)
- **Premium brands:** Custom cubic-bezier curves

### Multi-Property Animations
- Separate easing for different properties
- Stagger timing for visual flow
- Never use same easing on everything (monotone feel)

### Accessibility
- Google, Apple, Stripe all support `prefers-reduced-motion`
- Simplify, don't eliminate animations
- Critical: Test with motion disabled

---

## Key Learnings

1. **Ease-out is universal** - Apple, Google, Stripe all rely on it
2. **Spring physics for interaction** - Mobile apps prefer physics-based (responsive feel)
3. **Duration-based for sequences** - Timed animations for coordinated transitions
4. **Stagger is powerful** - Simple technique, big impact on perceived performance
5. **Custom easing = brand** - Stripe shows custom cubic-bezier creates memorable feel
6. **Respect settling time** - Never use bounce in under 800ms
7. **Different properties, different easing** - Don't apply same easing to scale + fade
8. **Performance matters** - Complex animations at 60fps (Lottie for heavy animations)
9. **Gesture velocity matters** - Spring animations that inherit gesture feel responsive
10. **Personality is earned** - Playful easing works only with short durations and rare use

---

## Study Ideas

1. **Inspect animations in your browser:**
   - Chrome DevTools → Animations tab
   - Slow down animation playback to 0.1x
   - Identify easing, duration, properties

2. **Try recreating:**
   - Pick an animation you like
   - Estimate duration and easing
   - Build it with CSS or animation library
   - Compare to original

3. **Test on different platforms:**
   - Same animation on mobile vs desktop
   - Perceived responsiveness differs
   - Platform defaults matter

4. **Measure perceptual impact:**
   - A/B test duration (150ms vs 300ms vs 500ms)
   - A/B test easing (ease-out vs ease-in-out)
   - Measure actual engagement (not just aesthetic preference)
