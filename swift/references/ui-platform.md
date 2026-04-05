# UI Platform Features Reference

## WidgetKit

### Basic Timeline Widget

```swift
import WidgetKit
import SwiftUI

struct SimpleEntry: TimelineEntry {
    let date: Date
    let title: String
}

struct SimpleProvider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: .now, title: "Placeholder")
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        completion(SimpleEntry(date: .now, title: "Snapshot"))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        let entry = SimpleEntry(date: .now, title: "Live Data")
        let next = Calendar.current.date(byAdding: .minute, value: 15, to: .now)!
        completion(Timeline(entries: [entry], policy: .after(next)))
    }
}

struct SimpleWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "SimpleWidget", provider: SimpleProvider()) { entry in
            SimpleWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("My Widget")
        .supportedFamilies([.systemSmall, .systemMedium, .accessoryCircular])
    }
}
```

### Interactive Widget (iOS 17+)

```swift
import AppIntents

struct ToggleIntent: AppIntent {
    static var title: LocalizedStringResource = "Toggle Item"
    @Parameter(title: "Item ID") var itemID: String

    func perform() async throws -> some IntentResult {
        DataStore.shared.toggle(itemID)
        return .result()
    }
}

struct InteractiveWidgetView: View {
    var entry: SimpleEntry

    var body: some View {
        Button(intent: ToggleIntent(itemID: entry.itemID)) {
            Label("Toggle", systemImage: entry.isOn ? "checkmark.circle.fill" : "circle")
        }
    }
}
```

### Widget Families

| Family | Where | Size |
|--------|-------|------|
| `.systemSmall` | Home screen | ~169x169 |
| `.systemMedium` | Home screen | ~360x169 |
| `.systemLarge` | Home screen | ~360x376 |
| `.systemExtraLarge` | iPad home | ~715x376 |
| `.accessoryCircular` | Lock screen | Circular |
| `.accessoryRectangular` | Lock screen | Small rect |
| `.accessoryInline` | Lock screen inline | Single line |

### Control Center Widget (iOS 18+)

```swift
import WidgetKit

struct MyControl: ControlWidget {
    var body: some ControlWidgetConfiguration {
        StaticControlConfiguration(kind: "com.app.mycontrol") {
            ControlWidgetToggle("Flashlight", isOn: FlashlightBinding()) {
                Label("Flashlight", systemImage: "flashlight.on.fill")
            }
        }
        .displayName("Flashlight")
    }
}
```

## Live Activities (iOS 16.1+)

### Define Attributes

```swift
import ActivityKit

struct DeliveryAttributes: ActivityAttributes {
    struct ContentState: Codable, Hashable {
        var status: String
        var eta: Date
    }
    var orderNumber: String
}
```

### Start / Update / End

```swift
// Start
let attributes = DeliveryAttributes(orderNumber: "12345")
let state = DeliveryAttributes.ContentState(status: "In transit", eta: .now.addingTimeInterval(1800))
let content = ActivityContent(state: state, staleDate: .now.addingTimeInterval(900))
let activity = try Activity.request(attributes: attributes, content: content, pushType: .token)

// Update
let updated = DeliveryAttributes.ContentState(status: "Arriving", eta: .now.addingTimeInterval(300))
await activity.update(ActivityContent(state: updated, staleDate: nil))

// End
await activity.end(content, dismissalPolicy: .after(.now.addingTimeInterval(60)))
```

### Live Activity UI

```swift
struct DeliveryLiveActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: DeliveryAttributes.self) { context in
            // Lock screen / banner
            VStack {
                Text("Order \(context.attributes.orderNumber)")
                Text(context.state.status)
                Text(context.state.eta, style: .timer)
            }
            .padding()
        } dynamicIsland: { context in
            DynamicIsland {
                DynamicIslandExpandedRegion(.leading) {
                    Image(systemName: "box.truck")
                }
                DynamicIslandExpandedRegion(.trailing) {
                    Text(context.state.eta, style: .timer)
                }
                DynamicIslandExpandedRegion(.bottom) {
                    Text(context.state.status)
                }
            } compactLeading: {
                Image(systemName: "box.truck")
            } compactTrailing: {
                Text(context.state.eta, style: .timer)
            } minimal: {
                Image(systemName: "box.truck")
            }
        }
    }
}
```

## App Intents (iOS 16+)

### Basic Intent

```swift
import AppIntents

struct OpenItemIntent: AppIntent {
    static var title: LocalizedStringResource = "Open Item"
    static var description = IntentDescription("Opens a specific item")
    static var openAppWhenRun = true

    @Parameter(title: "Item")
    var item: ItemEntity

    func perform() async throws -> some IntentResult & ProvidesDialog {
        NavigationManager.shared.navigate(to: item)
        return .result(dialog: "Opening \(item.name)")
    }
}
```

### Entity

```swift
struct ItemEntity: AppEntity {
    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "Item")
    static var defaultQuery = ItemQuery()

    var id: String
    var name: String

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(name)")
    }
}

struct ItemQuery: EntityQuery {
    func entities(for identifiers: [String]) async throws -> [ItemEntity] {
        DataStore.shared.items(for: identifiers).map { ItemEntity(id: $0.id, name: $0.name) }
    }

    func suggestedEntities() async throws -> [ItemEntity] {
        DataStore.shared.recentItems().map { ItemEntity(id: $0.id, name: $0.name) }
    }
}
```

### App Shortcuts (Spotlight / Siri)

```swift
struct MyAppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: OpenItemIntent(),
            phrases: ["Open \(\.$item) in \(.applicationName)"],
            shortTitle: "Open Item",
            systemImageName: "doc"
        )
    }
}
```

## StoreKit 2 Views (iOS 17+)

```swift
import StoreKit

// Product store view
StoreView(ids: ["com.app.premium", "com.app.pro"]) { product in
    ProductIcon(product: product)
}

// Subscription store
SubscriptionStoreView(groupID: "com.app.subscriptions") {
    VStack {
        Text("Go Premium").font(.title.bold())
        Text("Unlock all features").foregroundStyle(.secondary)
    }
}
.subscriptionStoreButtonLabel(.multiline)
.subscriptionStorePickerItemBackground(.thinMaterial)

// Check entitlements
.subscriptionStatusTask(for: "com.app.subscriptions") { taskState in
    if let statuses = taskState.value {
        hasSubscription = statuses.contains { $0.state == .subscribed }
    }
}
```

## TipKit (iOS 17+)

```swift
import TipKit

struct FavoriteTip: Tip {
    var title: Text { Text("Save Favorites") }
    var message: Text? { Text("Tap the heart to save items.") }
    var image: Image? { Image(systemName: "heart") }

    @Parameter static var appOpens: Int = 0
    var rules: [Rule] {
        #Rule(Self.$appOpens) { $0 >= 3 }
    }
}

// Usage
struct ContentView: View {
    let tip = FavoriteTip()

    var body: some View {
        VStack {
            TipView(tip)                   // inline
            Button { }.popoverTip(tip)     // popover
        }
        .task { try? Tips.configure() }
    }
}

// Invalidate
FavoriteTip().invalidate(reason: .actionPerformed)
```

## Deep Linking

### Route-based Navigation

```swift
enum Route: Hashable {
    case home
    case detail(id: UUID)
    case settings
    case profile(username: String)
}

@Observable
class Router {
    var path = NavigationPath()

    func handle(url: URL) {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: false) else { return }
        let segments = components.path.split(separator: "/").map(String.init)

        switch segments.first {
        case "detail":
            if let id = segments.dropFirst().first.flatMap(UUID.init) {
                path.append(Route.detail(id: id))
            }
        case "settings":
            path.append(Route.settings)
        case "profile":
            if let name = segments.dropFirst().first {
                path.append(Route.profile(username: name))
            }
        default: break
        }
    }

    func reset() { path = NavigationPath() }
}
```

### App integration

```swift
NavigationStack(path: $router.path) {
    HomeView()
        .navigationDestination(for: Route.self) { route in
            switch route {
            case .home: HomeView()
            case .detail(let id): DetailView(id: id)
            case .settings: SettingsView()
            case .profile(let name): ProfileView(username: name)
            }
        }
}
.onOpenURL { url in router.handle(url: url) }
```

## Performance Profiling

### Debug recomputation

```swift
var body: some View {
    let _ = Self._printChanges() // prints which property triggered
    // ...
}
```

### Instruments workflow

1. Product → Profile (Cmd-I) → SwiftUI template
2. Look for: frequent body evaluations, long layout passes, excessive state changes
3. Core Animation template → offscreen rendering, blending

### Common Fixes

| Problem | Fix |
|---------|-----|
| Whole list recomputes | Extract row into separate view with own `@State` |
| Expensive view body | Add `equatable()` modifier |
| Complex overlapping views | `drawingGroup()` → single bitmap render |
| Scroll jank | `LazyVStack` with stable `id`, avoid `GeometryReader` in rows |
| Image loading stutter | `AsyncImage` with `transaction`, or cache with `actor` |
| Animation stutter | Move mutation to `.task`, use `withAnimation` on main |
| Memory growth in lists | Ensure `LazyVStack` (not `VStack`), check for retain cycles |

### State isolation pattern

```swift
// BAD — whole parent recomputes on input change
struct ParentView: View {
    @State var value = 0
    var body: some View {
        VStack { ExpensiveView(); TextField("Value", value: $value, format: .number) }
    }
}

// GOOD — input isolated in subview
struct ParentView: View {
    var body: some View { VStack { ExpensiveView(); InputSection() } }
}

struct InputSection: View {
    @State var value = 0
    var body: some View { TextField("Value", value: $value, format: .number) }
}
```
