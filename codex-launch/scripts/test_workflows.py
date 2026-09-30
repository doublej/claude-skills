#!/usr/bin/env python3
"""Exercise Codex launch/capture boundaries without paid calls or GUI windows."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCH = ROOT / "codex-launch/scripts"
IMAGE = ROOT / "codex-image/scripts"
MOCK_CODEX = '''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
Path(os.environ["CALL_FILE"]).write_text(json.dumps(sys.argv[1:]))
print("live Codex event", flush=True)
if "-o" in sys.argv:
    result = {"image_path": os.environ["IMAGE_FILE"], "error": None}
    if os.environ.get("CODEX_ERROR"):
        result = {"image_path": None, "error": "image tool unavailable"}
    Path(sys.argv[sys.argv.index("-o") + 1]).write_text(json.dumps(result))
sys.exit(int(os.environ.get("CODEX_EXIT", "0")))
'''
MOCK_IT2 = '''#!/usr/bin/env python3
import json, os, shlex, sys
from pathlib import Path
args = sys.argv[1:]
if args[0] == "newtab":
    if os.environ.get("OPEN_EXIT"):
        sys.exit(int(os.environ["OPEN_EXIT"]))
    command = Path(shlex.split(args[args.index("--command") + 1])[1])
    Path(os.environ["OPEN_FILE"]).write_text(str(command))
    (command.parent / "ready").touch()
    print("Created new tab: 42")
elif args[:2] == ["session", "list"]:
    print(json.dumps([{"id": "test-session", "tab_id": "42"}]))
'''


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.image = self.root / "codex/generated_images/exact image.png"
        self.image.parent.mkdir(parents=True)
        self.image.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
        self.env = {**os.environ, "PATH": f"{self.bin}:{os.environ['PATH']}",
                    "CODEX_HOME": str(self.root / "codex"), "IMAGE_FILE": str(self.image),
                    "OPEN_FILE": str(self.root / "opened"), "CALL_FILE": str(self.root / "call")}
        for name, content in {"codex": MOCK_CODEX, "it2": MOCK_IT2}.items():
            path = self.bin / name
            path.write_text(content)
            path.chmod(0o700)

    def run_script(self, script, *args):
        return subprocess.run(["bash", str(script), *map(str, args)], env=self.env,
                              capture_output=True, text=True, timeout=10)

    def test_live_output_and_exit_code(self):
        self.env["CODEX_EXIT"] = "7"
        result = self.run_script(LAUNCH / "run_monitored.sh", "test", "codex")
        self.assertEqual(result.returncode, 7)
        self.assertIn("live Codex event", result.stdout)
        monitor = Path((self.root / "opened").read_text())
        self.assertTrue(monitor.is_file())
        log = Path(result.stderr.split("Log: ", 1)[1].strip())
        self.assertIn("live Codex event", log.read_text())
        self.assertEqual((log.parent / "exit-code").read_text().strip(), "7")

    def test_monitor_failure_prevents_execution(self):
        self.env["OPEN_EXIT"] = "3"
        result = self.run_script(LAUNCH / "run_monitored.sh", "test", "codex")
        self.assertEqual(result.returncode, 3)
        self.assertFalse((self.root / "call").exists())

    def test_interactive_prompt_cannot_execute_shell(self):
        marker = self.root / "injected"
        prompt = f'quotes " $HOME `touch {marker}` $(touch {marker})\nnext line'
        result = self.run_script(LAUNCH / "launch_cli.sh", prompt, "-m", "test model")
        self.assertEqual(result.returncode, 0, result.stderr)
        launch = Path((self.root / "opened").read_text())
        executed = self.run_script(launch)
        self.assertEqual(executed.returncode, 0)
        self.assertEqual(json.loads((self.root / "call").read_text()), ["-m", "test model", "--", prompt])
        self.assertFalse(marker.exists())

    def test_exact_image_and_multiple_references(self):
        second = self.root / "reference two.png"
        second.write_bytes(self.image.read_bytes())
        output = self.root / "output folder"
        result = self.run_script(IMAGE / "generate.sh", "Image 1: target; Image 2: style", output, self.image, second)
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = Path(json.loads(result.stdout)["image_path"])
        self.assertEqual(saved.read_bytes(), self.image.read_bytes())
        args = json.loads((self.root / "call").read_text())
        inputs = [args[i + 1] for i, value in enumerate(args) if value == "-i"]
        self.assertEqual(inputs, [str(self.image.resolve()), str(second.resolve())])
        self.assertEqual(args[args.index("-s") + 1], "read-only")

    def test_existing_output_is_preserved(self):
        output = self.root / "output"
        output.mkdir()
        original = output / self.image.name
        original.write_bytes(b"original")
        result = self.run_script(IMAGE / "generate.sh", "brief", output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(original.read_bytes(), b"original")

    def test_no_latest_image_fallback_on_error(self):
        self.env["CODEX_ERROR"] = "1"
        result = self.run_script(IMAGE / "generate.sh", "brief", self.root / "output")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("image tool unavailable", result.stderr)
        self.assertEqual(list((self.root / "output").iterdir()), [])

    def test_missing_and_outside_result_are_rejected(self):
        for image in [self.root / "codex/generated_images/missing.png", self.root / "outside.png"]:
            self.env["IMAGE_FILE"] = str(image)
            image.parent.mkdir(parents=True, exist_ok=True)
            result = self.run_script(IMAGE / "generate.sh", "brief", self.root / "output")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list((self.root / "output").iterdir()), [])

    def test_observer_flushes_final_output(self):
        log = self.root / "log"
        log.write_text("live event\nfinal answer\n")
        status = self.root / "exit"
        status.write_text("0\n")
        result = subprocess.run(["python3", str(LAUNCH / "follow_log.py"), str(log), str(status)],
                                capture_output=True, text=True, timeout=3)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("final answer", result.stdout)
        self.assertIn("exit 0", result.stdout)


if __name__ == "__main__":
    unittest.main()
