import re
from collections import defaultdict
from . import iter_source_files

# Multi-language function definition with params
FUNC_DEF_WITH_PARAMS = re.compile(r'(?:def|func|fn|function)\s+(\w+)\s*\(([^)]*)\)')

# Multi-language function body extraction (indented or braced)
INDENTED_FUNC = re.compile(r'(?:def|function)\s+(\w+)\s*\([^)]*\):[^\n]*\n((?:    .+\n)+)')
BRACED_FUNC = re.compile(r'(?:func|fn|function)\s+(\w+)\s*\([^)]*\)\s*(?:[^{]*)\{([^}]+)\}')


def normalize_params(params):
    parts = [p.strip().split('=')[0].split(':')[0].strip() for p in params.split(',')]
    return ', '.join(p for p in parts if p)


def normalize_body(body):
    body = re.sub(r'(?:#|//).*', '', body)  # strip comments
    body = re.sub(r'\s+', ' ', body)
    body = re.sub(r'["\'].*?["\']', 'STR', body)
    body = re.sub(r'\b\d+\b', 'NUM', body)
    return body.strip()


def extract_signatures(repomap_data):
    signatures = defaultdict(list)
    for filepath, data in repomap_data.items():
        for definition in data['definitions']:
            match = FUNC_DEF_WITH_PARAMS.match(definition['content'])
            if not match:
                continue
            name = match.group(1)
            params = normalize_params(match.group(2))
            sig = f"{name}({params})"
            signatures[sig].append({
                'file': filepath,
                'line': definition['line'],
                'name': name,
            })
    return signatures


def find_duplicate_signatures(signatures):
    findings = []
    for locations in signatures.values():
        if len(locations) < 2:
            continue
        unique_files = {loc['file'] for loc in locations}
        if len(unique_files) < 2:
            continue
        loc = locations[0]
        others = ', '.join(f"{l['file']}:{l['line']}" for l in locations[1:])
        findings.append({
            'type': 'duplicate_code',
            'file': loc['file'],
            'line': loc['line'],
            'message': f"Duplicate signature '{loc['name']}' also in {others}",
            'severity': 'medium',
        })
    return findings


def find_similar_functions(source_dir):
    findings = []
    function_bodies = defaultdict(list)

    for filepath in iter_source_files(source_dir):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Try both indented (Python) and braced (JS/Go/Rust) patterns
        for pattern in (INDENTED_FUNC, BRACED_FUNC):
            for match in pattern.finditer(content):
                name = match.group(1)
                body = match.group(2)
                normalized = normalize_body(body)
                if len(normalized) > 50:
                    function_bodies[normalized].append({
                        'file': str(filepath.relative_to(source_dir)),
                        'name': name,
                        'line': content[:match.start()].count('\n') + 1,
                    })

    for locations in function_bodies.values():
        if len(locations) < 2:
            continue
        loc = locations[0]
        others = ', '.join(f"{l['file']}:{l['line']}" for l in locations[1:])
        findings.append({
            'type': 'duplicate_code',
            'file': loc['file'],
            'line': loc['line'],
            'message': f"Similar function '{loc['name']}' to {others}",
            'severity': 'low',
        })

    return findings


def detect(repomap_data, source_dir):
    signatures = extract_signatures(repomap_data)
    findings = find_duplicate_signatures(signatures)
    findings.extend(find_similar_functions(source_dir))
    return findings
