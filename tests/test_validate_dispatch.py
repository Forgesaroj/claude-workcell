import unittest
from pathlib import Path

from scripts.validate_dispatch import validate


EXAMPLE = Path(__file__).parents[1] / "examples" / "dispatch.valid.md"


class ValidateDispatchTests(unittest.TestCase):
    def setUp(self):
        self.packet = EXAMPLE.read_text(encoding="utf-8")

    def test_accepts_completed_packet(self):
        self.assertEqual(validate(self.packet), [])

    def test_reports_missing_section(self):
        errors = validate(self.packet.replace("## Outcome\n", "## Result\n", 1))
        self.assertIn("missing section: ## Outcome", errors)

    def test_rejects_unresolved_placeholder(self):
        errors = validate(self.packet.replace("Worker: runtime-tests", "Worker: <worker>", 1))
        self.assertTrue(any("unresolved placeholders" in error for error in errors))

    def test_requires_full_commit_sha(self):
        errors = validate(self.packet.replace("4b825dc642cb6eb9a060e54bf8d69288fbee4904", "1234", 1))
        self.assertIn("Baseline commit must be a 7–40 character hexadecimal commit SHA", errors)

    def test_requires_allowed_and_excluded_paths(self):
        changed = self.packet.replace("- Allowed paths: tests/runtime/**", "- Allowed paths:", 1)
        errors = validate(changed)
        self.assertIn("fill in Scope fence field: Allowed paths", errors)

    def test_requires_checked_acceptance_and_commands(self):
        changed = self.packet.replace("- [x] Defect-detecting", "- [ ] Defect-detecting", 1)
        changed = changed.replace("- [ ] Exact commands and expected outcomes: `python3 -m unittest discover -s tests -v` exits 0", "- [ ] Exact commands and expected outcomes:", 1)
        errors = validate(changed)
        self.assertIn("Acceptance must include at least one checked, completed acceptance item", errors)
        self.assertIn("Acceptance must record exact commands and expected outcomes", errors)


if __name__ == "__main__":
    unittest.main()
