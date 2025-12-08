# SwiftUI API Reference

Quick lookup for common SwiftUI patterns used in production interfaces.

## View Modifiers - Common Usage

### Layout
- `.frame(width:, height:)` - Fixed dimensions
- `.frame(maxWidth: .infinity)` - Expand horizontally
- `.frame(idealWidth:, maxWidth:)` - Flexible with constraints
- `.padding()` / `.padding(.horizontal, 20)` - Spacing
- `.spacing(12)` - In containers (VStack, HStack)

### Appearance
- `.background(Color)` / `.background(.ultraThinMaterial)` - Background
- `.foregroundColor(Color)` - Text/icon color
- `.cornerRadius(8)` / `.clipShape(RoundedRectangle(cornerRadius: 8))` - Rounding
- `.shadow(color:, radius:, x:, y:)` - Shadows
- `.opacity(0.5)` - Transparency

### Text
- `.font(.headline)` / `.font(.system(size: 16, weight: .semibold))`
- `.lineLimit(1)` / `.lineLimit(...)` - Truncation
- `.truncationMode(.tail)` - Where to truncate
- `.lineSpacing(4)` - Space between lines
- `.tracking(0.5)` - Letter spacing (kerning)

### Interaction
- `.onTapGesture { }` - Single tap
- `.onLongPressGesture { }` - Long press
- `.gesture(DragGesture())` - Complex gestures
- `.disabled(isDisabled)` - Enable/disable
- `.allowsHitTesting(false)` - Ignore taps

### State & Binding
- `.sheet(isPresented: $showModal)` - Modal
- `.fullScreenCover(isPresented:)` - Full screen modal
- `.alert("Title", isPresented:)` - Alert dialog
- `.onChange(of: value)` - React to state changes
- `.task { }` - Run async code on appear

### Animation
- `.animation(.spring(), value: animatingValue)` - Animate value changes
- `.transition(.scale)` - Entry/exit transition
- `.withAnimation { state = newValue }` - Animate state change

## Common View Containers

### Navigation
- `NavigationStack(path:)` - Modern navigation stack
- `NavigationView { } .navigationDestination(for:)` - Destination link (deprecated in iOS 16)
- `NavigationLink(value:)` - Link to destination
- `NavigationSplitView { } detail: { }` - Split view for iPad/macOS

### Lists & Collections
- `List { }` - Scrollable list
- `ScrollView { }` - Manual scrolling
- `LazyVStack(spacing:)` / `LazyHStack()` - Lazy rendering
- `Grid { }` - Grid layout (iOS 16+)
- `ForEach(items) { item in }` - Loop with identity

### Grouping
- `VStack(spacing:, alignment:)` - Vertical stack
- `HStack(spacing:, alignment:)` - Horizontal stack
- `ZStack(alignment:)` - Z-order stack
- `Group { }` - View grouping (no layout effect)
- `Section(header:) { }` - List sections

### Presentation
- `TabView(selection:)` - Tabs
- `Picker("Label", selection:)` - Picker (dropdown, segmented, wheel)
- `Form { }` - Form layout
- `Menu { }` - Context menu
- `.contextMenu(menuItems:)` - Long-press menu

## Environment Values

Access via `@Environment` property wrapper:

```swift
@Environment(\.colorScheme) var colorScheme
@Environment(\.dynamicTypeSize) var dynamicTypeSize
@Environment(\.accessibilityEnabled) var a11yEnabled
@Environment(\.reduceMotion) var reduceMotion
@Environment(\.layoutDirection) var layoutDirection
```

## State Management

### Property Wrappers
- `@State` - Local mutable state
- `@StateObject` - Object state (persist across recomputes)
- `@ObservedObject` - External observable object
- `@EnvironmentObject` - App-level shared state
- `@Binding` - Reference to external @State
- `@FocusState` - Keyboard focus
- `@AppStorage` - UserDefaults persistence

## Previews

```swift
#Preview {
  ContentView()
    .preferredColorScheme(.dark)
}

#Preview("Light Mode") {
  ContentView()
    .preferredColorScheme(.light)
}

#Preview("Large Text") {
  ContentView()
    .environment(\.dynamicTypeSize, .xLarge)
}
```

## Common Patterns

### Conditional View
```swift
if condition {
  TrueView()
} else {
  FalseView()
}
```

### Optional Unwrapping
```swift
if let value = optionalValue {
  Text(value)
}
```

### List with Loading State
```swift
List {
  if isLoading {
    ProgressView()
  } else {
    ForEach(items) { item in
      ItemRow(item)
    }
  }
}
```

### Sheet with Binding
```swift
@State var showSheet = false

var body: some View {
  Button("Show") { showSheet = true }
    .sheet(isPresented: $showSheet) {
      SheetContent()
        .presentationDetents([.medium, .large])
    }
}
```

## Performance Tips

- Decompose view bodies > 20 lines into separate views
- Use `.lazy` in large lists
- Cache expensive computations with `@State`
- Use `.id()` to force recomputation when needed
- Profile with Instruments (Core Animation, Debug View Hierarchy)
- Use `.redacted(reason: .placeholder)` for loading skeletons
