from collections.abc import Iterator
from pathlib import Path

# Supported source file extensions for multi-language detection
SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.go', '.rs', '.rb', '.java', '.kt',
    '.swift', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.php', '.lua', '.ex', '.exs',
    '.svelte', '.vue', '.mjs', '.cjs', '.kts', '.cc', '.dart', '.scala',
}

# Source languages no detector reads; reported as coverage.unscanned so zero findings aren't mistaken for clean
UNSCANNED_EXTENSIONS = {
    '.erl', '.hs', '.ml', '.clj', '.r', '.jl', '.zig', '.nim', '.m', '.mm',
    '.fs', '.elm', '.sol', '.gd',
}

# Directories to skip during source file iteration
SKIP_DIRS = {
    'node_modules', '.svelte-kit', 'dist', 'build', '.git',
    '__pycache__', '.venv', 'venv', '.next', '.nuxt',
    'coverage', '.turbo', '.cache', '.output', '.wrangler',
    'vendor', 'third_party', 'bower_components', 'target', 'Pods', '.build',
    'DerivedData', '.gradle', '.dart_tool', 'generated', '__generated__',
}
GENERATED_SUFFIXES = ('.min.js', '.bundle.js', '.d.ts')


def iter_source_files(source_dir: str) -> Iterator[Path]:
    """Yield source files from source_dir matching supported extensions."""
    for filepath in Path(source_dir).rglob('*'):
        if any(part in SKIP_DIRS for part in filepath.parts):
            continue
        if filepath.name.endswith(GENERATED_SUFFIXES):
            continue
        if filepath.is_file() and filepath.suffix in SOURCE_EXTENSIONS:
            yield filepath


def coverage(source_dir: str) -> dict[str, dict[str, int]]:
    """Source files per extension: read by the detectors, or present but unread."""
    scanned: dict[str, int] = {}
    unscanned: dict[str, int] = {}
    for filepath in Path(source_dir).rglob('*'):
        if any(part in SKIP_DIRS for part in filepath.parts) or not filepath.is_file():
            continue
        if filepath.name.endswith(GENERATED_SUFFIXES):
            continue
        bucket = scanned if filepath.suffix in SOURCE_EXTENSIONS else unscanned if filepath.suffix in UNSCANNED_EXTENSIONS else None
        if bucket is not None:
            bucket[filepath.suffix] = bucket.get(filepath.suffix, 0) + 1
    return {'scanned': scanned, 'unscanned': unscanned}
