---
name: transcript-capture
description: Capture Claude Code session transcripts from JSONL session files. Extract AI assistant output, tool calls, and conversation text for use as creative or documentary content. Use when you need to capture "making of" footage from a Claude session.
---

# Transcript Capture

Reads Claude Code session JSONL files and extracts conversation content into structured text for downstream use (video content, documentation, logging).

## Session File Location

```
~/.claude/projects/<encoded-path>/*.jsonl
```

Encoded path: replace `/` with `-` in the absolute project path.

Example for `/Users/jurrejan/Documents/development/_management/claude-skills`:
```
~/.claude/projects/-Users-jurrejan-Documents-development--management-claude-skills/
```

## Capture Script

Use `scripts/capture_session.py` to extract the current or most recent session.

```bash
# Capture most recent session to stdout
python3 scripts/capture_session.py

# Capture to file (for video pipeline)
python3 scripts/capture_session.py --out /tmp/session_transcript.txt

# Capture specific session
python3 scripts/capture_session.py --session <uuid>.jsonl
```

## JSONL Format

Each line is a JSON object. Relevant fields:
```json
{"type": "message", "role": "assistant", "content": [{"type": "text", "text": "..."}]}
{"type": "tool_use", "name": "Write", "input": {...}}
{"type": "tool_result", "content": [...]}
```

## Workflow

1. Find session file: `ls -t ~/.claude/projects/<encoded-path>/*.jsonl | head -1`
2. Run `capture_session.py --out transcript.txt`
3. Filter to assistant text-only output for display
4. Pass to `lyric-video-maker` as overlay content
