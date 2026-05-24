"""Template — Scalar mount. Requires `pip install scalar-fastapi`.

Scalar is the primary UI: it claims `/docs` (FastAPI's default Swagger path).
The built-in Swagger UI is disabled via `docs_url=None` on FastAPI(...) and
re-mounted at `/swagger` (see mount_swagger.py).

Adds:
    GET /docs  →  Scalar API reference UI

Theming: pick one of default | alternate | moon | purple | solarized | bluePlanet |
saturn | kepler | mars | deepSpace | none. Layout: modern | classic.
"""

from scalar_fastapi import get_scalar_api_reference


@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        scalar_theme="purple",
        layout="modern",
        dark_mode=True,
        hide_models=False,
        hide_download_button=False,
        default_open_all_tags=False,
    )
