import re
from .utils import iter_source_files

# Language-aware definition patterns
DEF_PATTERNS = {
    'func': re.compile(r'(?:def|func|fn|function)\s+(\w+)'),
    'class': re.compile(r'class\s+(\w+)'),
}

# Deprecated markers across languages
DEPRECATED_PATTERNS = [
    re.compile(r'#\s*deprecated', re.IGNORECASE),
    re.compile(r'@deprecated', re.IGNORECASE),
    re.compile(r'@Deprecated', re.IGNORECASE),
    re.compile(r'//\s*deprecated', re.IGNORECASE),
    re.compile(r'#\s*(?:fixme|todo).*(?:deprecat|remove)', re.IGNORECASE),
    re.compile(r'//\s*(?:FIXME|TODO).*(?:deprecat|remove)', re.IGNORECASE),
]


def extract_identifiers(repomap_data):
    identifiers = {}
    for filepath, data in repomap_data.items():
        identifiers[filepath] = []
        for definition in data['definitions']:
            content = definition['content'].strip()
            for pattern in DEF_PATTERNS.values():
                match = pattern.search(content)
                if match:
                    identifiers[filepath].append(match.group(1))
                    break
    return identifiers


def to_snake_case(name):
    return re.sub('([A-Z]+)', r'_\1', name).lower().lstrip('_')


def to_camel_case(name):
    parts = name.split('_')
    return ''.join(word.capitalize() for word in parts)


def find_naming_inconsistencies(identifiers):
    findings = []
    all_names = {}

    for filepath, names in identifiers.items():
        for name in names:
            all_names.setdefault(name, []).append(filepath)

    for name, files in all_names.items():
        snake = to_snake_case(name)
        camel = to_camel_case(name)

        if snake != name and snake in all_names:
            for filepath in files:
                findings.append({
                    'type': 'deprecated_pattern',
                    'file': filepath,
                    'line': 0,
                    'message': f"Old convention '{name}' coexists with '{snake}'",
                    'severity': 'medium',
                })

        if camel != name and camel in all_names:
            for filepath in files:
                findings.append({
                    'type': 'deprecated_pattern',
                    'file': filepath,
                    'line': 0,
                    'message': f"Inconsistent naming: '{name}' vs '{camel}'",
                    'severity': 'medium',
                })

    return findings


def check_deprecated_markers(source_dir):
    findings = []
    for filepath in iter_source_files(source_dir):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in DEPRECATED_PATTERNS:
                    if pattern.search(line):
                        findings.append({
                            'type': 'deprecated_pattern',
                            'file': str(filepath.relative_to(source_dir)),
                            'line': line_num,
                            'message': f"Deprecated marker: {line.strip()[:60]}",
                            'severity': 'medium',
                        })
                        break
    return findings


def detect(repomap_data, source_dir):
    identifiers = extract_identifiers(repomap_data)
    findings = find_naming_inconsistencies(identifiers)
    findings.extend(check_deprecated_markers(source_dir))
    return findings
