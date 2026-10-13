import os
import subprocess
import sys
import tempfile
import unittest

from rover import run_instructions

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def simulate(text):
    out = []
    ok = run_instructions(text.splitlines(), output=out.append)
    return ok, out


class SimulatorTests(unittest.TestCase):
    def test_full_run_output(self):
        ok, out = simulate("Move 10 meters forward\nTurn 90 degrees clockwise\nMove 5 meters backward")
        self.assertTrue(ok)
        self.assertEqual(
            out,
            [
                "I'm at (0.00, 0.00) facing 0.00 degrees",
                "Moving 10.0 meters forward (instruction 1.0)",
                "I'm at (0.00, 10.00) facing 0.00 degrees",
                "Turning 90.0 degrees clockwise (instruction 2.0)",
                "I'm at (0.00, 10.00) facing 90.00 degrees",
                "Moving 5.0 meters backward (instruction 3.0)",
                "I'm at (-5.00, 10.00) facing 90.00 degrees",
            ],
        )

    def test_abort_on_bad_instruction(self):
        ok, out = simulate("Move 1 meters forward\nFly away\nMove 1 meters forward")
        self.assertFalse(ok)
        self.assertEqual(
            out[-1],
            "I've encountered an instruction I don't understand, aborting (instruction 2.0)",
        )
        self.assertEqual(len(out), 4)

    def test_blank_lines_count_toward_instruction_number(self):
        ok, out = simulate("Move 1 meters forward\n\nbad line")
        self.assertFalse(ok)
        self.assertIn("(instruction 3.0)", out[-1])

    def test_square_returns_to_origin(self):
        text = "\n".join(["Move 10 meters forward", "Turn 90 degrees clockwise"] * 4)
        ok, out = simulate(text)
        self.assertTrue(ok)
        self.assertEqual(out[-1], "I'm at (0.00, 0.00) facing 0.00 degrees")

    def test_cli(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("Move 2 meters forward\n")
        try:
            script = os.path.join(ROOT, "simulate_rover.py")
            result = subprocess.run([sys.executable, script, f.name], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Moving 2.0 meters forward (instruction 1.0)", result.stdout)

            missing = subprocess.run(
                [sys.executable, script, f.name + ".nope"], capture_output=True, text=True
            )
            self.assertEqual(missing.returncode, 1)
            self.assertIn("Could not read", missing.stderr)

            usage = subprocess.run([sys.executable, script], capture_output=True, text=True)
            self.assertEqual(usage.returncode, 2)
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
