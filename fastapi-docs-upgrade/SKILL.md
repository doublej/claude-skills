---
name: fastapi-docs-upgrade
description: Audit and upgrade a FastAPI app's auto-generated docs from "thin Swagger" to rich, production-grade API reference. Enriches app metadata, openapi_tags, per-route summaries/descriptions/examples/responses, Pydantic Field examples, custom_openapi hook, and mounts modern alt UIs (Scalar, RapiDoc, Stoplight Elements) alongside Swagger UI + ReDoc. Triggers on "/fastapi-docs-upgrade", "make my fastapi docs better", "richer swagger docs", "add scalar to fastapi", "upgrade openapi docs".
---

# FastAPI Docs Upgrade

Transform a FastAPI project's docs from default Swagger UI + ReDoc into a polished, fully-described, multi-UI API reference — in one sweep.

<when_to_use>
User invokes `/fastapi-docs-upgrade` or asks to make their FastAPI docs richer, more professional, more detailed, or to add Scalar / RapiDoc / Stoplight Elements.
</when_to_use>

<scope>
This is a **whole-app, one-sweep** upgrade. Don't ask for permission per file. Audit → plan → apply → commit per phase. Match the user's `git_discipline` rule by committing each phase, not each file.
</scope>

<workflow>

## Phase 0 — Discover (read-only, ~30s)

Run the audit script and read its JSON output:

```bash
python3 ~/.claude/skills/fastapi-docs-upgrade/scripts/audit_fastapi.py [project_root]
```

It locates:
- The `FastAPI(...)` instantiation (the "app file")
- All `APIRouter` definitions and their prefixes/tags
- Every route decorator with its current metadata coverage
- Every Pydantic model and which fields have `examples=` / `description=`
- Whether a `custom_openapi` hook, `openapi_tags`, `swagger_ui_parameters`, or alt UI is already mounted

Read the JSON. Identify gaps. Print a one-screen plan to the user before editing.

## Phase 1 — App metadata

Edit the `FastAPI(...)` constructor. Add every applicable param:
- `title`, `summary` (one-liner, <300 chars), `description` (markdown, multi-paragraph), `version`
- `terms_of_service`, `contact={"name","url","email"}`, `license_info={"name","url"}`
- `servers=[{"url","description"}, ...]` — at minimum local + prod
- `openapi_tags=tags_metadata` (defined in same file or imported)
- `docs_url`, `redoc_url` — keep defaults unless user overrode

Use `assets/app_metadata.py` as the template.

**Commit:** `docs(api): enrich FastAPI app metadata`

## Phase 2 — Tags metadata

Define `tags_metadata` as a module-level list of dicts. One entry per logical group present in the app's routes. Each entry:
```python
{"name": "users", "description": "User CRUD, profile, preferences.\n\nUse **/users/me** for the current authenticated user.", "externalDocs": {"description": "Auth flow", "url": "https://..."}}
```

Markdown is rendered in Swagger UI / ReDoc / Scalar. Use it: bold for entities, lists for operations, code spans for paths.

Use `assets/tags_metadata.py` as the template.

**Commit:** `docs(api): add tags metadata with rich descriptions`

## Phase 3 — Per-route enrichment

For each route decorator (`@app.get`, `@router.post`, ...), add these where missing:
- `summary="Verb-phrase title"` (≤60 chars, appears in nav)
- `description=` — markdown body in the **docstring** (FastAPI auto-uses docstring as description; prefer that over the param)
- `response_description="What the 200 body represents"`
- `responses={400: {...}, 404: {...}, 422: {...}}` with `description`, `model`, and `content` examples — see `references/route_responses.md`
- `openapi_examples={...}` on `Body(...)`, `Query(...)`, `Path(...)` — multi-example dicts surface as a dropdown in Swagger UI
- `operation_id="snake_case_unique"` — clean IDs for SDK codegen (skip if user doesn't care about SDKs)
- `deprecated=True` where applicable
- `tags=["users"]` if routes use loose `@app.get` without a router

Don't touch route logic. Don't reorder params. Add metadata-only kwargs and docstrings.

Use `references/route_enrichment.md` for the full pattern catalog.

**Commit:** `docs(api): enrich route summaries, descriptions, responses, examples`

## Phase 4 — Pydantic model enrichment

For every Pydantic model used in request/response:
- Each field gets `Field(..., description="...", examples=[...])` where missing
- Add `model_config = ConfigDict(json_schema_extra={"examples": [{...full body...}]})` for top-level request/response models
- Use realistic, copy-pasteable example values — not "string", "foo", "bar"

See `references/pydantic_examples.md` for the patterns.

**Commit:** `docs(api): add Field examples and json_schema_extra to models`

## Phase 5 — Custom OpenAPI hook

Install an `app.openapi = custom_openapi` hook (cached) that:
- Injects `x-logo` for ReDoc branding
- Adds `servers` if not already set
- Adds top-level `externalDocs`
- Patches `info.x-something` for vendor extensions
- Sorts tags in a deliberate order

Use `assets/custom_openapi_hook.py` as the template. Only add this phase if the user has a logo URL or wants any of the above — otherwise skip and note why.

**Commit:** `docs(api): install custom_openapi hook for branding and ordering`

## Phase 6 — Alt UIs (Scalar, RapiDoc, Elements)

Mount all three alongside Swagger UI + ReDoc. Endpoints:
- `/docs` — Swagger UI (existing)
- `/redoc` — ReDoc (existing)
- `/scalar` — Scalar (new, via `scalar-fastapi`)
- `/rapidoc` — RapiDoc (new, single-file HTMLResponse)
- `/elements` — Stoplight Elements (new, single-file HTMLResponse)

Code lives in `assets/mount_scalar.py`, `assets/mount_rapidoc.py`, `assets/mount_elements.py`. Either copy into the app file or create `app/docs_ui.py` and import.

For Scalar, add to deps: `scalar-fastapi`. Use `uv add scalar-fastapi` if the project uses uv (check `pyproject.toml`), else `pip install scalar-fastapi` with a note to add to requirements.

Also polish the built-in UIs:
- Pass `swagger_ui_parameters={"docExpansion": "none", "filter": True, "syntaxHighlight.theme": "obsidian", "tryItOutEnabled": True, "persistAuthorization": True}` to `FastAPI(...)`
- For ReDoc, customizations live in the custom_openapi hook (`x-logo`, etc.) since FastAPI doesn't expose redoc_ui_parameters

See `references/alt_uis.md` for full details.

**Commit:** `docs(api): mount Scalar, RapiDoc, and Stoplight Elements; polish Swagger UI`

## Phase 7 — Verify

Start the app (use `references/run_hints.md`) and curl each docs route:
```bash
curl -fsS http://localhost:PORT/openapi.json | jq '.info, .tags[0], (.paths | to_entries[0])' | head -40
for path in docs redoc scalar rapidoc elements; do
  curl -fsSo /dev/null -w "%{http_code} /$path\n" http://localhost:PORT/$path
done
```

All five should return 200. The openapi.json should show populated `info.description`, `info.contact`, `tags[].description`, and at least one route with `description`/`responses`/`examples`.

If the project has a typecheck/test step, run it. Surface any failures.

</workflow>

<bundled_resources>

### scripts/
- `audit_fastapi.py` — discovery script; outputs JSON report of FastAPI app structure and metadata gaps

### references/ (read on demand)
- `route_enrichment.md` — full per-route pattern catalog
- `route_responses.md` — `responses={}` with examples for 400/404/422/etc.
- `pydantic_examples.md` — Field examples + json_schema_extra patterns
- `alt_uis.md` — Scalar, RapiDoc, Elements mount details + theming options
- `swagger_ui_tweaks.md` — full swagger_ui_parameters reference + custom CSS injection
- `run_hints.md` — how to start the app to verify (uvicorn, fastapi dev, justfile, etc.)

### assets/ (copy-paste templates)
- `app_metadata.py` — full FastAPI(...) constructor template
- `tags_metadata.py` — tags_metadata list template
- `custom_openapi_hook.py` — cached openapi hook with x-logo, servers, externalDocs
- `mount_scalar.py` — Scalar mount route
- `mount_rapidoc.py` — RapiDoc mount route
- `mount_elements.py` — Stoplight Elements mount route
- `swagger_custom.css` — subtle Swagger UI polish (optional, mount via swagger_ui_parameters)

</bundled_resources>

<rules>
- One sweep, no per-file confirmation. Commit per phase.
- Never change route logic. Metadata-only edits + docstrings + new mount routes.
- Realistic example values (real-looking IDs, emails, ISO timestamps). Never "string"/"foo"/"bar".
- Use the project's package manager (uv > pip) — check `pyproject.toml` / `requirements.txt`.
- If a phase has nothing to do (e.g. all routes already documented), skip the commit and note why.
- Match existing code style. Don't reformat unrelated lines.
- Don't add `# noqa` or backwards-compat shims. Don't delete the user's existing description/summary fields — only add and enrich.
- If `app.openapi_url` is None (docs disabled), bail with a clear message — user must enable docs first.
</rules>
