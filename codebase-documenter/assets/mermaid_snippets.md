# Mermaid Diagram Snippets

Reusable Mermaid patterns for documentation. Copy and customize for specific projects.

## C4 Architecture Diagram

```mermaid
graph TB
    subgraph "System Context"
        User[User]
        System[Your System]
        External[External Service]
    end

    User -->|Uses| System
    System -->|Calls| External
```

## Layered Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        API[API Routes]
        UI[Web UI]
    end

    subgraph "Business Logic Layer"
        Service[Services]
        Validation[Validation]
    end

    subgraph "Data Layer"
        Models[Models]
        DB[(Database)]
    end

    API --> Service
    UI --> Service
    Service --> Validation
    Service --> Models
    Models --> DB
```

## Request/Response Sequence

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant DB

    Client->>API: POST /endpoint
    API->>Service: Process request
    Service->>DB: Query data
    DB-->>Service: Return results
    Service-->>API: Formatted response
    API-->>Client: 200 OK
```

## Component Dependency Graph

```mermaid
graph LR
    A[Frontend] -->|REST| B[Backend API]
    B -->|ORM| C[(Database)]
    B -->|HTTP| D[External API]
    A -->|WebSocket| E[Realtime Service]
    E -->|Pub/Sub| F[Message Queue]
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Processing: Start
    Processing --> Completed: Success
    Processing --> Failed: Error
    Failed --> Processing: Retry
    Completed --> [*]
    Failed --> [*]: Max retries
```

## Monorepo Structure

```mermaid
graph TB
    subgraph "Monorepo"
        subgraph "Apps"
            Web[Web App]
            API[API Server]
            Mobile[Mobile App]
        end

        subgraph "Packages"
            UI[UI Components]
            Utils[Utils]
            Types[Shared Types]
        end
    end

    Web --> UI
    Web --> Utils
    Web --> Types
    API --> Utils
    API --> Types
    Mobile --> UI
    Mobile --> Types
```

## Data Flow Pipeline

```mermaid
graph LR
    Input[Input Data] --> Validate[Validation]
    Validate --> Transform[Transformation]
    Transform --> Process[Processing]
    Process --> Store[(Storage)]
    Store --> Output[Output API]
```

## Microservices Architecture

```mermaid
graph TB
    Gateway[API Gateway]

    subgraph "Services"
        Auth[Auth Service]
        User[User Service]
        Order[Order Service]
    end

    subgraph "Databases"
        AuthDB[(Auth DB)]
        UserDB[(User DB)]
        OrderDB[(Order DB)]
    end

    Gateway --> Auth
    Gateway --> User
    Gateway --> Order

    Auth --> AuthDB
    User --> UserDB
    Order --> OrderDB

    Order -.->|gRPC| User
```

## Component Hierarchy (React/Frontend)

```mermaid
graph TB
    App[App]

    App --> Layout
    App --> Router

    Layout --> Header
    Layout --> Sidebar
    Layout --> Content

    Content --> Page1[Dashboard Page]
    Content --> Page2[Profile Page]

    Page1 --> Widget1[Chart Widget]
    Page1 --> Widget2[Stats Widget]
```

## Deployment Pipeline

```mermaid
graph LR
    Code[Code Push] --> Test[Run Tests]
    Test --> Build[Build]
    Build --> Stage[Deploy to Staging]
    Stage --> Approve{Manual Approval}
    Approve -->|Yes| Prod[Deploy to Production]
    Approve -->|No| Stop[Stop]
```

## Database Schema (ER Diagram)

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string email
        string name
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        int id PK
        int user_id FK
        datetime created_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
    }
    PRODUCT ||--o{ ORDER_ITEM : referenced
    PRODUCT {
        int id PK
        string name
        decimal price
    }
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Auth
    participant Resource

    User->>Frontend: Login
    Frontend->>Auth: POST /auth/login
    Auth-->>Frontend: JWT Token
    Frontend->>Frontend: Store token
    Frontend->>Resource: GET /api/data (with token)
    Resource->>Auth: Validate token
    Auth-->>Resource: Token valid
    Resource-->>Frontend: Protected data
    Frontend-->>User: Display data
```

## Branching Strategy

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    branch feature/new-feature
    checkout feature/new-feature
    commit
    commit
    checkout develop
    merge feature/new-feature
    checkout main
    merge develop tag: "v1.0.0"
```

## Usage Tips

1. **Choose the right diagram type:**
   - Architecture overview → C4 or component graph
   - API flow → Sequence diagram
   - State management → State diagram
   - Data models → ER diagram

2. **Keep it simple:**
   - Limit to 10-15 nodes per diagram
   - Use subgraphs for grouping
   - Avoid crossing arrows when possible

3. **Add context:**
   - Label all arrows with actions
   - Use descriptive node names
   - Add notes for complex interactions

4. **Customize for your stack:**
   - Replace generic names with actual service names
   - Update node types to match your tech
   - Add technology icons if supported
