import re
from collections import Counter
from . import iter_source_files

# Comment-style languages for quote checking
QUOTE_LANGS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.rb'}

# Languages with import-order conventions
IMPORT_LANGS = {'.py', '.js', '.ts', '.jsx', '.tsx'}

# Python stdlib modules (subset for fast checks)
PYTHON_STDLIB = {
    'os', 'sys', 're', 'json', 'datetime', 'collections', 'itertools',
    'functools', 'pathlib', 'subprocess', 'argparse', 'typing', 'math',
    'hashlib', 'logging', 'unittest', 'io', 'abc', 'enum', 'dataclasses',
}

# Multi-language function definition pattern
FUNC_DEF_PATTERN = re.compile(
    r'(?:def|func|fn|function)\s+(\w+)'
)


def check_import_order(filepath):
    """Check Python import ordering (stdlib before third-party before local)."""
    if filepath.suffix != '.py':
        return []

    findings = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    import_section = []
    in_imports = False
    start_line = 0

    for i, line in enumerate(lines, 1):
        if re.match(r'^(import |from .+ import)', line):
            if not in_imports:
                in_imports = True
                start_line = i
            import_section.append((i, line.strip()))
        elif in_imports and line.strip() and not line.startswith('#'):
            break

    if len(import_section) < 2:
        return findings

    stdlib, third_party = [], []
    for line_num, line in import_section:
        if line.startswith('from .') or line.startswith('from ..'):
            continue  # local imports — skip
        match = re.search(r'(?:from|import)\s+(\w+)', line)
        if match and match.group(1) in PYTHON_STDLIB:
            stdlib.append(line_num)
        else:
            third_party.append(line_num)

    if stdlib and third_party and min(third_party) < max(stdlib):
        findings.append({
            'type': 'mixed_conventions',
            'file': str(filepath),
            'line': start_line,
            'message': 'Imports not organized: stdlib should come before third-party',
            'severity': 'low',
        })

    return findings


def check_quote_style(filepath):
    """Check for mixed quote styles in files that commonly use them."""
    if filepath.suffix not in QUOTE_LANGS:
        return []

    findings = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.read().split('\n')

    single = sum(1 for l in lines if "'" in l and '"' not in l)
    double = sum(1 for l in lines if '"' in l and "'" not in l)

    if single > 5 and double > 5:
        ratio = min(single, double) / max(single, double)
        if ratio > 0.3:
            findings.append({
                'type': 'mixed_conventions',
                'file': str(filepath),
                'line': 1,
                'message': f'Mixed quote styles: {single} single, {double} double',
                'severity': 'low',
            })

    return findings


def check_naming_conventions(repomap_data):
    """Check for mixed naming conventions across all languages."""
    findings = []
    styles = Counter()

    for data in repomap_data.values():
        for definition in data['definitions']:
            match = FUNC_DEF_PATTERN.search(definition['content'])
            if not match:
                continue
            name = match.group(1)
            if re.match(r'^[a-z_][a-z0-9_]*$', name):
                styles['snake_case'] += 1
            elif re.match(r'^[a-z][a-zA-Z0-9]*$', name):
                styles['camelCase'] += 1

    if styles['snake_case'] > 5 and styles['camelCase'] > 5:
        ratio = min(styles.values()) / max(styles.values())
        if ratio > 0.2:
            findings.append({
                'type': 'mixed_conventions',
                'file': 'multiple files',
                'line': 0,
                'message': f"Mixed naming: {styles['snake_case']} snake_case, {styles['camelCase']} camelCase",
                'severity': 'medium',
            })

    return findings


def detect(repomap_data, source_dir):
    findings = check_naming_conventions(repomap_data)
    for filepath in iter_source_files(source_dir):
        findings.extend(check_import_order(filepath))
        findings.extend(check_quote_style(filepath))
    return findings
