#!/usr/bin/env python3
"""
Mathematical Logo Generator

Constructs logos from geometric first principles using grid systems,
tangency, Bézier continuity, and parametric curves.

Usage:
    python generate-logo.py [output_path]

No external dependencies. Standard library only.
"""

import math
import sys
from pathlib import Path

# Bézier circle approximation constant (quarter-arc)
KAPPA = 4 * (math.sqrt(2) - 1) / 3  # ≈ 0.55228475


# --- Grid System ---

class Grid:
    """Module grid for quantized logo construction."""

    def __init__(self, canvas: int = 1000, divisions: int = 24):
        self.S = canvas
        self.N = divisions
        self.m = canvas / divisions

    def snap(self, v: float, resolution: float = 0.5) -> float:
        """Snap value to grid. resolution=0.5 means half-module steps."""
        step = self.m * resolution
        return round(v / step) * step

    def snap_pt(self, x: float, y: float, resolution: float = 0.5) -> tuple[float, float]:
        return self.snap(x, resolution), self.snap(y, resolution)


# --- Tangency ---

def fillet_params(theta: float, r: float) -> tuple[float, float]:
    """Tangent fillet for two lines meeting at angle theta with radius r.
    Returns (t, d): tangent distance from vertex, center distance from vertex."""
    half = theta / 2
    return r / math.tan(half), r / math.sin(half)


def circle_tangent_to_two_circles(
    c1: tuple[float, float], r1: float,
    c2: tuple[float, float], r2: float,
    r: float,
    external: bool = True,
) -> list[tuple[float, float]]:
    """Find centers of circle with radius r tangent to two circles.
    Returns 0-2 solutions."""
    r1p = r1 + r if external else abs(r1 - r)
    r2p = r2 + r if external else abs(r2 - r)

    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    if d < 1e-9 or d > r1p + r2p or d < abs(r1p - r2p):
        return []

    a = (r1p**2 - r2p**2 + d**2) / (2 * d)
    h_sq = r1p**2 - a**2
    if h_sq < 0:
        return []
    h = math.sqrt(h_sq)

    ux, uy = dx / d, dy / d
    mx, my = c1[0] + a * ux, c1[1] + a * uy

    if h < 1e-9:
        return [(mx, my)]
    return [
        (mx + h * (-uy), my + h * ux),
        (mx - h * (-uy), my - h * uy),
    ]


# --- Optical Corrections ---

def overshoot(extent: float, factor: float = 0.015) -> float:
    """Round shapes extend past flat baselines by this amount."""
    return extent * factor


def optical_center(bbox_min: float, bbox_max: float, offset_pct: float = 0.02) -> float:
    """Shift geometric center slightly upward/lighter side."""
    geo = (bbox_min + bbox_max) / 2
    return geo - (bbox_max - bbox_min) * offset_pct


def h_stroke_compensation(v_width: float, factor: float = 0.9) -> float:
    """Horizontal strokes thinner than vertical to appear equal."""
    return v_width * factor


# --- Parametric Curves ---

def polar_fourier(
    n: int, a: float, r0: float = 1.0, points: int = 360,
) -> list[tuple[float, float]]:
    """Generate points on a polar Fourier curve: r(θ) = r0 + a*cos(n*θ)."""
    result = []
    for i in range(points):
        theta = 2 * math.pi * i / points
        r = r0 + a * math.cos(n * theta)
        result.append((r * math.cos(theta), r * math.sin(theta)))
    return result


def superellipse(
    a: float, b: float, p: float, points: int = 360,
) -> list[tuple[float, float]]:
    """Generate points on superellipse |x/a|^p + |y/b|^p = 1."""
    result = []
    for i in range(points):
        theta = 2 * math.pi * i / points
        ct, st = math.cos(theta), math.sin(theta)
        x = a * _sign(ct) * abs(ct) ** (2 / p)
        y = b * _sign(st) * abs(st) ** (2 / p)
        result.append((x, y))
    return result


def _sign(v: float) -> float:
    return 1.0 if v > 0 else (-1.0 if v < 0 else 0.0)


# --- SVG Primitives ---

def svg_circle_path(cx: float, cy: float, r: float) -> str:
    """Circle as cubic Bézier path (4 quarter-arcs), not <circle>."""
    k = KAPPA * r
    return (
        f"M {cx+r},{cy} "
        f"C {cx+r},{cy+k} {cx+k},{cy+r} {cx},{cy+r} "
        f"C {cx-k},{cy+r} {cx-r},{cy+k} {cx-r},{cy} "
        f"C {cx-r},{cy-k} {cx-k},{cy-r} {cx},{cy-r} "
        f"C {cx+k},{cy-r} {cx+r},{cy-k} {cx+r},{cy} Z"
    )


def svg_path(d: str, fill: str) -> str:
    return f'<path d="{d}" fill="{fill}"/>'


def svg_group(elements: list[str], transform: str = "") -> str:
    tx = f' transform="{transform}"' if transform else ""
    inner = "\n    ".join(elements)
    return f"<g{tx}>\n    {inner}\n  </g>"


def svg_letterform(d: str, fill: str, transform: str = "") -> str:
    """Single letter as path data — construct on the logo grid, not as <text>."""
    tx = f' transform="{transform}"' if transform else ""
    return f'<path d="{d}" fill="{fill}"{tx}/>'


def svg_wordmark(letters: list[str], fill: str, x_offset: float = 0, y_offset: float = 0) -> str:
    """Group letter paths into a single wordmark unit."""
    tx = f' transform="translate({x_offset},{y_offset})"' if x_offset or y_offset else ""
    paths = "\n    ".join(f'<path d="{d}" fill="{fill}"/>' for d in letters)
    return f'<g{tx}>\n    {paths}\n  </g>'


def points_to_path(pts: list[tuple[float, float]], close: bool = True) -> str:
    """Convert point list to SVG path (line segments)."""
    if not pts:
        return ""
    d = f"M {pts[0][0]:.2f},{pts[0][1]:.2f}"
    for x, y in pts[1:]:
        d += f" L {x:.2f},{y:.2f}"
    if close:
        d += " Z"
    return d


# --- Logo Generator ---

def generate_elements(grid: Grid, colors: dict) -> list[str]:
    """
    Customise this function for your logo.

    Uses the grid module system and construction helpers above.
    """
    elements = []
    cx, cy = grid.S / 2, grid.S / 2

    # Example: 6-fold polar Fourier mark
    pts = polar_fourier(n=6, a=0.18, r0=1.0, points=360)

    # Scale to grid
    r_outer = grid.snap(grid.S * 0.4)
    scaled = [(cx + x * r_outer, cy + y * r_outer) for x, y in pts]
    elements.append(svg_path(points_to_path(scaled), colors["primary"]))

    # Inner void (negative space)
    r_inner = grid.snap(r_outer * 0.55)
    inner_pts = [(cx + x * r_inner, cy + y * r_inner) for x, y in pts]
    elements.append(svg_path(points_to_path(inner_pts), colors["secondary"]))

    return elements


def generate_logo(
    output_path: str = "logo.svg",
    brand_name: str = "Brand",
    canvas: int = 1000,
    divisions: int = 24,
    primary: str = "#1a1a1a",
    secondary: str = "#ffffff",
    accent: str = "#0066ff",
) -> None:
    grid = Grid(canvas, divisions)
    colors = {"primary": primary, "secondary": secondary, "accent": accent}
    elements = generate_elements(grid, colors)

    svg = f"""<svg viewBox="0 0 {canvas} {canvas}" xmlns="http://www.w3.org/2000/svg">
  <title>{brand_name} Logo</title>
  {chr(10).join(f"  {el}" for el in elements)}
</svg>"""

    Path(output_path).write_text(svg)
    print(f"Logo saved: {output_path}")


def main() -> None:
    output = sys.argv[1] if len(sys.argv) > 1 else "logo.svg"
    generate_logo(output_path=output)


if __name__ == "__main__":
    main()
