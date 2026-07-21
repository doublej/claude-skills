#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "pillow", "scipy"]
# ///
"""Detect typography problems in UI screenshots via pixel analysis.

Finds text lines, estimates font size / stroke weight / line measure /
letter-spacing per line, clusters sizes, and flags the classic agent-design
failures: sizes too similar (weak hierarchy), text too small, lines too wide.
No OCR, no DOM — pixels only.
"""

import argparse
import json
import statistics
import sys
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

# Cap-height as a fraction of em for common UI fonts (Helvetica/Inter/SF ~0.70-0.73)
CAP_RATIO = 0.72
# Mixed-case detector: ascender height / x-height ratio threshold
MIXED_CASE_RATIO = 1.22
# Relative gap that separates two font-size clusters
CLUSTER_GAP = 1.12


@dataclass
class Glyph:
    x0: int
    y0: int
    x1: int  # exclusive
    y1: int
    area: int

    @property
    def w(self) -> int:
        return self.x1 - self.x0

    @property
    def h(self) -> int:
        return self.y1 - self.y0


@dataclass
class Line:
    glyphs: list[Glyph]
    polarity: str  # "dark" (dark text on light) or "light"
    em: float = 0.0  # estimated font size, device px
    weight: float = 0.0  # stroke width / em
    advance: float = 0.0  # estimated char advance, device px
    max_cpl: float = 0.0  # chars per line of the longest run
    max_run_w: float = 0.0  # widest continuous run, device px
    tracking: float = 0.0  # median intra-word ink gap / em
    chars: int = 0  # rough char count
    cluster: int = -1

    @property
    def x0(self) -> int:
        return min(g.x0 for g in self.glyphs)

    @property
    def x1(self) -> int:
        return max(g.x1 for g in self.glyphs)

    @property
    def y0(self) -> int:
        return min(g.y0 for g in self.glyphs)

    @property
    def y1(self) -> int:
        return max(g.y1 for g in self.glyphs)

    @property
    def bbox(self) -> list[int]:
        return [self.x0, self.y0, self.x1, self.y1]


@dataclass
class Cluster:
    em: float  # weighted mean font size, device px
    weight: float  # mean stroke-weight ratio
    lines: list[Line] = field(default_factory=list)

    @property
    def chars(self) -> int:
        return sum(ln.chars for ln in self.lines)


def binarize(gray: np.ndarray, window: int, delta: float) -> dict[str, np.ndarray]:
    local_mean = ndimage.uniform_filter(gray, size=window)
    return {
        "dark": gray < local_mean - delta,
        "light": gray > local_mean + delta,
    }


def extract_glyphs(ink: np.ndarray) -> list[Glyph]:
    labels, n = ndimage.label(ink, structure=np.ones((3, 3), dtype=int))
    if n == 0:
        return []
    slices = ndimage.find_objects(labels)
    areas = ndimage.sum_labels(ink, labels, index=np.arange(1, n + 1))
    img_area = ink.shape[0] * ink.shape[1]
    glyphs = []
    for sl, area in zip(slices, areas):
        y0, y1 = sl[0].start, sl[0].stop
        x0, x1 = sl[1].start, sl[1].stop
        w, h = x1 - x0, y1 - y0
        if not (4 <= h <= 200):
            continue
        if w < 1 or w > 400:
            continue
        if area < 4 or area > 0.05 * img_area:
            continue
        fill = area / (w * h)
        if not (0.08 <= fill <= 0.98):  # excludes solid blocks and sparse noise
            continue
        if w / h > 10 or h / w > 40:  # rules, dividers
            continue
        glyphs.append(Glyph(x0, y0, x1, y1, int(area)))
    return glyphs


def group_lines(glyphs: list[Glyph], polarity: str) -> list[Line]:
    """Greedy left-to-right sweep: attach each glyph to a vertically overlapping
    open line within horizontal reach, else start a new line."""
    glyphs = sorted(glyphs, key=lambda g: g.x0)
    open_lines: list[dict] = []  # {top, bottom, h_med, x_right, glyphs}
    done: list[Line] = []

    for g in glyphs:
        best = None
        best_overlap = 0.0
        for ln in open_lines:
            if g.x0 - ln["x_right"] > 3.0 * ln["h_med"]:
                continue
            ov = min(g.y1, ln["bottom"]) - max(g.y0, ln["top"])
            denom = min(g.h, ln["bottom"] - ln["top"])
            if denom <= 0:
                continue
            ov_frac = ov / denom
            if ov_frac < 0.5:
                continue
            if not (0.35 <= g.h / ln["h_med"] <= 2.8):  # don't merge huge with tiny
                continue
            if ov_frac > best_overlap:
                best_overlap, best = ov_frac, ln
        if best is None:
            open_lines.append(
                {"top": g.y0, "bottom": g.y1, "h_med": float(g.h),
                 "x_right": g.x1, "glyphs": [g]}
            )
        else:
            best["glyphs"].append(g)
            best["x_right"] = max(best["x_right"], g.x1)
            hs = [gl.h for gl in best["glyphs"]]
            best["h_med"] = float(statistics.median(hs))
            tops = [gl.y0 for gl in best["glyphs"]]
            bots = [gl.y1 for gl in best["glyphs"]]
            best["top"] = statistics.median(tops)
            best["bottom"] = statistics.median(bots)
        # retire lines far behind the sweep to keep the scan fast
        if len(open_lines) > 64:
            keep = []
            for ln in open_lines:
                if g.x0 - ln["x_right"] > 6.0 * ln["h_med"]:
                    done.append(Line(ln["glyphs"], polarity))
                else:
                    keep.append(ln)
            open_lines = keep

    done.extend(Line(ln["glyphs"], polarity) for ln in open_lines)
    return [ln for ln in done if len(ln.glyphs) >= 3]


def measure_line(line: Line, ink: np.ndarray) -> bool:
    """Fill in em, weight, advance, cpl, tracking, chars. False → discard as noise."""
    hs = sorted(g.h for g in line.glyphs)
    h_med = hs[len(hs) // 2]
    body_hs = [h for h in hs if h >= 0.3 * h_med]  # drop dots and punctuation
    if len(body_hs) < 3:
        return False
    mean_h = statistics.fmean(body_hs)
    if mean_h > 0 and statistics.pstdev(body_hs) / mean_h > 0.45:
        return False  # heights too erratic — likely graphics, not a text line
    h50 = float(np.percentile(body_hs, 50))
    h80 = float(np.percentile(body_hs, 80))
    if h80 / max(h50, 1.0) >= MIXED_CASE_RATIO:
        line.em = h80 / CAP_RATIO  # mixed case: tall glyphs are caps/ascenders
    else:
        line.em = h50 / 0.70  # uniform heights: assume caps/digits
    if line.em < 5:
        return False

    # Stroke width from ink area / perimeter (robust at small sizes where a
    # distance transform is quantization-floored): ribbon of width w has
    # area ≈ L*w and edge ≈ 2L, so w ≈ 2 * area / edge.
    pad = 2
    y0, y1 = max(0, line.y0 - pad), min(ink.shape[0], line.y1 + pad)
    x0, x1 = max(0, line.x0 - pad), min(ink.shape[1], line.x1 + pad)
    crop = ink[y0:y1, x0:x1]
    area = int(crop.sum())
    if area:
        edge = area - int(ndimage.binary_erosion(crop).sum())
        line.weight = (2.0 * area / max(edge, 1)) / line.em
    else:
        line.weight = 0.0

    # Provisional advance for run-splitting; refined from measured gaps below
    narrow = [g.w for g in line.glyphs if g.w / g.h <= 1.6 and g.h >= 0.5 * h_med]
    w_med = statistics.median(narrow) if len(narrow) >= 5 else 0.55 * line.em
    provisional = min(max(w_med * 1.35, 0.40 * line.em), 0.75 * line.em)

    # Split into runs at large gaps (columns, nav items, table cells)
    xs = sorted((g.x0, g.x1) for g in line.glyphs)
    runs: list[list[int]] = [[xs[0][0], xs[0][1]]]
    gaps: list[float] = []
    for a, b in xs[1:]:
        gap = a - runs[-1][1]
        if gap > 2.2 * provisional:
            runs.append([a, b])
        else:
            if 0 < gap < provisional:
                gaps.append(gap)
            runs[-1][1] = max(runs[-1][1], b)

    # True advance ≈ char ink width + intra-word ink gap (side bearings)
    if len(narrow) >= 5 and len(gaps) >= 4:
        line.advance = min(max(w_med + statistics.median(gaps), 0.35 * line.em),
                           0.75 * line.em)
    else:
        line.advance = provisional
    cpls = [(r[1] - r[0]) / line.advance + 1 for r in runs]
    line.chars = int(round(sum(cpls)))
    long_runs = [c for c in cpls if c >= 20]
    line.max_cpl = max(long_runs) if long_runs else max(cpls)
    line.max_run_w = max(r[1] - r[0] for r in runs)
    line.tracking = (statistics.median(gaps) / line.em) if len(gaps) >= 4 else 0.0
    return True


def dedupe_ghosts(lines: list[Line]) -> list[Line]:
    """Anti-aliasing halos around text register on the opposite polarity mask
    and form phantom lines. When two lines of opposite polarity overlap, keep
    the one with more ink."""
    lines = sorted(lines, key=lambda ln: ln.y0)
    drop: set[int] = set()
    for i, a in enumerate(lines):
        for j in range(i + 1, len(lines)):
            b = lines[j]
            if b.y0 >= a.y1:
                break
            if a.polarity == b.polarity or i in drop or j in drop:
                continue
            ix = min(a.x1, b.x1) - max(a.x0, b.x0)
            iy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ix <= 0 or iy <= 0:
                continue
            area_a = (a.x1 - a.x0) * (a.y1 - a.y0)
            area_b = (b.x1 - b.x0) * (b.y1 - b.y0)
            if ix * iy >= 0.5 * min(area_a, area_b):
                ink_a = sum(g.area for g in a.glyphs)
                ink_b = sum(g.area for g in b.glyphs)
                drop.add(i if ink_a < ink_b else j)
    return [ln for k, ln in enumerate(lines) if k not in drop]


def cluster_sizes(lines: list[Line]) -> list[Cluster]:
    """1-D gap clustering of per-line em sizes, char-count weighted stats."""
    if not lines:
        return []
    lines = sorted(lines, key=lambda ln: ln.em)
    groups: list[list[Line]] = [[lines[0]]]
    for ln in lines[1:]:
        ref = statistics.fmean(x.em for x in groups[-1])
        if ln.em / ref > CLUSTER_GAP:
            groups.append([ln])
        else:
            groups[-1].append(ln)
    clusters = []
    for i, grp in enumerate(groups):
        total = sum(ln.chars for ln in grp) or 1
        em = sum(ln.em * ln.chars for ln in grp) / total
        weight = sum(ln.weight * ln.chars for ln in grp) / total
        c = Cluster(em=em, weight=weight, lines=grp)
        for ln in grp:
            ln.cluster = i
        clusters.append(c)
    return clusters


def paragraph_leading(lines: list[Line]) -> list[dict]:
    """Group same-size, left-aligned consecutive lines into blocks; measure
    line pitch / em. Returns blocks of >=3 lines."""
    blocks = []
    by_cluster: dict[int, list[Line]] = {}
    for ln in lines:
        by_cluster.setdefault(ln.cluster, []).append(ln)
    for cl_lines in by_cluster.values():
        cl_lines = sorted(cl_lines, key=lambda ln: ln.y0)
        cur: list[Line] = []
        for ln in cl_lines:
            if cur:
                prev = cur[-1]
                pitch = ln.y0 - prev.y0
                aligned = abs(ln.x0 - prev.x0) < 1.0 * prev.em
                if aligned and 0 < pitch < 3.0 * prev.em:
                    cur.append(ln)
                    continue
                if len(cur) >= 3:
                    blocks.append(cur)
                cur = []
            cur = cur or [ln]
        if len(cur) >= 3:
            blocks.append(cur)
    out = []
    for blk in blocks:
        pitches = [b.y0 - a.y0 for a, b in zip(blk, blk[1:])]
        em = statistics.fmean(ln.em for ln in blk)
        out.append({
            "lines": blk,
            "em": em,
            "leading": statistics.median(pitches) / em,
            "bbox": [min(l.x0 for l in blk), min(l.y0 for l in blk),
                     max(l.x1 for l in blk), max(l.y1 for l in blk)],
        })
    return out


def analyze(img: Image.Image, args) -> dict:
    rgb = img.convert("RGB")
    gray = np.asarray(rgb, dtype=np.float32) @ np.array([0.299, 0.587, 0.114],
                                                        dtype=np.float32)
    masks = binarize(gray, window=31, delta=12.0)

    lines: list[Line] = []
    for polarity, ink in masks.items():
        for ln in group_lines(extract_glyphs(ink), polarity):
            if measure_line(ln, ink):
                lines.append(ln)
    lines = dedupe_ghosts(lines)

    scale = args.scale
    result: dict = {
        "image": {"path": args.image, "width": rgb.width, "height": rgb.height,
                  "scale": scale},
        "lines": len(lines),
        "clusters": [],
        "findings": [],
    }
    if not lines:
        result["findings"].append({
            "id": "no-text", "severity": "info",
            "message": "No text lines detected — image may be non-UI, very low "
                       "contrast, or heavily stylized.",
        })
        return result

    clusters = cluster_sizes(lines)
    body = max(clusters, key=lambda c: c.chars)
    css = lambda px: round(px / scale, 1)

    for c in clusters:
        result["clusters"].append({
            "font_px": css(c.em),
            "stroke_weight": round(c.weight, 3),
            "lines": len(c.lines),
            "chars": c.chars,
            "role": ("body" if c is body else
                     "heading" if c.em >= body.em * 1.25 else
                     "small" if c.em < body.em else "text"),
        })

    findings = result["findings"]

    def add(fid, severity, message, boxes=None):
        f = {"id": fid, "severity": severity, "message": message}
        if boxes:
            f["boxes"] = boxes[:8]
        findings.append(f)

    # -- too small ------------------------------------------------------------
    body_css = css(body.em)
    if body_css < args.min_body:
        sev = "high" if body_css < args.min_body - 2 else "warn"
        add("body-too-small", sev,
            f"Body text ≈{body_css}px (want ≥{args.min_body}px) across "
            f"{len(body.lines)} lines.",
            [ln.bbox for ln in body.lines])
    for c in clusters:
        if c is not body and c.em < body.em and c.chars >= 40 and css(c.em) < 10:
            add("tiny-text", "warn",
                f"Secondary text ≈{css(c.em)}px — below 10px legibility floor "
                f"({len(c.lines)} lines).",
                [ln.bbox for ln in c.lines])

    # -- too similar ----------------------------------------------------------
    headings = [c for c in clusters if c.em >= body.em * 1.25 and c is not body]
    if headings:
        top = max(headings, key=lambda c: c.em)
        ratio = top.em / body.em
        if ratio < args.min_heading_ratio:
            sev = "high" if ratio < 1.35 else "warn"
            add("weak-hierarchy", sev,
                f"Largest heading is only {ratio:.2f}× body "
                f"({css(top.em)}px vs {css(body.em)}px; want ≥"
                f"{args.min_heading_ratio}×).",
                [ln.bbox for ln in top.lines])
        if ratio < 1.5 and body.weight > 0 and top.weight / body.weight < 1.12:
            add("no-weight-contrast", "high",
                f"Headings differ from body by neither size ({ratio:.2f}×) nor "
                f"stroke weight ({top.weight:.3f} vs {body.weight:.3f}) — levels "
                "are visually interchangeable.",
                [ln.bbox for ln in top.lines])
    elif len(lines) >= 8:
        add("weak-hierarchy", "high",
            f"Flat typography: no size cluster ≥1.25× body ({css(body.em)}px) — "
            "everything reads as one level.")
    sized = sorted((c for c in clusters if c.chars >= 40), key=lambda c: c.em)
    for a, b in zip(sized, sized[1:]):
        r = b.em / a.em
        if r < 1.22:
            add("muddy-scale", "warn",
                f"Near-identical sizes {css(a.em)}px and {css(b.em)}px "
                f"({r:.2f}× apart) — merge them or push them ≥1.25× apart.")
    if len(sized) > 5:
        add("too-many-sizes", "warn",
            f"{len(sized)} distinct text sizes with substantial use "
            f"({', '.join(str(css(c.em)) for c in sized)}px) — consolidate to a "
            "4–5 step scale.")

    # -- too wide -------------------------------------------------------------
    wide = [ln for ln in body.lines if ln.max_cpl > args.max_cpl and ln.chars >= 40]
    if wide:
        worst = max(ln.max_cpl for ln in wide)
        sev = "high" if worst > args.max_cpl + 30 else "warn"
        add("long-lines", sev,
            f"{len(wide)} body line(s) exceed {args.max_cpl} chars per line "
            f"(worst ≈{worst:.0f}cpl) — constrain the measure to 60–75ch.",
            [ln.bbox for ln in wide])
    span = [ln for ln in body.lines
            if ln.max_run_w > 0.75 * rgb.width and ln.chars >= 40]
    if len(span) >= 2:
        frac = max(ln.max_run_w for ln in span) / rgb.width
        sev = "high" if frac > 0.85 and len(span) >= 4 else "warn"
        add("wide-measure", sev,
            f"{len(span)} body line(s) run {frac:.0%} of the full viewport "
            "width — text should not fill its container edge to edge; wrap "
            "earlier or constrain the column.",
            [ln.bbox for ln in span])
    tracked = [ln for ln in lines if ln.tracking > 0.30 and ln.chars >= 6]
    total_chars = sum(ln.chars for ln in lines) or 1
    if sum(ln.tracking > 0.30 for ln in body.lines) >= 2 or \
       sum(ln.chars for ln in tracked) / total_chars > 0.25:
        add("wide-tracking", "warn",
            f"{len(tracked)} line(s) with letter-spacing >0.3em — wide tracking "
            "belongs on small caps labels only, not running text.",
            [ln.bbox for ln in tracked])

    # -- alignment ------------------------------------------------------------
    for c in clusters:
        cand = sorted((ln for ln in c.lines if ln.chars >= 6), key=lambda ln: ln.x0)
        if len(cand) < 4:
            continue
        group: list[Line] = []
        for ln in cand + [None]:
            if ln is not None and (not group or ln.x0 - group[-1].x0 <= 12):
                group.append(ln)
                continue
            if len(group) >= 4:
                spread = group[-1].x0 - group[0].x0
                edges: dict[int, int] = {}
                for g in group:  # bucket left edges to ±1px
                    edges[g.x0 // 2] = edges.get(g.x0 // 2, 0) + 1
                cols = [n for n in edges.values() if n >= 2]
                # min spread scales with em: ink left-bearing varies ~0.1-0.3em
                # with the starting letterform even when CSS x is identical.
                # Two clean edges a real indent apart (≥0.4em) is a deliberate
                # hanging indent, not drift — only scattered edges are sloppy.
                indent = len(edges) == 2 and spread >= 0.40 * c.em
                if max(4.0, 0.30 * c.em) < spread <= 14 and len(cols) >= 2 \
                        and not indent:
                    add("ragged-alignment", "warn",
                        f"{len(group)} lines at ≈{css(c.em)}px share a column "
                        f"but their left edges drift by {spread}px — snap them "
                        "to one axis.",
                        [g.bbox for g in group])
            group = [ln] if ln is not None else []

    # -- leading --------------------------------------------------------------
    for blk in paragraph_leading(body.lines):
        if blk["leading"] < 1.3:
            sev = "high" if blk["leading"] < 1.15 else "warn"
            add("tight-leading", sev,
                f"Paragraph of {len(blk['lines'])} lines at line-height ≈"
                f"{blk['leading']:.2f} (want 1.45–1.65 for body).",
                [blk["bbox"]])

    if scale == 1.0 and rgb.width >= 2200 and body_css >= 22:
        add("scale-hint", "info",
            "Image looks like a 2× (retina) capture — if so, re-run with "
            "--scale 2 for CSS-pixel readings.")

    result["_lines"] = lines  # for annotation; stripped before output
    return result


SEV_ORDER = {"high": 0, "warn": 1, "info": 2}
CLUSTER_COLORS = ["#2f81f7", "#3fb950", "#a371f7", "#d29922", "#db61a2", "#58a6ff"]


def annotate(img: Image.Image, result: dict, path: str) -> None:
    out = img.convert("RGB")
    draw = ImageDraw.Draw(out)
    for ln in result.get("_lines", []):
        color = CLUSTER_COLORS[ln.cluster % len(CLUSTER_COLORS)]
        draw.rectangle(ln.bbox, outline=color, width=1)
    for f in result["findings"]:
        if f["severity"] == "info":
            continue
        color = "#f85149" if f["severity"] == "high" else "#d29922"
        for i, box in enumerate(f.get("boxes", [])):
            draw.rectangle([box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2],
                           outline=color, width=2)
            if i == 0:  # label only the first box to avoid stacked text
                draw.text((box[0], max(0, box[1] - 12)), f["id"], fill=color)
    out.save(path)


def print_report(result: dict) -> None:
    findings = sorted(result["findings"], key=lambda f: SEV_ORDER[f["severity"]])
    counts = {s: sum(1 for f in findings if f["severity"] == s)
              for s in ("high", "warn", "info")}
    total = counts["high"] + counts["warn"]
    print(f"ui-type-lint: {total} finding(s) "
          f"({counts['high']} high, {counts['warn']} warn) — "
          f"{result['lines']} text lines analyzed\n")
    if result["clusters"]:
        print(f"Size clusters (CSS px @ scale {result['image']['scale']}):")
        for c in sorted(result["clusters"], key=lambda c: -c["font_px"]):
            print(f"  {c['font_px']:>6.1f}px  weight {c['stroke_weight']:.3f}  "
                  f"{c['lines']:>3} lines  {c['chars']:>5} chars  [{c['role']}]")
        print()
    for f in findings:
        print(f"{f['severity'].upper():<5} {f['id']}: {f['message']}")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Detect typography problems in a UI screenshot "
                    "(sizes too similar, too small, lines too wide).")
    p.add_argument("image", help="Screenshot to analyze (PNG/JPG)")
    p.add_argument("--scale", type=float, default=1.0,
                   help="Device pixel ratio of the capture (2 for retina). "
                        "Findings are reported in CSS px = device px / scale.")
    p.add_argument("--min-body", type=float, default=14.0,
                   help="Minimum acceptable body size in CSS px (default 14)")
    p.add_argument("--min-heading-ratio", type=float, default=1.5,
                   help="Minimum heading/body size ratio (default 1.5)")
    p.add_argument("--max-cpl", type=float, default=90.0,
                   help="Maximum chars per line for body text (default 90)")
    p.add_argument("--annotate", metavar="OUT.png",
                   help="Write a copy with line boxes and flagged regions drawn")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p.add_argument("--fail-on", choices=["warn", "high"],
                   help="Exit 2 if findings at/above this severity exist")
    args = p.parse_args()

    try:
        img = Image.open(args.image)
    except OSError as e:
        print(f"error: cannot open {args.image}: {e}", file=sys.stderr)
        return 1

    result = analyze(img, args)
    if args.annotate:
        annotate(img, result, args.annotate)
        result["annotated"] = args.annotate
    result.pop("_lines", None)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)

    if args.fail_on:
        threshold = SEV_ORDER[args.fail_on]
        if any(SEV_ORDER[f["severity"]] <= threshold for f in result["findings"]):
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
