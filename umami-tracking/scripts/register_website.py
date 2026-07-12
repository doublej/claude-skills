#!/usr/bin/env python3
"""Register a new website in Umami and return its website ID.

Usage:
    python register_website.py <name> <domain>

Authenticates with the Umami API, creates the website, and prints the website ID.
"""
import json
import sys
import urllib.request
from pathlib import Path

UMAMI_URL = "https://umami-inky-two.vercel.app"


def load_credentials() -> tuple[str, str]:
    env_file = Path(__file__).parent / ".env"
    env = {}
    for line in env_file.read_text().strip().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env["UMAMI_USERNAME"], env["UMAMI_PASSWORD"]


def api_request(path: str, data: dict | None = None, token: str | None = None) -> dict:
    url = f"{UMAMI_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def authenticate() -> str:
    username, password = load_credentials()
    result = api_request("/api/auth/login", {"username": username, "password": password})
    return result["token"]


def create_website(token: str, name: str, domain: str) -> str:
    result = api_request("/api/websites", {"name": name, "domain": domain}, token)
    return result["id"]


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <name> <domain>", file=sys.stderr)
        sys.exit(1)

    name, domain = sys.argv[1], sys.argv[2]
    token = authenticate()
    website_id = create_website(token, name, domain)
    print(website_id)


if __name__ == "__main__":
    main()
