#!/usr/bin/env python3
"""Scan text for AI copywriting tells.

Deterministic detector for the lexical, phrasal, punctuation, and rhythm
tells cataloged in references/tells.md. Reports findings with line numbers,
severity, and a density score. Fixing is the model's job — this only scans.

Usage:
    python3 scan.py draft.md
    python3 scan.py draft.md --json
    cat draft.txt | python3 scan.py -
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys

# ---------------------------------------------------------------- word lists
# Weight 3: the delve-cluster — 10-30x human baseline in corpus studies.
WORDS_HIGH = """
delve delves delving delved tapestry testament showcasing underscore
underscores underscoring boasts boasting intricate intricacies meticulous meticulously
pivotal realm beacon myriad plethora synergy groundbreaking transformative
unparalleled unprecedented seamless seamlessly effortless effortlessly
cutting-edge ever-evolving revolutionize revolutionizes supercharge
cornerstone paradigm nexus labyrinth bustling vibrant commendable garnered
elucidate unveil unveiling game-changer game-changing
""".split()

# Weight 2: heavily overused but common enough to be legitimate.
WORDS_MED = """
leverage leveraging robust crucial comprehensive nuanced holistic actionable
multifaceted noteworthy invaluable foster fosters fostering harness harnessing
streamline streamlining empower empowers empowering elevate elevates elevating
journey insights unlock unlocking
unleash unleashing embark embarking amplify bolster spearhead facilitate
transcend catalyze utilize utilizing landscape ecosystem trajectory hallmark
prowess advancements
""".split()

# Weight 1: connectives AI leans on.
WORDS_LOW = """
additionally moreover furthermore notably ultimately undoubtedly certainly
strategically
""".split()

# ------------------------------------------------------------------- phrases
# (pattern, label, severity)  severity: critical | high | med | low
PHRASES = [
    # smoking guns — chat/placeholder leakage
    (r"\bas an ai\b", "chat leakage: 'as an AI'", "critical"),
    (r"\bas of my last (?:knowledge )?update\b", "knowledge-cutoff leakage", "critical"),
    (r"\blet me know if you (?:need|want|would like) any (?:modifications|changes|adjustments)\b",
     "chat leakage: closing offer", "critical"),
    (r"\byou'?re absolutely right\b", "chat leakage: sycophancy", "critical"),
    (r"\[(?:insert|your) [^\]]{1,30}\]", "placeholder leakage", "critical"),
    (r"utm_source=chatgpt", "chatgpt URL artifact", "critical"),
    (r"\b(?:oaicite|turn\d+search\d+|grok_card|ppl-ai-file-upload)\b", "model citation artifact", "critical"),

    # negative parallelism family — #1 cited tell
    (r"\b(?:it|this|that)['’]s not (?:just |only |simply |merely )?(?:about )?[^.!?\n]{2,60}?[—–;,:-]+\s*it['’]s\b",
     "negative parallelism: it's not X, it's Y", "high"),
    (r"\bisn['’]t (?:just|only|merely|simply) (?:a |an |the )?\w+[^.!?\n]{0,50}?[—–;,:-]+\s*it['’]s\b",
     "negative parallelism: isn't just X — it's Y", "high"),
    (r"\bit['’]s less about\b[^.!?\n]{2,60}\bmore about\b", "negative parallelism: less about X, more about Y", "high"),
    (r"\bnot just [^.!?\n]{2,50}?, but (?:also )?", "not just X, but also Y", "med"),

    # stock openers / closers
    (r"\bin today['’]s (?:fast-paced|digital|ever-changing|modern|competitive)\b", "stock opener: in today's …", "high"),
    (r"\bin a world where\b", "stock opener: in a world where", "high"),
    (r"\bwithout further ado\b", "stock opener", "high"),
    (r"\blet['’]s dive in\b", "stock opener: let's dive in", "med"),
    (r"\bin conclusion\b", "stock closer: in conclusion", "med"),
    (r"\bi hope this helps\b", "stock closer", "med"),
    (r"\bthere you have it\b", "stock closer", "med"),

    # hype constructions
    (r"\blook no further\b", "hype: look no further", "high"),
    (r"\btake (?:your |its |their )?\w+ to the next level\b", "hype: next level", "high"),
    (r"\bsay goodbye to\b", "hype: say goodbye to X", "high"),
    (r"\bsay hello to\b", "hype: say hello to Y", "high"),
    (r"\bgone are the days\b", "hype: gone are the days", "high"),
    (r"\bunlock(?:ing)? the (?:power|potential|secrets?) of\b", "hype: unlock the power of", "high"),
    (r"\bunleash(?:ing)? the (?:power|potential) of\b", "hype: unleash the power of", "high"),
    (r"\belevate your\b", "hype: elevate your X", "high"),
    (r"\bnavigate the (?:complexities|landscape|world|challenges) of\b", "hype: navigate the complexities", "high"),
    (r"\btreasure trove\b", "hype: treasure trove", "high"),
    (r"\bwe['’]ve got you covered\b", "hype: we've got you covered", "med"),
    (r"\bparadigm shift\b", "hype: paradigm shift", "med"),
    (r"\bsecret (?:sauce|weapon)\b", "hype: secret sauce/weapon", "med"),
    (r"\bembark on a journey\b", "hype: embark on a journey", "high"),
    (r"\bthe new standard\b", "hype: the new standard", "low"),

    # significance inflation
    (r"\b(?:stands? as|is) a testament to\b", "inflation: testament to", "high"),
    (r"\bplays? a (?:crucial|vital|significant|pivotal|key) role\b", "inflation: plays a crucial role", "high"),
    (r"\bnestled in the heart of\b", "inflation: nestled in the heart of", "high"),
    (r"\brich (?:cultural )?(?:heritage|history|tapestry)\b", "inflation: rich heritage/tapestry", "high"),
    (r"\bshed(?:s|ding)? light on\b", "inflation: shed light on", "med"),
    (r"\bdriving force\b", "inflation: driving force", "med"),
    (r"\bdeep dive\b", "inflation: deep dive", "med"),

    # hedging / meta-commentary
    (r"\bit['’]s (?:important|worth) (?:to note|noting)\b", "hedge: important to note", "high"),
    (r"\bit goes without saying\b", "hedge", "med"),
    (r"\bat the end of the day\b", "hedge: at the end of the day", "med"),
    (r"\bthat being said\b", "hedge: that being said", "low"),
    (r"\bwhen it comes to\b", "hedge: when it comes to", "low"),

    # audience pandering
    (r"\bwhether you['’]re (?:a |an )?[^.!?\n]{2,60}? or (?:a |an )?", "pandering: whether you're A or B", "med"),
    (r"\bbusy professionals\b", "pandering: busy professionals", "med"),

    # email tells
    (r"\bhope this (?:email |message )?finds you well\b", "email: finds you well", "high"),
    (r"\b(?:just )?circling back\b", "email: circling back", "high"),
    (r"\bjust (?:wanted|wanting) to (?:reach out|touch base|follow up)\b", "email: reaching out register", "med"),

    # social tells
    (r"\blet that sink in\b", "social: let that sink in", "high"),
    (r"\bhere['’]s the kicker\b", "social: here's the kicker", "high"),
    (r"\bbut here['’]s the thing\b", "social: but here's the thing", "med"),
    (r"\bimagine a world\b", "social: imagine a world", "high"),
    (r"\bpicture this\b", "social: picture this", "med"),

    # rhetorical transitions
    (r"\bthe (?:result|best part|bottom line|catch|takeaway)\?", "rhetorical transition question", "high"),
    (r"\bso what does this mean\b", "rhetorical transition question", "med"),

    # -ing analysis riders
    (r",\s*(?:highlighting|underscoring|showcasing|reflecting|emphasizing|demonstrating|signaling|reinforcing|cementing|solidifying)\b",
     "participial rider: ', verbing …'", "high"),
]

STACCATO = re.compile(r"\bNo \w+\. No \w+\. No [\w.]+")
TRIAD = re.compile(r"\b\w+, \w+, and \w+\b", re.IGNORECASE)
CONNECTIVE_OPENER = re.compile(r"^\s*(?:However|Moreover|Additionally|Furthermore|Overall),")
BOLD_LEADIN = re.compile(r"^\s*[-*•]\s*\*\*[^*]+?(?::\*\*|\*\*\s*[:—–-])")
EMOJI_BULLET = re.compile(r"^\s*(?:[-*•]\s*)?[\U0001F300-\U0001FAFF✅✨⚡\U0001F525\U0001F4A1\U0001F680]")
CODE_FENCE = re.compile(r"^\s*```")


def build_word_res() -> list[tuple[re.Pattern, str, str]]:
    res = []
    for words, sev in ((WORDS_HIGH, "high"), (WORDS_MED, "med"), (WORDS_LOW, "low")):
        for w in words:
            res.append((re.compile(r"\b" + re.escape(w) + r"\b", re.IGNORECASE), w, sev))
    return res


SEV_WEIGHT = {"critical": 6, "high": 3, "med": 2, "low": 1}


def mask_code_blocks(lines: list[str]) -> list[str]:
    """Blank out fenced code blocks, preserving line numbers."""
    out, in_code = [], False
    for line in lines:
        if CODE_FENCE.match(line):
            in_code = not in_code
            out.append("")
            continue
        out.append("" if in_code else line)
    return out


def sentence_stats(text: str) -> tuple[int, float, float]:
    """Return (n_sentences, mean_len, cv) over prose sentences with >=3 words."""
    prose = re.sub(r"^#+ .*$|^\s*[-*•].*$", "", text, flags=re.MULTILINE)
    parts = re.split(r"(?<=[.!?])\s+", prose)
    lens = [len(re.findall(r"\w+", s)) for s in parts]
    lens = [n for n in lens if n >= 3]
    if len(lens) < 2:
        return len(lens), float(lens[0]) if lens else 0.0, 0.0
    mean = statistics.mean(lens)
    cv = statistics.stdev(lens) / mean if mean else 0.0
    return len(lens), mean, cv


def scan(text: str) -> dict:
    raw_lines = text.splitlines()
    lines = mask_code_blocks(raw_lines)
    clean_text = "\n".join(lines)
    word_count = max(1, len(re.findall(r"\w+", clean_text)))

    findings: list[dict] = []

    phrase_res = [(re.compile(p, re.IGNORECASE), label, sev) for p, label, sev in PHRASES]
    word_res = build_word_res()

    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        for rx, label, sev in phrase_res:
            for m in rx.finditer(line):
                findings.append({"line": i, "severity": sev, "category": "phrase",
                                 "tell": label, "match": m.group(0)[:80]})
        for rx, word, sev in word_res:
            n = len(rx.findall(line))
            if n:
                findings.append({"line": i, "severity": sev, "category": "word",
                                 "tell": f"AI-vocabulary: {word}", "match": word if n == 1 else f"{word} x{n}"})
        for m in STACCATO.finditer(line):
            findings.append({"line": i, "severity": "high", "category": "rhetoric",
                             "tell": "staccato triplet: No X. No Y. No Z.", "match": m.group(0)[:80]})

    # structural counters
    def add_structural(count: int, threshold: int, sev: str, tell: str, detail: str):
        if count >= threshold:
            findings.append({"line": 0, "severity": sev, "category": "structure",
                             "tell": tell, "match": detail})

    em_dashes = clean_text.count("—")
    em_per_1k = em_dashes * 1000 / word_count
    if em_per_1k > 8:
        add_structural(1, 1, "high", "em-dash saturation", f"{em_dashes} em-dashes ({em_per_1k:.1f}/1k words)")
    elif em_per_1k > 3:
        add_structural(1, 1, "med", "em-dash density", f"{em_dashes} em-dashes ({em_per_1k:.1f}/1k words)")

    curly = bool(re.search(r"[‘’“”]", clean_text))
    straight = bool(re.search(r"[\"'](?=\w)|\w[\"']", clean_text))
    if curly and straight:
        add_structural(1, 1, "med", "mixed curly/straight quotes", "both typographic and straight quotes present")

    triads = len(TRIAD.findall(clean_text))
    if triads >= 3 and triads * 1000 / word_count > 2:
        add_structural(1, 1, "med", "rule-of-three density",
                       f"{triads} 'X, Y, and Z' triads ({triads * 1000 / word_count:.1f}/1k words)")

    connectives = sum(1 for l in lines if CONNECTIVE_OPENER.match(l))
    add_structural(connectives, 2, "med", "paragraph-initial connectives",
                   f"{connectives} paragraphs open with However/Moreover/Additionally/…")

    bold_leads = sum(1 for l in lines if BOLD_LEADIN.match(l))
    add_structural(bold_leads, 3, "med", "bolded lead-in bullets",
                   f"{bold_leads} bullets shaped '- **Term:** text'")

    emoji_bullets = sum(1 for l in lines if EMOJI_BULLET.match(l))
    add_structural(emoji_bullets, 3, "med", "emoji-as-formatting",
                   f"{emoji_bullets} emoji-prefixed lines")

    n_sent, mean_len, cv = sentence_stats(clean_text)
    if n_sent >= 8 and cv < 0.35:
        add_structural(1, 1, "med", "low burstiness",
                       f"sentence-length CV {cv:.2f} over {n_sent} sentences (uniform rhythm)")

    score = sum(SEV_WEIGHT[f["severity"]] for f in findings) * 1000 / word_count
    criticals = sum(1 for f in findings if f["severity"] == "critical")
    if criticals:
        verdict = "smoking-gun"
    elif score > 12:
        verdict = "saturated"
    elif score > 6:
        verdict = "heavy"
    elif score > 2:
        verdict = "mild"
    else:
        verdict = "clean"

    sev_order = {"critical": 0, "high": 1, "med": 2, "low": 3}
    findings.sort(key=lambda f: (sev_order[f["severity"]], f["line"]))

    return {
        "verdict": verdict,
        "score_per_1k": round(score, 1),
        "word_count": word_count,
        "metrics": {
            "em_dashes_per_1k": round(em_per_1k, 1),
            "sentence_count": n_sent,
            "sentence_mean_len": round(mean_len, 1),
            "sentence_length_cv": round(cv, 2),
            "triads": triads,
        },
        "counts": {s: sum(1 for f in findings if f["severity"] == s)
                   for s in ("critical", "high", "med", "low")},
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan text for AI copywriting tells")
    ap.add_argument("path", help="file to scan, or - for stdin")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    if not text.strip():
        print("scan.py: empty input", file=sys.stderr)
        return 1

    result = scan(text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    m = result["metrics"]
    print(f"verdict: {result['verdict']}  score: {result['score_per_1k']}/1k words "
          f"({result['word_count']} words)")
    print(f"metrics: em-dash {m['em_dashes_per_1k']}/1k · sentence CV {m['sentence_length_cv']} "
          f"(mean {m['sentence_mean_len']}w, n={m['sentence_count']}) · triads {m['triads']}")
    c = result["counts"]
    print(f"findings: {c['critical']} critical · {c['high']} high · {c['med']} med · {c['low']} low")
    for f in result["findings"]:
        loc = f"L{f['line']}" if f["line"] else "doc"
        print(f"  [{f['severity']:8}] {loc:>6}  {f['tell']}  ->  {f['match']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
