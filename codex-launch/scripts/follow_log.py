#!/usr/bin/env python3
"""Display a growing Codex log in a visible terminal."""
import argparse
import sys
import time
from pathlib import Path


def follow_log(args):
    print(f"{args.label}\nLog: {args.log}\nClose this window to stop watching.\n", flush=True)
    if args.ready_file:
        args.ready_file.touch()
    with args.log.open(encoding="utf-8", errors="replace") as stream:
        while True:
            sys.stdout.write(stream.read())
            sys.stdout.flush()
            if args.exit_file and args.exit_file.exists():
                sys.stdout.write(stream.read())
                code = args.exit_file.read_text().strip()
                print(f"\nCodex finished (exit {code}). Log retained.", flush=True)
                return
            time.sleep(0.25)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("exit_file", nargs="?", default="")
    parser.add_argument("label", nargs="?", default="Codex live monitor")
    parser.add_argument("ready_file", nargs="?", default="")
    args = parser.parse_args()
    args.exit_file = Path(args.exit_file) if args.exit_file else None
    args.ready_file = Path(args.ready_file) if args.ready_file else None
    return args


if __name__ == "__main__":
    follow_log(parse_args())
