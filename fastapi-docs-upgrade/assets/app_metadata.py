"""Template — paste into the file that creates the FastAPI app.

Replace placeholders. Delete fields the project doesn't have (e.g. no license = drop license_info).
"""

from fastapi import FastAPI

from .tags_metadata import tags_metadata  # see assets/tags_metadata.py


DESCRIPTION = """\
# {Project Name}

{One-paragraph elevator pitch. Markdown renders in Swagger UI, ReDoc, and Scalar.}

## Quick start

```bash
curl -H "Authorization: Bearer $TOKEN" {BASE_URL}/users/me
```

## Conventions

- All timestamps are **UTC ISO-8601** (`2026-05-24T12:34:56Z`).
- IDs are **ULIDs** unless noted.
- Errors follow the standard `{ "detail": str, "code": str | null }` shape (see the **Errors** tag).
- Pagination uses `?cursor=…&limit=…`, never page numbers.

## Authentication

Bearer tokens via the `Authorization` header. See the **Auth** tag for the OAuth2 flow.
"""


app = FastAPI(
    title="{Project Name} API",
    summary="{One-liner under 300 chars — appears in nav and OpenAPI info.}",
    description=DESCRIPTION,
    version="{0.1.0}",
    terms_of_service="https://{example.com}/terms",
    contact={
        "name": "{Project Name} support",
        "url": "https://{example.com}/support",
        "email": "{api@example.com}",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    servers=[
        {"url": "https://api.{example.com}", "description": "Production"},
        {"url": "https://staging.api.{example.com}", "description": "Staging"},
        {"url": "http://localhost:8000", "description": "Local dev"},
    ],
    openapi_tags=tags_metadata,
    # Scalar takes over /docs (see assets/mount_scalar.py).
    # Built-in Swagger UI is disabled here and re-mounted at /swagger (see assets/mount_swagger.py).
    docs_url=None,
    # swagger_ui_parameters is unused when docs_url=None — the same dict is passed
    # to get_swagger_ui_html() in mount_swagger.py instead.
)
