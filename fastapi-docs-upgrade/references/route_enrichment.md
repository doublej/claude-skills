# Route enrichment patterns

Per-route metadata catalog. Apply only what's missing.

## The full-fat decorator

```python
from fastapi import APIRouter, Body, Path, status
from .models import User, UserCreate, ErrorDetail
from .examples import USER_EXAMPLES

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    response_description="The newly created user, including server-assigned id and timestamps.",
    operation_id="create_user",
    responses={
        409: {
            "description": "A user with that email already exists.",
            "model": ErrorDetail,
            "content": {"application/json": {"example": {"detail": "email already registered", "code": "user.email_taken"}}},
        },
        422: {"description": "Validation failed. See `detail[]` for per-field reasons."},
    },
)
async def create_user(
    payload: UserCreate = Body(..., openapi_examples=USER_EXAMPLES),
) -> User:
    """
    Register a new user account.

    The email must be unique. Password is hashed with argon2id and never returned.

    **Side effects:**
    - Sends a verification email to the supplied address.
    - Emits a `user.created` event to the audit log.
    """
    ...
```

## Rules of thumb

- **Docstring > `description=` kwarg.** FastAPI uses the docstring as the description if no `description=` is passed. Prefer docstrings — they render the same and don't bloat decorator lines.
- **`summary` is the nav title.** Keep ≤60 chars, verb-phrase (`"List orders"`, not `"Orders endpoint"`).
- **`response_description`** describes the 200 body in one sentence. Default is `"Successful Response"` which is useless.
- **`responses={}`** documents non-200 outcomes. Always include 422 with a sentence even though FastAPI auto-adds the schema — the prose helps.
- **`operation_id`** is what SDK generators turn into method names. Use `snake_case_verb_noun`. Required if the project will be consumed by openapi-generator / Speakeasy / Fern.
- **`tags=[...]`** only needed when the route isn't on a router that already declares them.
- **`deprecated=True`** crosses the entry out in Swagger UI / ReDoc. Use it for sunsetted routes that still answer.
- **`include_in_schema=False`** hides internal/healthcheck routes from docs entirely.

## `openapi_examples` on Body/Query/Path

The dict-form gives a dropdown of named examples (Swagger UI 4.x+):

```python
USER_EXAMPLES = {
    "minimal": {
        "summary": "Minimum required fields",
        "description": "Just the fields needed for signup.",
        "value": {"email": "ada@lovelace.dev", "password": "horse-battery-staple-42"},
    },
    "with_profile": {
        "summary": "With optional profile",
        "value": {
            "email": "grace@hopper.dev",
            "password": "compiler-1952",
            "profile": {"display_name": "Grace Hopper", "locale": "en-US"},
        },
    },
    "edge_unicode": {
        "summary": "Unicode display name",
        "value": {"email": "user@日本.jp", "password": "...", "profile": {"display_name": "山田太郎"}},
    },
}
```

## Markdown that actually renders

Swagger UI, ReDoc, and Scalar all render CommonMark in `description`/docstrings/tag descriptions. Use:

- **Bold** for entity names (`**User**`, `**Order**`)
- `Code spans` for paths, fields, header names
- Bullet lists for outcomes / side effects / error conditions
- Fenced code blocks for example payloads inside long descriptions
- Tables for status-code matrices (renders in ReDoc + Scalar, partial in Swagger UI)

Avoid: raw HTML (inconsistent across UIs), heading levels above `###` (clash with auto-generated headers).
