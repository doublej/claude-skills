---
name: fastapi-docs-upgrade
description: Audit and upgrade a FastAPI app's auto-generated docs from "thin Swagger" to rich, production-grade API reference. Enriches app metadata, openapi_tags, per-route summaries/descriptions/examples/responses, Pydantic Field examples, custom_openapi hook, and mounts Scalar as the primary docs UI at /docs (replacing the default Swagger UI). RapiDoc, Stoplight Elements, and a relocated Swagger UI are optional extras, built only when the user asks. Triggers on "/fastapi-docs-upgrade", "make my fastapi docs better", "richer swagger docs", "add scalar to fastapi", "upgrade openapi docs".
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
- `docs_url=None` — disables FastAPI's built-in Swagger UI at `/docs` so Scalar can claim that path in Phase 6
- `redoc_url` — keep default unless user overrode

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

## Phase 6 — Mount Scalar at /docs (default: build ONLY this UI)

**By default, build exactly one alt UI: Scalar at `/docs`.** Do NOT mount Swagger, RapiDoc, or Stoplight Elements unless the user explicitly asks for them. The earlier "build all five" behavior is gone — the default is Scalar only.

Default route map:
- `/docs` — **Scalar** (the one UI this skill builds, via `scalar-fastapi`)
- `/redoc` — ReDoc (FastAPI built-in, stays for free — no code, no dep; leave it unless the user wants it gone via `redoc_url=None`)

How to wire the default:
1. In Phase 1 you already set `docs_url=None` on `FastAPI(...)`, freeing `/docs`.
2. Mount Scalar at `/docs` (see `assets/mount_scalar.py`).
3. Add the dep: `uv add scalar-fastapi` if the project uses uv (check `pyproject.toml`), else `pip install scalar-fastapi` with a note to add to requirements.

That's it for the default. Stop here unless the user asked for more.

### Optional — only when the user explicitly requests extra UIs

If (and only if) the user asks for Swagger / RapiDoc / Elements, mount the ones they named:
- `/swagger` — Swagger UI, re-mounted manually via `get_swagger_ui_html` (see `assets/mount_swagger.py`). Pass the `swagger_ui_parameters` dict there.
- `/rapidoc` — RapiDoc (see `assets/mount_rapidoc.py`)
- `/elements` — Stoplight Elements (see `assets/mount_elements.py`)

Code lives in `assets/mount_*.py`. Either copy into the app file or create `app/docs_ui.py` and import. See `references/alt_uis.md` for full details. For ReDoc theming, customizations live in the custom_openapi hook (`x-logo`, etc.).

**Commit:** `docs(api): mount Scalar as the primary docs UI at /docs`

## Phase 7 — Verify

Start the app (use `references/run_hints.md`) and curl the docs routes you actually mounted (default: `docs` and `redoc`; add any optional UIs the user requested):
```bash
curl -fsS http://localhost:PORT/openapi.json | jq '.info, .tags[0], (.paths | to_entries[0])' | head -40
for path in docs redoc; do  # add swagger/rapidoc/elements only if you mounted them
  curl -fsSo /dev/null -w "%{http_code} /$path\n" http://localhost:PORT/$path
done
```

Each mounted route should return 200. `/docs` should serve Scalar (grep response body for `scalar` to confirm). The openapi.json should show populated `info.description`, `info.contact`, `tags[].description`, and at least one route with `description`/`responses`/`examples`.

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
- `mount_scalar.py` — Scalar mount route (binds `/docs`, the primary UI — the only one built by default)
- `mount_swagger.py` — Swagger UI mounted manually at `/swagger` (optional, only on request)
- `mount_rapidoc.py` — RapiDoc mount route (optional, only on request)
- `mount_elements.py` — Stoplight Elements mount route (optional, only on request)
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
