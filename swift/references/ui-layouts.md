# UI Layouts Reference

## Layout Protocol (iOS 16+)

Custom layout algorithm. Implement `sizeThatFits` and `placeSubviews`.

### Flow Layout (wrapping)

```swift
struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let maxWidth = proposal.width ?? .infinity
        var x: CGFloat = 0
        var y: CGFloat = 0
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > maxWidth, x > 0 {
                y += rowHeight + spacing
                x = 0
                rowHeight = 0
            }
            x += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
        return CGSize(width: maxWidth, height: y + rowHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x = bounds.minX
        var y = bounds.minY
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > bounds.maxX, x > bounds.minX {
                y += rowHeight + spacing
                x = bounds.minX
                rowHeight = 0
            }
            subview.place(at: CGPoint(x: x, y: y), proposal: .unspecified)
            x += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
    }
}

// Usage
FlowLayout(spacing: 8) {
    ForEach(tags) { tag in TagView(tag) }
}
```

### Radial Layout

```swift
struct RadialLayout: Layout {
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        proposal.replacingUnspecifiedDimensions()
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let radius = min(bounds.width, bounds.height) / 2 * 0.8
        let angle = Angle.degrees(360 / Double(subviews.count)).radians

        for (index, subview) in subviews.enumerated() {
            let x = bounds.midX + radius * cos(angle * Double(index) - .pi / 2)
            let y = bounds.midY + radius * sin(angle * Double(index) - .pi / 2)
            subview.place(at: CGPoint(x: x, y: y), anchor: .center, proposal: .unspecified)
        }
    }
}
```

### Layout with Cache (performance)

```swift
struct EqualWidthLayout: Layout {
    func makeCache(subviews: Subviews) -> CGFloat {
        subviews.map { $0.sizeThatFits(.unspecified).width }.max() ?? 0
    }

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout CGFloat) -> CGSize {
        let height = subviews.map { $0.sizeThatFits(.unspecified).height }.reduce(0, +)
        return CGSize(width: cache * CGFloat(subviews.count), height: height)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout CGFloat) {
        var x = bounds.minX
        for subview in subviews {
            subview.place(at: CGPoint(x: x, y: bounds.minY), proposal: ProposedViewSize(width: cache, height: bounds.height))
            x += cache
        }
    }
}
```

## Grid (iOS 16+)

Static grid — known rows at compile time (not lazy).

```swift
Grid(alignment: .leading, horizontalSpacing: 12, verticalSpacing: 8) {
    GridRow {
        Text("Name").gridColumnAlignment(.trailing)
        TextField("Name", text: $name)
    }
    GridRow {
        Text("Email")
        TextField("Email", text: $email)
    }
    Divider().gridCellColumns(2) // span columns
    GridRow {
        Color.clear.gridCellUnsizedAxes(.horizontal) // empty cell
        Button("Submit") { }
    }
}
```

## LazyVGrid / LazyHGrid

```swift
// Adaptive columns — auto-fill based on minimum width
let adaptive = [GridItem(.adaptive(minimum: 100, maximum: 200))]

// Fixed columns
let fixed = [GridItem(.fixed(120)), GridItem(.fixed(120))]

// Flexible — equal-width columns
let flexible = Array(repeating: GridItem(.flexible()), count: 3)

LazyVGrid(columns: adaptive, spacing: 16) {
    ForEach(items) { item in CardView(item: item) }
}
```

## ViewThatFits (iOS 16+)

Picks the first child that fits the available space.

```swift
ViewThatFits(in: .horizontal) {
    HStack { icon; title; subtitle; action } // wide
    HStack { icon; title; action }           // medium
    VStack { icon; title; action }           // narrow
}
```

## AnyLayout (iOS 16+)

Switch layout algorithm at runtime without losing state.

```swift
let layout = isCompact ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())
layout {
    Image(systemName: "star")
    Text("Favorites")
}
.animation(.default, value: isCompact)
```

## Custom Containers (iOS 18+)

`ForEach(subviewOf:)` — iterate over arbitrary child views in custom containers.

```swift
struct TagCloud<Content: View>: View {
    @ViewBuilder var content: Content

    var body: some View {
        FlowLayout(spacing: 8) {
            ForEach(subviewOf: content) { subview in
                subview
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(.quaternary, in: .capsule)
            }
        }
    }
}

// Usage
TagCloud {
    Text("Swift")
    Text("SwiftUI")
    Text("iOS")
    if showMore { Text("Xcode") }
}
```

### Sectioned Container

```swift
struct CardStack<Content: View>: View {
    @ViewBuilder var content: Content

    var body: some View {
        VStack(spacing: 12) {
            ForEach(sections: content) { section in
                VStack(alignment: .leading, spacing: 8) {
                    if !section.header.isEmpty {
                        section.header.font(.headline)
                    }
                    ForEach(subviewOf: section.content) { item in
                        item
                            .padding()
                            .background(.regularMaterial, in: .rect(cornerRadius: 12))
                    }
                }
            }
        }
    }
}
```

## ScrollView + ScrollPosition (iOS 18+)

Replaces `ScrollViewReader` for most use cases.

```swift
struct ScrollableList: View {
    @State private var position = ScrollPosition()

    var body: some View {
        ScrollView {
            LazyVStack {
                ForEach(items) { item in
                    ItemRow(item: item)
                }
            }
        }
        .scrollPosition($position)
        .onChange(of: position.viewID(type: Item.ID.self)) { _, id in
            // React to visible item change
        }

        // Programmatic scroll
        Button("Top") { position.scrollTo(edge: .top) }
        Button("Item") { position.scrollTo(id: targetItem.id) }
    }
}
```

### Scroll visibility

```swift
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
                .onScrollVisibilityChange(threshold: 0.5) { isVisible in
                    if isVisible { loadMoreIfNeeded(item) }
                }
        }
    }
}
```

### Scroll target behavior

```swift
// Paging
ScrollView(.horizontal) {
    LazyHStack(spacing: 16) {
        ForEach(pages) { page in PageView(page: page) }
    }
    .scrollTargetLayout()
}
.scrollTargetBehavior(.paging) // or .viewAligned

// Custom snap
.scrollTargetBehavior(.viewAligned(limitBehavior: .always))
```

## GeometryReader — Use Sparingly

```swift
// GOOD — measure once, pass value down via preference or @State
struct MeasuredContainer<Content: View>: View {
    @State private var size: CGSize = .zero
    @ViewBuilder var content: (CGSize) -> Content

    var body: some View {
        content(size)
            .background(GeometryReader { geo in
                Color.clear.onAppear { size = geo.size }
            })
    }
}

// BAD — GeometryReader inside scroll content (layout thrashing)
ScrollView {
    GeometryReader { ... } // Don't
}
```

## Preference Keys (child-to-parent communication)

```swift
struct HeightPreferenceKey: PreferenceKey {
    static var defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

// Child reports
ChildView()
    .background(GeometryReader { geo in
        Color.clear.preference(key: HeightPreferenceKey.self, value: geo.size.height)
    })

// Parent reads
.onPreferenceChange(HeightPreferenceKey.self) { height in
    containerHeight = height
}
```
