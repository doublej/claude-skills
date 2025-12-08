import re
from pathlib import Path
from collections import defaultdict


def extract_signatures(repomap_data):
    signatures = defaultdict(list)

    for filepath, data in repomap_data.items():
        for definition in data['definitions']:
            content = definition['content']
            func_match = re.match(r'def\s+(\w+)\s*\(([^)]*)\)', content)

            if func_match:
                name = func_match.group(1)
                params = normalize_params(func_match.group(2))
                signature = f"{name}({params})"
                signatures[signature].append({
                    'file': filepath,
                    'line': definition['line'],
                    'name': name
                })

    return signatures


def normalize_params(params):
    parts = [p.strip().split('=')[0].split(':')[0].strip() for p in params.split(',')]
    return ', '.join(p for p in parts if p)


def find_duplicate_signatures(signatures):
    findings = []

    for signature, locations in signatures.items():
        if len(locations) > 1:
            files = [loc['file'] for loc in locations]
            unique_files = set(files)

            if len(unique_files) > 1:
                loc = locations[0]
                other_locs = ', '.join(f"{l['file']}:{l['line']}" for l in locations[1:])
                findings.append({
                    'type': 'duplicate_code',
                    'file': loc['file'],
                    'line': loc['line'],
                    'message': f"Duplicate signature '{loc['name']}' also in {other_locs}",
                    'severity': 'medium'
                })

    return findings


def find_similar_functions(source_dir):
    findings = []
    function_bodies = defaultdict(list)

    for filepath in Path(source_dir).rglob('*.py'):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        func_pattern = r'def\s+(\w+)\s*\([^)]*\):[^\n]*\n((?:    .+\n)+)'
        for match in re.finditer(func_pattern, content):
            name = match.group(1)
            body = match.group(2)
            normalized = normalize_body(body)

            if len(normalized) > 50:
                function_bodies[normalized].append({
                    'file': str(filepath.relative_to(source_dir)),
                    'name': name,
                    'line': content[:match.start()].count('\n') + 1
                })

    for body, locations in function_bodies.items():
        if len(locations) > 1:
            loc = locations[0]
            other_locs = ', '.join(f"{l['file']}:{l['line']}" for l in locations[1:])
            findings.append({
                'type': 'duplicate_code',
                'file': loc['file'],
                'line': loc['line'],
                'message': f"Similar function '{loc['name']}' to {other_locs}",
                'severity': 'low'
            })

    return findings


def normalize_body(body):
    body = re.sub(r'#.*', '', body)
    body = re.sub(r'\s+', ' ', body)
    body = re.sub(r'["\'].*?["\']', 'STR', body)
    body = re.sub(r'\b\d+\b', 'NUM', body)
    return body.strip()


def detect(repomap_data, source_dir):
    signatures = extract_signatures(repomap_data)
    findings = find_duplicate_signatures(signatures)
    findings.extend(find_similar_functions(source_dir))
    return findings
