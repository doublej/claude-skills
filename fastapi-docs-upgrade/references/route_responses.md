# `responses={}` patterns

How to document non-200 outcomes per route. FastAPI merges these with the auto-generated 200 entry.

## The shape

```python
responses={
    <status_code_int>: {
        "description": "<one sentence>",
        "model": <PydanticErrorModel>,                  # optional but recommended
        "content": {                                      # optional — gives explicit example payload
            "application/json": {
                "example": {...},
                # or:
                "examples": {
                    "name_a": {"summary": "...", "value": {...}},
                    "name_b": {"summary": "...", "value": {...}},
                },
            }
        },
        "headers": {                                      # optional
            "X-RateLimit-Remaining": {
                "description": "Calls left in the current minute.",
                "schema": {"type": "integer", "example": 42},
            },
        },
    },
    ...
}
```

## Standard error model

Define once, reuse everywhere:

```python
from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    detail: str = Field(..., description="Human-readable failure reason.", examples=["resource not found"])
    code: str | None = Field(None, description="Stable machine-readable error code.", examples=["user.not_found"])
```

## Catalog by status code

```python
COMMON_ERRORS = {
    400: {"description": "Malformed request — missing or unparsable body/params.", "model": ErrorDetail},
    401: {"description": "Authentication required or token invalid/expired.", "model": ErrorDetail},
    403: {"description": "Authenticated but not permitted to perform this action.", "model": ErrorDetail},
    404: {"description": "The referenced resource does not exist.", "model": ErrorDetail},
    409: {"description": "State conflict — e.g. duplicate, version mismatch.", "model": ErrorDetail},
    422: {"description": "Validation failed. `detail[]` lists per-field reasons."},
    429: {"description": "Rate limit exceeded. Retry after the `Retry-After` header value."},
    500: {"description": "Unexpected server error. Correlation id in `X-Request-Id`."},
    503: {"description": "Upstream dependency degraded. Safe to retry with backoff."},
}
```

Then per-route:

```python
@router.get("/users/{user_id}", responses={**COMMON_ERRORS, 404: COMMON_ERRORS[404]})
```

Or just spread the subset you need:

```python
@router.get("/users/{user_id}", responses={k: COMMON_ERRORS[k] for k in (401, 403, 404)})
```

## App-level shared responses

For responses that should appear on every route, pass `responses=` on the router or include the catalog via dependency. Most projects just spread `COMMON_ERRORS` per route — clearer.
