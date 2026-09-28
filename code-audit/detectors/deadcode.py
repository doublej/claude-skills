import re
from pathlib import Path
from typing import Any

from .utils import iter_source_files

# Multi-language definition patterns
DEF_PATTERN = re.compile(r'(?:def|func|fn|function)\s+(\w+)')
CLASS_PATTERN = re.compile(r'class\s+(\w+)')

# Multi-language import patterns
IMPORT_PATTERNS = [
    re.compile(r'^import\s+[\w.]+\s+as\s+(\w+)'),          # Python `import a.b as c` binds c
    re.compile(r'^import\s+(\w+)'),                         # Python/Go/Java
    re.compile(r'^from\s+\S+\s+import\s+(.+)'),             # Python from-import
    re.compile(r"(?:import|require)\s*\(\s*['\"](.+?)['\"]\s*\)"),  # JS/TS require/import
    re.compile(r'^use\s+(.+);'),                             # Rust use
]

# Commented-out code, by comment syntax. `#` only in hash-comment languages and only at line
# start: elsewhere it is Svelte `{#if}`, a C `#if` directive or a CSS colour.
HASH_COMMENT_SUFFIXES = {'.py', '.rb', '.ex', '.exs'}
# Control keywords need code shape (`(` or a trailing `:`), so prose like "# for each file" passes.
HASH_COMMENTED_CODE = [
    re.compile(r'^\s*#\s*(?:def|class)\s+\w+\s*[(:]'),
    re.compile(r'^\s*#\s*(?:import\s+[\w.]+|from\s+[\w.]+\s+import\b)'),
    re.compile(r'^\s*#\s*(?:if|for|while)\b.*:\s*$'),
    re.compile(r'^\s*#\s*\w+\s*=\s*.+'),
    re.compile(r'^\s*#\s*return\s+'),
]
# Whole-line comments only; a trailing `// note` after code is not commented-out code.
SLASH_COMMENTED_CODE = [
    re.compile(r'^\s*//\s*(?:function\s+\w+\s*\(|class\s+\w+\s*[{(]|import\s+.+\s+from\s|(?:const|let|var)\s+\w+\s*=)'),
    re.compile(r'^\s*//\s*(?:if|for|while)\s*\('),
    re.compile(r'^\s*//\s*[A-Za-z_][\w.]*\s*=(?!=)\s*\S.*[;)\]}]\s*$'),
    re.compile(r'^\s*//\s*return\s+\S.*;\s*$'),
]
IMPORT_KEYWORDS = {'import', 'from', 'as', 'type', 'typeof'}
# Name-count checks only work where an import binds the names it lists. Go, Rust, Swift, Java and
# friends import modules, globs or traits used implicitly, and their compilers already flag unused ones.
NAMED_IMPORT_SUFFIXES = {'.py', '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs', '.svelte', '.vue'}


def find_orphaned_definitions(repomap_data: dict[str, Any]) -> list[dict[str, Any]]:
    findings = []
    for filepath, data in repomap_data.items():
        if data.get('rank', 0.0) != 0.0 or not data['definitions']:
            continue
        for definition in data['definitions']:
            content = definition['content']
            for pattern in (DEF_PATTERN, CLASS_PATTERN):
                match = pattern.search(content)
                if match:
                    name = match.group(1)
                    if not name.startswith('_'):
                        findings.append({
                            'type': 'dead_code',
                            'file': filepath,
                            'line': definition['line'],
                            'message': f"'{name}' has PageRank 0 (unreferenced)",
                            'severity': 'medium',
                        })
                    break
    return findings


def find_commented_code(source_dir: str | Path) -> list[dict[str, Any]]:
    findings = []
    for filepath in iter_source_files(source_dir):
        patterns = HASH_COMMENTED_CODE if filepath.suffix in HASH_COMMENT_SUFFIXES else SLASH_COMMENTED_CODE
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in patterns:
                    if pattern.search(line):
                        findings.append({
                            'type': 'dead_code',
                            'file': str(filepath.relative_to(source_dir)),
                            'line': line_num,
                            'message': f"Commented code: {line.strip()[:50]}",
                            'severity': 'low',
                        })
                        break
    return findings


def find_unused_imports(source_dir: str | Path) -> list[dict[str, Any]]:
    """Find imports where the imported name appears only once (the import line itself)."""
    findings = []
    for filepath in iter_source_files(source_dir):
        if filepath.suffix not in NAMED_IMPORT_SUFFIXES:
            continue
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        imports = {}
        for line_num, line in enumerate(lines, 1):
            for pattern in IMPORT_PATTERNS:
                match = pattern.match(line)
                if not match or line.startswith('from __future__'):
                    continue
                names_str = match.group(1)
                for name in re.findall(r'\b(\w+)\b', names_str):
                    if name not in IMPORT_KEYWORDS:
                        imports[name] = line_num
                break

        for name, line_num in imports.items():
            occurrences = len(re.findall(rf'\b{re.escape(name)}\b', content))
            if occurrences == 1:
                findings.append({
                    'type': 'dead_code',
                    'file': str(filepath.relative_to(source_dir)),
                    'line': line_num,
                    'message': f"Unused import: {name}",
                    'severity': 'low',
                })

    return findings


def detect(repomap_data: dict[str, Any], source_dir: str | Path) -> list[dict[str, Any]]:
    findings = find_orphaned_definitions(repomap_data)
    findings.extend(find_commented_code(source_dir))
    findings.extend(find_unused_imports(source_dir))
    return findings
