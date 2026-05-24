# Swagger UI + ReDoc tweaks

FastAPI exposes Swagger UI knobs via `swagger_ui_parameters=`. ReDoc has fewer first-class knobs — most ReDoc theming happens through the OpenAPI spec itself (`x-logo`, custom CSS via `redoc_ui_parameters` on a custom handler).

## Swagger UI parameters worth setting

```python
app = FastAPI(
    ...,
    swagger_ui_parameters={
        # Layout
        "docExpansion": "none",            # "list" (default) | "full" | "none"
        "defaultModelsExpandDepth": 1,     # -1 hides the schemas section entirely
        "defaultModelExpandDepth": 2,
        "displayRequestDuration": True,    # show ms after each Try-it response
        "filter": True,                    # search box above operations
        "deepLinking": True,
        "tryItOutEnabled": True,           # enable Try-it by default (no extra click)
        "persistAuthorization": True,      # remember Authorize between page loads
        "syntaxHighlight.theme": "obsidian",  # agate | arta | monokai | nord | obsidian | tomorrow-night
        "requestSnippetsEnabled": True,    # show curl/Node/etc snippets
        "showExtensions": True,            # show x-* fields
        "showCommonExtensions": True,
    },
)
```

## Injecting custom CSS into Swagger UI

`swagger_ui_parameters` doesn't expose a CSS hook directly. To inject CSS, override the Swagger UI HTML handler:

```python
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} — Swagger",
        swagger_favicon_url="/static/favicon.svg",
        swagger_ui_parameters=app.swagger_ui_parameters,
        # serve your overrides as a static file:
        swagger_css_url="/static/swagger_custom.css",
        # swagger_js_url defaults to the CDN bundle; override if you self-host
    )
```

Then disable the default `/docs` route by passing `docs_url=None` on the `FastAPI()` constructor.

A minimal `swagger_custom.css` (in `assets/swagger_custom.css`) is bundled with this skill — copy to `static/` of the project.

## ReDoc tweaks

FastAPI exposes nothing past `redoc_url`. To customize, replace the handler:

```python
from fastapi.openapi.docs import get_redoc_html

@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} — ReDoc",
        redoc_favicon_url="/static/favicon.svg",
        with_google_fonts=False,
    )
```

For real ReDoc theming (colors, fonts, logo, nav width), edit `x-tagGroups` and `x-logo` via the `custom_openapi` hook — see `assets/custom_openapi_hook.py`. Full theme object goes under `info.x-redocly` for ReDoc 2.x premium; the open-source build supports `x-logo` and `x-tagGroups`.
