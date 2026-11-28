import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from build_life_plans import PLAN_STARTER_FILES, ROOT
from build_trial_starter_guide import make_guide
from verify_candidate import REPOSITORY


class TrialStarterGuideTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.copies = Path(self.folder.name)
        (self.copies / "life-plans").mkdir()
        for path in PLAN_STARTER_FILES.values():
            (self.copies / "life-plans" / path.name).write_bytes(path.read_bytes())

    def test_only_public_blocks_with_the_same_text_get_the_same_version_link(self):
        def public_page(command, **kwargs):
            name = command[-1].split(":", 1)[1]
            if name.endswith("/learning.md"):
                return subprocess.CompletedProcess(command, 128, stdout=b"")
            text = (ROOT / name).read_text(encoding="utf-8")
            text = text.replace("我的目标：帮我从搬家日期往前倒排", "我的目标：帮我重新安排搬家")
            return subprocess.CompletedProcess(command, 0, stdout=text.encode("utf-8"))

        with patch("build_trial_starter_guide.subprocess.run", side_effect=public_page):
            doc = make_guide(self.copies, "a" * 40, "b" * 40, REPOSITORY)
        self.assertEqual(sum(line.startswith("- [P") for line in doc.splitlines()), 30)
        self.assertEqual(doc.count("[同版公开开局]"), 23)
        p23 = next(line for line in doc.splitlines() if line.startswith("- [P23"))
        self.assertIn(f"/blob/{'a' * 40}/prompts/life-plans/household.md#p23--", p23)
        self.assertNotIn("同版公开开局", p23)

    def test_candidate_has_to_match_the_plain_text_copy(self):
        (self.copies / "life-plans" / "p01.txt").write_text("changed", encoding="utf-8")
        with patch("build_trial_starter_guide.subprocess.run",
                   return_value=subprocess.CompletedProcess([], 128, stdout=b"")):
            with self.assertRaisesRegex(ValueError, "checked text: P01"):
                make_guide(self.copies, "a" * 40, "b" * 40, REPOSITORY)


if __name__ == "__main__":
    unittest.main()
