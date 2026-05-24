# Pydantic v2 examples and field descriptions

Two layers: per-field `Field(examples=[...])` and whole-model `model_config = ConfigDict(json_schema_extra={"examples": [...]})`.

## Per-field

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class User(BaseModel):
    id: str = Field(..., description="Server-assigned ULID.", examples=["01HMQ8X3T4K5N7V9YB2D6F0J8R"])
    email: EmailStr = Field(..., description="Primary contact email. Unique per tenant.", examples=["ada@lovelace.dev"])
    display_name: str | None = Field(
        None,
        description="Optional human-friendly name shown in UIs.",
        examples=["Ada Lovelace"],
        max_length=80,
    )
    created_at: datetime = Field(..., description="UTC timestamp of account creation.", examples=["2026-05-24T12:34:56Z"])
    is_active: bool = Field(True, description="False after soft-delete or admin disable.")
```

## Whole-model examples

`json_schema_extra` controls what appears in the request/response body example panel:

```python
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="...", examples=["ada@lovelace.dev"])
    password: str = Field(..., min_length=12, description="Min 12 chars. Hashed with argon2id server-side.")
    display_name: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "ada@lovelace.dev",
                    "password": "horse-battery-staple-42",
                    "display_name": "Ada Lovelace",
                },
                {
                    "email": "grace@hopper.dev",
                    "password": "compiler-1952",
                },
            ]
        }
    )
```

Note: top-level `examples` (plural, list of dicts) — not `example` (singular, deprecated in OpenAPI 3.1+).

## Reusable example dicts

When the same model is used in multiple routes with different example fits, define examples next to the route, not on the model:

```python
# routes/users.py
USER_CREATE_EXAMPLES = {
    "consumer_signup": {
        "summary": "Consumer signup",
        "value": {"email": "user@example.com", "password": "..."},
    },
    "admin_bootstrap": {
        "summary": "Admin bootstrap (internal)",
        "value": {"email": "ops@company.dev", "password": "...", "display_name": "Ops Bootstrap"},
    },
}

@router.post("/users")
async def create(payload: UserCreate = Body(..., openapi_examples=USER_CREATE_EXAMPLES)): ...
```

## Picking realistic values

- IDs: ULIDs / UUIDs, not `"string"` or `"id_1"`
- Emails: notable historical figures' first names + `@example.dev` keeps it obviously fake but human-looking
- Timestamps: real-looking ISO-8601 with Z suffix
- Money: integers in minor units (`1299` = `$12.99`) if that's the schema; document the unit
- URLs: `https://example.com/...`, not `http://localhost`
- Enums: the enum value the field most often holds in practice

## Aliases and computed fields

If the model uses `populate_by_name=True` and aliases, set `by_alias=True` in `model_config` so examples render under the wire name (not the Python attr name):

```python
model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, json_schema_serialization_defaults_required=True)
```
