---
name: swift-app-ui
description: Create distinctive, production-grade Swift app interfaces with high design quality. Use this skill when the user asks to build iOS, iPadOS, macOS, watchOS, or tvOS components, screens, or applications. Generate creative, polished Swift code that avoids generic AI aesthetics.
license: MIT
---

# Swift App UI Design Skill

Create distinctive, production-grade Swift app interfaces that avoid generic "AI slop" aesthetics.

## When to Use

- Building iOS, iPadOS, macOS, watchOS, or tvOS components
- Creating SwiftUI or UIKit interfaces with visual distinction
- Designing interactive experiences with intentional aesthetics
- Implementing production-grade app UIs

## Design Thinking

Before coding, commit to a **BOLD aesthetic direction**:

- **Purpose**: What problem does this solve? Who uses it?
- **Tone**: Pick an extreme—brutally minimal, maximalist, retro-futuristic, luxury, playful, brutalist, etc.
- **Differentiation**: What makes this UNFORGETTABLE?

## Implementation Stack

- **Language**: Swift 6.x / Swift 5.9+
- **UI**: SwiftUI (preferred), UIKit where needed
- **Architecture**: MVVM or TCA
- **State**: @State, @StateObject, @ObservedObject, @EnvironmentObject

## Apple HIG Core Principles

### Clarity
- Text legible at every size using SF Pro system font
- Icons use SF Symbols exclusively (no custom icons when SF Symbol exists)
- Subtle, appropriate adornments only

### Deference
- Content takes priority with full-bleed layouts
- Minimal UI chrome that doesn't distract

### Depth
- Layering and motion convey hierarchy
- Translucent backgrounds enhance understanding
- Realistic animations (not decorative noise)

### Liquid Glass (iOS 26+)
- Translucent elements adapting to light, motion, content
- Refined color palettes with dynamic adaptation
- Glass-like depth effects for modal surfaces

## Navigation Patterns

Choose the right structure:

| Pattern | Use When | Examples |
|---------|----------|----------|
| **Tab Bar** | 3-5 equal-importance sections | Music, Photos, App Store |
| **Hierarchical** | Tree-structured drill-down | Settings, Mail folders |
| **Modal** | Self-contained focused tasks | Compose, Edit, Share |

Rules:
- Tab bars: persistent visibility, never hide on scroll
- Hierarchical: clear back navigation, breadcrumb context
- Modal: obvious dismiss affordance (X or swipe)

## Gesture Vocabulary

Standard gestures—never override:
- **Tap**: Primary action
- **Long Press**: Context menu / secondary actions
- **Swipe**: Navigate, delete, reveal actions
- **Pinch**: Zoom
- **Edge Swipe**: System navigation (NEVER override)

## Aesthetics Guidelines

### Typography
- SF Pro with optical sizes (Text, Display, Rounded)
- Embrace Dynamic Type—never fixed font sizes
- Pair distinctive display font with refined text style

### Color & Theme
- **Semantic colors only**: `Color("Primary")`, never RGB literals
- Use system colors: `.systemBlue`, `.systemRed`, `.label`, `.secondaryLabel`
- Implement light/dark variants in asset catalog
- Use system materials (`.ultraThinMaterial`, `.regularMaterial`) for depth
- Respect `colorScheme`, `accessibilityContrast`, `reduceTransparency`

### SF Symbols
- Use SF Symbols for ALL icons
- Match symbol weight to adjacent text weight
- Use rendering modes: monochrome, hierarchical, palette, multicolor
- Animate with `.symbolEffect()`

### Motion & Haptics
- Animations for high-impact moments only
- Respect `reduceMotion` environment value
- Core Haptics to punctuate interactions (`.impact()`, `.notification()`, `.selection()`)

### Accessibility (Non-Optional)

| Requirement | Standard |
|-------------|----------|
| Touch targets | 44×44pt minimum |
| Text contrast | 4.5:1 (normal), 3:1 (large 18pt+) |
| VoiceOver | All controls labeled |
| Dynamic Type | Support `.xSmall` to `.accessibility5` |
| Reduce Motion | Provide static alternatives |

## Anti-Patterns

Never ship:
- Default `.buttonStyle(.borderedProminent)` blue buttons
- Identical rounded card lists (vary presentation by content type)
- Unmodified SF Pro at default sizes
- Cookie-cutter components ignoring context
- Hamburger menus (use tab bar or hierarchical nav)
- Hidden tab bars on scroll
- Purple/indigo accent colors (overused)
- Hardcoded colors (`Color(red:green:blue:)`)
- Custom icons when SF Symbol exists
- Ignoring safe areas (notch, Dynamic Island)
- Overriding system edge gestures

## Resources

### AI-Readable Apple Documentation (via sosumi.ai)

- **SwiftUI**: `https://sosumi.ai/documentation/swiftui`
- **HIG**: `https://sosumi.ai/design/human-interface-guidelines`
- **SwiftData**: `https://sosumi.ai/documentation/swiftdata`
- **Accessibility**: `https://sosumi.ai/documentation/accessibility`
- **SF Symbols**: `https://sosumi.ai/design/human-interface-guidelines/sf-symbols`

Replace `developer.apple.com` with `sosumi.ai` for any Apple docs.

### Additional
- [Agent Rules - Swift Guidelines](https://github.com/steipete/agent-rules/tree/main/docs)

## Reference Files

See `references/` for:
- `swiftui-api-reference.md` - SwiftUI patterns
- `design-systems.md` - Color, typography, components
- `anti-patterns-and-gotchas.md` - Common mistakes

See `examples/` for:
- `starter-template.swift` - Complete working example
