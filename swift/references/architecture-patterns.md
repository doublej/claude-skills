# Architecture Patterns Reference

## Networking

### APIClient

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
        guard let http = response as? HTTPURLResponse else { throw APIError.invalidResponse }
        switch http.statusCode {
        case 200...299: return try decoder.decode(T.self, from: data)
        case 401: throw APIError.unauthorized
        case 404: throw APIError.notFound
        case 500...599: throw APIError.server(http.statusCode)
        default: throw APIError.unknown(http.statusCode)
        }
    }
}

enum APIError: LocalizedError {
    case invalidResponse, unauthorized, notFound, server(Int), unknown(Int)
    var errorDescription: String? {
        switch self {
        case .invalidResponse: "Invalid response"
        case .unauthorized: "Session expired"
        case .notFound: "Not found"
        case .server(let c): "Server error (\(c))"
        case .unknown(let c): "Error (\(c))"
        }
    }
}
```

### Endpoint

```swift
struct Endpoint {
    let path: String
    let method: HTTPMethod
    let headers: [String: String]
    let body: Data?

    enum HTTPMethod: String { case get = "GET", post = "POST", put = "PUT", delete = "DELETE" }

    func urlRequest(baseURL: URL = API.baseURL) throws -> URLRequest {
        guard let url = URL(string: path, relativeTo: baseURL) else { throw APIError.invalidResponse }
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
        self.title = title; self.timestamp = timestamp; self.isCompleted = false
    }
}

// App entry
@main struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: Item.self)
    }
}

// Usage
@Query(sort: \Item.timestamp, order: .reverse) private var items: [Item]
@Environment(\.modelContext) private var context
func addItem() { context.insert(Item(title: "New")) }
```

### Keychain for Secrets

```swift
protocol KeychainStoreProtocol {
    func save(_ data: Data, for key: String) throws
    func load(for key: String) throws -> Data?
}

enum KeychainError: Error {
    case saveFailed
    case loadFailed
}

struct KeychainStore: KeychainStoreProtocol {

    func save(_ data: Data, for key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        SecItemDelete(query as CFDictionary)
        guard SecItemAdd(query as CFDictionary, nil) == errSecSuccess else {
            throw KeychainError.saveFailed
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
            throw KeychainError.loadFailed
        }
        return result as? Data
    }
}

// Dependency injection
final class AuthTokenRepository {
    private let keychain: KeychainStoreProtocol

    init(keychain: KeychainStoreProtocol = KeychainStore()) {
        self.keychain = keychain
    }
}
```

## Dependency Injection

### Protocol-Based

```swift
final class UserRepository: UserRepositoryProtocol {
    private let api: APIClientProtocol

    init(api: APIClientProtocol = APIClient()) { self.api = api }

    func fetch(id: UUID) async throws -> User {
        try await api.request(.user(id: id))
    }
}

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

### Environment-Based (SwiftUI)

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
// Test injection
MyView().environment(\.apiClient, MockAPIClient())
```

## Error Handling

```swift
enum AppError: LocalizedError {
    case network(APIError), validation(String), persistence(Error)
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
    do { return try await api.request(.user(id: id)) }
    catch let error as APIError { throw .network(error) }
    catch { throw .network(.unknown(0)) }
}
```

## Testing

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
        let expected = User(id: UUID(), name: "Test", email: "test@example.com")
        mockRepo.stubbedUser = expected
        await sut.fetch(id: expected.id)
        XCTAssertEqual(sut.user, expected)
        XCTAssertFalse(sut.isLoading)
    }

    func test_fetch_failure_setsError() async {
        mockRepo.stubbedUser = nil
        await sut.fetch(id: UUID())
        XCTAssertNil(sut.user)
        XCTAssertNotNil(sut.error)
    }
}
```

### Swift Testing (optional, newer)

```swift
import Testing

@Suite("CounterModel")
struct CounterModelTests {
    @Test func incrementAndDecrement() async {
        let model = CounterModel(client: LiveNumberFactClient())
        #expect(model.count == 0)
        model.increment()
        #expect(model.count == 1)
    }
}
```

## Project Structure

```
MyApp/
├── App/
│   └── MyApp.swift
├── Features/
│   ├── User/
│   │   ├── UserView.swift
│   │   ├── UserModel.swift          # @Observable (iOS 17+) or ViewModel
│   │   └── UserClient.swift
│   └── Settings/
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
