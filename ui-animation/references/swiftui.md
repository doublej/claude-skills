# SwiftUI / Native Motion

The decision tree, durations and squire rule in SKILL.md are platform-agnostic. This file maps them to SwiftUI (and AppKit/UIKit where it differs).

## CSS → SwiftUI mapping

| SKILL.md choice | CSS | SwiftUI |
|-----------------|-----|---------|
| Ease-out (enter) | `cubic-bezier(0, 0, 0.58, 1)` | `.easeOut(duration: 0.22)` |
| Ease-in-out (move) | `cubic-bezier(0.42, 0, 0.58, 1)` | `.easeInOut(duration: 0.3)` |
| Ease-in (exit) | `cubic-bezier(0.42, 0, 1, 1)` | `.easeIn(duration: 0.18)` |
| Linear (spinner) | `linear` | `.linear(duration: 1).repeatForever(autoreverses: false)` |
| Custom bezier (Material standard) | `cubic-bezier(0.4, 0, 0.2, 1)` | `.timingCurve(0.4, 0, 0.2, 1, duration: 0.3)` |
| Spring, no overshoot | — | `.smooth` (bounce 0) |
| Spring, slight overshoot (UI default on Apple platforms) | — | `.snappy` (bounce 0.15) |
| Spring, playful | — | `.bouncy` (bounce 0.3) |
| Spring, explicit | — | `.spring(duration: 0.4, bounce: 0.2)` (iOS 17 / macOS 14) or `.spring(response: 0.4, dampingFraction: 0.8)` (older) |

Spring parameters: `duration`/`response` ≈ perceived length; `bounce` 0 = critically damped, keep ≤ 0.3 outside playful UI. `dampingFraction` = 1 − bounce, so Apple's 0.7–0.9 damping ≈ bounce 0.1–0.3. Springs keep gesture velocity, so prefer them for anything driven by drag.

## Applying animations

- State change: `withAnimation(.snappy) { isOpen.toggle() }`.
- Bound to a value: `.animation(.easeOut(duration: 0.22), value: isOpen)`. Always pass `value:` — the value-less `.animation(_:)` is deprecated and animates unrelated changes.
- Enter/exit asymmetry (squire rule): `.transition(.asymmetric(insertion: .move(edge: .bottom).combined(with: .opacity), removal: .opacity))`.
- Stagger: `.animation(.easeOut(duration: 0.25).delay(Double(index) * 0.05), value: shown)`.
- Multi-step: `phaseAnimator` / `keyframeAnimator` (iOS 17 / macOS 14) instead of chained `DispatchQueue.asyncAfter`.

## Reduce motion

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

withAnimation(reduceMotion ? .easeOut(duration: 0.1) : .snappy) { isOpen.toggle() }
// transitions: swap movement for a fade
.transition(reduceMotion ? .opacity : .move(edge: .bottom).combined(with: .opacity))
```

Outside a View: `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion` (AppKit), `UIAccessibility.isReduceMotionEnabled` (UIKit). Same rule as CSS: simplify to a short fade, don't remove feedback.

## Motion tokens

Put every curve in one file next to the other design tokens (e.g. `Design/Motion.swift` beside `Design/Spacing.swift`) and reference only the tokens at call sites:

```swift
extension Animation {
    static let enter = Animation.easeOut(duration: 0.22)
    static let exit  = Animation.easeIn(duration: 0.18)
    static let move  = Animation.snappy(duration: 0.3)
}
```

A motion pass then means: grep `withAnimation\|\.animation(\|\.spring(\|\.easeInOut` across the target, map each site to a token by purpose (enter/exit/move/feedback), and add the reduce-motion branch once in the token or a helper.

## Performance

- Animate `opacity`, `scaleEffect`, `offset`, `rotationEffect` — the transform/opacity equivalent. Animating `frame` or layout in long lists re-lays out every row.
- `.drawingGroup()` for many simultaneously animated shapes; `.geometryGroup()` (iOS 17) when a parent's geometry animation tears children.
- macOS desktop baseline applies: 150–200ms for most UI, springs ~0.3s.
