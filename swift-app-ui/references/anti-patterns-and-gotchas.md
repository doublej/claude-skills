# Anti-Patterns & Common Gotchas

Mistakes to avoid when building Swift UI.

## Code Smells

### ❌ Bloated View Bodies
Anything over 20 lines should be extracted.

```swift
// BAD
struct ContentView: View {
  @State private var items = []
  // ... 30 more lines of logic
  var body: some View {
    VStack {
      // 40 lines of view hierarchy
    }
  }
}

// GOOD
struct ContentView: View {
  @State private var items = []
  var body: some View {
    VStack {
      HeaderView()
      ItemListView(items: items)
      FooterView()
    }
  }
}

struct ItemListView: View {
  let items: [Item]
  var body: some View {
    // Focused implementation
  }
}
```

### ❌ Try/Catch for Control Flow
Never use exceptions for expected failures.

```swift
// BAD
do {
  let result = try someOperation()
  if let value = result {
    // handle
  }
} catch {
  // This is a control flow path, not an error!
}

// GOOD
let result = someOperation()
if let value = result {
  // handle
}

// GOOD - For actual errors
do {
  let data = try URLSession.shared.data(from: url)
} catch {
  print("Network error: \(error)")
}
```

### ❌ Ignoring `reduceMotion`
Always respect accessibility preferences.

```swift
// BAD
.animation(.easeInOut(duration: 0.5), value: isShown)

// GOOD
@Environment(\.reduceMotion) var reduceMotion
var animationDuration: Double { reduceMotion ? 0 : 0.5 }

.animation(.easeInOut(duration: animationDuration), value: isShown)

// OR - Use this modifier
extension View {
  func respectfulAnimation(_ animation: Animation, value: some Equatable) -> some View {
    @Environment(\.reduceMotion) var reduceMotion
    return self.animation(reduceMotion ? nil : animation, value: value)
  }
}
```

### ❌ Hardcoded Colors
Never hardcode colors—always use semantic assets.

```swift
// BAD
ZStack {
  Color(red: 0.2, green: 0.2, blue: 0.2)
  Text("Bad")
    .foregroundColor(Color(red: 1, green: 1, blue: 1))
}

// GOOD
ZStack {
  Color("BackgroundPrimary")
  Text("Good")
    .foregroundColor(Color("TextPrimary"))
}
```

### ❌ Missing Accessibility Labels
All interactive elements need labels.

```swift
// BAD
Button(action: { }) {
  Image(systemName: "plus")
}

// GOOD
Button(action: { }) {
  Image(systemName: "plus")
}
.accessibilityLabel("Add new item")
.accessibilityHint("Creates a new item in the list")
```

### ❌ Ignoring Dynamic Type
Never force fixed font sizes.

```swift
// BAD
Text("Title")
  .font(.system(size: 18)) // Fixed size
  .lineLimit(1)

// GOOD
Text("Title")
  .font(.headline) // Respects Dynamic Type
  .dynamicTypeSize(.small ... .xLarge) // Constrain if needed
  .lineLimit(1)
```

### ❌ No Loading/Empty/Error States
Always handle all data states.

```swift
// BAD
struct ListView: View {
  @State var items: [Item] = []
  var body: some View {
    List(items) { item in
      ItemRow(item)
    }
  }
}

// GOOD
struct ListView: View {
  @State var items: [Item]?
  @State var error: Error?

  var body: some View {
    if let error {
      ErrorView(error: error)
    } else if let items {
      if items.isEmpty {
        EmptyStateView()
      } else {
        List(items) { item in
          ItemRow(item)
        }
      }
    } else {
      ProgressView()
    }
  }
}
```

### ❌ Unnecessary State Objects
Don't create ObservableObjects for simple state.

```swift
// BAD
class FormModel: ObservableObject {
  @Published var name = ""
  @Published var email = ""
}

struct FormView: View {
  @StateObject var model = FormModel()
  // ...
}

// GOOD - If truly simple
struct FormView: View {
  @State private var name = ""
  @State private var email = ""
  // ...
}

// GOOD - Only if complex business logic
class FormModel: ObservableObject {
  @Published var name = ""
  @Published var email = ""

  var isValidEmail: Bool {
    // Complex validation logic
  }

  func submit() async {
    // Complex async operations
  }
}
```

### ❌ No Keyboard Dismissal
Forms without keyboard dismissal are annoying.

```swift
// BAD
TextField("Name", text: $name)

// GOOD
TextField("Name", text: $name)
  .submitLabel(.next)
  .onSubmit {
    // Move to next field or validate
  }

// GOOD - For final field
TextField("Email", text: $email)
  .submitLabel(.done)
  .onSubmit {
    hideKeyboard()
  }

// Helper
extension View {
  func hideKeyboard() {
    UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
  }
}
```

## Design Mistakes

### ❌ Generic Blue Buttons
Every app shouldn't look the same.

```swift
// BAD - Forgettable
Button("Save") { }
  .buttonStyle(.borderedProminent) // Default blue

// GOOD - Distinctive
Button(action: { }) {
  Label("Save", systemImage: "checkmark.circle.fill")
    .fontWeight(.semibold)
}
.frame(maxWidth: .infinity)
.frame(height: 44)
.background(Color("AccentColor"))
.foregroundColor(.white)
.cornerRadius(8)
.shadow(color: Color("AccentColor").opacity(0.3), radius: 4)
```

### ❌ Identical Rounded Cards Everywhere
Vary your layout strategies.

```swift
// BAD - Every list looks the same
List(items) { item in
  RoundedRectangle(cornerRadius: 12)
    .fill(Color(.systemGray6))
    .overlay(
      Text(item.name)
    )
}

// GOOD - Variety in presentation
List(items) { item in
  switch item.type {
  case .feature:
    FeatureCardView(item)
  case .alert:
    AlertBannerView(item)
  case .simple:
    SimpleRowView(item)
  }
}
```

### ❌ No Contrast Testing
Colors that look fine in light mode fail in dark mode.

```swift
// BAD - Untested
Color(red: 0.8, green: 0.8, blue: 0.8)

// GOOD - Test in both modes
Color("SemanticColor") // Defined with light/dark variants
// Test with Accessibility Inspector:
// Xcode → Xcode → Open Developer Tool → Accessibility Inspector
```

### ❌ Ignoring Safe Areas
Notches and Dynamic Island matter.

```swift
// BAD
ZStack {
  Image("Background")
    .ignoresSafeArea() // Too aggressive

  VStack {
    Text("Content")
  }
}

// GOOD
ZStack {
  Image("Background")
    .ignoresSafeArea(.container, edges: .bottom) // Precise

  VStack {
    Text("Content")
  }
  .ignoresSafeArea(.keyboard) // Allow keyboard
}
```

## Performance Gotchas

### ❌ Recomputing Everything on State Change
```swift
// BAD - Whole view recomputes
struct ParentView: View {
  @State var value = 0

  var body: some View {
    VStack {
      ExpensiveView() // Recomputes every state change!
      TextField("Input", value: $value)
    }
  }
}

// GOOD - Isolate state updates
struct ParentView: View {
  var body: some View {
    VStack {
      ExpensiveView()
      InputSection()
    }
  }
}

struct InputSection: View {
  @State var value = 0

  var body: some View {
    TextField("Input", value: $value)
  }
}
```

### ❌ No Image Caching
```swift
// BAD
AsyncImage(url: url) { image in
  image.resizable()
}

// GOOD
AsyncImage(url: url, transaction: Transaction(animation: .easeIn(duration: 0.2))) { phase in
  switch phase {
  case .success(let image):
    image
      .resizable()
      .scaledToFill()
  case .loading:
    ProgressView()
  case .empty:
    Image(systemName: "photo")
  @unknown default:
    EmptyView()
  }
}
```

### ❌ Large Lists Without `.lazy`
```swift
// BAD - Renders all 1000 items immediately
List(items) { item in
  ItemRow(item)
}

// GOOD - Renders only visible items
LazyVStack {
  ForEach(items) { item in
    ItemRow(item)
  }
}
```

## Testing Checklist

- [ ] Tested on light mode
- [ ] Tested on dark mode
- [ ] Tested with Dynamic Type (Small, Regular, xLarge)
- [ ] Tested with VoiceOver enabled
- [ ] Tested with `reduceMotion` enabled
- [ ] Tested on small device (iPhone SE)
- [ ] Tested on large device (iPhone 15 Pro Max)
- [ ] Tested on iPad (orientation changes)
- [ ] Network error state tested
- [ ] Empty state verified
- [ ] Loading state animated correctly
- [ ] Keyboard interaction works
- [ ] Memory profile is clean (Instruments)
- [ ] No hardcoded strings (localization ready)

## Quick Debug Tips

```swift
// Highlight all views to see hierarchy
.border(Color.red) // Add to any view

// Check view recomputation
print("Body computed for \(type(of: self))")

// Profile performance
struct ContentView: View {
  var body: some View {
    let _ = Self._printChanges()
    return VStack { /* ... */ }
  }
}

// Simulate slow network
@Environment(\.urlCache) var cache
// Use Instruments → Network → Network Conditions
```
