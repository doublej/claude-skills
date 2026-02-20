---
name: vlc
description: Control and configure VLC media player. Use when playing media, controlling playback, streaming, converting, managing playlists, adjusting audio/video, or automating VLC via CLI, AppleScript, or HTTP API.
---

# VLC Media Player

Binary: `/Applications/VLC.app/Contents/MacOS/VLC` (macOS), `vlc` (Linux/Windows)

## Control Interfaces

### 1. AppleScript (macOS — preferred for runtime control)

```applescript
-- Query state
tell application "VLC"
  get playing               -- boolean
  get name of current item  -- text
  get path of current item  -- text
  get current time          -- seconds (integer, rw)
  get duration of current item -- seconds (integer, ro)
  get audio volume          -- 0-512 (256 = 100%)
  get muted                 -- boolean (ro)
  get fullscreen mode       -- boolean (rw)
  get audio desync          -- ms offset (rw)
end tell

-- Commands
tell application "VLC"
  play          -- toggle play/pause
  stop
  next          -- next track/chapter
  previous
  mute          -- toggle mute
  fullscreen    -- toggle fullscreen
  volumeUp      -- +1 step (32 steps total, 0-400%)
  volumeDown
  step forward  -- skip forward (1=extraShort 2=short 3=medium 4=long)
  step backward
  set current time to 120   -- seek to 2:00
  set audio volume to 200   -- ~78%
  set fullscreen mode to true
  OpenURL "http://stream.url/path"
end tell
```

Run via: `osascript -e 'tell application "VLC" to play'`

### 2. CLI (launch with options)

```bash
VLC="/Applications/VLC.app/Contents/MacOS/VLC"

# Basic playback
$VLC file.mp4                          # play file
$VLC file1.mp4 file2.mp4               # playlist
$VLC --fullscreen file.mp4             # fullscreen
$VLC --start-time 30 --stop-time 90 file.mp4  # play segment
$VLC --rate 1.5 file.mp4               # speed
$VLC --no-video file.mp3               # audio only
$VLC --play-and-exit file.mp4          # quit after playback
$VLC --play-and-pause file.mp4         # pause at end

# Repeat/loop
$VLC --repeat file.mp4                 # repeat current
$VLC --loop file1.mp4 file2.mp4        # loop playlist
$VLC --random file1.mp4 file2.mp4      # shuffle

# Network streams
$VLC http://example.com/stream.m3u8
$VLC rtsp://camera.local:554/stream
$VLC udp://@:1234
$VLC screen://                         # screen capture
```

### 3. HTTP API (runtime control over network)

Start VLC with HTTP interface:
```bash
$VLC --extraintf http --http-host 127.0.0.1 --http-port 8080 --http-password secret
```

All requests use basic auth (empty username, password as set):
```bash
AUTH=":secret"
BASE="http://127.0.0.1:8080/requests"

# Status (JSON)
curl -s -u "$AUTH" "$BASE/status.json"

# Commands via status.json?command=<cmd>&val=<val>
curl -s -u "$AUTH" "$BASE/status.json?command=pl_play"
curl -s -u "$AUTH" "$BASE/status.json?command=pl_pause"
curl -s -u "$AUTH" "$BASE/status.json?command=pl_stop"
curl -s -u "$AUTH" "$BASE/status.json?command=pl_next"
curl -s -u "$AUTH" "$BASE/status.json?command=pl_previous"
curl -s -u "$AUTH" "$BASE/status.json?command=pl_empty"       # clear playlist
curl -s -u "$AUTH" "$BASE/status.json?command=fullscreen"
curl -s -u "$AUTH" "$BASE/status.json?command=volume&val=200"  # 0-512
curl -s -u "$AUTH" "$BASE/status.json?command=seek&val=120"    # absolute seconds
curl -s -u "$AUTH" "$BASE/status.json?command=seek&val=%2B30"  # relative +30s
curl -s -u "$AUTH" "$BASE/status.json?command=seek&val=-30"    # relative -30s
curl -s -u "$AUTH" "$BASE/status.json?command=rate&val=1.5"    # speed

# Add to playlist
curl -s -u "$AUTH" "$BASE/status.json?command=in_play&input=file:///path/to/file.mp4"
curl -s -u "$AUTH" "$BASE/status.json?command=in_enqueue&input=file:///path/to/file.mp4"

# Playlist (JSON)
curl -s -u "$AUTH" "$BASE/playlist.json"
# Play specific playlist item by id
curl -s -u "$AUTH" "$BASE/status.json?command=pl_play&id=3"
# Delete playlist item
curl -s -u "$AUTH" "$BASE/status.json?command=pl_delete&id=3"

# Snapshot
curl -s -u "$AUTH" "$BASE/status.json?command=snapshot"
```

See `references/http-api.md` for full command list and response format.

### 4. RC Interface (socket/stdin control)

```bash
# Unix socket
$VLC --extraintf rc --rc-unix /tmp/vlc.sock
echo "play" | socat - UNIX-CONNECT:/tmp/vlc.sock

# TCP
$VLC --extraintf rc --rc-host 127.0.0.1:9090
echo "play" | nc 127.0.0.1 9090
```

RC commands: `play`, `stop`, `pause`, `next`, `prev`, `seek <seconds>`, `volume <0-1024>`,
`atrack <id>`, `strack <id>`, `vratio <ratio>`, `snapshot`, `stats`, `info`,
`enqueue <uri>`, `add <uri>`, `playlist`, `clear`, `status`, `quit`

## Audio

```bash
# Audio output
$VLC -A auhal file.mp3                 # CoreAudio (macOS default)

# Volume and gain
$VLC --gain 1.5 file.mp3               # pre-amp gain (0-8)
$VLC --audio-desync -200 file.mp3       # delay audio 200ms

# Stereo mode
$VLC --stereo-mode 1 file.mp3          # 1=stereo 3=left 4=right 5=dolby 6=headphone 7=mono

# Equalizer
$VLC --audio-filter equalizer --equalizer-preset rock file.mp3
# Presets: flat classical club dance fullbass fullbasstreble fulltreble
#          headphones largehall live party pop reggae rock ska soft softrock techno

# Compressor
$VLC --audio-filter compressor \
  --compressor-threshold -20 --compressor-ratio 4 \
  --compressor-attack 25 --compressor-release 100 \
  --compressor-makeup-gain 6 file.mp3

# Spatializer (reverb)
$VLC --audio-filter spatializer \
  --spatializer-roomsize 0.8 --spatializer-width 0.9 \
  --spatializer-wet 0.4 --spatializer-dry 0.5 --spatializer-damp 0.4

# Chain multiple filters
$VLC --audio-filter "equalizer:compressor" --equalizer-preset rock file.mp3

# Replay gain
$VLC --audio-replay-gain-mode track file.mp3
```

## Subtitles

```bash
# External subtitle file
$VLC --sub-file subs.srt video.mp4
$VLC --input-slave subs.srt video.mp4   # alternative

# Track selection
$VLC --sub-track 0 video.mkv            # by index
$VLC --sub-language en video.mkv         # by language code

# Auto-detection
$VLC --sub-autodetect-file video.mp4     # auto-detect subs in same dir
$VLC --sub-autodetect-path ./subs video.mp4

# Subtitle styling
$VLC --freetype-font "Helvetica Neue" --freetype-rel-fontsize 16 \
  --freetype-color 16777215 --freetype-opacity 200 \
  --freetype-outline-thickness 4 video.mp4
# fontsize: 20=smaller 18=small 16=normal 12=large 6=larger
```

## Video

```bash
# Crop and aspect ratio
$VLC --crop 16:9 video.mp4
$VLC --aspect-ratio 4:3 video.mp4

# Filters
$VLC --video-filter "adjust" --contrast 1.2 --brightness 1.1 \
  --saturation 1.3 --hue 10 --gamma 1.0 video.mp4

# Deinterlace
$VLC --deinterlace 1 --deinterlace-mode yadif video.mp4

# Window
$VLC --video-on-top --width 1280 --height 720 video.mp4
$VLC --no-video-deco video.mp4          # borderless window

# Snapshots
$VLC --snapshot-path ~/Pictures --snapshot-format png --snapshot-prefix "vlc_" video.mp4
```

## Streaming & Transcoding

```bash
# Stream to HTTP
$VLC input.mp4 --sout '#standard{access=http,mux=ts,dst=:8090}'

# Transcode + stream
$VLC input.mp4 --sout '#transcode{vcodec=h264,acodec=mp4a,vb=2000,ab=192}:standard{access=http,mux=ts,dst=:8090}'

# Save/convert to file
$VLC input.avi --sout '#transcode{vcodec=h264,acodec=mp4a,vb=2000,ab=128}:standard{access=file,mux=mp4,dst=output.mp4}' --play-and-exit

# Audio extraction
$VLC video.mp4 --no-video --sout '#transcode{acodec=mp3,ab=320}:standard{access=file,mux=raw,dst=output.mp3}' --play-and-exit

# Chromecast
$VLC video.mp4 --sout-chromecast-ip=192.168.1.100

# Duplicate (display + stream)
$VLC input.mp4 --sout '#duplicate{dst=display,dst=standard{access=http,mux=ts,dst=:8090}}'

# RTP multicast
$VLC input.mp4 --sout '#rtp{mux=ts,dst=239.255.0.1,port=5004,sdp=sap}'
```

## Caching & Performance

```bash
$VLC --file-caching 1000 file.mp4           # ms buffer for local files
$VLC --network-caching 3000 stream_url      # ms buffer for network
$VLC --disc-caching 2000 dvd://             # ms buffer for discs
$VLC --live-caching 500 udp://@:1234        # ms buffer for live
$VLC --avcodec-hw videotoolbox video.mp4    # hardware decode (macOS)
```

## macOS-Specific Options

```bash
$VLC --macosx-nativefullscreenmode          # native macOS fullscreen
$VLC --macosx-video-autoresize              # auto-resize window
$VLC --macosx-pause-minimized               # pause when minimised
$VLC --macosx-continue-playback 1           # always resume (0=ask 1=always 2=never)
$VLC --macosx-control-itunes 1              # pause iTunes/Spotify (0=none 1=pause 2=pause+resume)
$VLC --macosx-mediakeys                     # media key support
```

## Config File

Location: `~/Library/Preferences/org.videolan.vlc/vlcrc` (macOS)

Edit with CLI: `$VLC --reset-config` to regenerate defaults.
Preferences set in GUI are written to this file.

## Common Patterns

```bash
# Play folder of music with shuffle
$VLC --random --loop ~/Music/playlist/

# Background audio (no GUI)
$VLC -I dummy --no-video file.mp3

# Watch folder for new files (with RC)
$VLC --extraintf rc --rc-unix /tmp/vlc.sock -I dummy &
echo "add /path/to/new/file.mp4" | socat - UNIX-CONNECT:/tmp/vlc.sock

# Take periodic snapshots
# (via HTTP API in a loop)
while true; do
  curl -s -u ":secret" "http://127.0.0.1:8080/requests/status.json?command=snapshot"
  sleep 10
done
```
