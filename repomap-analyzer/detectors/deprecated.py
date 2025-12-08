import re
from pathlib import Path


def extract_identifiers(repomap_data):
    identifiers = {}
    for filepath, data in repomap_data.items():
        identifiers[filepath] = []
        for definition in data['definitions']:
            content = definition['content'].strip()
            func_match = re.search(r'def\s+(\w+)', content)
            class_match = re.search(r'class\s+(\w+)', content)
            if func_match:
                identifiers[filepath].append(func_match.group(1))
            elif class_match:
                identifiers[filepath].append(class_match.group(1))
    return identifiers


def find_naming_inconsistencies(identifiers):
    findings = []
    all_names = {}

    for filepath, names in identifiers.items():
        for name in names:
            if name not in all_names:
                all_names[name] = []
            all_names[name].append(filepath)

    for name in all_names:
        snake_version = to_snake_case(name)
        camel_version = to_camel_case(name)

        if snake_version != name and snake_version in all_names:
            for filepath in all_names[name]:
                findings.append({
                    'type': 'deprecated_pattern',
                    'file': filepath,
                    'line': 0,
                    'message': f"Old convention '{name}' used alongside new '{snake_version}'",
                    'severity': 'medium'
                })

        if camel_version != name and camel_version in all_names:
            for filepath in all_names[name]:
                findings.append({
                    'type': 'deprecated_pattern',
                    'file': filepath,
                    'line': 0,
                    'message': f"Inconsistent naming: '{name}' vs '{camel_version}'",
                    'severity': 'medium'
                })

    return findings


def to_snake_case(name):
    result = re.sub('([A-Z]+)', r'_\1', name)
    return result.lower().lstrip('_')


def to_camel_case(name):
    parts = name.split('_')
    return ''.join(word.capitalize() for word in parts)


def check_deprecated_markers(source_dir):
    findings = []
    deprecated_patterns = [
        r'#\s*deprecated',
        r'@deprecated',
        r'#\s*fixme.*deprecat',
        r'#\s*todo.*remove'
    ]

    for pattern in deprecated_patterns:
        for filepath in Path(source_dir).rglob('*.py'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append({
                            'type': 'deprecated_pattern',
                            'file': str(filepath.relative_to(source_dir)),
                            'line': line_num,
                            'message': f"Deprecated marker found: {line.strip()[:60]}",
                            'severity': 'medium'
                        })

    return findings


def detect(repomap_data, source_dir):
    identifiers = extract_identifiers(repomap_data)
    findings = find_naming_inconsistencies(identifiers)
    findings.extend(check_deprecated_markers(source_dir))
    return findings
