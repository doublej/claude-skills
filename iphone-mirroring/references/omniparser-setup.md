# OmniParser v2 — Local Server Setup

OmniParser v2 = YOLO icon detector + Florence-2 caption model. We run it as a small FastAPI service so the skill can POST screenshots and get back labeled JSON + an annotated PNG.

## One-time install

```bash
# 1. Pick an install root (this skill defaults to ~/.local/omniparser)
export OMNI_ROOT="${OMNI_ROOT:-$HOME/.local/omniparser}"
mkdir -p "$OMNI_ROOT" && cd "$OMNI_ROOT"

# 2. Clone
git clone https://github.com/microsoft/OmniParser.git repo
cd repo

# 3. Python env (uv is faster than conda for this)
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install fastapi uvicorn python-multipart pillow huggingface_hub

# 4. Download v2 weights
mkdir -p weights
huggingface-cli download microsoft/OmniParser-v2.0 \
  icon_detect/train_args.yaml icon_detect/model.pt icon_detect/model.yaml \
  icon_caption/config.json icon_caption/generation_config.json icon_caption/model.safetensors \
  --local-dir weights
mv weights/icon_caption weights/icon_caption_florence
```

Apple Silicon notes:
- The YOLO detector falls back to CPU on macOS unless you build PyTorch with MPS for the model's ops. CPU is fast enough at 2–4 fps on M-series for this pipeline.
- If `torch.backends.mps.is_available()` is True, set `OMNI_DEVICE=mps` to enable it where supported.

## Running the server

```bash
bash scripts/serve_omniparser.sh   # foreground, logs to stdout
# or
nohup bash scripts/serve_omniparser.sh > /tmp/omniparser.log 2>&1 &
```

Health check:
```bash
curl -fsS http://127.0.0.1:8765/health
# {"ok": true, "device": "mps", "model": "OmniParser-v2.0"}
```

Parse a screenshot:
```bash
curl -X POST -F "image=@/tmp/iphone-mirror/capture.png" \
  http://127.0.0.1:8765/parse | jq '.elements[:3]'
```

## API contract

`POST /parse`
- multipart form: `image` (PNG/JPEG)
- query: `box_threshold=0.05` `iou_threshold=0.1` `imgsz=1920`

Response:
```json
{
  "elements": [
    {
      "id": 0,
      "bbox": [120, 340, 220, 440],
      "bbox_norm": [0.10, 0.30, 0.18, 0.39],
      "label": "Settings icon",
      "type": "icon",
      "interactable": true,
      "confidence": 0.91
    }
  ],
  "annotated_b64": "<base64 PNG with numbered overlays>",
  "size": [1170, 2532]
}
```

`bbox` is in **screenshot pixel coordinates** (origin top-left). Convert to **window pixels** then **screen pixels** in `act.py` — see `coordinate-translation.md`.

## Common problems

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: ultralytics` | `uv pip install ultralytics` |
| Server crashes on first request, "AGPL model" warning | Expected log, ignore — icon_detect is YOLO-AGPL but we're not redistributing |
| Detector returns 0 elements | Lower `box_threshold` to 0.03; upscale screenshot to 2x |
| Captions are nonsense | Florence model load failed silently — check that `weights/icon_caption_florence/model.safetensors` exists |
| Server slow on first request | Florence model warmup, ~6–10s. Subsequent requests ~300–800ms on M-series |

## Updating

OmniParser updates sometimes break the API. Pin to a known-good commit:

```bash
cd "$OMNI_ROOT/repo"
git log --oneline -5
git checkout <known-good-sha>
```
