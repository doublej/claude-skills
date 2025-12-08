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

- **Language**: Swift 5.9+
- **UI**: SwiftUI (preferred), UIKit where needed
- **Architecture**: MVVM or TCA
- **State**: @State, @StateObject, @ObservedObject, @EnvironmentObject

## Aesthetics Guidelines

### Typography
- Use Apple's typography intentionally (SF Pro with optical sizes)
- Embrace Dynamic Type
- Pair distinctive display font with refined text style

### Color & Theme
- Define semantic colors in asset catalog
- Implement light/dark variants
- Use system materials for depth
- Respect `colorScheme`, `accessibilityContrast`, `reduceTransparency`

### Motion & Haptics
- Use animations for high-impact moments
- Respect `reduceMotion`
- Use Core Haptics to punctuate interactions

### Accessibility
- Label controls for VoiceOver
- Ensure 4.5:1 contrast minimum
- Honor Dynamic Type
- 44pt minimum hit targets

## Anti-Patterns

Never ship:
- Default blue buttons everywhere
- Identical rounded card lists
- Unmodified SF Pro at default sizes
- Cookie-cutter components ignoring context

## Resources

### AI-Readable Apple Documentation (via sosumi.ai)

- **SwiftUI**: `https://sosumi.ai/documentation/swiftui`
- **HIG**: `https://sosumi.ai/design/human-interface-guidelines`
- **SwiftData**: `https://sosumi.ai/documentation/swiftdata`
- **Accessibility**: `https://sosumi.ai/documentation/accessibility`

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
