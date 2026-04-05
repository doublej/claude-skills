# UI Animations Reference

## PhaseAnimator (iOS 17+)

Cycles through phases continuously or on trigger.

### Continuous (looping)

```swift
PhaseAnimator([false, true]) { content, phase in
    content
        .scaleEffect(phase ? 1.1 : 1.0)
        .opacity(phase ? 0.8 : 1.0)
} animation: { phase in
    phase ? .easeInOut(duration: 1.0) : .easeInOut(duration: 0.8)
}
```

### Triggered

```swift
@State private var trigger = 0

Button("Shake") { trigger += 1 }
    .phaseAnimator([0, -10, 10, -5, 5, 0], trigger: trigger) { content, offset in
        content.offset(x: offset)
    } animation: { phase in
        switch phase {
        case -10, 10: .bouncy
        default: .smooth
        }
    }
```

## KeyframeAnimator (iOS 17+)

Precise multi-property keyframe control.

```swift
struct BounceValues {
    var scale: CGFloat = 1.0
    var yOffset: CGFloat = 0
    var rotation: Angle = .zero
}

@State private var trigger = 0

Button("Bounce") { trigger += 1 }
    .keyframeAnimator(initialValue: BounceValues(), trigger: trigger) { content, value in
        content
            .scaleEffect(value.scale)
            .offset(y: value.yOffset)
            .rotationEffect(value.rotation)
    } keyframes: { _ in
        KeyframeTrack(\.scale) {
            SpringKeyframe(1.3, duration: 0.15)
            SpringKeyframe(0.85, duration: 0.1)
            SpringKeyframe(1.0, duration: 0.2)
        }
        KeyframeTrack(\.yOffset) {
            LinearKeyframe(-30, duration: 0.15)
            SpringKeyframe(0, duration: 0.3, spring: .bouncy)
        }
        KeyframeTrack(\.rotation) {
            LinearKeyframe(.degrees(-5), duration: 0.1)
            LinearKeyframe(.degrees(5), duration: 0.1)
            LinearKeyframe(.zero, duration: 0.15)
        }
    }
```

### Keyframe Types

| Type | Behavior |
|------|----------|
| `LinearKeyframe` | Constant velocity interpolation |
| `SpringKeyframe` | Spring-driven, customizable |
| `CubicKeyframe` | Bezier curve timing |
| `MoveKeyframe` | Jump instantly (no interpolation) |

## Custom Transitions (iOS 17+)

```swift
struct BlurTransition: Transition {
    var radius: CGFloat = 10

    func body(content: Content, phase: TransitionPhase) -> some View {
        content
            .blur(radius: phase.isIdentity ? 0 : radius)
            .opacity(phase.isIdentity ? 1 : 0)
            .scaleEffect(phase == .willAppear ? 0.8 : phase == .didDisappear ? 1.1 : 1)
    }
}

// Usage
if showContent {
    ContentView()
        .transition(BlurTransition(radius: 15))
}
```

### TransitionPhase

| Phase | When |
|-------|------|
| `.willAppear` | View about to insert |
| `.identity` | Visible (resting state) |
| `.didDisappear` | View just removed |

### Combining

```swift
struct RotatingFadeTransition: Transition {
    func body(content: Content, phase: TransitionPhase) -> some View {
        content
            .opacity(phase.isIdentity ? 1.0 : 0.0)
            .rotationEffect(phase.rotation)
    }
}

extension TransitionPhase {
    fileprivate var rotation: Angle {
        switch self {
        case .willAppear: .degrees(30)
        case .identity: .zero
        case .didDisappear: .degrees(-30)
        }
    }
}
```

## matchedGeometryEffect (iOS 14+)

Hero transitions between views.

```swift
@Namespace private var heroNS
@State private var isExpanded = false

// Source
if !isExpanded {
    Image("photo")
        .matchedGeometryEffect(id: "hero", in: heroNS)
        .frame(width: 80, height: 80)
        .onTapGesture { withAnimation(.spring) { isExpanded = true } }
}

// Destination
if isExpanded {
    Image("photo")
        .matchedGeometryEffect(id: "hero", in: heroNS)
        .frame(maxWidth: .infinity, maxHeight: 300)
        .onTapGesture { withAnimation(.spring) { isExpanded = false } }
}
```

## Zoom Navigation Transition (iOS 18+)

Cinematic zoom between navigation source and destination.

```swift
@Namespace private var namespace

NavigationStack {
    ScrollView {
        LazyVGrid(columns: columns) {
            ForEach(items) { item in
                NavigationLink {
                    DetailView(item: item)
                        .navigationTransition(.zoom(sourceID: item.id, in: namespace))
                } label: {
                    CardView(item: item)
                        .matchedTransitionSource(id: item.id, in: namespace)
                }
            }
        }
    }
}
```

Also works with sheets:

```swift
.sheet(item: $selected) { item in
    DetailView(item: item)
        .navigationTransition(.zoom(sourceID: item.id, in: namespace))
}
```

## MeshGradient (iOS 18+)

2D grid of color control points with smooth interpolation.

### Static

```swift
MeshGradient(
    width: 3, height: 3,
    points: [
        [0, 0], [0.5, 0], [1, 0],
        [0, 0.5], [0.5, 0.5], [1, 0.5],
        [0, 1], [0.5, 1], [1, 1]
    ],
    colors: [
        .indigo, .cyan, .purple,
        .orange, .white, .blue,
        .yellow, .green, .mint
    ]
)
```

### Animated

```swift
@State private var animate = false

MeshGradient(
    width: 3, height: 3,
    points: [
        [0, 0], [0.5, 0], [1, 0],
        [0, 0.5], [animate ? 0.6 : 0.4, 0.5], [1, 0.5],
        [0, 1], [0.5, 1], [1, 1]
    ],
    colors: [.red, .orange, .yellow, .green, .blue, .purple, .pink, .mint, .cyan]
)
.onAppear {
    withAnimation(.easeInOut(duration: 3).repeatForever(autoreverses: true)) {
        animate = true
    }
}
```

## Canvas (iOS 15+)

Immediate-mode 2D drawing — high performance for many shapes.

```swift
Canvas { context, size in
    let rect = CGRect(origin: .zero, size: size)
    context.fill(Circle().path(in: rect), with: .color(.blue))

    let text = Text("Hello").font(.largeTitle)
    context.draw(text, at: CGPoint(x: size.width / 2, y: size.height / 2))

    if let resolved = context.resolveSymbol(id: "icon") {
        context.draw(resolved, at: CGPoint(x: 50, y: 50))
    }
} symbols: {
    Image(systemName: "star.fill").tag("icon")
}
```

### TimelineView + Canvas (continuous animation)

```swift
TimelineView(.animation) { timeline in
    Canvas { context, size in
        let t = timeline.date.timeIntervalSinceReferenceDate
        let x = (sin(t * 2) + 1) / 2 * size.width
        let rect = CGRect(x: x - 20, y: size.height / 2 - 20, width: 40, height: 40)
        context.fill(Circle().path(in: rect), with: .color(.red))
    }
}
```

## Gesture Patterns

### Drag with velocity

```swift
@State private var offset: CGSize = .zero
@State private var lastOffset: CGSize = .zero

Rectangle()
    .offset(offset)
    .gesture(
        DragGesture()
            .onChanged { value in
                offset = CGSize(
                    width: lastOffset.width + value.translation.width,
                    height: lastOffset.height + value.translation.height
                )
            }
            .onEnded { value in
                let predicted = value.predictedEndTranslation
                withAnimation(.spring(response: 0.4, dampingFraction: 0.7)) {
                    offset = CGSize(
                        width: lastOffset.width + predicted.width * 0.3,
                        height: lastOffset.height + predicted.height * 0.3
                    )
                }
                lastOffset = offset
            }
    )
```

### Pinch-to-zoom + rotate (simultaneous)

```swift
@State private var scale: CGFloat = 1.0
@State private var rotation: Angle = .zero
@GestureState private var gestureScale: CGFloat = 1.0
@GestureState private var gestureRotation: Angle = .zero

Image("photo")
    .scaleEffect(scale * gestureScale)
    .rotationEffect(rotation + gestureRotation)
    .gesture(
        MagnifyGesture()
            .updating($gestureScale) { value, state, _ in state = value.magnification }
            .onEnded { value in scale *= value.magnification }
            .simultaneously(with:
                RotateGesture()
                    .updating($gestureRotation) { value, state, _ in state = value.rotation }
                    .onEnded { value in rotation += value.rotation }
            )
    )
```

### Long press then drag (sequential)

```swift
@GestureState private var isDragging = false

Circle()
    .gesture(
        LongPressGesture(minimumDuration: 0.5)
            .sequenced(before: DragGesture())
            .updating($isDragging) { value, state, _ in
                if case .second(true, _) = value { state = true }
            }
    )
    .scaleEffect(isDragging ? 1.2 : 1.0)
    .animation(.spring, value: isDragging)
```

### Swipe-to-dismiss

```swift
@State private var offset: CGFloat = 0
@Environment(\.dismiss) private var dismiss

content
    .offset(y: offset)
    .gesture(
        DragGesture()
            .onChanged { value in
                if value.translation.height > 0 {
                    offset = value.translation.height
                }
            }
            .onEnded { value in
                if value.translation.height > 150 {
                    dismiss()
                } else {
                    withAnimation(.spring) { offset = 0 }
                }
            }
    )
```

## Spring Parameters

```swift
// Presets
.spring()       // default: response 0.5, dampingFraction 1.0
.bouncy         // response 0.5, dampingFraction 0.7
.smooth         // response 0.5, dampingFraction 1.0
.snappy         // response 0.3, dampingFraction 0.85

// Custom
.spring(response: 0.4, dampingFraction: 0.6, blendDuration: 0)
// response: duration feel (lower = faster)
// dampingFraction: 0 = infinite bounce, 1 = no bounce, >1 = overdamped
```

## SF Symbol Effects (iOS 17+)

```swift
Image(systemName: "wifi")
    .symbolEffect(.variableColor.iterative)       // animated color cycling
    .symbolEffect(.bounce, value: trigger)         // bounce on change
    .symbolEffect(.pulse)                          // continuous pulse
    .symbolEffect(.breathe)                        // continuous breathe (iOS 18+)
    .symbolEffect(.wiggle, value: trigger)         // wiggle on change (iOS 18+)
    .symbolEffect(.rotate, value: trigger)         // rotate on change (iOS 18+)
    .contentTransition(.symbolEffect(.replace))    // animated symbol swap
```

## iOS 26 Liquid Glass

Only adopt when explicitly requested. Always provide material fallback.

```swift
// Basic glass
Text("Title").glassEffect()

// Morphing between states
@Namespace private var ns

GlassEffectContainer {
    if isExpanded {
        ExpandedView().glassEffect().glassEffectID("card", in: ns)
    } else {
        CompactView().glassEffect().glassEffectID("card", in: ns)
    }
}
.animation(.smooth, value: isExpanded)

// Fallback
if #available(iOS 26, *) {
    content.glassEffect()
} else {
    content.background(.regularMaterial)
}
```
