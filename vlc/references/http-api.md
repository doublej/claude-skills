# VLC HTTP API Reference

Base: `http://<host>:<port>/requests/`
Auth: Basic (username empty, password = `--http-password` value)

## Endpoints

| Endpoint | Returns |
|----------|---------|
| `status.json` | Current playback status + accepts commands |
| `status.xml` | Same as above in XML |
| `playlist.json` | Full playlist tree |
| `playlist.xml` | Same in XML |

## status.json Commands

Pass via query params: `?command=<cmd>&val=<val>&id=<id>&input=<uri>&option=<opt>`

### Playback

| Command | Params | Description |
|---------|--------|-------------|
| `pl_play` | `id` (optional) | Play playlist item (or resume) |
| `pl_pause` | `id` (optional) | Toggle pause |
| `pl_forcepause` | | Force pause |
| `pl_forceresume` | | Force resume |
| `pl_stop` | | Stop |
| `pl_next` | | Next |
| `pl_previous` | | Previous |

### Seeking

| Command | Params | Description |
|---------|--------|-------------|
| `seek` | `val` | Seek. Formats: `120` (abs seconds), `+30s` / `-30s` (relative), `50%` (percentage), `1h2m3s` (time) |

### Volume

| Command | Params | Description |
|---------|--------|-------------|
| `volume` | `val` | Set volume 0-512 (256=100%). Prefix `+`/`-` for relative |

### Speed

| Command | Params | Description |
|---------|--------|-------------|
| `rate` | `val` | Playback speed (1.0 = normal) |

### Playlist Management

| Command | Params | Description |
|---------|--------|-------------|
| `in_play` | `input`, `option` | Add and play URI |
| `in_enqueue` | `input`, `option` | Add to playlist without playing |
| `pl_delete` | `id` | Remove item from playlist |
| `pl_empty` | | Clear playlist |
| `pl_sort` | `id` (mode), `val` (0=asc/1=desc) | Sort. Modes: 0=id, 1=name, 3=author, 5=random, 7=track |
| `pl_random` | | Toggle random |
| `pl_loop` | | Toggle loop |
| `pl_repeat` | | Toggle repeat |

### Video

| Command | Params | Description |
|---------|--------|-------------|
| `fullscreen` | | Toggle fullscreen |
| `snapshot` | | Take screenshot |
| `key` | `val` | Simulate hotkey |

### Audio

| Command | Params | Description |
|---------|--------|-------------|
| `audiodelay` | `val` | Audio delay in seconds |
| `preamp` | `val` | Preamp gain (dB) |
| `equalizer` | `val` | Set EQ band gains |
| `enableeq` | `val` | 0=disable, 1=enable EQ |
| `setpreset` | `val` | EQ preset index |

### Subtitles

| Command | Params | Description |
|---------|--------|-------------|
| `subdelay` | `val` | Subtitle delay in seconds |
| `subtitle_track` | `val` | Select subtitle track by id |
| `audio_track` | `val` | Select audio track by id |
| `video_track` | `val` | Select video track by id |

## status.json Response Fields

```json
{
  "state": "playing|paused|stopped",
  "time": 123,
  "length": 456,
  "position": 0.27,
  "volume": 256,
  "rate": 1.0,
  "fullscreen": false,
  "repeat": false,
  "loop": false,
  "random": false,
  "audiodelay": 0,
  "subtitledelay": 0,
  "equalizer": [],
  "information": {
    "category": {
      "meta": {
        "filename": "video.mp4",
        "title": "...",
        "artist": "...",
        "genre": "...",
        "album": "..."
      },
      "Stream 0": {
        "Type": "Video",
        "Codec": "H264 - MPEG-4 AVC (part 10) (avc1)",
        "Resolution": "1920x1080"
      },
      "Stream 1": {
        "Type": "Audio",
        "Codec": "MPEG AAC Audio (mp4a)",
        "Channels": "Stereo",
        "Sample rate": "48000 Hz"
      }
    }
  },
  "stats": {
    "inputbitrate": 0.5,
    "demuxbitrate": 0.4,
    "decodedvideo": 1234,
    "decodedaudio": 5678,
    "lostframes": 0
  }
}
```

## playlist.json Structure

```json
{
  "ro": "ro",
  "type": "node",
  "name": "Playlist",
  "id": "1",
  "children": [
    {
      "ro": "rw",
      "type": "node",
      "name": "Playlist",
      "id": "2",
      "children": [
        {
          "ro": "rw",
          "type": "leaf",
          "id": "3",
          "name": "video.mp4",
          "uri": "file:///path/to/video.mp4",
          "duration": 456,
          "current": "current"
        }
      ]
    }
  ]
}
```
