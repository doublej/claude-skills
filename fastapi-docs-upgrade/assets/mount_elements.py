"""Template — Stoplight Elements mount. Zero Python deps.

Adds:
    GET /elements  →  Stoplight Elements API reference UI
"""

from fastapi.responses import HTMLResponse


@app.get("/elements", include_in_schema=False)
async def elements_html():
    return HTMLResponse(
        f"""<!doctype html>
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
</html>"""
    )
