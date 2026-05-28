#!/usr/bin/env python3
"""Preview Mermaid diagrams in browser using multiple methods."""

import argparse
import base64
import json
import sys
import tempfile
import webbrowser
import zlib
from pathlib import Path
from urllib.parse import quote


def read_mermaid(source: str) -> str:
    """Read mermaid code from file or stdin."""
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text()


def mermaid_live_url(code: str) -> str:
    """Generate mermaid.live URL with encoded diagram."""
    state = {"code": code, "mermaid": {"theme": "default"}, "autoSync": True, "updateDiagram": True}
    json_str = json.dumps(state)
    compressed = zlib.compress(json_str.encode("utf-8"), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    return f"https://mermaid.live/edit#pako:{encoded}"


def kroki_url(code: str, fmt: str = "svg") -> str:
    """Generate kroki.io URL for diagram."""
    compressed = zlib.compress(code.encode("utf-8"), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    return f"https://kroki.io/mermaid/{fmt}/{encoded}"


def local_html(code: str, output_path: str = None) -> str:
    """Generate local HTML file with embedded diagram."""
    html = f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Mermaid Preview</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<style>body{{font-family:system-ui;padding:2rem;background:#f5f5f5}}
.mermaid{{background:#fff;padding:2rem;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.1)}}</style>
</head><body>
<pre class="mermaid">{code}</pre>
<script>mermaid.initialize({{startOnLoad:true,theme:"default"}});</script>
</body></html>'''
    if output_path:
        Path(output_path).write_text(html)
        return output_path
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html)
        return f.name


def main():
    parser = argparse.ArgumentParser(description="Preview Mermaid diagram in browser")
    parser.add_argument("input", nargs="?", default="-", help="Input .mmd file or - for stdin")
    parser.add_argument("-m", "--method", default="live",
                        choices=["live", "kroki", "local"],
                        help="live=mermaid.live, kroki=kroki.io, local=HTML file")
    parser.add_argument("-o", "--output", help="Output HTML file (local method only)")
    parser.add_argument("--url-only", action="store_true", help="Print URL without opening browser")

    args = parser.parse_args()
    code = read_mermaid(args.input)

    if args.method == "live":
        url = mermaid_live_url(code)
    elif args.method == "kroki":
        url = kroki_url(code)
    else:
        path = local_html(code, args.output)
        url = f"file://{Path(path).absolute()}"

    if args.url_only:
        print(url)
    else:
        print(f"Opening: {url[:80]}..." if len(url) > 80 else f"Opening: {url}")
        webbrowser.open(url)


if __name__ == "__main__":
    main()
