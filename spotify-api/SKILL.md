---
name: spotify-api
description: "Control playback, search music, manage playlists via the Web API, or check what's playing."
---

# Spotify API

Control Spotify through the Web API using bundled scripts. Zero dependencies (stdlib only).

<setup>

1. Create app at https://developer.spotify.com/dashboard
2. Set redirect URI to `http://localhost:8888/callback`
3. Run auth flow:

```bash
SPOTIFY_CLIENT_ID=your_client_id python3 ~/.claude/skills/spotify-api/scripts/spotify-auth.py
```

Tokens saved to `~/.spotify-tokens.json` (auto-refreshed on 401).

</setup>

<api_script>

All commands via `python3 ~/.claude/skills/spotify-api/scripts/spotify-api.py`:

### Playback

| Command | Description |
|---------|-------------|
| `now-playing` | Current track, artist, album, progress, state |
| `play [URI]` | Resume or play a specific track/album/playlist URI |
| `pause` | Pause playback |
| `next` | Skip to next track |
| `prev` | Skip to previous track |
| `volume PERCENT` | Set volume (0-100) |
| `devices` | List available Spotify Connect devices |
| `queue [--limit N]` | Show current queue |

### Search

```bash
spotify-api.py search track "bohemian rhapsody" --limit 5
spotify-api.py search artist "radiohead"
spotify-api.py search album "ok computer"
spotify-api.py search playlist "workout"
```

Returns JSON array with `name`, `uri`, `id` (+ `artists`, `album` for tracks).

### Playlists

| Command | Description |
|---------|-------------|
| `playlists [--limit N]` | List user's playlists |
| `playlist-tracks PLAYLIST_ID [--limit N]` | List tracks in a playlist |
| `create-playlist NAME [--description DESC] [--public]` | Create new playlist |
| `add-tracks PLAYLIST_ID URI [URI...]` | Add tracks to a playlist |

</api_script>

<workflows>

1. Search tracks: `search track "song name"` — note URIs
2. Create playlist: `create-playlist "My Playlist" --description "..."`
3. Add tracks: `add-tracks PLAYLIST_ID spotify:track:xxx spotify:track:yyy`

## Workflow: DJ Control

1. Check what's playing: `now-playing`
2. Search for next song: `search track "song name"`
3. Play it: `play spotify:track:xxx`
4. Adjust volume: `volume 75`

</workflows>

<notes>

- All output is JSON for easy parsing
- URIs follow format `spotify:track:ID`, `spotify:album:ID`, `spotify:playlist:ID`
- Playback commands require an active Spotify client (desktop/mobile/web)
- Token auto-refreshes on 401; run `refresh` to force refresh
- Scopes: playback control, playlist read/write, library read

</notes>
