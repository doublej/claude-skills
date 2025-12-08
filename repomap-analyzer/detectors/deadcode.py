import re
from pathlib import Path


def find_orphaned_definitions(repomap_data):
    findings = []

    for filepath, data in repomap_data.items():
        rank = data.get('rank', 0.0)
        if rank == 0.0 and data['definitions']:
            for definition in data['definitions']:
                content = definition['content']
                func_match = re.search(r'def\s+(\w+)', content)
                class_match = re.search(r'class\s+(\w+)', content)

                if func_match or class_match:
                    name = func_match.group(1) if func_match else class_match.group(1)
                    if not name.startswith('_'):
                        findings.append({
                            'type': 'dead_code',
                            'file': filepath,
                            'line': definition['line'],
                            'message': f"'{name}' has PageRank 0 (unreferenced)",
                            'severity': 'medium'
                        })

    return findings


def find_commented_code(source_dir):
    findings = []
    code_patterns = [
        r'#\s*(def|class|import|from|if|for|while)\s+\w+',
        r'#\s*\w+\s*=\s*.+',
        r'#\s*return\s+',
    ]

    for filepath in Path(source_dir).rglob('*.py'):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in code_patterns:
                    if re.search(pattern, line):
                        findings.append({
                            'type': 'dead_code',
                            'file': str(filepath.relative_to(source_dir)),
                            'line': line_num,
                            'message': f"Commented code: {line.strip()[:50]}",
                            'severity': 'low'
                        })
                        break

    return findings


def find_unused_imports(source_dir):
    findings = []

    for filepath in Path(source_dir).rglob('*.py'):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        imports = {}
        for line_num, line in enumerate(lines, 1):
            import_match = re.match(r'^import\s+(\w+)', line)
            from_match = re.match(r'^from\s+\S+\s+import\s+(.+)', line)

            if import_match:
                module = import_match.group(1)
                imports[module] = line_num
            elif from_match:
                names = from_match.group(1)
                for name in re.findall(r'\b(\w+)\b', names):
                    if name != 'import':
                        imports[name] = line_num

        for name, line_num in imports.items():
            pattern = rf'\b{re.escape(name)}\b'
            occurrences = len(re.findall(pattern, content))
            if occurrences == 1:
                findings.append({
                    'type': 'dead_code',
                    'file': str(filepath.relative_to(source_dir)),
                    'line': line_num,
                    'message': f"Unused import: {name}",
                    'severity': 'low'
                })

    return findings


def detect(repomap_data, source_dir):
    findings = find_orphaned_definitions(repomap_data)
    findings.extend(find_commented_code(source_dir))
    findings.extend(find_unused_imports(source_dir))
    return findings
