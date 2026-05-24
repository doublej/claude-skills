# How to start the FastAPI app for verification

Used in Phase 7. Detect from project files, then run.

## Detection order

1. **justfile** — check for `just dev`, `just serve`, `just run`, `just api`
2. **pyproject.toml [project.scripts]** — look for a console script that runs uvicorn
3. **Procfile / docker-compose.yml** — read the web/api service command
4. **README.md** — search for `uvicorn` or `fastapi dev`
5. **Fallback** — `fastapi dev path/to/app.py` (uses fastapi-cli, ships with FastAPI ≥0.100)

## Common commands

```bash
# fastapi-cli (preferred for FastAPI ≥0.100)
fastapi dev src/myapp/main.py

# Plain uvicorn (works for any version)
uvicorn myapp.main:app --reload --port 8000

# With uv-managed env
uv run uvicorn myapp.main:app --reload

# With poetry
poetry run uvicorn myapp.main:app --reload
```

## Verification curl

After the app is up (poll for ~5s before failing):

```bash
PORT=8000  # adjust
BASE="http://localhost:$PORT"

# Spec health
curl -fsS "$BASE/openapi.json" \
  | jq '{title: .info.title, version: .info.version, has_contact: (.info.contact != null), tag_count: (.tags // [] | length), path_count: (.paths | length)}'

# UI health
for path in docs redoc scalar rapidoc elements api; do
  code=$(curl -fsSo /dev/null -w "%{http_code}" "$BASE/$path" || echo "ERR")
  printf "%-10s %s\n" "/$path" "$code"
done
```

A 200 on `/scalar`, `/rapidoc`, `/elements` confirms the new mounts work. `/api` only if the optional index page was added.

## Don't start the server if user has one running

Before launching uvicorn, check `lsof -i :PORT` (or `curl -fsS $BASE/openapi.json` first). If the spec already returns, skip the start and just verify against the running instance.
