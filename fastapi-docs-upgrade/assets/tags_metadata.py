"""Template — define a tags_metadata list and pass to FastAPI(openapi_tags=...).

One entry per tag actually used on routes. Order matters: Swagger UI / ReDoc / Scalar
render tags in this order (any untagged tags appear after, alphabetical).
"""

tags_metadata = [
    {
        "name": "auth",
        "description": (
            "Sign-in, sign-out, token refresh, OAuth2 flows.\n\n"
            "All routes here are **public** (no bearer token required). "
            "After a successful login the response sets a `Set-Cookie: session=…` and returns a JSON `{ access_token, refresh_token, expires_in }`."
        ),
        "externalDocs": {
            "description": "Auth architecture diagram",
            "url": "https://example.com/docs/auth",
        },
    },
    {
        "name": "users",
        "description": (
            "User CRUD, profile, preferences.\n\n"
            "Use **`GET /users/me`** for the current authenticated user. "
            "Admin-only routes are explicitly tagged `admin`."
        ),
    },
    {
        "name": "products",
        "description": (
            "Catalog browse, search, faceted filters.\n\n"
            "Read-only for unauthenticated callers. Mutations require the `catalog:write` scope."
        ),
    },
    {
        "name": "orders",
        "description": (
            "Cart lifecycle, checkout, post-purchase order management.\n\n"
            "Orders transition: `pending → paid → fulfilled → completed | refunded | cancelled`. "
            "See `GET /orders/{id}/events` for the audit log."
        ),
    },
    {
        "name": "webhooks",
        "description": (
            "Inbound webhooks from payment / shipping providers.\n\n"
            "Each provider has its own path and signature scheme — see the per-route docs."
        ),
    },
    {
        "name": "admin",
        "description": (
            "**Admin-only.** Requires the `admin` scope and a service account token.\n\n"
            "These routes are excluded from the public SDK and may change without semver guarantees."
        ),
    },
    {
        "name": "internal",
        "description": "Internal-only utility routes. Hidden from production docs.",
    },
]
