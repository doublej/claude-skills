#!/usr/bin/env python3
import subprocess
import sys
import re
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).parent))
from detectors import deprecated, conventions, deadcode, duplicates
from report_generator import generate_report

# Resolve codebase-mapper's bundled repomap relative to this skill
SKILL_DIR = Path(__file__).parent
MAPPER_SCRIPT = SKILL_DIR.parent / "codebase-mapper" / "scripts" / "repomap.sh"


def get_repomap_cmd():
    if MAPPER_SCRIPT.exists():
        return ["bash", str(MAPPER_SCRIPT)]

    result = subprocess.run(["which", "repomap"], capture_output=True)
    if result.returncode == 0:
        return ["repomap"]

    print(f"Error: codebase-mapper not found at {MAPPER_SCRIPT}", file=sys.stderr)
    print("Install the codebase-mapper skill alongside repomap-analyzer.", file=sys.stderr)
    sys.exit(1)


def run_repomap(target_dir, map_tokens):
    cmd = get_repomap_cmd()
    result = subprocess.run(
        cmd + [target_dir, "--root", target_dir, "--map-tokens", str(map_tokens)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error: repomap failed (exit {result.returncode})", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    if not result.stdout:
        print("Error: repomap produced no output", file=sys.stderr)
        sys.exit(1)

    return parse_repomap_output(result.stdout)


def parse_repomap_output(output):
    data = {}
    current_file = None
    file_pattern = re.compile(r'^(.+?):\s*$')
    rank_pattern = re.compile(r'^\(Rank value: ([\d.]+)\)\s*$')
    line_pattern = re.compile(r'^\s*(\d+):\s*(.+)$')

    for line in output.split('\n'):
        file_match = file_pattern.match(line)
        if file_match:
            current_file = file_match.group(1)
            data[current_file] = {'rank': 0.0, 'definitions': []}
            continue

        if current_file:
            rank_match = rank_pattern.match(line)
            if rank_match:
                data[current_file]['rank'] = float(rank_match.group(1))
                continue

            line_match = line_pattern.match(line)
            if line_match:
                line_num = int(line_match.group(1))
                content = line_match.group(2)
                data[current_file]['definitions'].append({
                    'line': line_num,
                    'content': content
                })

    return data


def load_detectors():
    return [deprecated, conventions, deadcode, duplicates]


def run_analysis(repomap_data, source_dir):
    results = {}
    detector_modules = load_detectors()

    for detector in detector_modules:
        detector_name = detector.__name__.split('.')[-1]
        findings = detector.detect(repomap_data, source_dir)
        results[detector_name] = findings

    return results


def main():
    parser = argparse.ArgumentParser(description='Analyze repository for code quality issues')
    parser.add_argument('repository', help='Path to repository to analyze')
    parser.add_argument('--output', default='repomap-analysis.md', help='Output report file')
    parser.add_argument('--map-tokens', type=int, default=32768, help='Repomap token limit')
    args = parser.parse_args()

    repo_path = Path(args.repository).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing repository: {repo_path}")
    print("Generating repository map...")
    repomap_data = run_repomap(str(repo_path), args.map_tokens)

    print("Running detectors...")
    findings = run_analysis(repomap_data, str(repo_path))

    print(f"Generating report: {args.output}")
    generate_report(findings, args.output, str(repo_path))

    print("Analysis complete")


if __name__ == '__main__':
    main()
