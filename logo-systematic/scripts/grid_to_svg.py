#!/usr/bin/env python3
"""
Grid-to-SVG converter for systematic logo design.

Usage:
    python3 grid_to_svg.py input.json [output.svg]
    cat input.json | python3 grid_to_svg.py

JSON schema:
    {
      "brand": "Acme",
      "grid": 5,
      "palette": { "a": "#1a1a1a", "b": "#0066ff" },
      "cells": [
        { "r": 0, "c": 1, "w": 3, "h": 1, "color": "a" },
        { "r": 2, "c": 2, "shape": "circle", "color": "b" }
      ],
      "text": { "content": "ACME", "position": "right", "color": "a", "size": 0.6 }
    }
"""

import json
import sys
from pathlib import Path

SHAPES = {"rect", "circle", "triangle-up", "triangle-down", "triangle-left", "triangle-right", "diamond"}
CELL_SIZE = 100
CELL_GAP = 4
MAX_COLOURS = 4  # 3 + transparent


def validate_grid(data: dict) -> list[str]:
    errors = []
    grid = data.get("grid", 5)
    if not 3 <= grid <= 9:
        errors.append(f"grid must be 3-9, got {grid}")

    palette = data.get("palette", {})
    if len(palette) > MAX_COLOURS:
        errors.append(f"max {MAX_COLOURS} palette entries, got {len(palette)}")

    for cell in data.get("cells", []):
        r, c = cell.get("r", 0), cell.get("c", 0)
        w, h = cell.get("w", 1), cell.get("h", 1)
        if r < 0 or c < 0 or r + h > grid or c + w > grid:
            errors.append(f"cell at ({r},{c}) w={w} h={h} out of {grid}x{grid} bounds")
        shape = cell.get("shape", "rect")
        if shape not in SHAPES:
            errors.append(f"unknown shape '{shape}', valid: {sorted(SHAPES)}")
        color_key = cell.get("color")
        if color_key and color_key not in palette:
            errors.append(f"color key '{color_key}' not in palette")

    return errors


def cell_to_svg(cell: dict, palette: dict) -> str:
    r, c = cell.get("r", 0), cell.get("c", 0)
    w, h = cell.get("w", 1), cell.get("h", 1)
    shape = cell.get("shape", "rect")
    fill = palette.get(cell.get("color", ""), "#000000")

    x = c * CELL_SIZE + CELL_GAP / 2
    y = r * CELL_SIZE + CELL_GAP / 2
    bw = w * CELL_SIZE - CELL_GAP
    bh = h * CELL_SIZE - CELL_GAP
    cx = x + bw / 2
    cy = y + bh / 2

    if shape == "rect":
        return f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="{fill}"/>'

    if shape == "circle":
        radius = min(bw, bh) / 2
        return f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}"/>'

    if shape == "diamond":
        pts = f"{cx},{y} {x + bw},{cy} {cx},{y + bh} {x},{cy}"
        return f'<polygon points="{pts}" fill="{fill}"/>'

    # Triangles
    triangles = {
        "triangle-up": f"{cx},{y} {x + bw},{y + bh} {x},{y + bh}",
        "triangle-down": f"{x},{y} {x + bw},{y} {cx},{y + bh}",
        "triangle-left": f"{x + bw},{y} {x + bw},{y + bh} {x},{cy}",
        "triangle-right": f"{x},{y} {x + bw},{cy} {x},{y + bh}",
    }
    pts = triangles[shape]
    return f'<polygon points="{pts}" fill="{fill}"/>'


def text_to_svg(text: dict, grid: int, palette: dict) -> str:
    content = text.get("content", "")
    if not content:
        return ""

    fill = palette.get(text.get("color", ""), "#000000")
    size_ratio = text.get("size", 0.6)
    position = text.get("position", "right")
    font = text.get("font", "sans-serif")
    weight = text.get("weight", "bold")
    grid_px = grid * CELL_SIZE
    font_size = round(grid_px * size_ratio / max(len(content), 1) * 1.8)
    font_size = min(font_size, round(grid_px * 0.3))

    if position == "right":
        tx = grid_px + CELL_SIZE * 0.5
        ty = grid_px / 2
        anchor = "start"
        baseline = "central"
    elif position == "below":
        tx = grid_px / 2
        ty = grid_px + font_size * 1.2
        anchor = "middle"
        baseline = "hanging"
    elif position == "above":
        tx = grid_px / 2
        ty = -font_size * 0.4
        anchor = "middle"
        baseline = "alphabetic"
    else:  # center
        tx = grid_px / 2
        ty = grid_px / 2
        anchor = "middle"
        baseline = "central"

    return (
        f'<text x="{tx}" y="{ty}" fill="{fill}" '
        f'font-size="{font_size}" font-family="{font}" '
        f'font-weight="{weight}" text-anchor="{anchor}" '
        f'dominant-baseline="{baseline}">{content}</text>'
    )


def generate_svg(data: dict) -> str:
    brand = data.get("brand", "Logo")
    grid = data.get("grid", 5)
    palette = data.get("palette", {})
    cells = data.get("cells", [])
    text = data.get("text")

    cell_elements = [cell_to_svg(c, palette) for c in cells]

    grid_px = grid * CELL_SIZE
    vb_w = grid_px
    vb_h = grid_px

    text_el = ""
    if text:
        text_el = text_to_svg(text, grid, palette)
        pos = text.get("position", "right")
        if pos == "right":
            vb_w = grid_px + CELL_SIZE * (max(len(text.get("content", "")), 3))
        elif pos == "below":
            font_size = round(grid_px * text.get("size", 0.6) / max(len(text.get("content", "")), 1) * 1.8)
            font_size = min(font_size, round(grid_px * 0.3))
            vb_h = grid_px + font_size * 2

    lines = [
        f'<svg viewBox="0 0 {vb_w} {vb_h}" xmlns="http://www.w3.org/2000/svg">',
        f"  <title>{brand} Logo</title>",
        '  <g id="mark">',
    ]
    for el in cell_elements:
        lines.append(f"    {el}")
    lines.append("  </g>")

    if text_el:
        lines.append('  <g id="text">')
        lines.append(f"    {text_el}")
        lines.append("  </g>")

    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        raw = Path(sys.argv[1]).read_text()
    else:
        raw = sys.stdin.read()

    data = json.loads(raw)
    errors = validate_grid(data)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    svg = generate_svg(data)

    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(svg)
        print(f"saved: {sys.argv[2]}")
    else:
        print(svg)


if __name__ == "__main__":
    main()
