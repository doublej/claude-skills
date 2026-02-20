# Codegen Patterns Reference

## Client Pattern

```swift
protocol SearchClient: Sendable {
    func search(query: String) async throws -> [SearchResult]
}

enum SearchClientError: Error {
    case invalidURL
}

struct LiveSearchClient: SearchClient {
    func search(query: String) async throws -> [SearchResult] {
        var components = URLComponents(string: "https://api.example.com/search")
        components?.queryItems = [URLQueryItem(name: "q", value: query)]
        guard let url = components?.url else {
            throw SearchClientError.invalidURL
        }
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode([SearchResult].self, from: data)
    }
}
```

## View Pattern

```swift
struct SearchView: View {
    @State private var model = SearchModel(client: LiveSearchClient())

    var body: some View {
        @Bindable var model = model
        VStack {
            TextField(String(localized: "search.placeholder"), text: $model.query)
                .accessibilityLabel(String(localized: "search.field.label"))
                .onSubmit { model.search() }
            if model.isLoading { ProgressView() }
            if let error = model.errorMessage { Text(error).foregroundStyle(.red) }
            List(model.results) { item in Text(item.title) }
        }
        .task(id: model.query) {
            model.search()
        }
    }
}
```

## Actor-Backed Cache

```swift
actor DataCache {
    private var storage: [URL: Data] = [:]
    func get(_ url: URL) -> Data? { storage[url] }
    func set(_ data: Data, for url: URL) { storage[url] = data }
}
```

## Task Group Fan-Out

```swift
func loadFeeds(urls: [URL], client: FeedClient) async throws -> [FeedItem] {
    try await withThrowingTaskGroup(of: [FeedItem].self) { group in
        for url in urls { group.addTask { try await client.fetch(url) } }
        var all: [FeedItem] = []
        for try await items in group { all.append(contentsOf: items) }
        return all
    }
}
```

## Combine → AsyncThrowingStream Bridge

```swift
func values<P: Publisher>(_ publisher: P) -> AsyncThrowingStream<P.Output, Error>
    where P.Failure == Error
{
    AsyncThrowingStream { continuation in
        let cancellable = publisher.sink(
            receiveCompletion: {
                switch $0 {
                case .finished: continuation.finish()
                case .failure(let e): continuation.finish(throwing: e)
                }
            },
            receiveValue: { continuation.yield($0) }
        )
        continuation.onTermination = { _ in cancellable.cancel() }
    }
}
```

## Minimal TCA Feature Shape

```swift
import ComposableArchitecture

@Reducer
struct CounterFeature {
    @ObservableState
    struct State: Equatable {
        var count = 0
        var isLoading = false
        var fact: String?
    }

    enum Action: Equatable {
        case incrementTapped, decrementTapped, factTapped
        case factResponse(String), factFailed(String)
    }

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .incrementTapped: state.count += 1; return .none
            case .decrementTapped: state.count -= 1; return .none
            case .factTapped:
                state.isLoading = true
                let n = state.count
                return .run { send in
                    await send(.factResponse("Fact about \(n)"))
                }
            case let .factResponse(text):
                state.isLoading = false; state.fact = text; return .none
            case let .factFailed(msg):
                state.isLoading = false; state.fact = "Failed: \(msg)"; return .none
            }
        }
    }
}
```

## SwiftLint Baseline (.swiftlint.yml)

```yaml
disabled_rules: [trailing_whitespace, todo]
opt_in_rules: [explicit_init, force_unwrapping, sorted_imports]
analyzer_rules: [unused_import]
line_length: { warning: 120, error: 160 }
function_body_length: { warning: 60, error: 120 }
excluded: [DerivedData, .build, "**/Generated/**"]
```

## GitHub Actions CI

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
jobs:
  build-and-test:
    runs-on: macos-latest
    strategy:
      matrix:
        destination: ["platform=iOS Simulator,name=iPhone 15", "platform=macOS"]
    steps:
      - uses: actions/checkout@v4
      - run: brew install swiftlint && swiftlint --strict
      - run: |
          xcodebuild test \
            -project MyApp.xcodeproj -scheme MyApp \
            -destination "${{ matrix.destination }}" \
            -enableCodeCoverage YES | xcpretty
```

## Privacy Manifest (PrivacyInfo.xcprivacy)

Required for App Store submission since May 2024.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>NSPrivacyAccessedAPITypes</key>
  <array>
    <dict>
      <key>NSPrivacyAccessedAPIType</key>
      <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
      <key>NSPrivacyAccessedAPITypeReasons</key>
      <array><string>CA92.1</string></array>
    </dict>
  </array>
</dict>
</plist>
```

## SPM Module Layout

```
App/                    # Xcode app target
Packages/
  AppCore/              # Shared: foundation, DI, utilities
  Features/
    Search/Sources/     # Feature target
    Settings/Sources/
  Clients/
    NetworkClient/      # Injectable abstraction
    AnalyticsClient/
```

## Custom Environment / Design Tokens

```swift
struct AppTheme: Sendable {
    var cornerRadius: CGFloat = 12
    var verticalPadding: CGFloat = 12
    var horizontalPadding: CGFloat = 16
}

private struct AppThemeKey: EnvironmentKey {
    static let defaultValue = AppTheme()
}

extension EnvironmentValues {
    var appTheme: AppTheme {
        get { self[AppThemeKey.self] }
        set { self[AppThemeKey.self] = newValue }
    }
}
```
