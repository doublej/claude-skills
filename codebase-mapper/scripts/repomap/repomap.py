#!/usr/bin/env python3
"""
Standalone RepoMap Tool

A command-line tool that generates a "map" of a software repository,
highlighting important files and definitions based on their relevance.
Uses Tree-sitter for parsing and PageRank for ranking importance.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List

from utils import count_tokens, read_text, Tag
from scm import get_scm_fname
from importance import is_important, filter_important_files
from repomap_class import RepoMap


DEFAULT_EXCLUDE_DIRS = {
    'node_modules', '__pycache__', 'venv', 'env', '.venv',
    'build', 'dist', '.cache', '.next', '.nuxt',
}


def find_git_files(directory: str) -> set:
    """Get set of files tracked by git (respects .gitignore)."""
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
            capture_output=True, text=True, cwd=directory,
        )
        if result.returncode == 0:
            abs_dir = os.path.abspath(directory)
            return {os.path.join(abs_dir, f) for f in result.stdout.splitlines() if f}
    except FileNotFoundError:
        pass
    return set()


def find_src_files(
    directory: str,
    exclude_extensions: List[str] = None,
    exclude_dirs: List[str] = None,
    respect_gitignore: bool = True,
) -> List[str]:
    """Find source files in a directory."""
    if not os.path.isdir(directory):
        if os.path.isfile(directory):
            if exclude_extensions:
                _, ext = os.path.splitext(directory)
                if ext in exclude_extensions:
                    return []
            return [directory]
        return []

    exclude_extensions = exclude_extensions or []
    skip_dirs = DEFAULT_EXCLUDE_DIRS | set(exclude_dirs or [])

    # Try git ls-files for .gitignore awareness
    git_files = find_git_files(directory) if respect_gitignore else set()
    use_git = bool(git_files)

    src_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d for d in dirs
            if not d.startswith('.') and d not in skip_dirs
        ]
        for file in files:
            if file.startswith('.'):
                continue
            _, ext = os.path.splitext(file)
            if ext in exclude_extensions:
                continue
            full_path = os.path.join(root, file)
            if use_git and os.path.abspath(full_path) not in git_files:
                continue
            src_files.append(full_path)

    return src_files


def tool_output(*messages):
    """Print informational messages."""
    print(*messages, file=sys.stdout)


def tool_warning(message):
    """Print warning messages."""
    print(f"Warning: {message}", file=sys.stderr)


def tool_error(message):
    """Print error messages."""
    print(f"Error: {message}", file=sys.stderr)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a repository map showing important code structures.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .                              # Map current directory
  %(prog)s src/ --map-tokens 2048         # Map src/ with token limit
  %(prog)s --focus-files main.py .        # Boost files you're working on
  %(prog)s --focus-files main.py --context-files src/
        """
    )
    
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to include in the map"
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Repository root directory (default: current directory)"
    )

    parser.add_argument(
        "--map-tokens",
        type=int,
        default=8192*4,
        help="Maximum tokens for the generated map (default: 32768)"
    )

    parser.add_argument(
        "--focus-files",
        nargs="*",
        help="Files being actively investigated or modified (20x boost)"
    )

    parser.add_argument(
        "--context-files",
        nargs="*",
        help="Additional files to include in the map"
    )

    parser.add_argument(
        "--mentioned-files",
        nargs="*",
        help="Files explicitly mentioned in conversation (5x boost)"
    )

    parser.add_argument(
        "--mentioned-idents",
        nargs="*",
        help="Identifiers to trace across the codebase (10x boost)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--model",
        default="gpt-4",
        help="Model name for tiktoken counter (default: gpt-4)"
    )

    parser.add_argument(
        "--max-context-window",
        type=int,
        help="Maximum context window size"
    )
    
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force refresh of caches"
    )

    parser.add_argument(
        "--exclude-unranked",
        action="store_true",
        help="Exclude files with Page Rank 0 from the map"
    )

    parser.add_argument(
        "--exclude-extensions",
        nargs="*",
        help="File extensions to exclude (e.g., .js .css .json)"
    )

    parser.add_argument(
        "--exclude-dirs",
        nargs="*",
        help="Directory names to exclude (e.g., build dist sketches)"
    )

    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Include files ignored by .gitignore (default: respect .gitignore)"
    )

    args = parser.parse_args()
    
    # Set up token counter with specified model
    def token_counter(text: str) -> int:
        return count_tokens(text, args.model)
    
    # Set up output handlers
    output_handlers = {
        'info': tool_output,
        'warning': tool_warning,
        'error': tool_error
    }
    
    # Process file arguments
    focus_files_from_args = args.focus_files or []

    # Determine context files from --context-files or positional paths
    context_paths = []
    if args.context_files:
        context_paths.extend(args.context_files)
    elif args.paths:
        context_paths.extend(args.paths)

    # Expand directories into file lists
    exclude_exts = args.exclude_extensions or []
    exclude_dirs = args.exclude_dirs or []
    expanded_context_files = []
    for path_spec in context_paths:
        expanded_context_files.extend(find_src_files(
            path_spec, exclude_exts, exclude_dirs,
            respect_gitignore=not args.no_gitignore,
        ))

    # Convert to absolute paths
    root_path = Path(args.root).resolve()
    focus_files = [str(Path(f).resolve()) for f in focus_files_from_args]
    context_files = [str(Path(f).resolve()) for f in expanded_context_files]

    # Convert mentioned files to sets
    mentioned_fnames = set(args.mentioned_files) if args.mentioned_files else None
    mentioned_idents = set(args.mentioned_idents) if args.mentioned_idents else None

    # Create RepoMap instance
    repo_map = RepoMap(
        map_tokens=args.map_tokens,
        root=str(root_path),
        token_counter_func=token_counter,
        file_reader_func=read_text,
        output_handler_funcs=output_handlers,
        verbose=args.verbose,
        max_context_window=args.max_context_window,
        exclude_unranked=args.exclude_unranked
    )

    # Generate the map
    try:
        map_content = repo_map.get_repo_map(
            focus_files=focus_files,
            context_files=context_files,
            mentioned_fnames=mentioned_fnames,
            mentioned_idents=mentioned_idents,
            force_refresh=args.force_refresh
        )
        
        if map_content:
            tokens = repo_map.token_count(map_content)
            total = len(context_files) + len(focus_files)
            ranked = repo_map.ranked_file_count
            tool_output(f"Analysed {total} files · ranked {ranked} · ~{tokens} tokens")
            print(map_content)
        else:
            tool_output("No repository map generated.")
            
    except KeyboardInterrupt:
        tool_error("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        tool_error(f"Error generating repository map: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
