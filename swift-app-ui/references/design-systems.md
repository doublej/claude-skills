# Design Systems & Brand Implementation

Guidelines for establishing coherent design systems in Swift apps.

## Semantic Color System

Define colors in the asset catalog, never hardcode:

```swift
// In Assets.xcassets, create Color Sets with Light/Dark variants

// Usage in code
Color("BackgroundPrimary")
Color("TextPrimary")
Color("TextSecondary")
Color("AccentColor")
Color("BorderLight")
```

### Color Hierarchy Example
```
Primary Background: #FFFFFF (light) / #1A1A1A (dark)
Secondary Background: #F5F5F5 (light) / #2D2D2D (dark)
Tertiary Background: #EBEBEB (light) / #3F3F3F (dark)

Primary Text: #000000 (light) / #FFFFFF (dark)
Secondary Text: #666666 (light) / #CCCCCC (dark)
Tertiary Text: #999999 (light) / #999999 (dark)

Accent: Consistent across themes
```

### Contrast Validation
- Text on background: minimum 4.5:1 (WCAG AA)
- Large text (18pt+): minimum 3:1
- Non-text contrast: minimum 3:1
- Interactive controls: minimum 44pt touch target

## Typography System

### Define a Type Scale
```swift
// Create a custom modifier
struct AppFont {
  static let display1 = Font.system(size: 32, weight: .bold, design: .default)
  static let display2 = Font.system(size: 28, weight: .semibold, design: .default)
  static let headline = Font.system(size: 18, weight: .semibold, design: .default)
  static let subheadline = Font.system(size: 16, weight: .semibold, design: .default)
  static let body = Font.system(size: 16, weight: .regular, design: .default)
  static let caption = Font.system(size: 14, weight: .regular, design: .default)
  static let micro = Font.system(size: 12, weight: .regular, design: .default)
}

// Usage
Text("Title")
  .font(AppFont.headline)
  .lineHeight(1.4)
  .tracking(0.3)
```

### Dynamic Type Support
```swift
Text("Adaptive Text")
  .font(.headline)
  .dynamicTypeSize(.small ... .xLarge)
```

### Custom Font Integration
```swift
// Register custom fonts in Info.plist or:
extension Font {
  static func customDisplay() -> Font {
    .custom("CustomFont-Bold", size: 32)
  }
}
```

## Spacing System

Establish a consistent spacing scale:

```swift
enum Spacing {
  static let xs = 4.0
  static let sm = 8.0
  static let md = 12.0
  static let lg = 16.0
  static let xl = 20.0
  static let xxl = 24.0
  static let xxxl = 32.0
}

// Usage
VStack(spacing: Spacing.md) {
  // content
}
.padding(.vertical, Spacing.lg)
```

## Component Library

Create reusable styled components:

### Button Style
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
  }
}

// Usage
Button("Save") { }
  .buttonStyle(PrimaryButtonStyle())
```

### Card Container
```swift
struct CardView<Content: View>: View {
  @ViewBuilder let content: Content
  var backgroundColor: Color = Color("CardBackground")

  var body: some View {
    content
      .padding(16)
      .background(backgroundColor)
      .cornerRadius(12)
      .shadow(color: Color.black.opacity(0.1), radius: 8, x: 0, y: 2)
  }
}

// Usage
CardView {
  VStack(alignment: .leading) {
    Text("Title")
  }
}
```

### Badge
```swift
struct BadgeView: View {
  let text: String
  var color: Color = Color("AccentColor")

  var body: some View {
    Text(text)
      .font(.caption)
      .fontWeight(.semibold)
      .foregroundColor(.white)
      .padding(.horizontal, 8)
      .padding(.vertical, 4)
      .background(color)
      .cornerRadius(4)
  }
}
```

### Loading Skeleton
```swift
struct SkeletonView: View {
  var body: some View {
    VStack(spacing: 12) {
      RoundedRectangle(cornerRadius: 8)
        .fill(Color.gray.opacity(0.2))
        .frame(height: 20)

      HStack {
        RoundedRectangle(cornerRadius: 4)
          .fill(Color.gray.opacity(0.2))
          .frame(height: 16)

        Spacer()

        RoundedRectangle(cornerRadius: 4)
          .fill(Color.gray.opacity(0.2))
          .frame(width: 60, height: 16)
      }
    }
    .shimmering()
  }
}

extension View {
  func shimmering() -> some View {
    modifier(ShimmeringModifier())
  }
}

struct ShimmeringModifier: ViewModifier {
  @State private var isShimmering = false

  func body(content: Content) -> some View {
    ZStack {
      content
        .opacity(isShimmering ? 0.6 : 1)

      LinearGradient(
        gradient: Gradient(colors: [.clear, .white.opacity(0.3), .clear]),
        startPoint: .topLeading,
        endPoint: .bottomTrailing
      )
      .offset(x: isShimmering ? 400 : -400)
    }
    .onAppear {
      withAnimation(.linear(duration: 1.5).repeatForever(autoreverses: false)) {
        isShimmering = true
      }
    }
  }
}
```

## Dark Mode Support

Test and support both light and dark modes:

```swift
struct ContentView: View {
  @Environment(\.colorScheme) var colorScheme

  var body: some View {
    ZStack {
      Color("BackgroundPrimary")
        .ignoresSafeArea()

      // Content adapts automatically
      Text("Hello")
        .foregroundColor(Color("TextPrimary"))
    }
  }
}

// In previews
#Preview("Light") {
  ContentView()
    .preferredColorScheme(.light)
}

#Preview("Dark") {
  ContentView()
    .preferredColorScheme(.dark)
}
```

## Accessibility Best Practices

### WCAG 2.1 Compliance Checklist
- [ ] Color not sole means of conveying information
- [ ] Text contrast minimum 4.5:1 (normal text)
- [ ] Text contrast minimum 3:1 (large text)
- [ ] Interactive elements minimum 44x44pt
- [ ] All images have `.accessibilityLabel()`
- [ ] Form inputs have `.accessibilityLabel()` and `.accessibilityHint()`
- [ ] Motion respects `reduceMotion` setting
- [ ] Supports Dynamic Type from `.xSmall` to `.xLarge`
- [ ] Keyboard navigation works (Tab key)
- [ ] VoiceOver labels are concise and descriptive

### Implementation
```swift
struct AccessibleButton: View {
  let title: String
  let action: () -> Void

  var body: some View {
    Button(action: action) {
      Image(systemName: "checkmark.circle.fill")
      Text(title)
    }
    .frame(minHeight: 44) // Touch target
    .accessibilityLabel(title)
    .accessibilityHint("Completes your action")
  }
}
```

## Localization & RTL

```swift
// In strings file:
"app.title" = "My App"
"app.description" = "An elegant interface"

// In code:
Text("app.title", bundle: .main)

// Automatic RTL support:
HStack {
  Image(systemName: "chevron.right")
  Text("Next")
}
// Mirrors automatically in RTL languages
```

## Performance Profiling

Use Instruments to verify:

1. **Core Animation**: Should be green (60 fps)
2. **System Trace**: Check for main thread blocking
3. **Memory**: Stable without growth
4. **Heat**: Reasonable CPU usage
5. **Energy**: Efficient power usage (battery impact)

Commands:
```bash
# Profile with Instruments from Xcode
# Product → Profile (⌘I)

# Or use command line
instruments -s devices
instruments -t "Core Animation" -D ~/output.trace
```
