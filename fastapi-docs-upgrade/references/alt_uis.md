# Alt UIs: Scalar (primary), Swagger, RapiDoc, Stoplight Elements

All UIs feed off the same `/openapi.json` FastAPI already serves.

**Default:** mount only Scalar at `/docs`. The Swagger / RapiDoc / Elements sections below are **opt-in** — build them only when the user explicitly asks. ReDoc stays at `/redoc` for free (FastAPI built-in).

## Scalar (primary — binds /docs)

Modern UI from scalar.com. Best-looking defaults of the bunch. Takes over `/docs`.

**Prereq:** set `docs_url=None` on `FastAPI(...)` so the built-in Swagger doesn't claim `/docs`.

**Install:** `pip install scalar-fastapi` (or `uv add scalar-fastapi`)

**Mount:**
```python
from scalar_fastapi import get_scalar_api_reference

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        # Optional theming:
        # scalar_theme="purple",   # default | alternate | moon | purple | solarized | bluePlanet | saturn | kepler | mars | deepSpace | none
        # scalar_favicon_url="/static/favicon.svg",
        # layout="modern",         # modern | classic
        # dark_mode=True,
        # hide_models=False,
        # hide_download_button=False,
        # default_open_all_tags=False,
        # hidden_clients=[],       # list of HTTP client snippets to hide, e.g. ["clj", "powershell"]
    )
```

`get_scalar_api_reference` returns an `HTMLResponse`. The `include_in_schema=False` keeps the docs route out of the spec itself.

## Swagger UI (manual mount at /swagger)

Since `docs_url=None` disables FastAPI's auto-mount, re-mount it manually so try-it-out and OAuth2 redirect still work:

```python
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html

SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none",
    "filter": True,
    "tryItOutEnabled": True,
    "persistAuthorization": True,
    "syntaxHighlight.theme": "obsidian",
}

@app.get("/swagger", include_in_schema=False)
async def swagger_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} — Swagger UI",
        oauth2_redirect_url="/swagger/oauth2-redirect",
        swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
    )

@app.get("/swagger/oauth2-redirect", include_in_schema=False)
async def swagger_oauth_redirect():
    return get_swagger_ui_oauth2_redirect_html()
```

## RapiDoc

Single web component, no Python dep. Customizable via attributes.

```python
from fastapi.responses import HTMLResponse

@app.get("/rapidoc", include_in_schema=False)
async def rapidoc_html():
    return HTMLResponse(f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{app.title} — RapiDoc</title>
  <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
</head>
<body>
  <rapi-doc
    spec-url="{app.openapi_url}"
    theme="dark"
    render-style="read"
    schema-style="table"
    show-header="false"
    allow-spec-url-load="false"
    allow-spec-file-load="false"
    primary-color="#6366f1"
    nav-bg-color="#0f172a"
    bg-color="#0b1220"
    text-color="#e2e8f0"
    regular-font="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"
    mono-font="ui-monospace, SF Mono, Menlo, Consolas, monospace"
    show-method-in-nav-bar="as-colored-block"
    use-path-in-nav-bar="true"
  ></rapi-doc>
</body>
</html>""")
```

Key attrs:
- `render-style`: `read` (one-page) | `view` (collapsible) | `focused` (selected op only)
- `schema-style`: `tree` | `table`
- `theme`: `light` | `dark`
- `default-schema-tab`: `schema` | `example` | `model`

## Stoplight Elements

```python
@app.get("/elements", include_in_schema=False)
async def elements_html():
    return HTMLResponse(f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{app.title} — Elements</title>
  <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
  <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
</head>
<body style="margin:0">
  <elements-api
    apiDescriptionUrl="{app.openapi_url}"
    router="hash"
    layout="sidebar"
    tryItCredentialsPolicy="same-origin"
  ></elements-api>
</body>
</html>""")
```

Attrs:
- `layout`: `sidebar` (default) | `stacked`
- `router`: `hash` | `memory` | `history`
- `hideTryIt`: `"true"` to disable the "Try it" panel
- `hideExport`: `"true"` to hide the download button

## Single index page (optional)

If serving multiple UIs feels overwhelming, add a tiny `/api` landing page:

```python
@app.get("/api", include_in_schema=False)
async def docs_index():
    return HTMLResponse(f"""<!doctype html>
<title>{app.title}</title>
<style>
  body{{font:16px/1.5 system-ui;margin:4rem auto;max-width:40rem;padding:0 1rem;color:#1e293b}}
  a{{display:block;padding:1rem;border:1px solid #e2e8f0;border-radius:8px;margin:.5rem 0;text-decoration:none;color:inherit}}
  a:hover{{border-color:#6366f1}}
  small{{color:#64748b}}
</style>
<h1>{app.title} API</h1>
<a href="/docs"><strong>Scalar</strong><br><small>Primary — modern reference UI</small></a>
<a href="/swagger"><strong>Swagger UI</strong><br><small>Interactive try-it-out</small></a>
<a href="/redoc"><strong>ReDoc</strong><br><small>Long-form documentation layout</small></a>
<a href="/rapidoc"><strong>RapiDoc</strong><br><small>Single-page dense reference</small></a>
<a href="/elements"><strong>Stoplight Elements</strong><br><small>Hierarchical browser</small></a>
<a href="{app.openapi_url}"><strong>openapi.json</strong><br><small>Raw spec</small></a>
""")
```
