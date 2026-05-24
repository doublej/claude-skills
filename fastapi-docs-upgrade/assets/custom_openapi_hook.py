"""Template — drop into the app file (after the FastAPI() call).

Customizes the generated spec: branding (x-logo for ReDoc/Scalar), tag ordering,
externalDocs, vendor extensions. Cached so it only runs once per process.
"""

from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
        contact=app.contact,
        license_info=app.license_info,
        terms_of_service=app.terms_of_service,
    )

    # Branding — picked up by ReDoc and Scalar
    schema["info"]["x-logo"] = {
        "url": "https://example.com/static/logo.svg",
        "backgroundColor": "#ffffff",
        "altText": f"{app.title} logo",
        "href": "https://example.com",
    }

    # Top-level external docs
    schema["externalDocs"] = {
        "description": "Full developer guide",
        "url": "https://example.com/docs",
    }

    # ReDoc tag groups (ignored by Swagger UI, rendered by ReDoc + Scalar)
    schema["x-tagGroups"] = [
        {"name": "Core", "tags": ["auth", "users", "products", "orders"]},
        {"name": "Integrations", "tags": ["webhooks"]},
        {"name": "Admin", "tags": ["admin", "internal"]},
    ]

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
