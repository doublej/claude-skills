#!/usr/bin/env python3
"""Generate an Ollama Modelfile from a YAML config."""

import sys
import yaml
from pathlib import Path


def gen_modelfile(config_path: str) -> str:
    raw = Path(config_path).read_text()
    cfg = yaml.safe_load(raw)

    lines = [f'FROM {cfg.get("model", "llama3.1:8b")}', ""]

    if system := cfg.get("system"):
        lines += [f'SYSTEM """{system.strip()}"""', ""]

    for key, val in cfg.get("parameters", {}).items():
        if key == "stop" and isinstance(val, list):
            for s in val:
                lines.append(f'PARAMETER stop "{s}"')
        else:
            lines.append(f"PARAMETER {key} {val}")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config.yaml>", file=sys.stderr)
        sys.exit(1)
    print(gen_modelfile(sys.argv[1]))
