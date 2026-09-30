#!/usr/bin/env python3
"""Self-check for the argv filter and the live `claude --help` parse. Run: python3 test_restart.py"""

from restart import keep_flags, read_flag_arity

arity = read_flag_arity()
assert arity["--model"] == "one" and arity["-r"] == "opt" and arity["--add-dir"] == "many", arity
assert arity["--dangerously-skip-permissions"] is None and arity["--file"] == "many"

args = [
    "--dangerously-skip-permissions",
    "--model",
    "haiku",
    "--resume",
    "abc",
    "--append-system-prompt",
    "be terse",
    "--add-dir",
    "/a",
    "/b",
    "-c",
    "--effort=high",
    "fix the bug",
]
assert keep_flags(args, arity) == [
    "--dangerously-skip-permissions",
    "--model",
    "haiku",
    "--append-system-prompt",
    "be terse",
    "--add-dir",
    "/a",
    "/b",
    "--effort=high",
], keep_flags(args, arity)
assert keep_flags(["--chrome", "do", "x"], arity) == ["--chrome"]
print("ok")
