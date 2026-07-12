"""Template — RapiDoc mount. Zero Python deps; pulls a JS module from unpkg.

Adds:
    GET /rapidoc  →  RapiDoc single-page reference UI
"""

from fastapi.responses import HTMLResponse


@app.get("/rapidoc", include_in_schema=False)
async def rapidoc_html() -> HTMLResponse:
    return HTMLResponse(
        f"""<!doctype html>
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
    default-schema-tab="example"
    show-header="false"
    show-method-in-nav-bar="as-colored-block"
    use-path-in-nav-bar="true"
    allow-spec-url-load="false"
    allow-spec-file-load="false"
    primary-color="#6366f1"
    nav-bg-color="#0f172a"
    bg-color="#0b1220"
    text-color="#e2e8f0"
    nav-text-color="#cbd5e1"
    regular-font="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"
    mono-font="ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
  ></rapi-doc>
</body>
</html>"""
    )
