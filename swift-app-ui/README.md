# Swift App UI Design Skill

A comprehensive skill for building distinctive, production-grade Swift app interfaces with high design quality.

## Skill Overview

This skill guides the creation of SwiftUI and UIKit interfaces that avoid generic "AI slop" aesthetics and instead deliver real working code with exceptional attention to design details.

### When to Use
- Building iOS, iPadOS, macOS, watchOS, or tvOS components
- Creating distinctive app screens and applications
- Designing production-grade user interfaces
- Implementing custom design systems
- Seeking high-quality, non-generic interface designs

## Folder Structure

```
swift-app-ui/
├── SKILL.md                          # Main skill documentation (entrypoint)
├── README.md                         # This file
├── references/
│   ├── swiftui-api-reference.md      # Quick lookup for SwiftUI patterns
│   ├── design-systems.md              # Color, typography, component systems
│   └── anti-patterns-and-gotchas.md  # Common mistakes and how to avoid them
└── examples/
    └── starter-template.swift         # Complete working example app
```

## Quick Start

### For New Developers
1. Read `SKILL.md` for the design thinking framework
2. Review `references/design-systems.md` to establish patterns
3. Study `examples/starter-template.swift` for real code
4. Reference `references/swiftui-api-reference.md` while coding

### For Designers Building Code
1. Commit to a bold aesthetic direction (read design philosophy in SKILL.md)
2. Use `references/design-systems.md` to implement color/typography systems
3. Follow component patterns from `starter-template.swift`
4. Test thoroughly using the checklist in `anti-patterns-and-gotchas.md`

## Key Features

### SKILL.md Sections
- **Design Thinking Framework**: How to approach a UI problem
- **Implementation Stack**: Technology choices and defaults
- **Aesthetics Guidelines**: Typography, color, motion, interaction, accessibility
- **Common Patterns**: Real code examples for frequent scenarios
- **Anti-Patterns**: What to avoid
- **Xcode Previews**: Multi-device/appearance testing setup
- **Performance Checklist**: Profile and optimize
- **Decision Tree**: Quick reference for choosing the right approach

### Reference Files
- **swiftui-api-reference.md**: View modifiers, containers, state management
- **design-systems.md**: Implementing color systems, typography scales, component libraries
- **anti-patterns-and-gotchas.md**: Code smells, design mistakes, performance gotchas

### Examples
- **starter-template.swift**: Complete app with tab navigation, loading states, empty states, cards, badges

## Design Philosophy

The skill is built on these core principles:

1. **Intentionality**: Every design choice must serve the purpose and aesthetic
2. **Bold Direction**: Pick an extreme (minimalist, maximalist, etc.) and execute thoroughly
3. **Production Quality**: Real working code, not placeholder examples
4. **Detail Focus**: Micro-interactions, spacing, typography matter enormously
5. **Accessibility**: WCAG 2.1 compliance, respect user preferences
6. **No Generic AI**: Avoid default blue buttons, purple gradients, cookie-cutter cards

## Technology Stack

- **Language**: Swift 5.9+
- **Primary UI**: SwiftUI
- **Secondary**: UIKit where beneficial
- **Architecture**: MVVM (default) or The Composable Architecture
- **State**: @State, @StateObject, @ObservedObject, @EnvironmentObject
- **Persistence**: SwiftData, Core Data, or File system
- **Package Manager**: Swift Package Manager

## Usage in Claude Code

The skill can be used in several ways:

1. **Direct Reference**: Invoke the skill when working on iOS/Swift apps
2. **Copy Patterns**: Use starter template as a foundation
3. **Lookup References**: Search references during implementation
4. **Checklist**: Use testing and performance checklists to validate work

## What This Skill Does NOT Do

- Generate AI-looking generic UIs
- Provide boilerplate without design intention
- Ignore accessibility or localization
- Override user preferences (motion, colors, text size)
- Use try/catch for control flow
- Create oversized, unmaintainable view hierarchies

## Performance & Quality

All code in this skill is:
- ✅ Production-ready
- ✅ Accessible (WCAG 2.1)
- ✅ Performant (profiled with Instruments)
- ✅ Tested on multiple devices
- ✅ Respecting user preferences (dark mode, motion, text size)
- ✅ Properly localized

## Contributing

To extend this skill:

1. Add new component examples to `examples/`
2. Document new patterns in appropriate `references/` file
3. Include working code with previews
4. Test for accessibility and performance
5. Keep SKILL.md core documentation up to date

## License

MIT

---

**Last Updated**: November 2025

For the latest SwiftUI patterns and best practices, see:
- [sosumi.ai](https://sosumi.ai/) - AI-readable Apple Developer documentation
- [Agent Rules - Swift & iOS Guidelines](https://github.com/steipete/agent-rules/tree/main/docs)

### Using sosumi.ai
Replace `developer.apple.com` with `sosumi.ai` in any Apple documentation URL to get Markdown:
```
https://sosumi.ai/documentation/swiftui
https://sosumi.ai/design/human-interface-guidelines
```
