#!/usr/bin/env python3
"""Static server for the PWA probe that also accepts POST /report and appends JSON to reports.jsonl."""
import json, os, sys, ssl, pathlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).parent
if "--root" in sys.argv:
    ROOT = pathlib.Path(sys.argv[sys.argv.index("--root") + 1]).resolve()
OUT = ROOT / "reports.jsonl"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_POST(self):
        if self.path != "/report":
            return self.send_error(404)
        n = int(self.headers.get("content-length", 0))
        body = self.rfile.read(n)
        with OUT.open("a") as f:
            f.write(body.decode("utf-8") + "\n")
        try:
            d = json.loads(body)
            print(f"[report] {d.get('tag')}: {d['window']['innerWidth']}x{d['window']['innerHeight']} "
                  f"dpr={d['screen']['dpr']} insets={d['safeAreaInsets']} "
                  f"vh={d['viewportUnits']}", flush=True)
        except Exception as e:
            print(f"[report] unparsed ({e})", flush=True)
        self.send_response(204)
        self.send_header("access-control-allow-origin", "*")
        self.end_headers()

    def end_headers(self):
        self.send_header("cache-control", "no-store")
        self.send_header("access-control-allow-origin", "*")
        super().end_headers()



if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    cert = ROOT / "cert.pem"
    if cert.exists():
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, ROOT / "key.pem")
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
        print(f"serving https://0.0.0.0:{port}", flush=True)
    else:
        print(f"serving http://0.0.0.0:{port}", flush=True)
    srv.serve_forever()
