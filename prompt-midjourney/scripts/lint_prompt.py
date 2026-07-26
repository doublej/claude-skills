#!/usr/bin/env python3
"""Lint a Midjourney prompt against V8.2 syntax, parameter ranges, and known anti-patterns.

Checks only what is deterministically checkable. Craft judgement (is the subject
front-loaded? is the lighting specific?) stays with the model.
"""

import argparse
import json
import re
import sys

# Parameters that no longer work on the V8 family, mapped to their replacement.
DEAD_PARAMS = {
    "cref": "removed after V6; use --oref (Omni Reference) for subject/character transfer",
    "cw": "paired with --cref; removed. Use --ow with --oref",
    "q": "V7-only quality flag; V8 has no --q. Use --hd / --sd instead",
    "quality": "V7-only quality flag; V8 has no --q. Use --hd / --sd instead",
    "turbo": "turbo generation is gone on V8; use --draft for fast iteration",
    "fast": "not a prompt parameter; set mode in account settings",
    "relax": "not a prompt parameter; set mode in account settings",
    "uplight": "V4-era upscaler flag",
    "upbeta": "V4-era upscaler flag",
    "test": "V4-era test models",
    "testp": "V4-era test models",
}

# Numeric parameters: flag -> (min, max, default, note)
NUMERIC_RANGES = {
    "s": (0, 1000, 100, "stylize"),
    "stylize": (0, 1000, 100, "stylize"),
    "chaos": (0, 100, 0, "chaos"),
    "c": (0, 100, 0, "chaos"),
    "weird": (0, 3000, 0, "weird"),
    "w": (0, 3000, 0, "weird"),
    "sw": (0, 1000, 100, "style weight"),
    "ow": (0, 1000, 100, "omni weight"),
    "iw": (0, 2, 1, "image weight"),
    "exp": (0, 100, 0, "experimental"),
    "stop": (10, 100, 100, "stop"),
    "r": (1, 40, 1, "repeat"),
    "repeat": (1, 40, 1, "repeat"),
}

# Words that degrade V7+ output. They read as quality-spam and pull toward
# over-airbrushed stock-photo defaults instead of adding fidelity.
ANTI_PATTERN_WORDS = [
    "8k", "4k", "16k", "uhd", "hd quality", "high resolution",
    "masterpiece", "award winning", "award-winning", "best quality",
    "highly detailed", "ultra detailed", "ultra-detailed", "extremely detailed",
    "hyperrealistic", "hyper realistic", "hyper-realistic",
    "photorealistic", "photo realistic", "photo-realistic",
    "beautiful", "stunning", "gorgeous", "breathtaking",
    "flawless", "immaculate", "perfect skin", "perfect face",
    "trending on artstation", "artstation", "deviantart",
    "unreal engine", "octane render",
    "intricate details",
]

# Anti-patterns that are only a problem as bare filler, fine when qualified.
# Kept at info severity because each has a legitimate use ("a professional kitchen").
SOFT_ANTI_PATTERNS = {
    "professional": "if this describes quality rather than a subject, cut it — it reads as spam",
    "sharp focus": "state the aperture instead (f/8, deep focus)",
    "cinematic lighting": "name the actual setup (low-key rim light, overcast softbox, practical neon)",
    "dramatic lighting": "name the actual setup (hard key from camera-left, deep falloff)",
    "epic": "describe the scale concretely (figure dwarfed by a 200m concrete wall)",
    "detailed": "say which details matter (frayed cuffs, chipped enamel, condensation)",
}

PARAM_RE = re.compile(r"--([a-zA-Z]+)(?:\s+([^\s-][^\s]*(?:\s+[^\s-][^\s]*)*?))?(?=\s+--|\s*$)")
SIMPLE_PARAM_RE = re.compile(r"--([a-zA-Z]+)")


def _add(findings, severity, code, message, fix=None):
    findings.append({"severity": severity, "code": code, "message": message, "fix": fix})


def check_dashes(prompt, findings):
    """Em/en dashes and smart quotes silently break the parser."""
    for ch, name in (("—", "em dash"), ("–", "en dash"), ("‒", "figure dash")):
        if ch in prompt:
            _add(findings, "error", "bad-dash",
                 f"Prompt contains a {name} ({ch!r}) — Midjourney only parses two ASCII hyphens",
                 "replace with --")
    for ch, name in (("“", "smart quote"), ("”", "smart quote"), ("‘", "smart apostrophe"), ("’", "smart apostrophe")):
        if ch in prompt:
            _add(findings, "warn", "smart-quote",
                 f"Prompt contains a {name} ({ch!r}); quoted text for rendering should use plain \" characters",
                 "replace with \" or '")
            break


def parse_params(prompt):
    """Return [(flag, raw_value, start_index)] in order of appearance."""
    out = []
    for m in re.finditer(r"--([a-zA-Z]+)", prompt):
        flag = m.group(1)
        rest = prompt[m.end():]
        nxt = re.search(r"\s--[a-zA-Z]", rest)
        value = (rest[: nxt.start()] if nxt else rest).strip()
        out.append((flag, value, m.start()))
    return out


# Flags taking no value at all.
BOOLEAN_FLAGS = {"hd", "sd", "raw", "tile", "draft", "video", "fast", "relax", "turbo"}
# Flags taking exactly one token.
SINGLE_VALUE_FLAGS = {
    "ar", "aspect", "s", "stylize", "chaos", "c", "weird", "w", "sw", "ow", "iw", "exp",
    "stop", "seed", "sv", "r", "repeat", "niji", "v", "version", "profile", "motion", "style", "q", "quality", "cw",
}
# Flags whose value is a list or free text: --no, --sref, --oref, --p. Not position-checked.


def check_param_position(prompt, params, findings):
    """All parameters sit at the end. Prose after a flag that can't hold it is misplaced text."""
    for flag, value, _idx in params:
        key = flag.lower()
        tokens = value.split()
        if key in BOOLEAN_FLAGS and tokens:
            leftover = tokens
        elif key in SINGLE_VALUE_FLAGS and len(tokens) > 1:
            leftover = tokens[1:]
        else:
            continue
        _add(findings, "error", "param-position",
             f"Text follows --{flag} that it cannot take ({' '.join(leftover[:6])}); "
             "a parameter mid-prompt breaks the parser",
             "move every --flag to the end, after all natural language")
        return


def check_dead_params(params, findings):
    for flag, _value, _idx in params:
        key = flag.lower()
        if key in DEAD_PARAMS:
            _add(findings, "error", "dead-param",
                 f"--{flag} does not work on the V8 family: {DEAD_PARAMS[key]}")


def check_ranges(params, findings):
    for flag, value, _idx in params:
        key = flag.lower()
        if key not in NUMERIC_RANGES:
            continue
        lo, hi, default, label = NUMERIC_RANGES[key]
        token = value.split()[0] if value else ""
        if not token:
            _add(findings, "warn", "missing-value",
                 f"--{flag} given with no value; it will fall back to the default ({default})")
            continue
        try:
            num = float(token)
        except ValueError:
            _add(findings, "error", "bad-value",
                 f"--{flag} expects a number for {label}, got {token!r}")
            continue
        if num < lo or num > hi:
            _add(findings, "error", "out-of-range",
                 f"--{flag} {token} is outside the valid {label} range {lo}-{hi}")


def check_aspect_ratio(params, findings):
    ar = next((v for f, v, _ in params if f.lower() == "ar" or f.lower() == "aspect"), None)
    if not ar:
        return
    token = ar.split()[0]
    m = re.match(r"^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$", token)
    if not m:
        _add(findings, "error", "bad-ar", f"--ar {token!r} is not in W:H form (e.g. 16:9)")
        return
    w, h = float(m.group(1)), float(m.group(2))
    if h == 0:
        _add(findings, "error", "bad-ar", "--ar height cannot be zero")
        return
    ratio = max(w / h, h / w)
    flags = {f.lower() for f, _v, _i in params}
    if "hd" in flags and ratio > 4.0:
        _add(findings, "error", "ar-hd-conflict",
             f"--ar {token} is {ratio:.1f}:1 but HD mode caps aspect ratio at 4:1",
             "drop --hd, or use a ratio within 4:1")
    elif ratio > 14.0:
        _add(findings, "error", "ar-limit",
             f"--ar {token} is {ratio:.1f}:1; V8 caps at 14:1 (4:1 in HD)")


def check_conflicts(prompt, params, findings):
    flags = [f.lower() for f, _v, _i in params]
    seen = set()
    for f in flags:
        if f in seen:
            _add(findings, "warn", "duplicate-param", f"--{f} appears more than once; the last one wins")
        seen.add(f)

    if "hd" in flags and "sd" in flags:
        _add(findings, "error", "hd-sd-conflict", "--hd and --sd are mutually exclusive")

    if "style" in flags:
        val = next((v for f, v, _ in params if f.lower() == "style"), "")
        if val.split()[:1] == ["raw"]:
            _add(findings, "warn", "style-raw-v7",
                 "--style raw is the V7 spelling; the V8 family uses --raw")

    if "oref" in flags:
        _add(findings, "info", "oref-v7-path",
             "--oref routes through V7 even when V8 is selected; expect V7 aesthetics on referenced subjects")
        if "ow" not in flags:
            _add(findings, "info", "oref-no-ow",
                 "--oref without --ow uses weight 100; raise toward 300+ for strict likeness, drop to 30 for loose inspiration")

    ver = next((v for f, v, _ in params if f.lower() in {"v", "version"}), None)
    if ver:
        try:
            if float(ver.split()[0]) < 7:
                _add(findings, "info", "old-model",
                     f"--v {ver.split()[0]} selects a pre-2025 model; V8.2 is the current default",
                     "drop --v to use the default, or --v 7 if you need native --oref")
        except ValueError:
            pass

    if "::" in prompt:
        _add(findings, "error", "multiprompt",
             ":: multi-prompt weighting is not supported on V7 or V8",
             "express emphasis in words, or split into separate generations")

    # --no items that also appear as positive prompt terms
    no_val = next((v for f, v, _ in params if f.lower() == "no"), None)
    if no_val:
        body = prompt[: params[0][2]].lower()
        for item in [i.strip() for i in re.split(r"[,\s]+", no_val) if len(i.strip()) > 3]:
            if re.search(rf"\b{re.escape(item.lower())}\b", body):
                _add(findings, "warn", "no-contradiction",
                     f"--no {item!r} contradicts {item!r} in the prompt body",
                     f"remove {item!r} from one side")


def check_anti_patterns(prompt, params, findings):
    body = (prompt[: params[0][2]] if params else prompt).lower()
    hits = [w for w in ANTI_PATTERN_WORDS if re.search(rf"\b{re.escape(w)}\b", body)]
    if hits:
        _add(findings, "warn", "quality-spam",
             f"Quality-spam terms degrade V7+ output: {', '.join(sorted(set(hits)))}",
             "delete them; build realism from named lighting, film stock, camera, and lens instead")
    for phrase, advice in SOFT_ANTI_PATTERNS.items():
        if phrase in body:
            _add(findings, "info", "vague-term", f"{phrase!r} is vague", advice)


def check_text_rendering(prompt, params, findings):
    body = prompt[: params[0][2]] if params else prompt
    for quoted in re.findall(r'"([^"]+)"', body):
        words = quoted.split()
        if len(words) > 4:
            _add(findings, "warn", "long-text",
                 f'Rendered text "{quoted}" is {len(words)} words; text rendering degrades past ~4 words',
                 "shorten, or split across separate elements")


def check_length(prompt, params, findings):
    body = (prompt[: params[0][2]] if params else prompt).strip()
    words = len(body.split())
    if words == 0:
        _add(findings, "error", "empty", "No prompt text before the parameters")
    elif words > 60:
        _add(findings, "warn", "too-long",
             f"{words} words of prompt text; V8 rewards short prompts and dilutes past ~40",
             "cut to the load-bearing nouns, then add back only what the output is missing")


def lint(prompt):
    findings = []
    params = parse_params(prompt)
    check_dashes(prompt, findings)
    check_param_position(prompt, params, findings)
    check_dead_params(params, findings)
    check_ranges(params, findings)
    check_aspect_ratio(params, findings)
    check_conflicts(prompt, params, findings)
    check_anti_patterns(prompt, params, findings)
    check_text_rendering(prompt, params, findings)
    check_length(prompt, params, findings)
    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: order[f["severity"]])
    return findings


def main():
    ap = argparse.ArgumentParser(description="Lint a Midjourney prompt for V8.2 syntax and anti-patterns.")
    ap.add_argument("prompt", nargs="?", help="the prompt text; omit to read stdin")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    prompt = args.prompt if args.prompt is not None else sys.stdin.read()
    prompt = prompt.strip()
    findings = lint(prompt)

    if args.json:
        counts = {s: sum(1 for f in findings if f["severity"] == s) for s in ("error", "warn", "info")}
        print(json.dumps({"prompt": prompt, "counts": counts, "findings": findings}, indent=2))
    elif not findings:
        print("clean")
    else:
        for f in findings:
            line = f"[{f['severity']}] {f['code']}: {f['message']}"
            if f["fix"]:
                line += f"\n         fix: {f['fix']}"
            print(line)

    return 1 if any(f["severity"] == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
