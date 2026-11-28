"""Verify a downloaded S0 candidate directory and its pinned source links."""
import argparse
import csv
import hashlib
import re
from pathlib import Path

from build_life_plans import PLAN_FILES, PLAN_PACK, SCENE_FILES

REPOSITORY = "https://github.com/Fangx-AI/awesome-xiaodou"
STARTERS = ("xiaodou-start.txt", PLAN_PACK.name, *(f"life-plans/{path.stem}.txt" for path in PLAN_FILES))
EXPECTED = {"xiaodou-skill.zip", "xiaodou-pilot-start.txt", "CANDIDATE.txt", "STARTERS.tsv", *STARTERS}
SCENE_STARTERS = tuple(f"life-plans/{path.name}" for path in SCENE_FILES.values())


def verify_hashes(directory, expected_files):
    recorded = {}
    manifest = (directory / "SHA256SUMS").read_text(encoding="utf-8")
    for line in manifest.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
        if not match:
            raise ValueError("invalid checksum row")
        digest, name = match.groups()
        if name not in expected_files or name in recorded:
            raise ValueError(f"unexpected or duplicate checksum entry: {name}")
        recorded[name] = digest
    if recorded.keys() != expected_files:
        raise ValueError(f"missing checksum entries: {', '.join(sorted(expected_files - recorded.keys()))}")

    for name, digest in recorded.items():
        with (directory / name).open("rb") as file:
            if hashlib.file_digest(file, "sha256").hexdigest() != digest:
                raise ValueError(f"checksum mismatch: {name}")


def read_candidate(directory):
    fields = {}
    for line in (directory / "CANDIDATE.txt").read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if not separator or key in fields:
            raise ValueError("invalid or duplicate candidate metadata")
        fields[key] = value
    for key in ("candidate_commit", "public_readme_commit"):
        if not re.fullmatch(r"[0-9a-f]{40}", fields.get(key, "")):
            raise ValueError(f"missing or invalid pinned commit: {key}")
    return fields


def verify(directory, expected_commit=None, repository=REPOSITORY):
    fields = read_candidate(directory)
    if fields.get("scene_starters") not in (None, "true"):
        raise ValueError("invalid scene starter metadata")
    scenes = SCENE_STARTERS if fields.get("scene_starters") == "true" else ()
    starters = set(STARTERS + scenes)
    verify_hashes(directory, EXPECTED.union(scenes))
    candidate_commit = fields["candidate_commit"]
    if expected_commit is not None and candidate_commit != expected_commit:
        raise ValueError("candidate commit does not match the expected commit")
    base = repository.rstrip("/") + "/blob/"
    candidate = base + candidate_commit
    public = base + fields["public_readme_commit"]
    links = {"readme": f"{candidate}/README.md", "public_readme": f"{public}/README.md",
             "pilot": f"{candidate}/docs/field-tests/pilot-s0.md",
             "seven_day": f"{candidate}/docs/field-tests/seven-day.md", "starter_versions": "STARTERS.tsv"}
    for key, expected in links.items():
        if fields.get(key) != expected:
            raise ValueError(f"missing or mismatched candidate metadata: {key}")

    statuses = {}
    with (directory / "STARTERS.tsv").open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        if reader.fieldnames != ["file", "candidate_url", "public_url", "public_status"]:
            raise ValueError("invalid starter table header")
        for row in reader:
            name, status = row["file"], row["public_status"]
            if None in row or name not in starters or name in statuses or status not in ("identical", "different", "missing"):
                raise ValueError("invalid or duplicate starter table row")
            if row["candidate_url"] != f"{candidate}/prompts/{name}":
                raise ValueError(f"candidate starter link does not match: {name}")
            expected_public = "" if status == "missing" else f"{public}/prompts/{name}"
            if row["public_url"] != expected_public:
                raise ValueError(f"public starter link does not match: {name}")
            statuses[name] = status
    if statuses.keys() != starters:
        raise ValueError("starter table must contain every public starter")
    opener_matches = "true" if statuses[STARTERS[0]] == "identical" else "false"
    if fields.get("public_starter_matches_candidate") != opener_matches:
        raise ValueError("public starter status conflicts with the candidate metadata")
    return candidate_commit, statuses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--commit", help="Expected full commit from the Actions run")
    parser.add_argument("--repository", default=REPOSITORY)
    args = parser.parse_args()
    try:
        commit, statuses = verify(args.directory, args.commit, args.repository)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Candidate verification failed: {exc}\n")
    print(f"Verified {len(EXPECTED) + len(statuses) - len(STARTERS)} checksummed files for {commit}.")
    for name, status in statuses.items():
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
