#!/usr/bin/env python3
"""Spotify OAuth2 PKCE auth flow. Saves tokens to ~/.spotify-tokens.json."""

import base64
import hashlib
import http.server
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request

TOKEN_PATH = os.path.expanduser("~/.spotify-tokens.json")
REDIRECT_PORT = 8888
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}/callback"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

SCOPES = " ".join([
    "user-modify-playback-state",
    "user-read-playback-state",
    "user-read-currently-playing",
    "playlist-modify-public",
    "playlist-modify-private",
    "playlist-read-private",
    "user-library-read",
])


def generate_pkce():
    verifier = secrets.token_urlsafe(64)[:128]
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def build_auth_url(client_id, challenge, state):
    params = urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "code_challenge_method": "S256",
        "code_challenge": challenge,
        "scope": SCOPES,
        "state": state,
    })
    return f"{AUTH_URL}?{params}"


def exchange_code(client_id, code, verifier):
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "code_verifier": verifier,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def save_tokens(client_id, tokens):
    payload = {
        "client_id": client_id,
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "expires_in": tokens["expires_in"],
        "scope": tokens.get("scope", SCOPES),
    }
    with open(TOKEN_PATH, "w") as f:
        json.dump(payload, f, indent=2)
    os.chmod(TOKEN_PATH, 0o600)
    print(f"Tokens saved to {TOKEN_PATH}")


def main():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "").strip()
    if not client_id:
        print("Error: set SPOTIFY_CLIENT_ID environment variable")
        print("Get one at https://developer.spotify.com/dashboard")
        print("Set redirect URI to http://localhost:8888/callback")
        sys.exit(1)

    verifier, challenge = generate_pkce()
    state = secrets.token_urlsafe(16)
    url = build_auth_url(client_id, challenge, state)

    print(f"\nOpen this URL in your browser:\n\n{url}\n")

    auth_code = None

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal auth_code
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if params.get("state", [None])[0] != state:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"State mismatch")
                return
            auth_code = params.get("code", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Done! Close this tab.</h1>")

        def log_message(self, format, *args):  # noqa: A002
            pass

    server = http.server.HTTPServer(("localhost", REDIRECT_PORT), Handler)
    server.handle_request()

    if not auth_code:
        print("Error: no auth code received")
        sys.exit(1)

    tokens = exchange_code(client_id, auth_code, verifier)
    save_tokens(client_id, tokens)
    print("Auth complete!")


if __name__ == "__main__":
    main()
