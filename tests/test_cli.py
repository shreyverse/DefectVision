"""Tests for CLI parsing and subcommands."""
import unittest
import os
import subprocess
import sys


class TestCLI(unittest.TestCase):

    def test_cli_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.cli.main", "--help"],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("DefectVision", result.stdout)

    def test_cli_inspect_single_image(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.cli.main", "inspect", "--input", "data/samples/sample_scratch.png", "--output", "output/test_cli_out"],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("output/test_cli_out/inspection_summary.json"))


if __name__ == "__main__":
    unittest.main()
