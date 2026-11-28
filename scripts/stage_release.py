"""Build and verify the files published together in a Xiaodou release."""

import sys
from hashlib import file_digest
from pathlib import Path
from shutil import copyfile

from build_life_plans import APP_PACK_NAME, PLAN_PACK, SCENE_FILES
from build_skill import PASTE_PACK, QUICK_PACK, ROOT, main as build_skill
from check_release import verify


def stage_release(output):
    if output.exists() and any(output.iterdir()):
        raise ValueError("Use an empty directory for the release files")

    build_skill(output)
    skill_zip = output / "xiaodou-skill.zip"
    verify(skill_zip)

    text_sources = (ROOT / "prompts/xiaodou-start.txt", PLAN_PACK, QUICK_PACK, PASTE_PACK, *SCENE_FILES.values())
    assets = [skill_zip, output / APP_PACK_NAME]
    for source in text_sources:
        asset = output / source.name
        copyfile(source, asset)
        assets.append(asset)

    checksums = []
    for asset in sorted(assets):
        with asset.open("rb") as content:
            digest = file_digest(content, "sha256").hexdigest()
        checksums.append(f"{digest}  {asset.name}\n")
    (output / "SHA256SUMS").write_text("".join(checksums), encoding="ascii", newline="\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/stage_release.py OUTPUT_DIRECTORY")
    stage_release(Path(sys.argv[1]))
