"""
Important file filtering for RepoMap.
"""

import os
from typing import List

IMPORTANT_FILENAMES = {
    # Project docs
    "README.md", "README.txt", "readme.md", "README.rst", "README",
    "CLAUDE.md",
    # Python
    "requirements.txt", "Pipfile", "pyproject.toml", "setup.py", "setup.cfg",
    "uv.lock",
    # Node/Bun
    "package.json", "yarn.lock", "package-lock.json", "bun.lockb",
    "tsconfig.json",
    # Containers
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    # Git/ignore
    ".gitignore", ".gitattributes", ".dockerignore",
    # Build
    "Makefile", "makefile", "CMakeLists.txt",
    # Env
    ".env", ".env.example", ".env.local",
    # Python tooling
    "tox.ini", "pytest.ini", ".pytest.ini",
    ".flake8", ".pylintrc", "mypy.ini", "ruff.toml",
    # Go / Rust
    "go.mod", "go.sum", "Cargo.toml", "Cargo.lock",
    # JVM
    "pom.xml", "build.gradle", "build.gradle.kts",
    # PHP / Ruby
    "composer.json", "composer.lock",
    "Gemfile", "Gemfile.lock",
    # Swift
    "Package.swift",
    # Svelte
    "svelte.config.js", "vite.config.ts", "vite.config.js",
    # MCP
    ".mcp.json",
}

IMPORTANT_DIR_PATTERNS = {
    os.path.normpath(".github/workflows"): lambda fname: fname.endswith((".yml", ".yaml")),
    os.path.normpath(".github"): lambda fname: fname.endswith((".md", ".yml", ".yaml")),
    os.path.normpath(".claude"): lambda fname: fname.endswith((".md", ".json")),
    os.path.normpath("docs"): lambda fname: fname.endswith((".md", ".rst", ".txt")),
}


def is_important(rel_file_path: str) -> bool:
    """Check if a file is considered important."""
    normalized_path = os.path.normpath(rel_file_path)
    file_name = os.path.basename(normalized_path)
    dir_name = os.path.dirname(normalized_path)

    # Check specific directory patterns
    for important_dir, checker_func in IMPORTANT_DIR_PATTERNS.items():
        if dir_name == important_dir and checker_func(file_name):
            return True
    
    # Check if the full normalized path is important
    if normalized_path in IMPORTANT_FILENAMES:
        return True
    
    # Check if just the basename is important
    if file_name in IMPORTANT_FILENAMES:
        return True
        
    return False


def filter_important_files(file_paths: List[str]) -> List[str]:
    """Filter list to only include important files."""
    return [path for path in file_paths if is_important(path)]
