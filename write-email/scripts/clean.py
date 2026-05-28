#!/usr/bin/env python3
"""Strip AI watermarks and slop punctuation from email text.

Mirrors raycast/raycast-ext-clean-watermark/src/clean-watermark.tsx — same
Unicode codepoints, same em-dash rules, same NFKC normalization. Reads stdin,
writes cleaned text to stdout, prints a one-line removal summary to stderr.

Usage:
    python3 clean.py < draft.txt > cleaned.txt
    echo "$DRAFT" | python3 clean.py
"""

from __future__ import annotations

import re
import sys
import unicodedata

ZERO_WIDTH = [
    "​", "‌", "‍", "﻿", "⁠",
    " ", " ", " ", " ", " ",
    " ", " ", " ", " ", " ",
    " ", " ", " ", " ", "᠎",
    "؜", "‎", "‏", "‪", "‫",
    "‬", "‭", "‮",
]
NBSP = " "

RTF_PATTERNS = [
    r"\\rtf\d+", r"\\ansi", r"\\deff\d+", r"\\deflang\d+",
    r"\\fonttbl[^}]*}", r"\\colortbl[^}]*}", r"\\f\d+", r"\\fs\d+",
    r"\\cf\d+", r"\\cb\d+", r"\\highlight\d+", r"\\strike\d*",
    r"\\par\b", r"\\pard\b", r"\\sa\d+", r"\\sb\d+", r"\\sl\d+",
    r"\\qc\b", r"\\ql\b", r"\\qr\b", r"\\qj\b",
]

FONT_PATTERNS = [
    r"<font[^>]*>", r"</font>",
    r"font-family:[^;\"'\s]*[;\"']?", r"font-size:[^;\"'\s]*[;\"']?",
    r"font-weight:[^;\"'\s]*[;\"']?", r"font-style:[^;\"'\s]*[;\"']?",
    r"color:[^;\"'\s]*[;\"']?",
]

FORMATTING_PATTERNS = [
    r"background[^;\"'\s]*:[^;\"'\s]*[;\"']?",
    r"background-color:[^;\"'\s]*[;\"']?",
    r"style\s*=\s*[\"'][^\"']*[\"']",
    r"class\s*=\s*[\"'][^\"']*[\"']",
    r"<meta[^>]*>", r"<span[^>]*>", r"</span>",
    r"<div[^>]*>", r"</div>", r"<p[^>]*>", r"</p>",
]

GUID_RE = re.compile(r"[A-F0-9]{8}(?:-[A-F0-9]{4}){3}-[A-F0-9]{12}", re.IGNORECASE)
NON_PRINTABLE = re.compile(r"[^\t\n\r\x20-\x7E]+")


def clean(text: str) -> tuple[str, list[str]]:
    parts: list[str] = []
    before = len(text)

    text = unicodedata.normalize("NFKC", text)

    spaced = len(re.findall(r" —", text))
    text = re.sub(r" —", ",", text)
    bare = text.count("—")
    text = text.replace("—", ", ")
    if spaced:
        parts.append(f"{spaced} spaced em-dash")
    if bare:
        parts.append(f"{bare} bare em-dash")

    zw_count = 0
    for zw in ZERO_WIDTH:
        n = text.count(zw)
        if n:
            zw_count += n
            text = text.replace(zw, " " if zw == NBSP else "")
    if zw_count:
        parts.append(f"{zw_count} zero-width")

    ctrl = sum(len(m) for m in NON_PRINTABLE.findall(text))
    text = NON_PRINTABLE.sub("", text)
    if ctrl:
        parts.append(f"{ctrl} control")

    guids = len(GUID_RE.findall(text))
    text = GUID_RE.sub("", text)
    if guids:
        parts.append(f"{guids} guid")

    font_count = 0
    for p in RTF_PATTERNS + FONT_PATTERNS:
        rx = re.compile(p, re.IGNORECASE)
        font_count += len(rx.findall(text))
        text = rx.sub("", text)
    if font_count:
        parts.append(f"{font_count} font")

    fmt_count = 0
    for p in FORMATTING_PATTERNS:
        rx = re.compile(p, re.IGNORECASE)
        fmt_count += len(rx.findall(text))
        text = rx.sub("", text)
    if fmt_count:
        parts.append(f"{fmt_count} formatting")

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = text.strip()

    removed = before - len(text)
    if removed:
        parts.insert(0, f"{removed} chars")

    return text, parts


def main() -> int:
    data = sys.stdin.read()
    if not data.strip():
        print("clean.py: empty input", file=sys.stderr)
        return 1
    cleaned, parts = clean(data)
    sys.stdout.write(cleaned)
    if not cleaned.endswith("\n"):
        sys.stdout.write("\n")
    summary = ", ".join(parts) if parts else "nothing removed"
    print(f"clean.py: {summary}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
