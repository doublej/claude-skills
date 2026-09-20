# Framework Architectural Patterns

Common patterns for popular frameworks. Reference these when generating documentation for detected frameworks.

## FastAPI (Python)

**Standard Structure:**
```
project/
├── app/
│   ├── main.py          # FastAPI app initialization
│   ├── routers/         # API route modules
│   ├── models/          # Pydantic/SQLAlchemy models
│   ├── services/        # Business logic
│   ├── dependencies.py  # Dependency injection
│   └── config.py        # Settings
├── tests/
└── requirements.txt
```

**Architectural Pattern:** Layered (routes → services → models)
**Key Concepts:** Dependency injection, Pydantic validation, async/await

## Next.js (React/TypeScript)

**App Router Structure:**
```
project/
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   ├── api/             # API routes
│   └── [dynamic]/       # Dynamic routes
├── components/
├── lib/                 # Utilities
└── public/
```

**Pages Router Structure:**
```
project/
├── pages/
│   ├── _app.tsx
│   ├── index.tsx
│   └── api/
├── components/
└── public/
```

**Architectural Pattern:** Server/client components, file-based routing
**Key Concepts:** RSC, data fetching patterns, middleware

## React (SPA)

**Standard Structure:**
```
src/
├── components/          # Reusable UI components
├── pages/              # Page-level components
├── hooks/              # Custom React hooks
├── contexts/           # Context providers
├── services/           # API clients
├── utils/              # Helper functions
└── App.tsx
```

**Architectural Pattern:** Component-based, unidirectional data flow
**Key Concepts:** Props, state, hooks, composition

## Django (Python)

**Standard Structure:**
```
project/
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py   # If Django REST
│   ├── urls.py
│   └── admin.py
├── templates/
└── manage.py
```

**Architectural Pattern:** MTV (Model-Template-View)
**Key Concepts:** ORM, migrations, middleware, apps

## Express.js (Node.js)

**Standard Structure:**
```
src/
├── routes/             # Route handlers
├── controllers/        # Business logic
├── models/            # Data models
├── middleware/        # Custom middleware
├── services/          # External service clients
├── config/            # Configuration
└── app.js
```

**Architectural Pattern:** MVC, middleware pipeline
**Key Concepts:** Middleware, routing, async error handling

## Go (Standard)

**Standard Structure:**
```
project/
├── cmd/
│   └── server/         # Application entrypoint
│       └── main.go
├── internal/
│   ├── handlers/       # HTTP handlers
│   ├── models/         # Data structures
│   ├── services/       # Business logic
│   └── middleware/
├── pkg/               # Public packages
└── go.mod
```

**Architectural Pattern:** Clean architecture, hexagonal
**Key Concepts:** Interfaces, dependency injection, error handling

## Rust (Actix Web)

**Standard Structure:**
```
src/
├── main.rs
├── handlers/          # Request handlers
├── models/            # Data structures
├── db/                # Database layer
├── middleware/
└── config.rs
```

**Architectural Pattern:** Modular, ownership-based
**Key Concepts:** Ownership, async, Result types

## Monorepo Patterns

**Turborepo/Nx Structure:**
```
monorepo/
├── apps/              # Applications
│   ├── web/
│   └── api/
├── packages/          # Shared libraries
│   ├── ui/
│   ├── config/
│   └── types/
└── turbo.json / nx.json
```

**Key Concepts:** Workspace dependencies, build caching, task orchestration

## General Patterns

### Layered Architecture
- **Presentation** → **Business Logic** → **Data Access**
- Common in: FastAPI, Django, Express, Spring

### Component-Based
- **Components** → **Props/State** → **Lifecycle**
- Common in: React, Vue, Svelte, SwiftUI

### Modular/Hexagonal
- **Ports** → **Adapters** → **Core Domain**
- Common in: Go, Rust, Java (Spring)

### MVC/MTV
- **Model** → **View** → **Controller/Template**
- Common in: Django, Rails, Laravel
