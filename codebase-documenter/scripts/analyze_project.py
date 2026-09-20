#!/usr/bin/env python3
"""
Analyze project structure and detect technologies.

Usage:
    python3 analyze_project.py <project_path> [--output analysis.json]
"""
import argparse
import json
import os
from pathlib import Path
from collections import defaultdict
import re


LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
}

FRAMEWORK_INDICATORS = {
    "FastAPI": ["from fastapi", "import fastapi"],
    "Django": ["from django", "import django"],
    "Flask": ["from flask", "import flask"],
    "React": ["from 'react'", "from \"react\"", "react-dom"],
    "Next.js": ["next/", "next.config"],
    "Vue": ["from 'vue'", "from \"vue\""],
    "Svelte": [".svelte", "svelte.config"],
    "Express": ["express()", "require('express')"],
    "NestJS": ["@nestjs/"],
    "Gin": ["github.com/gin-gonic/gin"],
    "Actix": ["actix-web"],
    "Spring": ["@SpringBootApplication", "spring-boot"],
    "SwiftUI": ["import SwiftUI"],
    "UIKit": ["import UIKit"],
}

CONFIG_FILES = {
    "package.json": "Node/npm",
    "requirements.txt": "Python/pip",
    "pyproject.toml": "Python/poetry",
    "Cargo.toml": "Rust/cargo",
    "go.mod": "Go modules",
    "pom.xml": "Java/Maven",
    "build.gradle": "Java/Gradle",
    "Gemfile": "Ruby/bundler",
    "composer.json": "PHP/composer",
}

ENTRY_POINT_PATTERNS = {
    "main.py": "Python entry",
    "app.py": "Python app",
    "__main__.py": "Python module",
    "index.ts": "TypeScript entry",
    "index.js": "JavaScript entry",
    "main.go": "Go entry",
    "main.rs": "Rust entry",
    "Main.java": "Java entry",
}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""
    ignore_patterns = [
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", "target", ".idea", ".vscode"
    ]
    return any(pattern in path.parts for pattern in ignore_patterns)


def detect_languages(project_path: Path) -> dict:
    """Detect programming languages by file extensions."""
    lang_counts = defaultdict(int)

    for file_path in project_path.rglob("*"):
        if file_path.is_file() and not should_ignore(file_path):
            ext = file_path.suffix
            if ext in LANGUAGE_EXTENSIONS:
                lang_counts[LANGUAGE_EXTENSIONS[ext]] += 1

    return dict(sorted(lang_counts.items(), key=lambda x: x[1], reverse=True))


def detect_frameworks(project_path: Path, languages: list) -> list:
    """Detect frameworks by scanning source files and config."""
    detected = set()

    # Scan source files for import patterns
    if "Python" in languages or "TypeScript" in languages or "JavaScript" in languages:
        for file_path in project_path.rglob("*"):
            if file_path.is_file() and not should_ignore(file_path):
                if file_path.suffix in [".py", ".ts", ".tsx", ".js", ".jsx"]:
                    try:
                        content = file_path.read_text(errors="ignore")
                        for framework, patterns in FRAMEWORK_INDICATORS.items():
                            if any(pattern in content for pattern in patterns):
                                detected.add(framework)
                    except Exception:
                        continue

    # Check config files
    if "Go" in languages:
        go_mod = project_path / "go.mod"
        if go_mod.exists():
            content = go_mod.read_text(errors="ignore")
            for framework, patterns in FRAMEWORK_INDICATORS.items():
                if any(pattern in content for pattern in patterns):
                    detected.add(framework)

    if "Rust" in languages:
        cargo_toml = project_path / "Cargo.toml"
        if cargo_toml.exists():
            content = cargo_toml.read_text(errors="ignore")
            for framework, patterns in FRAMEWORK_INDICATORS.items():
                if any(pattern in content for pattern in patterns):
                    detected.add(framework)

    return sorted(detected)


def find_entry_points(project_path: Path) -> list:
    """Find entry point files."""
    entry_points = []

    for file_path in project_path.rglob("*"):
        if file_path.is_file() and not should_ignore(file_path):
            if file_path.name in ENTRY_POINT_PATTERNS:
                rel_path = file_path.relative_to(project_path)
                entry_points.append({
                    "file": str(rel_path),
                    "type": ENTRY_POINT_PATTERNS[file_path.name]
                })

    # Check package.json scripts
    package_json = project_path / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text())
            if "scripts" in data:
                for script_name in ["start", "dev", "main"]:
                    if script_name in data["scripts"]:
                        entry_points.append({
                            "file": "package.json",
                            "type": f"npm script: {script_name}",
                            "command": data["scripts"][script_name]
                        })
        except Exception:
            pass

    return entry_points


def find_dependencies(project_path: Path) -> dict:
    """Extract dependencies from config files."""
    deps = {}

    # package.json
    package_json = project_path / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text())
            deps["npm"] = {
                "dependencies": data.get("dependencies", {}),
                "devDependencies": data.get("devDependencies", {})
            }
        except Exception:
            pass

    # requirements.txt
    requirements = project_path / "requirements.txt"
    if requirements.exists():
        try:
            deps["pip"] = requirements.read_text().strip().split("\n")
        except Exception:
            pass

    # pyproject.toml
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            # Simple parsing for dependencies section
            deps["poetry"] = "See pyproject.toml [tool.poetry.dependencies]"
        except Exception:
            pass

    # go.mod
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_deps = re.findall(r"^\s+(.+?) v(.+?)$", content, re.MULTILINE)
            deps["go"] = {dep: ver for dep, ver in go_deps}
        except Exception:
            pass

    return deps


def build_structure_tree(project_path: Path, max_depth: int = 3) -> dict:
    """Build simplified project structure tree."""
    def _build_tree(path: Path, depth: int = 0) -> dict:
        if depth > max_depth or should_ignore(path):
            return None

        # Skip non-regular files (sockets, pipes, etc.)
        if not path.is_dir() and not path.is_file():
            return None

        if path.is_file():
            return {"type": "file", "name": path.name}

        children = []
        try:
            for item in sorted(path.iterdir()):
                if not should_ignore(item):
                    child = _build_tree(item, depth + 1)
                    if child:
                        children.append(child)
        except (PermissionError, OSError):
            pass

        return {"type": "dir", "name": path.name, "children": children[:20]}  # Limit children

    return _build_tree(project_path)


def analyze_project(project_path: Path) -> dict:
    """Main analysis function."""
    print(f"Analyzing project: {project_path}")

    languages = detect_languages(project_path)
    print(f"Languages detected: {list(languages.keys())}")

    frameworks = detect_frameworks(project_path, list(languages.keys()))
    print(f"Frameworks detected: {frameworks}")

    entry_points = find_entry_points(project_path)
    print(f"Entry points found: {len(entry_points)}")

    dependencies = find_dependencies(project_path)
    print(f"Dependency managers: {list(dependencies.keys())}")

    structure = build_structure_tree(project_path)

    # Detect project type
    project_type = "single-app"
    if (project_path / "packages").exists() or (project_path / "apps").exists():
        project_type = "monorepo"
    elif len(entry_points) > 3:
        project_type = "multi-package"

    return {
        "project_path": str(project_path.absolute()),
        "project_type": project_type,
        "languages": languages,
        "frameworks": frameworks,
        "entry_points": entry_points,
        "dependencies": dependencies,
        "structure": structure,
        "config_files": [
            f for f in CONFIG_FILES.keys()
            if (project_path / f).exists()
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze project structure")
    parser.add_argument("project_path", type=str, help="Path to project directory")
    parser.add_argument("--output", type=str, default="analysis_report.json",
                        help="Output JSON file")

    args = parser.parse_args()
    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return 1

    analysis = analyze_project(project_path)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(analysis, indent=2))
    print(f"\nAnalysis saved to: {output_path.absolute()}")

    return 0


if __name__ == "__main__":
    exit(main())
