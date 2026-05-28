#!/usr/bin/env python3
"""Multi-language logging scanner. Mechanical extraction only — semantic judgment is Claude's job.

Detects log call sites, classifies mechanical issues, surfaces gap candidates.
Languages: Python, JavaScript/TypeScript, Rust, Go, Swift.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

EXCLUDE_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".venv", "venv", "__pycache__", "target", ".cargo", "vendor",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "coverage",
    ".DS_Store", "DerivedData", ".build",
}
EXCLUDE_FILE_PATTERNS = (".min.js", ".bundle.js", ".d.ts", ".lock", ".pyc")
TEST_HINTS = ("test_", "_test.", ".test.", ".spec.", "tests/", "/__tests__/")

LANG_BY_EXT = {
    ".py": "python",
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript",
    ".rs": "rust",
    ".go": "go",
    ".swift": "swift",
}

VAGUE_TERMS = {
    "done", "ok", "okay", "error", "failed", "fail", "success", "successful",
    "start", "started", "starting", "stop", "stopped", "stopping",
    "completed", "complete", "running", "processing", "processed",
    "log", "logging", "here", "test", "debug", "info", "warn", "warning",
    "called", "entered", "exit", "exited", "returning", "returned",
    "yes", "no", "true", "false", "null", "none", "n/a",
    "got it", "all good", "doing it", "happens", "happened",
}

CRITICAL_WORDS = re.compile(r"\b(fatal|critical|panic|crash|corrupt|data\s*loss|unrecoverable)\b", re.I)
ERROR_WORDS = re.compile(r"\b(error|exception|fail|failed|failure|denied|rejected|timeout|abort)\b", re.I)


@dataclass
class LogCall:
    line: int
    level: str
    message: str
    scope: str
    has_interpolation: bool
    has_structured_fields: bool
    in_loop: bool
    in_error_handler: bool
    issues: list[str] = field(default_factory=list)


@dataclass
class Gap:
    line: int
    kind: str
    scope: str
    snippet: str


@dataclass
class FileResult:
    path: str
    language: str
    logger: str
    calls: list[LogCall] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)


# ---------- file walking ----------

def walk_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if any(p.name.endswith(suf) for suf in EXCLUDE_FILE_PATTERNS):
            continue
        if p.suffix not in LANG_BY_EXT:
            continue
        yield p


def is_test_file(path: Path) -> bool:
    s = str(path).lower()
    return any(h in s for h in TEST_HINTS)


# ---------- logger detection ----------

LOGGER_SIGS = {
    "python": [
        ("loguru", re.compile(r"from\s+loguru\s+import|import\s+loguru")),
        ("structlog", re.compile(r"import\s+structlog|from\s+structlog")),
        ("logging", re.compile(r"import\s+logging|from\s+logging\s+import|getLogger\s*\(")),
    ],
    "javascript": [
        ("pino", re.compile(r"from\s+['\"]pino['\"]|require\(\s*['\"]pino['\"]")),
        ("winston", re.compile(r"from\s+['\"]winston['\"]|require\(\s*['\"]winston['\"]")),
        ("bunyan", re.compile(r"from\s+['\"]bunyan['\"]|require\(\s*['\"]bunyan['\"]")),
        ("console", re.compile(r"console\.(log|info|warn|error|debug|trace)")),
    ],
    "typescript": [
        ("pino", re.compile(r"from\s+['\"]pino['\"]")),
        ("winston", re.compile(r"from\s+['\"]winston['\"]")),
        ("bunyan", re.compile(r"from\s+['\"]bunyan['\"]")),
        ("console", re.compile(r"console\.(log|info|warn|error|debug|trace)")),
    ],
    "rust": [
        ("tracing", re.compile(r"use\s+tracing(::|\s)")),
        ("log", re.compile(r"use\s+log(::|\s)")),
    ],
    "go": [
        ("zap", re.compile(r"go\.uber\.org/zap")),
        ("zerolog", re.compile(r"github\.com/rs/zerolog")),
        ("logrus", re.compile(r"github\.com/sirupsen/logrus")),
        ("slog", re.compile(r'"log/slog"|slog\.(Info|Warn|Error|Debug)')),
        ("log", re.compile(r'"log"|log\.(Print|Fatal|Panic)')),
    ],
    "swift": [
        ("os.Logger", re.compile(r"import\s+os|Logger\s*\(\s*subsystem")),
        ("print", re.compile(r"\bprint\s*\(")),
    ],
}


def detect_logger(language: str, source: str) -> str:
    for name, pat in LOGGER_SIGS.get(language, []):
        if pat.search(source):
            return f"{language}:{name}"
    return f"{language}:none"


# ---------- per-language call extraction ----------

CALL_PATTERNS: dict[str, list[tuple[str, re.Pattern]]] = {
    "python": [
        # logger.info("msg") / log.info("msg") / logging.info("msg") / loguru's logger.info
        ("info",  re.compile(r"\b(?:logger|log|logging|_log)\.info\s*\(")),
        ("debug", re.compile(r"\b(?:logger|log|logging|_log)\.debug\s*\(")),
        ("warn",  re.compile(r"\b(?:logger|log|logging|_log)\.(?:warning|warn)\s*\(")),
        ("error", re.compile(r"\b(?:logger|log|logging|_log)\.(?:error|exception)\s*\(")),
        ("error", re.compile(r"\b(?:logger|log|logging|_log)\.critical\s*\(")),
        ("info",  re.compile(r"^\s*print\s*\(")),  # bare print → flag as candidate
    ],
    "javascript": [
        ("info",  re.compile(r"\bconsole\.(?:log|info)\s*\(")),
        ("debug", re.compile(r"\bconsole\.(?:debug|trace)\s*\(")),
        ("warn",  re.compile(r"\bconsole\.warn\s*\(")),
        ("error", re.compile(r"\bconsole\.error\s*\(")),
        ("info",  re.compile(r"\b(?:logger|log)\.info\s*\(")),
        ("debug", re.compile(r"\b(?:logger|log)\.debug\s*\(")),
        ("warn",  re.compile(r"\b(?:logger|log)\.warn\s*\(")),
        ("error", re.compile(r"\b(?:logger|log)\.(?:error|fatal)\s*\(")),
    ],
    "rust": [
        ("info",  re.compile(r"\b(?:tracing|log)?::?info!\s*\(|\binfo!\s*\(")),
        ("debug", re.compile(r"\b(?:tracing|log)?::?debug!\s*\(|\bdebug!\s*\(|\btrace!\s*\(")),
        ("warn",  re.compile(r"\b(?:tracing|log)?::?warn!\s*\(|\bwarn!\s*\(")),
        ("error", re.compile(r"\b(?:tracing|log)?::?error!\s*\(|\berror!\s*\(")),
    ],
    "go": [
        ("info",  re.compile(r"\b(?:slog|log|logger)\.Info\w*\s*\(")),
        ("debug", re.compile(r"\b(?:slog|log|logger)\.Debug\w*\s*\(")),
        ("warn",  re.compile(r"\b(?:slog|log|logger)\.Warn\w*\s*\(")),
        ("error", re.compile(r"\b(?:slog|log|logger)\.(?:Error|Fatal|Panic)\w*\s*\(")),
    ],
    "swift": [
        ("info",  re.compile(r"\b(?:logger|log)\.(?:info|notice)\s*\(")),
        ("debug", re.compile(r"\b(?:logger|log)\.(?:debug|trace)\s*\(")),
        ("warn",  re.compile(r"\b(?:logger|log)\.warning\s*\(")),
        ("error", re.compile(r"\b(?:logger|log)\.(?:error|fault|critical)\s*\(")),
        ("info",  re.compile(r"^\s*print\s*\(")),
    ],
}
CALL_PATTERNS["typescript"] = CALL_PATTERNS["javascript"]


def extract_message(call_line: str) -> tuple[str, bool, bool]:
    """Pull first string literal out of a call line.

    Returns (message, has_interpolation, has_structured_fields).
    Best-effort: regex-only, copes with single/double/backtick/triple-quote starts.
    """
    has_interp = bool(re.search(r"\$\{|\{[^{}]*\}|%[sdifr]|%\([^)]+\)|\\\(", call_line))
    has_fields = bool(re.search(r"=\s*[\w.\[\]]+|extra\s*=|fields\s*\(|with_fields|\.With\(", call_line))

    for quote in ('"""', "'''", '"', "'", "`"):
        idx = call_line.find(quote)
        if idx == -1:
            continue
        end = call_line.find(quote, idx + len(quote))
        if end == -1:
            return (call_line[idx + len(quote):].strip()[:120], has_interp, has_fields)
        return (call_line[idx + len(quote):end].strip()[:120], has_interp, has_fields)
    return ("", has_interp, has_fields)


# ---------- scope detection (cheap heuristic) ----------

SCOPE_PATTERNS = {
    "python": re.compile(r"^\s*(?:async\s+)?def\s+(\w+)"),
    "javascript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(\w+)\s*[:=]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>)"),
    "typescript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(\w+)\s*[:=]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>)"),
    "rust": re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)"),
    "go": re.compile(r"^\s*func\s+(?:\([^)]+\)\s+)?(\w+)"),
    "swift": re.compile(r"^\s*(?:public\s+|private\s+|internal\s+|fileprivate\s+|open\s+)?(?:static\s+)?func\s+(\w+)"),
}


def find_scope(lines: list[str], lineno: int, language: str) -> str:
    pat = SCOPE_PATTERNS.get(language)
    if not pat:
        return "<top-level>"
    for i in range(lineno - 1, -1, -1):
        m = pat.match(lines[i])
        if m:
            return next((g for g in m.groups() if g), "<anon>")
    return "<top-level>"


# ---------- structural context ----------

LOOP_PATTERNS = {
    "python": re.compile(r"^\s*(?:for|while)\b"),
    "javascript": re.compile(r"^\s*(?:for|while)\s*\("),
    "typescript": re.compile(r"^\s*(?:for|while)\s*\("),
    "rust": re.compile(r"^\s*(?:for|while|loop)\b"),
    "go": re.compile(r"^\s*for\b"),
    "swift": re.compile(r"^\s*(?:for|while|repeat)\b"),
}

ERROR_HANDLER_PATTERNS = {
    "python": re.compile(r"^\s*except\b"),
    "javascript": re.compile(r"^\s*}?\s*catch\s*\("),
    "typescript": re.compile(r"^\s*}?\s*catch\s*\("),
    "rust": re.compile(r"\bErr\s*\(|\.unwrap_err\(\)|match.*\{[^}]*Err"),
    "go": re.compile(r"if\s+err\s*!=\s*nil"),
    "swift": re.compile(r"^\s*}?\s*catch\b"),
}


def in_construct(lines: list[str], lineno: int, language: str, pat: re.Pattern, look_back: int = 8) -> bool:
    base_indent = len(lines[lineno]) - len(lines[lineno].lstrip()) if lineno < len(lines) else 0
    for i in range(lineno - 1, max(-1, lineno - look_back - 1), -1):
        line = lines[i]
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent >= base_indent:
            continue
        return bool(pat.search(line))
    return False


# ---------- gap detection ----------

EXTERNAL_CALL_PATTERNS = {
    "python": re.compile(r"\b(?:requests|httpx|aiohttp|urllib)\.(?:get|post|put|patch|delete|request)\b|\.execute\(|\.commit\(|subprocess\.|os\.system"),
    "javascript": re.compile(r"\bfetch\s*\(|\baxios\.|\.query\(|\.execute\(|child_process\."),
    "typescript": re.compile(r"\bfetch\s*\(|\baxios\.|\.query\(|\.execute\(|child_process\."),
    "rust": re.compile(r"reqwest::|sqlx::|tokio::process::|std::process::Command"),
    "go": re.compile(r"http\.(?:Get|Post|Do)|sql\.Exec|exec\.Command"),
    "swift": re.compile(r"URLSession|dataTask|Process\("),
}


def find_gaps(lines: list[str], language: str) -> list[Gap]:
    gaps: list[Gap] = []
    err_pat = ERROR_HANDLER_PATTERNS.get(language)
    ext_pat = EXTERNAL_CALL_PATTERNS.get(language)
    call_pats = [p for _, p in CALL_PATTERNS.get(language, [])]

    def block_has_log(start: int, end: int) -> bool:
        for j in range(start, min(end, len(lines))):
            if any(p.search(lines[j]) for p in call_pats):
                return True
        return False

    for i, line in enumerate(lines):
        if err_pat and err_pat.search(line):
            indent = len(line) - len(line.lstrip())
            block_end = i + 1
            for j in range(i + 1, min(i + 12, len(lines))):
                if not lines[j].strip():
                    continue
                jindent = len(lines[j]) - len(lines[j].lstrip())
                if jindent <= indent and lines[j].strip():
                    break
                block_end = j + 1
            if block_end - i <= 1:
                continue
            if not block_has_log(i + 1, block_end):
                scope = find_scope(lines, i, language)
                snippet = "\n".join(lines[i:block_end])[:240]
                gaps.append(Gap(line=i + 1, kind="silent_error_branch", scope=scope, snippet=snippet))

        if ext_pat and ext_pat.search(line):
            window_start = max(0, i - 3)
            window_end = min(len(lines), i + 4)
            if not block_has_log(window_start, window_end):
                scope = find_scope(lines, i, language)
                snippet = lines[i].strip()[:200]
                gaps.append(Gap(line=i + 1, kind="silent_external_call", scope=scope, snippet=snippet))
    return gaps


# ---------- per-call classification ----------

def classify(call: LogCall, language: str) -> None:
    msg_lower = call.message.lower().strip().rstrip(".!:").strip()

    if not call.message or len(msg_lower) < 3 or msg_lower in VAGUE_TERMS:
        call.issues.append("vague_message")

    if CRITICAL_WORDS.search(call.message) and call.level not in ("error",):
        call.issues.append("level_too_low_critical")
    elif ERROR_WORDS.search(call.message) and call.level in ("debug", "info"):
        call.issues.append("level_too_low_error_word")

    if call.in_error_handler and call.level in ("debug", "info"):
        call.issues.append("error_branch_low_level")

    if call.in_loop and call.level in ("info", "warn", "error"):
        call.issues.append("hot_loop_candidate")

    if not call.has_interpolation and not call.has_structured_fields:
        call.issues.append("no_context_fields")

    if re.search(r"['\"]\s*\+\s*\w|\w\s*\+\s*['\"]", call.message):
        call.issues.append("string_concat_format")


# ---------- per-file scan ----------

def scan_file(path: Path) -> FileResult | None:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    language = LANG_BY_EXT[path.suffix]
    lines = source.splitlines()
    logger = detect_logger(language, source)
    fr = FileResult(path=str(path), language=language, logger=logger)

    loop_pat = LOOP_PATTERNS.get(language)
    err_pat = ERROR_HANDLER_PATTERNS.get(language)

    for level, pat in CALL_PATTERNS.get(language, []):
        for m in pat.finditer(source):
            lineno = source.count("\n", 0, m.start())
            line_text = lines[lineno] if lineno < len(lines) else ""
            message, has_interp, has_fields = extract_message(line_text)
            scope = find_scope(lines, lineno, language)
            in_loop = bool(loop_pat and in_construct(lines, lineno, language, loop_pat))
            in_err = bool(err_pat and in_construct(lines, lineno, language, err_pat, look_back=4))
            call = LogCall(
                line=lineno + 1,
                level=level,
                message=message,
                scope=scope,
                has_interpolation=has_interp,
                has_structured_fields=has_fields,
                in_loop=in_loop,
                in_error_handler=in_err,
            )
            classify(call, language)
            fr.calls.append(call)

    fr.gaps = find_gaps(lines, language)
    return fr


# ---------- summary ----------

def build_summary(results: list[FileResult]) -> dict:
    issue_counts: dict[str, int] = {}
    gap_counts: dict[str, int] = {}
    loggers: dict[str, int] = {}
    by_lang: dict[str, int] = {}
    total_calls = 0
    for fr in results:
        loggers[fr.logger] = loggers.get(fr.logger, 0) + 1
        by_lang[fr.language] = by_lang.get(fr.language, 0) + len(fr.calls)
        total_calls += len(fr.calls)
        for c in fr.calls:
            for issue in c.issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        for g in fr.gaps:
            gap_counts[g.kind] = gap_counts.get(g.kind, 0) + 1
    return {
        "files_scanned": len(results),
        "log_calls_found": total_calls,
        "calls_by_language": by_lang,
        "loggers_detected": loggers,
        "issue_counts": dict(sorted(issue_counts.items(), key=lambda kv: -kv[1])),
        "gap_counts": dict(sorted(gap_counts.items(), key=lambda kv: -kv[1])),
    }


# ---------- top issue surface (for token-tight reports) ----------

def top_issues(results: list[FileResult], limit: int = 50) -> list[dict]:
    flat: list[tuple[int, dict]] = []
    severity = {
        "level_too_low_critical": 5,
        "error_branch_low_level": 4,
        "level_too_low_error_word": 3,
        "vague_message": 2,
        "string_concat_format": 2,
        "no_context_fields": 1,
        "hot_loop_candidate": 1,
    }
    for fr in results:
        for c in fr.calls:
            if not c.issues:
                continue
            score = sum(severity.get(i, 1) for i in c.issues)
            flat.append((score, {
                "file": fr.path, "line": c.line, "level": c.level,
                "scope": c.scope, "message": c.message,
                "issues": c.issues,
            }))
    flat.sort(key=lambda kv: -kv[0])
    return [d for _, d in flat[:limit]]


# ---------- CLI ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-language logging scanner")
    parser.add_argument("root", help="project root")
    parser.add_argument("--json", action="store_true", help="emit full JSON")
    parser.add_argument("--summary", action="store_true", help="emit summary only")
    parser.add_argument("--top", type=int, default=50, help="top N issues to surface")
    parser.add_argument("--include-tests", action="store_true", help="scan test files too")
    parser.add_argument("--no-gaps", action="store_true", help="skip gap detection")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    results: list[FileResult] = []
    for p in walk_files(root):
        if not args.include_tests and is_test_file(p):
            continue
        fr = scan_file(p)
        if fr and (fr.calls or fr.gaps):
            if args.no_gaps:
                fr.gaps = []
            results.append(fr)

    summary = build_summary(results)
    payload = {
        "root": str(root),
        "summary": summary,
        "top_issues": top_issues(results, args.top),
    }
    if args.json:
        payload["files"] = [asdict(fr) for fr in results]
    elif not args.summary:
        payload["files"] = [
            {"path": fr.path, "language": fr.language, "logger": fr.logger,
             "calls_with_issues": [asdict(c) for c in fr.calls if c.issues],
             "gaps": [asdict(g) for g in fr.gaps]}
            for fr in results
        ]
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
