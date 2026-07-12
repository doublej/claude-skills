#!/usr/bin/env python3
"""Spotify Web API helper. Handles token refresh and provides simple API calls.

Usage:
  spotify-api.py now-playing
  spotify-api.py play [URI]
  spotify-api.py pause
  spotify-api.py next
  spotify-api.py prev
  spotify-api.py volume PERCENT
  spotify-api.py search TYPE QUERY [--limit N]
  spotify-api.py playlists [--limit N]
  spotify-api.py playlist-tracks PLAYLIST_ID [--limit N]
  spotify-api.py create-playlist NAME [--description DESC] [--public]
  spotify-api.py add-tracks PLAYLIST_ID URI [URI...]
  spotify-api.py devices
  spotify-api.py queue [--limit N]
  spotify-api.py refresh
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.spotify.com/v1"
TOKEN_URL = "https://accounts.spotify.com/api/token"
TOKEN_PATH = os.path.expanduser("~/.spotify-tokens.json")


def load_tokens() -> dict[str, Any]:
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: {TOKEN_PATH} not found. Run spotify-auth.py first.")
        sys.exit(1)
    with open(TOKEN_PATH) as f:
        return json.load(f)


def save_tokens(data: dict[str, Any]) -> None:
    with open(TOKEN_PATH, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(TOKEN_PATH, 0o600)


def refresh_access_token(tokens: dict[str, Any]) -> dict[str, Any]:
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": tokens["client_id"],
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded",
    })
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    tokens["access_token"] = result["access_token"]
    if "refresh_token" in result:
        tokens["refresh_token"] = result["refresh_token"]
    tokens["refreshed_at"] = int(time.time())
    tokens["expires_in"] = result.get("expires_in", 3600)
    save_tokens(tokens)
    return tokens


def api(
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    tokens: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if tokens is None:
        tokens = load_tokens()

    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    data = json.dumps(body).encode() if body else None
    if data:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                return {}
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            tokens = refresh_access_token(tokens)
            return api(method, path, body, params, tokens)
        error_body = e.read().decode()
        print(f"API error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def now_playing() -> None:
    data = api("GET", "/me/player/currently-playing")
    if not data or not data.get("item"):
        return print("Nothing playing")
    item = data["item"]
    artists = ", ".join(a["name"] for a in item.get("artists", []))
    progress = data.get("progress_ms", 0) // 1000
    duration = item.get("duration_ms", 0) // 1000
    state = "Playing" if data.get("is_playing") else "Paused"
    print(json.dumps({
        "track": item["name"],
        "artists": artists,
        "album": item.get("album", {}).get("name", ""),
        "uri": item["uri"],
        "progress": f"{progress // 60}:{progress % 60:02d}",
        "duration": f"{duration // 60}:{duration % 60:02d}",
        "state": state,
    }, indent=2))


def play(uri: str | None = None) -> None:
    body = {"uris": [uri]} if uri and uri.startswith("spotify:track:") else None
    if uri and not body:
        body = {"context_uri": uri}
    api("PUT", "/me/player/play", body=body)
    print("Playback started")


def search(search_type: str, query: str, limit: int = 10) -> None:
    data = api("GET", "/search", params={
        "q": query, "type": search_type, "limit": limit,
    })
    key = f"{search_type}s"
    items = data.get(key, {}).get("items", [])
    results = []
    for item in items:
        entry = {"name": item["name"], "uri": item["uri"], "id": item["id"]}
        if search_type == "track":
            entry["artists"] = ", ".join(a["name"] for a in item.get("artists", []))
            entry["album"] = item.get("album", {}).get("name", "")
        elif search_type == "artist":
            entry["followers"] = item.get("followers", {}).get("total", 0)
        results.append(entry)
    print(json.dumps(results, indent=2))


def playlists(limit: int = 20) -> None:
    data = api("GET", "/me/playlists", params={"limit": limit})
    items = data.get("items", [])
    results = [{"name": p["name"], "id": p["id"], "tracks": p["tracks"]["total"],
                "public": p.get("public")} for p in items]
    print(json.dumps(results, indent=2))


def playlist_tracks(playlist_id: str, limit: int = 50) -> None:
    data = api("GET", f"/playlists/{playlist_id}/tracks", params={"limit": limit})
    items = data.get("items", [])
    results = [{"name": t["track"]["name"], "uri": t["track"]["uri"],
                "artists": ", ".join(a["name"] for a in t["track"].get("artists", []))}
               for t in items if t.get("track")]
    print(json.dumps(results, indent=2))


def create_playlist(name: str, description: str = "", public: bool = False) -> None:
    data = api("GET", "/me")
    user_id = data["id"]
    result = api("POST", f"/users/{user_id}/playlists", body={
        "name": name, "description": description, "public": public,
    })
    print(json.dumps({"id": result["id"], "name": result["name"],
                       "url": result["external_urls"]["spotify"]}, indent=2))


def add_tracks(playlist_id: str, uris: list[str]) -> None:
    api("POST", f"/playlists/{playlist_id}/tracks", body={"uris": uris})
    print(f"Added {len(uris)} tracks to playlist")


def devices() -> None:
    data = api("GET", "/me/player/devices")
    results = [{"name": d["name"], "id": d["id"], "type": d["type"],
                "active": d["is_active"], "volume": d.get("volume_percent")}
               for d in data.get("devices", [])]
    print(json.dumps(results, indent=2))


def queue(limit: int = 10) -> None:
    data = api("GET", "/me/player/queue")
    items = data.get("queue", [])[:limit]
    current = data.get("currently_playing")
    result = {"currently_playing": None, "queue": []}
    if current:
        result["currently_playing"] = {
            "name": current["name"], "uri": current["uri"],
            "artists": ", ".join(a["name"] for a in current.get("artists", [])),
        }
    for item in items:
        result["queue"].append({
            "name": item["name"], "uri": item["uri"],
            "artists": ", ".join(a["name"] for a in item.get("artists", [])),
        })
    print(json.dumps(result, indent=2))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    rest = args[1:]

    def get_flag(name: str, default: str | None = None) -> str | None:
        if name in rest:
            idx = rest.index(name)
            return rest[idx + 1] if idx + 1 < len(rest) else default
        return default

    if cmd == "now-playing":
        now_playing()
    elif cmd == "play":
        play(rest[0] if rest else None)
    elif cmd == "pause":
        api("PUT", "/me/player/pause")
        print("Paused")
    elif cmd == "next":
        api("POST", "/me/player/next")
        print("Skipped to next")
    elif cmd == "prev":
        api("POST", "/me/player/previous")
        print("Skipped to previous")
    elif cmd == "volume":
        if not rest:
            print("Usage: volume PERCENT")
            sys.exit(1)
        api("PUT", "/me/player/volume", params={"volume_percent": int(rest[0])})
        print(f"Volume set to {rest[0]}%")
    elif cmd == "search":
        if len(rest) < 2:
            print("Usage: search TYPE QUERY [--limit N]")
            sys.exit(1)
        limit = int(get_flag("--limit", "10"))
        search(rest[0], rest[1], limit)
    elif cmd == "playlists":
        limit = int(get_flag("--limit", "20"))
        playlists(limit)
    elif cmd == "playlist-tracks":
        if not rest:
            print("Usage: playlist-tracks PLAYLIST_ID [--limit N]")
            sys.exit(1)
        limit = int(get_flag("--limit", "50"))
        playlist_tracks(rest[0], limit)
    elif cmd == "create-playlist":
        if not rest:
            print("Usage: create-playlist NAME [--description DESC] [--public]")
            sys.exit(1)
        desc = get_flag("--description", "")
        public = "--public" in rest
        create_playlist(rest[0], desc, public)
    elif cmd == "add-tracks":
        if len(rest) < 2:
            print("Usage: add-tracks PLAYLIST_ID URI [URI...]")
            sys.exit(1)
        add_tracks(rest[0], rest[1:])
    elif cmd == "devices":
        devices()
    elif cmd == "queue":
        limit = int(get_flag("--limit", "10"))
        queue(limit)
    elif cmd == "refresh":
        tokens = load_tokens()
        refresh_access_token(tokens)
        print("Token refreshed")
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
