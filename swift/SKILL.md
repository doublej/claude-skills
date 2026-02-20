---
name: swift
description: >
  Unified Swift/SwiftUI development skill. Use when:
  (1) generating SwiftUI feature modules with @Observable MVVM, or refactoring ObservableObject code;
  (2) building app architecture — data flow, networking, persistence, DI, or testing;
  (3) implementing iOS/iPadOS/macOS/watchOS/tvOS UI components with HIG compliance;
  (4) designing distinctive brand aesthetics — palette, motion, and haptics.
  Replaces swift-app-arch, swift-app-ui, swift-design, swiftui-codegen.
license: MIT
---

# Swift Development Skill

Four branches. Pick the right one, or combine.

## Which Branch?

| Task | Branch |
|------|--------|
| New feature module, @Observable codegen, refactor prompts | [Codegen](#codegen) |
| Architecture, networking, persistence, DI, testing | [Architecture](#architecture) |
| UI components, HIG, navigation, SF Symbols, accessibility | [UI](#ui) |
| Bold brand identity, palette, motion, haptics | [Design](#design) |

---

## Shared Non-Negotiables

### Accessibility
- 44×44pt touch targets minimum
- 4.5:1 contrast (body), 3:1 (large text 18pt+)
- `.accessibilityLabel` on every icon-only control
- Dynamic Type from `.xSmall` to `.accessibility5`
- Check `@Environment(\.accessibilityReduceMotion)` on every custom animation

### Never Ship
- Hardcoded colors (`Color(red:green:blue:)` or `Color.gray`) — use semantic Color assets
- Force-unwrap `!` except IBOutlets
- `try?` swallowing errors silently
- Business logic in views
- Network/disk I/O in views
- Secrets in UserDefaults

---

## Codegen

Generate complete `@Observable` MVVM features. Default to iOS 17+/macOS 14+. Fall back to `ObservableObject` only when explicitly needed.

### Feature Module Scaffold

```
Features/<Name>/
├── <Name>View.swift      — pure SwiftUI, @State model, @Bindable bindings
├── <Name>Model.swift     — @Observable @MainActor, orchestration + cancellation
├── <Name>Client.swift    — protocol + live implementation, async/await only
└── <Name>Tests.swift     — success, error, cancellation
```

### Prompt Header (prepend to every codegen task)

```
You are generating Swift 5.9+ SwiftUI code for a multi-platform app (iOS/iPadOS/macOS/tvOS).
Rules:
- @Observable + @Bindable (iOS 17+/macOS 14+)
- Never perform I/O in views — models orchestrate, clients execute
- Feature must include: View, Model, Client, Tests
- async/await only; tasks must be cancelable; use .task for view lifecycle
- SwiftLint-clean; no force-unwrap; views < 200 lines
Output: file-by-file code blocks labeled by filename.
```

### Canonical Model

```swift
@MainActor
@Observable
final class SearchModel {
    var query = ""
    var results: [SearchResult] = []
    var isLoading = false
    var errorMessage: String?

    private let client: any SearchClient
    private var searchTask: Task<Void, Never>?

    init(client: any SearchClient) { self.client = client }

    func search() {
        searchTask?.cancel()
        let q = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { results = []; return }
        searchTask = Task { [q] in
            isLoading = true
            defer { isLoading = false }
            do {
                let items = try await client.search(query: q)
                try Task.checkCancellation()
                results = items; errorMessage = nil
            } catch is CancellationError {
            } catch { results = []; errorMessage = error.localizedDescription }
        }
    }
}
```

### Refactor Prompt (ObservableObject → @Observable)

```
Refactor to template rules (iOS 17+/macOS 14+):
- Replace ObservableObject + @Published with @Observable
- Move all side effects out of view into a client protocol
- Use .task(id:) for view-driven async with cancellation
- Add accessibility labels and string catalog keys
Output: 1) plan ≤10 lines  2) file-by-file patches
```

### Definition of Done

- [ ] SwiftLint passes
- [ ] All UI strings use string catalog keys (`String(localized: "key")`)
- [ ] Accessibility labels on icon-only controls
- [ ] Tests cover success, error, and cancellation
- [ ] View-bound tasks cancel on disappear

### Concurrency Primitives

| Need | Use |
|------|-----|
| Single async result | `async/await` |
| View lifecycle | `.task` / `.task(id:)` — auto-cancels |
| Shared mutable state | `actor` |
| Dynamic parallelism | `withThrowingTaskGroup` |
| Combine bridge | `AsyncThrowingStream` |

See `references/codegen-patterns.md` for actor cache, task groups, Combine bridge, TCA shape, CI/CD, privacy manifest, SPM layout.

---

## Architecture

For app structure, networking, persistence, DI, and testing.

### Pattern Selection

| Pattern | Use when |
|---------|----------|
| `@Observable` MVVM | Default for new apps (iOS 17+) — see Codegen branch |
| TCA | Complex state, many effects, need time-travel debugging |
| Clean Architecture | Multiple front-ends, complex domain rules |

### DI Contract

Every injectable dependency must have a protocol. Live implementation + test mock as separate types. Never use singletons without a protocol.

```swift
protocol UserRepositoryProtocol {
    func fetch(id: UUID) async throws -> User
}
```

### Error Handling

```swift
// Domain errors
enum AppError: LocalizedError {
    case network(APIError)
    case validation(String)
    var errorDescription: String? { /* ... */ }
}
// Never use try/catch for control flow
```

See `references/architecture-patterns.md` for complete networking, persistence, TCA, testing, and project structure.

---

## UI

HIG-compliant SwiftUI components. Use when building interfaces, not defining brand.

### Navigation

| Pattern | Use when |
|---------|----------|
| Tab Bar | 3-5 equal sections, never hide on scroll |
| Hierarchical (`NavigationStack`) | Tree-structured drill-down |
| Modal | Self-contained focused task, clear dismiss affordance |

### SF Symbols

- All icons via SF Symbols — match weight to adjacent text
- Animate with `.symbolEffect()`
- Rendering modes: monochrome, hierarchical, palette, multicolor

### Key Modifiers

```swift
// Always prefer system semantics
.font(.headline)                         // Dynamic Type auto-scaling
.dynamicTypeSize(.small ... .xLarge)    // Constrain if needed
.background(.regularMaterial)           // Depth via material
.foregroundStyle(.primary)              // Semantic color
```

### State Skeleton Pattern

```swift
if let error { ErrorView(error: error) }
else if let items {
    items.isEmpty ? EmptyStateView() : List(items) { ItemRow($0) }
} else { SkeletonView() } // Never just ProgressView()
```

### System Materials

For translucent surfaces, prefer built-in materials (`.thinMaterial`, `.regularMaterial`, `.ultraThinMaterial`) so blur, contrast, and color adaptation stay platform-correct across OS releases.

See `references/ui-components.md` for design systems, component library, SwiftUI API reference, and anti-patterns.

---

## Design

For brand identity and visual distinction. Skip this branch for enterprise, system utilities, or accessibility-focused apps — use UI branch instead.

### Design Brief (output before any code)

```
DESIGN BRIEF
Feeling: [one word]
Material: [physical metaphor — metal, glass, paper, fabric]
Signature interaction: [gesture + response]
Aesthetic: [from table below]
Palette: background [hex], surface [hex], primary [hex], secondary [hex], accent [hex]
```

### Aesthetic by App Type

| App Type | Direction | Characteristics |
|----------|-----------|-----------------|
| Productivity/Tools | Industrial Precision | Grid-locked, monospace, cool grays, mechanical motion |
| Social/Communication | Soft Tech | Rounded, pastels with depth, bouncy springs (max 2/screen) |
| Finance/Health | Quiet Luxury | Generous whitespace, muted palette, slow deliberate motion |
| Games/Entertainment | Maximalist Joy | Dense, multi-color with intention, playful motion |
| Content/Media | Bold Editorial | Strong type hierarchy, asymmetric, snappy confident motion |

### Required on Every Screen

- Custom AccentColor asset (light + dark variants, never `.blue`)
- ≥2 font size variations; ≥2 font weight variations
- Non-default animation timing on each interactive element
- Haptics on primary actions

### Color System

```swift
// ALWAYS asset catalog, never inline
extension Color {
    static let appBackground = Color("Background")
    static let appSurface    = Color("Surface")
    static let appPrimary    = Color("Primary")
    static let appAccent     = Color("Accent")
}
// Dark mode = separate design, not inverted light
// Tint grays (add 0.02+ to one channel) — never Color.gray
```

### Motion Budget

| Moment | Timing |
|--------|--------|
| Primary action completion | Custom spring or easeOut, 0.3–0.5s |
| Micro-interactions | easeOut, 0.15–0.25s |
| Loading/skeleton | Linear, looping |

Max 2 bouncy springs per screen. No animation may block input. Always check `reduceMotion`.

### Haptic Vocabulary

| Action | Haptic |
|--------|--------|
| Primary tap | `.impact(.light)` |
| Selection change | `.selection()` |
| Success | `.notification(.success)` |
| Error | `.notification(.error)` |
| Boundary hit | `.impact(.rigid)` |

Do not vibrate on every tap.

### Typography

SF Pro required. Distinctive through weight contrast:
- Pair Ultralight/Light with Medium/Semibold (never all-Medium)
- SF Mono for numbers, codes, data displays
- Custom fonts for logo/wordmark only, must use `@ScaledMetric`

---

## Reference Files

- `references/codegen-patterns.md` — actor cache, task groups, Combine bridge, TCA, CI/CD, privacy manifest, SPM
- `references/architecture-patterns.md` — networking, APIClient, persistence, DI, TCA, testing, project structure
- `references/ui-components.md` — design systems, component library, SwiftUI API reference, anti-patterns, testing checklist

## Resources

- Apple docs (AI-readable): replace `developer.apple.com` with `sosumi.ai`
  - SwiftUI: `https://sosumi.ai/documentation/swiftui`
  - HIG: `https://sosumi.ai/design/human-interface-guidelines`
  - Concurrency: `https://sosumi.ai/documentation/swift/concurrency`
