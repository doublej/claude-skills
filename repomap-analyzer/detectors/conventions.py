import re
from pathlib import Path
from collections import Counter


def check_import_order(file_path):
    findings = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
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

    stdlib = []
    third_party = []
    local = []

    for line_num, line in import_section:
        if line.startswith('from .') or line.startswith('from ..'):
            local.append(line_num)
        elif is_stdlib_import(line):
            stdlib.append(line_num)
        else:
            third_party.append(line_num)

    if stdlib and third_party and min(third_party) < max(stdlib):
        findings.append({
            'type': 'mixed_conventions',
            'file': str(file_path),
            'line': start_line,
            'message': 'Imports not organized: stdlib should come before third-party',
            'severity': 'low'
        })

    return findings


def is_stdlib_import(line):
    stdlib_modules = {
        'os', 'sys', 're', 'json', 'datetime', 'collections', 'itertools',
        'functools', 'pathlib', 'subprocess', 'argparse', 'typing'
    }
    match = re.search(r'(?:from|import)\s+(\w+)', line)
    if match:
        return match.group(1) in stdlib_modules
    return False


def check_quote_style(file_path):
    findings = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        lines = content.split('\n')

    single_quotes = sum(1 for line in lines if "'" in line and '"' not in line)
    double_quotes = sum(1 for line in lines if '"' in line and "'" not in line)

    if single_quotes > 5 and double_quotes > 5:
        ratio = min(single_quotes, double_quotes) / max(single_quotes, double_quotes)
        if ratio > 0.3:
            findings.append({
                'type': 'mixed_conventions',
                'file': str(file_path),
                'line': 1,
                'message': f'Mixed quote styles: {single_quotes} single, {double_quotes} double',
                'severity': 'low'
            })

    return findings


def check_naming_conventions(repomap_data):
    findings = []
    naming_styles = Counter()

    for filepath, data in repomap_data.items():
        for definition in data['definitions']:
            content = definition['content']
            func_match = re.search(r'def\s+(\w+)', content)
            if func_match:
                name = func_match.group(1)
                if re.match(r'^[a-z_][a-z0-9_]*$', name):
                    naming_styles['snake_case'] += 1
                elif re.match(r'^[a-z][a-zA-Z0-9]*$', name):
                    naming_styles['camelCase'] += 1

    if naming_styles['snake_case'] > 5 and naming_styles['camelCase'] > 5:
        ratio = min(naming_styles.values()) / max(naming_styles.values())
        if ratio > 0.2:
            findings.append({
                'type': 'mixed_conventions',
                'file': 'multiple files',
                'line': 0,
                'message': f"Mixed naming: {naming_styles['snake_case']} snake_case, {naming_styles['camelCase']} camelCase",
                'severity': 'medium'
            })

    return findings


def detect(repomap_data, source_dir):
    findings = check_naming_conventions(repomap_data)

    for filepath in Path(source_dir).rglob('*.py'):
        findings.extend(check_import_order(filepath))
        findings.extend(check_quote_style(filepath))

    return findings
