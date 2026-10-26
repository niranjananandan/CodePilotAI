import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_FOLDER = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_FOLDER))

from fix_generator import generate_candidate


class TestFixGenerator(unittest.TestCase):

    def setUp(self):
        self.target = (
            PROJECT_ROOT / "sample_projects" / "division_demo.py"
        )
        self.relative_path = "sample_projects/division_demo.py"

    def test_no_change_preserves_original_code(self):
        original = self.target.read_text(encoding="utf-8")

        with patch(
            "fix_generator.chat_with_model",
            return_value="NO_CHANGE",
        ):
            target, old_code, candidate = generate_candidate(
                self.relative_path,
                "Review this file without changes.",
            )

        self.assertEqual(target, self.target.resolve())
        self.assertEqual(old_code, original)
        self.assertEqual(candidate, original)

    def test_valid_fix_is_returned(self):
        proposed_code = (
            "def safe_divide(a, b):\n"
            "    if b == 0:\n"
            "        raise ValueError('division by zero')\n"
            "    return a / b\n"
        )

        response = f"```python\n{proposed_code}```"

        with patch(
            "fix_generator.chat_with_model",
            return_value=response,
        ):
            target, original, candidate = generate_candidate(
                self.relative_path,
                "Fix division by zero.",
            )

        self.assertEqual(candidate, proposed_code)
        self.assertNotEqual(candidate, original)

    def test_rejects_path_outside_project(self):
        with self.assertRaises(ValueError):
            generate_candidate(
                "../outside.py",
                "Review this file.",
            )

    def test_rejects_invalid_python_syntax(self):
        invalid_response = (
            "```python\n"
            "def broken(:\n"
            "    pass\n"
            "```"
        )

        with patch(
            "fix_generator.chat_with_model",
            return_value=invalid_response,
        ):
            with self.assertRaises(RuntimeError):
                generate_candidate(
                    self.relative_path,
                    "Fix the function syntax.",
                )


if __name__ == "__main__":
    unittest.main()