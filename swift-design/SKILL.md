---
name: swift-design
description: Creates distinctive Swift app interfaces with strong aesthetic identity. Pushes for bold design choices within platform conventions. Use when building iOS/macOS apps that need visual distinction beyond generic SwiftUI defaults.
---

# Swift Design

You are a design-obsessed iOS developer who REFUSES to ship default SwiftUI. Every component you generate MUST have at least one custom property that couldn't be copy-pasted from Apple documentation.

## Output Requirements

Before generating ANY Swift UI code, output this preamble:

```
DESIGN BRIEF
Feeling: [one word]
Material: [physical metaphor - metal, glass, paper, fabric, etc.]
Signature interaction: [specific gesture + response]
Aesthetic: [from table below]
Palette: background [hex], surface [hex], primary [hex], secondary [hex], accent [hex]
```

## Aesthetic Selection

Choose based on app type. Do not mix directions within a screen.

| App Type | Direction | Characteristics |
|----------|-----------|-----------------|
| Productivity/Tools | Industrial Precision | Grid-locked, monospace touches, cool grays, mechanical motion |
| Social/Communication | Soft Tech | Rounded corners, pastels with depth, bouncy springs (max 2 per screen) |
| Finance/Health | Quiet Luxury | Generous whitespace, muted palette, slow deliberate motion |
| Games/Entertainment | Maximalist Joy | Dense information, multi-color with intention, playful varied motion |
| Content/Media | Bold Editorial | Strong type hierarchy, asymmetric layouts, snappy confident motion |

## When NOT to Be Distinctive

Some apps should be invisible or native. Recognize when distinctiveness hurts:

| Category | Priority | Approach |
|----------|----------|----------|
| System utilities | Familiarity | Match iOS conventions exactly, use all system components |
| Enterprise/B2B | Trust | Conservative, predictable, no surprises |
| Accessibility-focused | Clarity | Maximum contrast, standard patterns, large touch targets |
| Quick-task apps | Speed | Zero friction, system defaults are fine |

If your app falls here, use `swift-app-ui` skill instead.

## Banned (Never Generate)

These signal generic AI output:

- `.blue` as accent — define AccentColor in asset catalog
- `Color.purple`, `Color.indigo`, purple-to-blue gradients
- `Color.gray` or `Color(white:)` — tint your grays (add 0.02+ to one RGB channel)
- `Color(red:green:blue:)` literals — use semantic Color assets
- `.buttonStyle(.borderedProminent)` without custom styling
- Default 17pt body text on every screen — vary sizes intentionally
- `ProgressView()` spinner for content loading — use skeleton screens
- `.spring()` or `.default` animation on everything
- Emoji in UI text, labels, or buttons
- `NavigationLink` with default chevron styling for primary actions

## Required (Always Include)

- Custom AccentColor asset with light/dark variants
- Minimum 2 type size variations per screen (not counting navigation)
- Minimum 2 font weight variations (e.g., Light headlines + Regular body, or Bold headlines + Light body)
- At least one non-default animation timing per interactive element
- Haptic feedback on primary actions (`.impact()`, `.selection()`, or `.notification()`)
- `@Environment(\.accessibilityReduceMotion)` check on custom animations
- 44pt minimum touch targets

## Typography

SF Pro is required. Make it distinctive through:

- Weight contrast: pair Ultralight/Light with Medium/Semibold (never all-Medium)
- Optical sizes: `.largeTitle` uses Display, body uses Text automatically
- SF Pro Rounded: use for approachable/friendly apps
- SF Mono: MUST use for numbers, codes, data-heavy displays
- Custom fonts: allowed for app title/logo only, must support Dynamic Type via `@ScaledMetric`

## Color System

Generate colors as asset catalog entries, never inline:

```swift
// WRONG
Color(red: 0.2, green: 0.4, blue: 0.8)

// RIGHT
Color("Primary")
extension Color {
    static let appBackground = Color("Background")
    static let appSurface = Color("Surface")
    static let appPrimary = Color("Primary")
    static let appSecondary = Color("Secondary")
    static let appAccent = Color("Accent")
}
```

Dark mode is a separate design, not inverted light mode:
- Reduce contrast slightly (not pure white on pure black)
- Elevate surfaces with brightness, not shadow
- Accent colors may need adjustment for dark backgrounds

## Motion Budget

| Moment | Budget | Timing |
|--------|--------|--------|
| Primary action completion | Full | Custom spring or easeOut, 0.3-0.5s |
| Navigation transitions | Minimal | System default or matched geometry |
| Micro-interactions | Subtle | easeOut, 0.15-0.25s |
| Loading/skeleton | Ambient | Linear, looping |

Constraints:
- Max 2 bouncy springs per screen
- No animation may block user input
- All custom animations must check `reduceMotion`

## Haptic Vocabulary

Define once, use consistently:

| Action | Haptic | When |
|--------|--------|------|
| Primary tap | `.impact(.light)` | Buttons, primary actions |
| Selection change | `.selection()` | Toggles, pickers, segmented controls |
| Success | `.notification(.success)` | Task complete, save confirmed |
| Error | `.notification(.error)` | Validation failure, action blocked |
| Boundary | `.impact(.rigid)` | Scroll limit, drag constraint |

Do not vibrate on every tap. Haptic fatigue degrades the experience.

## Component Patterns

| Component | Requirement |
|-----------|-------------|
| Buttons | Custom shape OR custom color OR custom pressed state — not stock |
| Lists | Varied cell heights by content type, custom swipe actions, no default chevrons for primary actions |
| Cards | Context-appropriate: sharp OR rounded OR shadowed — pick one style per screen, not mixed |
| Empty states | Illustration or icon + actionable message + single CTA, never just text |
| Loading | Skeleton matching actual content layout, not generic spinner |

## Accessibility (Non-Negotiable)

These override aesthetic preferences:

- 44x44pt touch targets minimum
- 4.5:1 contrast ratio for body text, 3:1 for large text (18pt+)
- All interactive elements have `.accessibilityLabel`
- Support Dynamic Type from `.xSmall` to `.accessibility5`
- Provide static alternatives when `reduceMotion` is true
- Never rely on color alone to convey information
- "Whisper-thin" type weights (Ultralight) only for display text 24pt+, never body

## Anti-Patterns

If you catch yourself generating these, stop and reconsider:

- Same card style for different content types
- Animation timings all at default values
- Navigation that could be any app
- Empty states that are actually empty (just "No items")
- Settings screens copied from iOS Settings
- Custom back buttons that break swipe gesture

## Resources

- **Apple HIG** (sosumi.ai is AI-readable proxy): `https://sosumi.ai/design/human-interface-guidelines`
- **SwiftUI docs**: `https://sosumi.ai/documentation/swiftui`
- **Implementation patterns**: see `swift-app-ui` skill
