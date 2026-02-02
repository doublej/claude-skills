#!/usr/bin/env python3
"""Render Mermaid diagrams to PNG, SVG, or PDF using mermaid-cli (mmdc)."""

import argparse
import subprocess
import sys
import shutil
from pathlib import Path


def check_mmdc():
    """Check if mmdc is available."""
    if shutil.which("mmdc"):
        return "mmdc"
    npx = shutil.which("npx")
    if npx:
        return ["npx", "-p", "@mermaid-js/mermaid-cli", "mmdc"]
    return None


def render(input_file: str, output_file: str, theme: str = "default",
           bg_color: str = "white", width: int = 800, height: int = 600):
    """Render a .mmd file to image."""
    mmdc = check_mmdc()
    if not mmdc:
        print("Error: mermaid-cli not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

    cmd = mmdc if isinstance(mmdc, list) else [mmdc]
    cmd.extend(["-i", input_file, "-o", output_file, "-t", theme, "-b", bg_color,
                "-w", str(width), "-H", str(height)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(f"Rendered: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Render Mermaid diagram to image")
    parser.add_argument("input", help="Input .mmd file")
    parser.add_argument("-o", "--output", help="Output file (svg/png/pdf)")
    parser.add_argument("-t", "--theme", default="default",
                        choices=["default", "forest", "dark", "neutral"])
    parser.add_argument("-b", "--background", default="white")
    parser.add_argument("-w", "--width", type=int, default=800)
    parser.add_argument("-H", "--height", type=int, default=600)

    args = parser.parse_args()
    input_path = Path(args.input)
    output = args.output or str(input_path.with_suffix(".svg"))

    render(args.input, output, args.theme, args.background, args.width, args.height)


if __name__ == "__main__":
    main()
