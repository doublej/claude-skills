# UI Components Reference

## Component Library

### Primary Button Style

```swift
struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline)
            .frame(maxWidth: .infinity)
            .frame(height: 44)
            .foregroundColor(.white)
            .background(Color("AccentColor"))
            .cornerRadius(8)
            .scaleEffect(configuration.isPressed ? 0.98 : 1)
            .opacity(configuration.isPressed ? 0.8 : 1)
            .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
    }
}
```

### Card Container

```swift
struct Card<Content: View>: View {
    @Environment(\.appTheme) private var theme
    private let content: Content
    init(@ViewBuilder content: () -> Content) { self.content = content() }
    var body: some View {
        content
            .padding(theme.horizontalPadding)
            .background(Color("CardBackground"))
            .cornerRadius(theme.cornerRadius)
            .shadow(color: Color("ShadowColor").opacity(0.08), radius: 8, x: 0, y: 2)
    }
}
```

### Loading Skeleton

```swift
struct SkeletonView: View {
    var body: some View {
        VStack(spacing: 12) {
            RoundedRectangle(cornerRadius: 8).fill(Color("SkeletonFill")).frame(height: 20)
            HStack {
                RoundedRectangle(cornerRadius: 4).fill(Color("SkeletonFill")).frame(height: 16)
                Spacer()
                RoundedRectangle(cornerRadius: 4).fill(Color("SkeletonFill")).frame(width: 60, height: 16)
            }
        }
        .shimmering()
    }
}

struct ShimmeringModifier: ViewModifier {
    @State private var phase = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    func body(content: Content) -> some View {
        content.overlay(
            Group {
                if !reduceMotion {
                    LinearGradient(
                        colors: [.clear, Color("SkeletonHighlight").opacity(0.3), .clear],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                    .offset(x: phase ? 400 : -400)
                }
            }
        )
        .onAppear {
            guard !reduceMotion else { return }
            withAnimation(.linear(duration: 1.5).repeatForever(autoreverses: false)) { phase = true }
        }
    }
}

extension View { func shimmering() -> some View { modifier(ShimmeringModifier()) } }
```

### Accessible Icon Button

```swift
Button(action: toggle) {
    Image(systemName: isFavorite ? "heart.fill" : "heart")
}
.frame(minWidth: 44, minHeight: 44)
.accessibilityLabel(isFavorite ? "Remove from favorites" : "Add to favorites")
.accessibilityHint("Toggles this item in your favorites list")
```

## Spacing System

```swift
enum Spacing {
    static let xs: CGFloat  = 4
    static let sm: CGFloat  = 8
    static let md: CGFloat  = 12
    static let lg: CGFloat  = 16
    static let xl: CGFloat  = 20
    static let xxl: CGFloat = 24
    static let xxxl: CGFloat = 32
}
```

## Color Hierarchy Template

```
Primary Background:    #FFFFFF (light) / #1A1A1A (dark)
Secondary Background:  #F5F5F5 (light) / #2D2D2D (dark)
Primary Text:          #000000 (light) / #FFFFFF (dark)
Secondary Text:        #666666 (light) / #CCCCCC (dark)
Accent:                Consistent across themes
```

## SwiftUI API Quick Reference

### Navigation
- `NavigationStack(path:)` — modern stack
- `NavigationSplitView` — split view (iPad/macOS)
- `NavigationLink(value:)` — data-driven link

### Common Modifiers
```swift
.frame(maxWidth: .infinity)
.clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
.background(.ultraThinMaterial)         // depth
.foregroundStyle(.primary)              // semantic color
.dynamicTypeSize(.small ... .xLarge)    // constrain DT
.symbolEffect(.bounce)                  // SF Symbol animation
```

### State
```swift
@State          // local mutable
@Observable     // iOS 17+ view model (Observation)
@Bindable       // bindings into @Observable (use in body)
@StateObject    // ObservableObject owner (legacy)
@ObservedObject // ObservableObject reference (legacy)
@Environment    // environment injection
@AppStorage     // UserDefaults persistence
```

### Previews
```swift
#Preview("Light") { ContentView().preferredColorScheme(.light) }
#Preview("Dark")  { ContentView().preferredColorScheme(.dark) }
#Preview("Large") { ContentView().environment(\.dynamicTypeSize, .xLarge) }
```

## Anti-Patterns & Gotchas

### State Management
```swift
// BAD — ObservableObject for simple state
class FormModel: ObservableObject { @Published var name = "" }

// GOOD — @State for simple, @Observable for complex
struct FormView: View {
    @State private var name = ""  // simple
}
```

### Performance
```swift
// BAD — whole view recomputes
struct ParentView: View {
    @State var value = 0
    var body: some View {
        VStack { ExpensiveView(); TextField("Value", value: $value, format: .number) }
    }
}

// GOOD — isolate state
struct ParentView: View {
    var body: some View { VStack { ExpensiveView(); InputSection() } }
}
struct InputSection: View {
    @State var value = 0
    var body: some View { TextField("Value", value: $value, format: .number) }
}
```

### Image Loading
```swift
// GOOD — handle all phases
AsyncImage(url: url, transaction: Transaction(animation: .easeIn(duration: 0.2))) { phase in
    switch phase {
    case .success(let image): image.resizable().scaledToFill()
    case .empty: ProgressView()
    case .failure: Image(systemName: "photo")
    @unknown default: EmptyView()
    }
}
```

### Motion
```swift
// ALWAYS check reduceMotion
@Environment(\.accessibilityReduceMotion) var reduceMotion

.animation(reduceMotion ? nil : .spring(response: 0.4), value: isExpanded)
```

### Safe Areas
```swift
// GOOD — precise, not aggressive
Image("Background")
    .ignoresSafeArea(.container, edges: .bottom)  // not .all
```

## Testing Checklist

- [ ] Light mode
- [ ] Dark mode
- [ ] Dynamic Type — Small, Regular, xLarge, accessibility5
- [ ] VoiceOver enabled
- [ ] Reduce Motion enabled
- [ ] iPhone SE (small)
- [ ] iPhone 15 Pro Max (large)
- [ ] iPad (orientation changes)
- [ ] Network error state
- [ ] Empty state
- [ ] Loading/skeleton state
- [ ] Keyboard interaction
- [ ] Memory profile clean (Instruments)
- [ ] No hardcoded strings

## Performance Debug

```swift
// See what's recomputing
let _ = Self._printChanges()

// Highlight view bounds
.border(Color.red)

// Profile: Xcode → Product → Profile (⌘I) → Core Animation
```
