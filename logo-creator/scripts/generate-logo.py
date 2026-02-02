#!/usr/bin/env python3
"""
Logo Generator Template

Usage:
    python generate-logo.py [output_path]

Generates an SVG logo using only Python standard library.
Customize the generate_elements() function for your brand.
"""

import sys
from pathlib import Path


def svg_circle(cx: float, cy: float, r: float, fill: str) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'


def svg_rect(x: float, y: float, w: float, h: float, fill: str, rx: float = 0) -> str:
    rx_attr = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{rx_attr}/>'


def svg_path(d: str, fill: str) -> str:
    return f'<path d="{d}" fill="{fill}"/>'


def svg_polygon(points: list[tuple[float, float]], fill: str) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}"/>'


def svg_text(
    x: float,
    y: float,
    text: str,
    fill: str,
    font_size: float = 48,
    font_family: str = "sans-serif",
    font_weight: str = "bold",
    anchor: str = "middle",
) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" '
        f'font-size="{font_size}" font-family="{font_family}" '
        f'font-weight="{font_weight}" text-anchor="{anchor}" '
        f'dominant-baseline="central">{text}</text>'
    )


def generate_elements(width: float, height: float, colors: dict) -> list[str]:
    """
    Customize this function to create your logo geometry.

    Args:
        width: Canvas width
        height: Canvas height
        colors: Dict with 'primary', 'secondary', 'accent' hex colors

    Returns:
        List of SVG element strings
    """
    elements = []
    cx, cy = width / 2, height / 2

    # Example: Abstract geometric mark
    # Replace this with your actual logo geometry

    # Outer circle
    elements.append(svg_circle(cx, cy, 200, colors["primary"]))

    # Inner geometric shape
    elements.append(
        svg_polygon(
            [
                (cx, cy - 120),  # top
                (cx + 104, cy + 60),  # bottom right
                (cx - 104, cy + 60),  # bottom left
            ],
            colors["secondary"],
        )
    )

    return elements


def generate_logo(
    output_path: str = "logo.svg",
    brand_name: str = "Brand",
    width: int = 512,
    height: int = 512,
    primary: str = "#1a1a1a",
    secondary: str = "#ffffff",
    accent: str = "#0066ff",
) -> None:
    """Generate logo SVG file."""

    colors = {"primary": primary, "secondary": secondary, "accent": accent}
    elements = generate_elements(width, height, colors)

    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
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
