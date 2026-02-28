import re
from .utils import iter_source_files

# Multi-language definition patterns
DEF_PATTERN = re.compile(r'(?:def|func|fn|function)\s+(\w+)')
CLASS_PATTERN = re.compile(r'class\s+(\w+)')

# Multi-language import patterns
IMPORT_PATTERNS = [
    re.compile(r'^import\s+(\w+)'),                         # Python/Go/Java
    re.compile(r'^from\s+\S+\s+import\s+(.+)'),             # Python from-import
    re.compile(r"(?:import|require)\s*\(\s*['\"](.+?)['\"]\s*\)"),  # JS/TS require/import
    re.compile(r'^use\s+(.+);'),                             # Rust use
]

# Multi-language commented-out code patterns
COMMENTED_CODE_PATTERNS = [
    re.compile(r'#\s*(def|class|import|from|if|for|while)\s+\w+'),
    re.compile(r'#\s*\w+\s*=\s*.+'),
    re.compile(r'#\s*return\s+'),
    re.compile(r'//\s*(function|class|import|const|let|var|if|for|while)\s+\w+'),
    re.compile(r'//\s*\w+\s*=\s*.+'),
    re.compile(r'//\s*return\s+'),
]


def find_orphaned_definitions(repomap_data):
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


def find_commented_code(source_dir):
    findings = []
    for filepath in iter_source_files(source_dir):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in COMMENTED_CODE_PATTERNS:
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


def find_unused_imports(source_dir):
    """Find imports where the imported name appears only once (the import line itself)."""
    findings = []
    for filepath in iter_source_files(source_dir):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        imports = {}
        for line_num, line in enumerate(lines, 1):
            for pattern in IMPORT_PATTERNS:
                match = pattern.match(line)
                if not match:
                    continue
                names_str = match.group(1)
                for name in re.findall(r'\b(\w+)\b', names_str):
                    if name not in ('import', 'from', 'as'):
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


def detect(repomap_data, source_dir):
    findings = find_orphaned_definitions(repomap_data)
    findings.extend(find_commented_code(source_dir))
    findings.extend(find_unused_imports(source_dir))
    return findings
