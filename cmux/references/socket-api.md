# V2 socket API (JSON-RPC)

cmux exposes every CLI verb over a unix-domain socket at
`$CMUX_SOCKET_PATH` using JSON-RPC 2.0 framed with `Content-Length:`
headers (LSP-style). The CLI is a thin wrapper over this socket.

**Reach for the socket only when CLI fork overhead hurts** — tight loops,
hundreds of small ops, or when you need batched commands with one
round-trip. Otherwise the CLI is fine and this doc is a pointer, not a
replacement.

## When to use direct socket calls

- Driving > 50 ops/sec (each `cmux` invocation forks a process).
- Subscribing to events (`surface.output`, `workspace.changed`) — CLI
  polls, socket pushes.
- Transactional batches (apply 20 splits atomically on workspace create).

## Connect

```python
import json, os, socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(os.environ["CMUX_SOCKET_PATH"])
```

Node:

```javascript
import { createConnection } from "node:net";
const sock = createConnection(process.env.CMUX_SOCKET_PATH);
```

Every message: `Content-Length: <N>\r\n\r\n<JSON body>`.

## Three canonical calls

### 1. List workspaces

```json
{ "jsonrpc": "2.0", "id": 1, "method": "workspaces.list" }
```

Response:

```json
{ "jsonrpc": "2.0", "id": 1,
  "result": { "workspaces": [ {"id": "...", "name": "...", "tabs": [...]} ] } }
```

### 2. Create tab inside workspace

```json
{ "jsonrpc": "2.0", "id": 2, "method": "surfaces.create",
  "params": { "workspace": "ws_abc", "tab": "myproj:dev",
              "kind": "pane", "direction": "row" } }
```

### 3. Send input

```json
{ "jsonrpc": "2.0", "id": 3, "method": "surface.send",
  "params": { "surface": "srf_xyz", "data": "bun dev\r" } }
```

Note the `\r` — `surface.send` is raw bytes; unlike the CLI there is no
`--enter` sugar. For named keys use `surface.sendKey` with an xterm key
name (`Return`, `Escape`, `C-c`, …).

## Subscriptions (events)

```json
{ "jsonrpc": "2.0", "id": 4, "method": "surface.subscribe",
  "params": { "surface": "srf_xyz", "events": ["output","exit"] } }
```

The daemon then pushes notifications (no `id`) until you
`surface.unsubscribe`:

```json
{ "jsonrpc": "2.0", "method": "surface.output",
  "params": { "surface": "srf_xyz", "data": "compiled in 82ms\n" } }
```

## Error shape

```json
{ "jsonrpc": "2.0", "id": 2,
  "error": { "code": -32001, "message": "workspace not found",
             "data": { "workspace": "ws_abc" } } }
```

Codes: `-32600..-32603` are JSON-RPC standard; cmux-specific codes live
in `-32000..-32099`. Treat `data` as best-effort — shape varies by verb.

## Versioning

The CLI pins a specific API version at launch via the `cmux.hello`
handshake. If you're speaking JSON-RPC directly, send `cmux.hello`
first and read back the server's `version` — bail if it's newer than
you recognize. The socket API moves faster than the CLI; this skill
intentionally does not mirror the full surface. Use the CLI unless you
need what only the socket can give you.

## Further reading

No stable public doc exists yet. The fastest source of truth is
`cmux <verb> --help` (each verb prints its JSON-RPC method and param
schema in the epilogue). For subscriptions, grep cmux source for
`"method": "surface.`.
