#!/usr/bin/env python3
"""Deterministic checks for humor drafts.

Catches the mechanical failures — the ones that are true regardless of taste:
punch buried mid-sentence, explanation trailing after the reveal, crutch
phrases that signal the writer does not trust the joke, setup bloat, hedging
inside the punch, and diluted lists.

It cannot tell you whether something is funny. It tells you whether the
machinery is in the way.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# --- rule data -------------------------------------------------------------

# Writer does not trust the joke and is nudging the reader to laugh.
CRUTCHES = [
    "just kidding", "jk", "lol", "haha", "hehe", "no offense", "am i right",
    "amirite", "if you know what i mean", "iykyk", "that's the joke",
    "thats the joke", "see what i did there", "pun intended", "no pun intended",
    "i'll see myself out", "ill see myself out", "asking for a friend",
    "let that sink in", "i can't even", "i cant even", "and i'm not even kidding",
    "and im not even kidding", "true story", "you can't make this up",
    "you cant make this up", "*ahem*", "/s", "😂", "🤣", "😅", "🙃",
]

# Explaining the joke after landing it.
EXPLAINERS = [
    "because what i mean is", "which is to say", "in other words", "basically what",
    "the point being", "the joke being", "get it", "geddit", "if that makes sense",
    "what i'm saying is", "what im saying is", "the funny part is",
    "the irony is", "which is funny because",
]

# Softeners that defuse a punch from inside it.
HEDGES = [
    "kind of", "kinda", "sort of", "sorta", "maybe", "i guess", "i suppose",
    "a bit", "a little bit", "somewhat", "arguably", "probably", "perhaps",
    "more or less", "in a way", "to be fair", "i think",
]

# Padding that steals the stress from the punch word.
INTENSIFIERS = [
    "very", "really", "so", "super", "totally", "absolutely", "extremely",
    "incredibly", "literally", "actually", "honestly", "genuinely", "quite",
]

# Attitude vocabulary — a premise without one of these is usually description.
ATTITUDE = [
    "hard", "weird", "scary", "stupid", "embarrassing", "unfair", "fake",
    "exhausting", "petty", "absurd", "ridiculous", "insulting", "pointless",
    "humiliating", "grim", "bleak", "desperate", "smug", "delusional",
    "shameless", "tedious", "unhinged", "cruel", "sad", "pathetic", "insane",
    "baffling", "obscene", "gross", "annoying", "terrifying", "dishonest",
]

# Subordinators that, when they open the tail of a punch, bury the reveal.
BURIERS = [
    "because", "which", "so that", "even though", "although", "while",
    "since", "in order to", "due to", "as a result",
]

SEVERITY_ORDER = {"error": 0, "warn": 1, "info": 2}


# --- helpers ---------------------------------------------------------------

def split_units(text, mode):
    """Yield (start_line, [lines]) for each unit to analyze."""
    lines = text.splitlines()
    if mode == "line":
        for i, line in enumerate(lines, 1):
            if line.strip():
                yield i, [line]
        return

    buf, start = [], None
    for i, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = i
            buf.append(line)
        elif buf:
            yield start, buf
            buf, start = [], None
    if buf:
        yield start, buf


def split_sentences(text):
    parts = re.split(r"(?<=[.!?…])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text):
    return re.findall(r"[a-zA-Z0-9']+", text)


def find_phrases(haystack, needles):
    """Return phrases present in haystack, matched on word boundaries."""
    low = haystack.lower()
    hits = []
    for n in needles:
        if not n.isascii() or not re.match(r"^[a-z0-9' ]+$", n):
            if n in low:  # emoji and punctuation markers
                hits.append(n)
            continue
        if re.search(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])", low):
            hits.append(n)
    return hits


def add(findings, line, rule, severity, message, fix):
    findings.append({
        "line": line,
        "rule": rule,
        "severity": severity,
        "message": message,
        "fix": fix,
    })


# --- checks ----------------------------------------------------------------

def check_unit(start_line, unit_lines, opts, findings):
    text = " ".join(l.strip() for l in unit_lines)
    if not text.strip():
        return
    end_line = start_line + len(unit_lines) - 1
    sentences = split_sentences(text)
    if not sentences:
        return

    punch = sentences[-1]
    setup = " ".join(sentences[:-1])
    punch_words = words(punch)
    setup_words = words(setup)

    # 1. crutch phrases (anywhere)
    for phrase in find_phrases(text, CRUTCHES):
        add(findings, start_line, "comedy-crutch", "error",
            f'crutch phrase "{phrase}" — flags the joke instead of landing it',
            "Delete it. If the line needs a laugh-sign, the line is the problem.")

    # 2. explaining after the punch
    for phrase in find_phrases(punch, EXPLAINERS):
        add(findings, end_line, "explained-punch", "error",
            f'"{phrase}" explains the reveal',
            "Cut the explanation. The audience gets it or the connector was wrong.")

    # 3. hedges inside the punch
    for phrase in find_phrases(punch, HEDGES):
        add(findings, end_line, "hedged-punch", "error",
            f'hedge "{phrase}" inside the punch',
            "Commit. A hedged punch tells the reader you are not sure it is true.")

    # 4. reveal buried before the end of the punch
    if len(punch_words) >= 8:
        tail_start = int(len(punch_words) * 0.65)
        tail = " ".join(punch_words[tail_start:])
        for phrase in find_phrases(tail, BURIERS):
            add(findings, end_line, "buried-reveal", "warn",
                f'punch trails into a "{phrase}" clause after the reveal',
                "Move the decisive word or image to the final position.")
            break

    # 5. punch ends weak
    if punch_words:
        last = punch_words[-1].lower()
        if last in {"is", "are", "was", "were", "be", "been", "it", "that", "this",
                    "them", "him", "her", "too", "though", "anyway", "really"}:
            add(findings, end_line, "weak-final-word", "warn",
                f'punch ends on "{last}"',
                "End on the concrete noun, image, or verb that carries the turn.")

    # 6. intensifier padding in the punch
    for phrase in find_phrases(punch, INTENSIFIERS):
        add(findings, end_line, "intensifier-padding", "info",
            f'"{phrase}" pads the punch',
            "Cut it. Intensifiers borrow stress the punch word should own.")

    # 7. setup bloat
    if setup_words and punch_words:
        ratio = len(setup_words) / len(punch_words)
        if len(setup_words) > opts.max_setup:
            add(findings, start_line, "setup-bloat", "warn",
                f"setup is {len(setup_words)} words (limit {opts.max_setup})",
                "Cut every word that does not build the assumption you plan to break.")
        elif ratio > opts.max_ratio:
            add(findings, start_line, "setup-bloat", "info",
                f"setup:punch ratio is {ratio:.1f}:1 (limit {opts.max_ratio}:1)",
                "Either trim the setup or earn it with a bigger turn.")

    # 8. list dilution
    for sent in sentences:
        items = [p for p in re.split(r",|\band\b", sent) if p.strip()]
        if len(items) >= 5:
            add(findings, start_line, "list-dilution", "warn",
                f"list of {len(items)} items",
                "Three is the comic maximum: two to set the pattern, one to break it.")
        elif len(items) == 3 and opts.strict:
            add(findings, start_line, "rule-of-three", "info",
                "three-item list — verify the third item breaks the pattern",
                "Items one and two establish; item three must violate, not continue.")

    # 9. premise with no attitude
    if opts.premise and not find_phrases(text, ATTITUDE):
        add(findings, start_line, "no-attitude", "warn",
            "no attitude word found",
            "Name what is hard/weird/stupid/unfair about it. Neutral is not comic.")


def check_document(text, opts):
    findings = []
    for start_line, unit_lines in split_units(text, opts.unit):
        check_unit(start_line, unit_lines, opts, findings)
    findings.sort(key=lambda f: (f["line"], SEVERITY_ORDER[f["severity"]]))
    return findings


# --- output ----------------------------------------------------------------

def render_text(findings, source):
    if not findings:
        return f"{source}: clean — no mechanical faults found.\n"
    out = [f"{source}: {len(findings)} finding(s)\n"]
    for f in findings:
        out.append(f"  {f['line']:>4}  [{f['severity']}] {f['rule']}: {f['message']}")
        out.append(f"        fix: {f['fix']}")
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items(),
                                                      key=lambda kv: SEVERITY_ORDER[kv[0]]))
    out.append(f"\n  {summary}")
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(
        description="Lint humor drafts for mechanical faults (not for funniness).")
    p.add_argument("path", nargs="?", default="-",
                   help="file to lint, or - for stdin (default: -)")
    p.add_argument("--json", action="store_true",
                   help="emit JSON findings")
    p.add_argument("--unit", choices=["paragraph", "line"], default="paragraph",
                   help="treat each paragraph or each line as one joke (default: paragraph)")
    p.add_argument("--premise", action="store_true",
                   help="also check that each unit carries an attitude word")
    p.add_argument("--strict", action="store_true",
                   help="add advisory checks (rule-of-three verification)")
    p.add_argument("--max-setup", type=int, default=45,
                   help="max setup words before flagging bloat (default: 45)")
    p.add_argument("--max-ratio", type=float, default=4.0,
                   help="max setup:punch word ratio (default: 4.0)")
    args = p.parse_args()

    if args.path == "-":
        text, source = sys.stdin.read(), "<stdin>"
    else:
        path = Path(args.path)
        if not path.is_file():
            p.error(f"not a file: {path}")
        text, source = path.read_text(encoding="utf-8"), str(path)

    findings = check_document(text, args)

    if args.json:
        print(json.dumps({"source": source, "findings": findings,
                          "count": len(findings)}, indent=2))
    else:
        sys.stdout.write(render_text(findings, source))

    return 1 if any(f["severity"] == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
