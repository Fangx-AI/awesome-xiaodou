import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from verify_candidate import EXPECTED, PLAN_STARTERS, REPOSITORY, SCENE_STARTERS, STARTERS, verify


class CandidateVerificationTests(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.directory = Path(folder.name)
        self.candidate_commit = "a" * 40
        public_commit = "b" * 40
        candidate = f"{REPOSITORY}/blob/{self.candidate_commit}"
        public = f"{REPOSITORY}/blob/{public_commit}"
        for name in EXPECTED:
            path = self.directory / name
            path.parent.mkdir(exist_ok=True)
            path.write_text("test content\n", encoding="utf-8")
        links = [f"candidate_commit={self.candidate_commit}", f"readme={candidate}/README.md",
                 f"public_readme_commit={public_commit}", f"public_readme={public}/README.md",
                 "public_starter_matches_candidate=true", "starter_versions=STARTERS.tsv",
                 f"pilot={candidate}/docs/field-tests/pilot-s0.md",
                 f"seven_day={candidate}/docs/field-tests/seven-day.md"]
        (self.directory / "CANDIDATE.txt").write_text("\n".join(links) + "\n", encoding="utf-8")
        tsv = ["file\tcandidate_url\tpublic_url\tpublic_status"]
        for name in STARTERS:
            tsv.append(f"{name}\t{candidate}/prompts/{name}\t{public}/prompts/{name}\tidentical")
        (self.directory / "STARTERS.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")
        self.write_hashes(EXPECTED)

    def write_hashes(self, names):
        rows = [f"{hashlib.sha256((self.directory / name).read_bytes()).hexdigest()}  {name}"
                for name in sorted(names)]
        (self.directory / "SHA256SUMS").write_text("\n".join(rows) + "\n", encoding="utf-8")

    def test_verified_candidate_and_pinned_commit(self):
        commit, statuses = verify(self.directory, expected_commit=self.candidate_commit)
        self.assertEqual(commit, self.candidate_commit)
        self.assertEqual(statuses, dict.fromkeys(STARTERS, "identical"))
        with self.assertRaisesRegex(ValueError, "does not match the expected commit"):
            verify(self.directory, expected_commit="c" * 40)

    def test_metadata_and_clipboard_contents_are_both_checksummed(self):
        (self.directory / "life-plans/health.txt").write_text("altered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "checksum mismatch: life-plans/health.txt"):
            verify(self.directory)
        self.write_hashes(EXPECTED - {"CANDIDATE.txt"})
        with self.assertRaisesRegex(ValueError, "missing checksum entries: CANDIDATE.txt"):
            verify(self.directory)

    def test_moving_a_starter_to_the_wrong_commit_is_rejected_even_with_new_hashes(self):
        table = self.directory / "STARTERS.tsv"
        contents = table.read_text(encoding="utf-8")
        table.write_text(contents.replace(f"/blob/{self.candidate_commit}/prompts/", "/blob/main/prompts/", 1),
                         encoding="utf-8")
        self.write_hashes(EXPECTED)
        with self.assertRaisesRegex(ValueError, "candidate starter link does not match"):
            verify(self.directory)

    def test_advertised_scene_starters_require_every_checksum_and_pinned_link(self):
        metadata = self.directory / "CANDIDATE.txt"
        with metadata.open("a", encoding="utf-8") as file:
            file.write("scene_starters=true\n")
        self.write_hashes(EXPECTED)
        with self.assertRaisesRegex(ValueError, "missing checksum entries: life-plans/scene-english.txt"):
            verify(self.directory)
        table = self.directory / "STARTERS.tsv"
        with table.open("a", encoding="utf-8") as file:
            for name in SCENE_STARTERS:
                (self.directory / name).write_text("scene opener\n", encoding="utf-8")
                file.write(f"{name}\t{REPOSITORY}/blob/{self.candidate_commit}/prompts/{name}\t\tmissing\n")
        self.write_hashes(EXPECTED.union(SCENE_STARTERS))
        _, statuses = verify(self.directory)
        self.assertEqual({name: statuses[name] for name in SCENE_STARTERS}, dict.fromkeys(SCENE_STARTERS, "missing"))

    def test_all_thirty_plan_starters_are_checksummed_and_versioned(self):
        metadata = self.directory / "CANDIDATE.txt"
        with metadata.open("a", encoding="utf-8") as file:
            file.write("plan_starters=true\n")
        self.write_hashes(EXPECTED)
        with self.assertRaisesRegex(ValueError, "life-plans/p30.txt"):
            verify(self.directory)

        with (self.directory / "STARTERS.tsv").open("a", encoding="utf-8") as file:
            for name in PLAN_STARTERS:
                (self.directory / name).write_text("plan opener\n", encoding="utf-8")
                file.write(f"{name}\t{REPOSITORY}/blob/{self.candidate_commit}/prompts/{name}\t\tmissing\n")
        self.write_hashes(EXPECTED.union(PLAN_STARTERS))
        _, statuses = verify(self.directory)
        self.assertEqual(len(PLAN_STARTERS), 30)
        self.assertEqual({name: statuses[name] for name in PLAN_STARTERS}, dict.fromkeys(PLAN_STARTERS, "missing"))
        with metadata.open("a", encoding="utf-8") as file:
            file.write("starter_guide=STARTERS.md\n")
        self.write_hashes(EXPECTED.union(PLAN_STARTERS))
        with self.assertRaisesRegex(ValueError, "missing checksum entries: STARTERS.md"):
            verify(self.directory)
        (self.directory / "STARTERS.md").write_text("checked copy links\n", encoding="utf-8")
        self.write_hashes(EXPECTED.union(PLAN_STARTERS, {"STARTERS.md"}))
        verify(self.directory)


if __name__ == "__main__":
    unittest.main()
