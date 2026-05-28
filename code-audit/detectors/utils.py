# Supported source file extensions for multi-language detection
SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.go', '.rs', '.rb', '.java', '.kt',
    '.swift', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.php', '.lua', '.ex', '.exs',
}

# Directories to skip during source file iteration
SKIP_DIRS = {
    'node_modules', '.svelte-kit', 'dist', 'build', '.git',
    '__pycache__', '.venv', 'venv', '.next', '.nuxt',
    'coverage', '.turbo', '.cache', '.output', '.wrangler',
}


def iter_source_files(source_dir):
    """Yield source files from source_dir matching supported extensions."""
    from pathlib import Path
    for filepath in Path(source_dir).rglob('*'):
        if any(part in SKIP_DIRS for part in filepath.parts):
            continue
        if filepath.is_file() and filepath.suffix in SOURCE_EXTENSIONS:
            yield filepath
