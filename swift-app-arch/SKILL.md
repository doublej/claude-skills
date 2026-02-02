---
name: swift-app-arch
description: Production-grade Swift application architecture and patterns. Use when building app structure, data flow, networking, persistence, or implementing MVVM/TCA/Clean Architecture. Counterpart to swift-app-ui (which handles visual design).
license: MIT
---

# Swift App Architecture Skill

Production-grade Swift application architecture, patterns, and infrastructure.

## When to Use

- Structuring a new Swift app or module
- Implementing data flow (MVVM, TCA, Clean Architecture)
- Building networking layers with async/await
- Setting up persistence (SwiftData, Core Data, UserDefaults)
- Dependency injection and testability
- Error handling strategies

## Architecture Patterns

### MVVM (Model-View-ViewModel)

```swift
// Model
struct User: Codable, Identifiable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModel
@MainActor
final class UserViewModel: ObservableObject {
    @Published private(set) var user: User?
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol = UserRepository()) {
        self.repository = repository
    }

    func fetch(id: UUID) async {
        isLoading = true
        error = nil
        defer { isLoading = false }

        do {
            user = try await repository.fetch(id: id)
        } catch {
            self.error = error
        }
    }
}

// View consumes ViewModel via @StateObject or @ObservedObject
```

### TCA (The Composable Architecture)

When to use: Complex state, many side effects, need time-travel debugging.

```swift
@Reducer
struct UserFeature {
    @ObservableState
    struct State: Equatable {
        var user: User?
        var isLoading = false
    }

    enum Action {
        case fetchUser(UUID)
        case userResponse(Result<User, Error>)
    }

    @Dependency(\.userClient) var userClient

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .fetchUser(let id):
                state.isLoading = true
                return .run { send in
                    await send(.userResponse(Result { try await userClient.fetch(id) }))
                }
            case .userResponse(.success(let user)):
                state.isLoading = false
                state.user = user
                return .none
            case .userResponse(.failure):
                state.isLoading = false
                return .none
            }
        }
    }
}
```

### Clean Architecture Layers

```
┌─────────────────────────────────────┐
│  Presentation (Views, ViewModels)   │
├─────────────────────────────────────┤
│  Domain (Use Cases, Entities)       │
├─────────────────────────────────────┤
│  Data (Repositories, Data Sources)  │
└─────────────────────────────────────┘

Dependencies point inward only.
Domain has zero external dependencies.
```

## Networking

### Modern async/await Pattern

```swift
protocol APIClientProtocol {
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T
}

final class APIClient: APIClientProtocol {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
    }

    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let request = try endpoint.urlRequest()
        let (data, response) = try await session.data(for: request)

        guard let http = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        switch http.statusCode {
        case 200...299:
            return try decoder.decode(T.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        case 500...599:
            throw APIError.server(http.statusCode)
        default:
            throw APIError.unknown(http.statusCode)
        }
    }
}

enum APIError: LocalizedError {
    case invalidResponse
    case unauthorized
    case notFound
    case server(Int)
    case unknown(Int)

    var errorDescription: String? {
        switch self {
        case .invalidResponse: "Invalid response"
        case .unauthorized: "Session expired"
        case .notFound: "Not found"
        case .server(let code): "Server error (\(code))"
        case .unknown(let code): "Error (\(code))"
        }
    }
}
```

### Endpoint Definition

```swift
struct Endpoint {
    let path: String
    let method: HTTPMethod
    let headers: [String: String]
    let body: Data?

    enum HTTPMethod: String {
        case get = "GET"
        case post = "POST"
        case put = "PUT"
        case delete = "DELETE"
    }

    func urlRequest(baseURL: URL = API.baseURL) throws -> URLRequest {
        guard let url = URL(string: path, relativeTo: baseURL) else {
            throw APIError.invalidResponse
        }
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.httpBody = body
        headers.forEach { request.setValue($1, forHTTPHeaderField: $0) }
        return request
    }
}

extension Endpoint {
    static func user(id: UUID) -> Endpoint {
        Endpoint(path: "/users/\(id)", method: .get, headers: [:], body: nil)
    }
}
```

## Persistence

### SwiftData (iOS 17+)

```swift
@Model
final class Item {
    var title: String
    var timestamp: Date
    var isCompleted: Bool

    init(title: String, timestamp: Date = .now) {
        self.title = title
        self.timestamp = timestamp
        self.isCompleted = false
    }
}

// Container setup
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Item.self)
    }
}

// Usage in views
@Query(sort: \Item.timestamp, order: .reverse)
private var items: [Item]

@Environment(\.modelContext) private var context

func addItem() {
    let item = Item(title: "New")
    context.insert(item)
}
```

### Keychain for Secrets

```swift
final class KeychainManager {
    static let shared = KeychainManager()

    func save(_ data: Data, for key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        SecItemDelete(query as CFDictionary)
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }

    func load(for key: String) throws -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess else {
            if status == errSecItemNotFound { return nil }
            throw KeychainError.loadFailed(status)
        }
        return result as? Data
    }

    func delete(for key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        SecItemDelete(query as CFDictionary)
    }
}
```

## Dependency Injection

### Protocol-Based DI

```swift
// Protocol
protocol UserRepositoryProtocol {
    func fetch(id: UUID) async throws -> User
    func save(_ user: User) async throws
}

// Production implementation
final class UserRepository: UserRepositoryProtocol {
    private let api: APIClientProtocol
    private let cache: CacheProtocol

    init(api: APIClientProtocol = APIClient(), cache: CacheProtocol = Cache()) {
        self.api = api
        self.cache = cache
    }

    func fetch(id: UUID) async throws -> User {
        if let cached: User = cache.get(key: "user-\(id)") {
            return cached
        }
        let user: User = try await api.request(.user(id: id))
        cache.set(user, key: "user-\(id)")
        return user
    }
}

// Test mock
final class MockUserRepository: UserRepositoryProtocol {
    var stubbedUser: User?
    var fetchCallCount = 0

    func fetch(id: UUID) async throws -> User {
        fetchCallCount += 1
        guard let user = stubbedUser else { throw APIError.notFound }
        return user
    }
}
```

### Environment-Based DI (SwiftUI)

```swift
private struct APIClientKey: EnvironmentKey {
    static let defaultValue: APIClientProtocol = APIClient()
}

extension EnvironmentValues {
    var apiClient: APIClientProtocol {
        get { self[APIClientKey.self] }
        set { self[APIClientKey.self] = newValue }
    }
}

// Usage
struct MyView: View {
    @Environment(\.apiClient) var api
}

// Injection for tests
MyView()
    .environment(\.apiClient, MockAPIClient())
```

## Error Handling

### Result Type Pattern

```swift
enum AppError: LocalizedError {
    case network(APIError)
    case validation(String)
    case persistence(Error)

    var errorDescription: String? {
        switch self {
        case .network(let e): e.localizedDescription
        case .validation(let msg): msg
        case .persistence(let e): "Save failed: \(e.localizedDescription)"
        }
    }
}

// Typed throws (Swift 6)
func fetchUser() async throws(AppError) -> User {
    do {
        return try await api.request(.user(id: id))
    } catch let error as APIError {
        throw .network(error)
    } catch {
        throw .network(.unknown(0))
    }
}
```

### Never Use Try/Catch for Control Flow

```swift
// BAD
do {
    let user = try findUser(name)
    return user
} catch {
    return nil  // Exception as control flow
}

// GOOD
func findUser(_ name: String) -> User? {
    users.first { $0.name == name }
}
```

## Testing

### Unit Test Structure

```swift
@MainActor
final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockRepo: MockUserRepository!

    override func setUp() {
        mockRepo = MockUserRepository()
        sut = UserViewModel(repository: mockRepo)
    }

    func test_fetch_success_updatesUser() async {
        // Given
        let expected = User(id: UUID(), name: "Test", email: "test@example.com")
        mockRepo.stubbedUser = expected

        // When
        await sut.fetch(id: expected.id)

        // Then
        XCTAssertEqual(sut.user, expected)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.error)
    }

    func test_fetch_failure_setsError() async {
        // Given
        mockRepo.stubbedUser = nil

        // When
        await sut.fetch(id: UUID())

        // Then
        XCTAssertNil(sut.user)
        XCTAssertNotNil(sut.error)
    }
}
```

## Project Structure

```
MyApp/
├── App/
│   ├── MyApp.swift
│   └── AppDelegate.swift
├── Features/
│   ├── User/
│   │   ├── UserView.swift
│   │   ├── UserViewModel.swift
│   │   └── UserRepository.swift
│   └── Settings/
│       └── ...
├── Core/
│   ├── Networking/
│   │   ├── APIClient.swift
│   │   └── Endpoint.swift
│   ├── Persistence/
│   │   ├── SwiftData/
│   │   └── Keychain/
│   └── Extensions/
├── Models/
│   └── User.swift
└── Resources/
    └── Assets.xcassets
```

## Anti-Patterns

Never do:
- Singletons without protocols (untestable)
- Network calls in Views
- Business logic in ViewModels (use UseCases)
- Force unwrapping with `!` outside IBOutlets
- Storing secrets in UserDefaults
- `try?` swallowing errors silently
- Massive ViewModels (split by responsibility)
- Circular dependencies

## Resources

### AI-Readable Apple Documentation (via sosumi.ai)

- **Swift**: `https://sosumi.ai/documentation/swift`
- **Concurrency**: `https://sosumi.ai/documentation/swift/concurrency`
- **SwiftData**: `https://sosumi.ai/documentation/swiftdata`
- **Foundation**: `https://sosumi.ai/documentation/foundation`

Replace `developer.apple.com` with `sosumi.ai` for any Apple docs.

## Reference Files

See `references/` for additional patterns and examples.
