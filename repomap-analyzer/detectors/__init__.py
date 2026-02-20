from . import deprecated
from . import conventions
from . import deadcode
from . import duplicates

__all__ = ['deprecated', 'conventions', 'deadcode', 'duplicates']

# Supported source file extensions for multi-language detection
SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.go', '.rs', '.rb', '.java', '.kt',
    '.swift', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.php', '.lua', '.ex', '.exs',
}


def iter_source_files(source_dir):
    """Yield source files from source_dir matching supported extensions."""
    from pathlib import Path
    for filepath in Path(source_dir).rglob('*'):
        if filepath.is_file() and filepath.suffix in SOURCE_EXTENSIONS:
            yield filepath
