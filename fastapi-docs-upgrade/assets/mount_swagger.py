"""Template — manual Swagger UI mount at /swagger.

Used when Scalar claims /docs as the primary UI. Set `docs_url=None` on FastAPI(...)
to free up the /docs path, then mount Swagger UI here with the same parameter dict
you would have passed via `swagger_ui_parameters=...`.
"""

from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html


SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none",
    "defaultModelsExpandDepth": 1,
    "displayRequestDuration": True,
    "filter": True,
    "tryItOutEnabled": True,
    "persistAuthorization": True,
    "syntaxHighlight.theme": "obsidian",
    "requestSnippetsEnabled": True,
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
