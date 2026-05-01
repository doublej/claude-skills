"""FastAPI wrapper around OmniParser v2.

Runs from inside the OmniParser repo's venv. Loads the YOLO icon detector
and Florence-2 caption model once, then serves /parse for repeated use.

Endpoints:
  GET  /health
  POST /parse  multipart: image=@file.png  query: box_threshold, iou_threshold, imgsz
"""
from __future__ import annotations
import argparse
import base64
import io
import os
import sys
from pathlib import Path

import torch
from fastapi import FastAPI, File, Query, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

# OmniParser repo modules — only importable when CWD is the repo root and
# its .venv is active. serve_omniparser.sh handles that.
try:
    from util.utils import (
        check_ocr_box,
        get_caption_model_processor,
        get_som_labeled_img,
        get_yolo_model,
    )
except ImportError as e:
    print(
        "Cannot import OmniParser util.utils. Run via serve_omniparser.sh, "
        "which activates the venv inside the OmniParser repo.",
        file=sys.stderr,
    )
    raise

DEVICE = os.environ.get(
    "OMNI_DEVICE",
    "mps" if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available() else "cpu",
)
WEIGHTS_DIR = Path(os.environ.get("OMNI_WEIGHTS", "weights"))

print(f"[omniparser] device={DEVICE}  weights={WEIGHTS_DIR.resolve()}")

# Models load once at import — slow first time, fast forever after.
yolo = get_yolo_model(model_path=str(WEIGHTS_DIR / "icon_detect" / "model.pt"))
caption = get_caption_model_processor(
    model_name="florence2",
    model_name_or_path=str(WEIGHTS_DIR / "icon_caption_florence"),
    device=DEVICE,
)

app = FastAPI(title="OmniParser v2 — iPhone Mirroring backend")


@app.get("/health")
def health() -> dict:
    return {"ok": True, "device": DEVICE, "model": "OmniParser-v2.0"}


@app.post("/parse")
async def parse(
    image: UploadFile = File(...),
    box_threshold: float = Query(0.05),
    iou_threshold: float = Query(0.10),
    imgsz: int = Query(1920),
) -> JSONResponse:
    raw = await image.read()
    pil = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = pil.size

    # OmniParser expects to read from disk; write to a tmp path.
    tmp = Path("/tmp/_omni_in.png")
    pil.save(tmp)

    ocr_bbox_rslt, _ = check_ocr_box(
        str(tmp),
        display_img=False,
        output_bb_format="xyxy",
        easyocr_args={"text_threshold": 0.8},
        use_paddleocr=False,
    )
    text, ocr_bbox = ocr_bbox_rslt

    annotated_b64, label_coords, parsed = get_som_labeled_img(
        str(tmp),
        yolo,
        BOX_TRESHOLD=box_threshold,
        output_coord_in_ratio=False,
        ocr_bbox=ocr_bbox,
        draw_bbox_config=None,
        caption_model_processor=caption,
        ocr_text=text,
        iou_threshold=iou_threshold,
        imgsz=imgsz,
        use_local_semantics=True,
    )

    # parsed is a list of dicts with keys like 'type', 'bbox', 'content', 'interactivity'.
    # Normalize to our schema.
    elements = []
    for i, p in enumerate(parsed):
        bb = p.get("bbox") or p.get("bbox_in_pixel") or [0, 0, 0, 0]
        # Some OmniParser builds return normalized coords; rescale if needed.
        x1, y1, x2, y2 = bb
        if max(bb) <= 1.0:
            x1, x2 = x1 * w, x2 * w
            y1, y2 = y1 * h, y2 * h
        elements.append({
            "id": i,
            "bbox": [round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)],
            "bbox_norm": [round(x1 / w, 4), round(y1 / h, 4), round(x2 / w, 4), round(y2 / h, 4)],
            "label": p.get("content") or p.get("text") or "",
            "type": p.get("type") or "icon",
            "interactable": bool(p.get("interactivity", True)),
            "confidence": round(float(p.get("confidence", 1.0)), 3),
        })

    return JSONResponse({
        "elements": elements,
        "annotated_b64": annotated_b64,
        "size": [w, h],
    })


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
