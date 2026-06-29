"""Template — Scalar mount. Requires `pip install scalar-fastapi`.

Scalar is the primary UI: it claims `/docs` (FastAPI's default Swagger path).
The built-in Swagger UI is disabled via `docs_url=None` on FastAPI(...) and
re-mounted at `/swagger` (see mount_swagger.py).

Adds:
    GET /docs  →  Scalar API reference UI

Theming: pick a `Theme` enum member (DEFAULT, ALTERNATE, MOON, PURPLE, SOLARIZED,
BLUE_PLANET, SATURN, KEPLER, MARS, DEEP_SPACE, LASERWAVE, NONE) and a `Layout` enum
member (MODERN, CLASSIC). scalar-fastapi v1.x requires enum instances here — plain
strings raise TypeError, and the kwarg is `theme=` (not `scalar_theme=`).
"""

from scalar_fastapi import Layout, Theme, get_scalar_api_reference


@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        theme=Theme.PURPLE,
        layout=Layout.MODERN,
        dark_mode=True,
        hide_models=False,
        hide_download_button=False,
        default_open_all_tags=False,
    )
