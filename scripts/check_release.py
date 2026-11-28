"""Check the staged Skill ZIP, clipboard entry, and README links."""
import json
import posixpath
import re
import sys
from pathlib import Path
from zipfile import ZipFile

from build_life_plans import (
    APP_PACK_NAME, APP_SCENE_DIR, CUSTOM_GOAL_HEADING, PLAN_COPY_DIR, PLAN_FILES,
    PLAN_INDEX, PLAN_PACK_PAGE, SCENE_COPY_PAGE, SCENE_FILES, SCENE_TITLES,
    app_pack_files, copy_packs,
)

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def verify(archive):
    readme = text(ROOT / "README.md")
    starter = text(ROOT / "prompts/xiaodou-start.txt").strip()
    block = re.search(r"^`{3}text\n(.*?)\n`{3}$", readme, re.MULTILINE | re.DOTALL)
    assert block and block[1] == starter, "README starter must match its copyable text"
    guide = text(ROOT / "docs/field-tests/pilot-s0.md")
    sample = re.search(r"^```text\n(.*?)\n```$", guide, re.MULTILINE | re.DOTALL)
    pilot = text(ROOT / "prompts/xiaodou-pilot-start.txt").strip()
    assert sample and sample[1] == pilot, "S0 guide opening must match the staged pilot text"
    assert pilot.startswith(starter + "\n\n"), "S0 opening must include the current starter"
    intro = readme.split("## 一句话在小豆里开始", maxsplit=1)[0]
    assert intro.startswith("# 小豆皇帝模拟器\n"), "README must identify the Skill at the top"
    assert all(role in intro for role in ("中书省", "门下省", "尚书省", "六部")), "the court workflow belongs in the README intro"

    share_page = text(ROOT / "docs/share-cards.md")
    gallery_path = SCENE_COPY_PAGE.relative_to(ROOT).as_posix()
    for title in SCENE_TITLES.values():
        target = f"{gallery_path}#{title})"
        assert target in readme and target in share_page, f"Missing mobile copy route for {title}"

    plan_index = text(PLAN_INDEX)
    for chapter in PLAN_FILES:
        gallery = (PLAN_COPY_DIR / chapter.name).relative_to(ROOT).as_posix()
        target = f"{gallery}#{CUSTOM_GOAL_HEADING})"
        assert target in readme and target in plan_index, f"Missing mobile custom-goal route: {chapter.name}"
    pack_target = PLAN_PACK_PAGE.relative_to(ROOT).as_posix() + ")"
    assert pack_target in readme and pack_target in plan_index, "Missing mobile life-plan pack route"

    markdown_targets = re.findall(r"\]\(([^)]+)\)", readme)
    image_targets = re.findall(r'src="([^"]+)"', readme)
    for target in markdown_targets + image_targets:
        if "://" in target or target.startswith("#"):
            continue
        assert (ROOT / target.split("#")[0]).is_file(), f"missing README target: {target}"

    counters = ("xiaodou-quick-pack.txt", "xiaodou-paste-pack.txt")
    prompt_ids = []
    for name in counters:
        contents = text(ROOT / "prompts" / name)
        ids = re.findall(r"^([A-Z]?\d{2}) · ", contents, re.MULTILINE)
        assert ids and len(ids) == len(set(ids)), f"duplicate or absent prompt ID in {name}"
        prompt_ids.append(ids)
    quick, full = prompt_ids
    catalog = json.loads(text(ROOT / "data/playbooks.json"))
    assert set(full) == {c["id"] for c in catalog} | {"G01", "H01"}
    assert set(quick) <= set(full)
    for count, label in [(len(quick), " 条常用指令"), (len(full), " 条提示词"), (len(catalog), " 个社区案例")]:
        assert f"{count}{label}" in readme, f"README count does not match {label}"

    skill = ROOT / "skills/xiaodou-skill"
    roles = json.loads(text(ROOT / "docs/studio/roles.json"))
    copies = copy_packs()
    expected_app = app_pack_files(copies)
    with ZipFile(archive.with_name(APP_PACK_NAME)) as app:
        assert app.testzip() is None, "damaged App starter ZIP"
        assert sorted(app.namelist()) == sorted(expected_app), "App starter ZIP entries do not match the index"
        for name, expected in expected_app.items():
            assert app.read(name).decode("utf-8") == expected, f"App starter ZIP content differs: {name}"
        offline_guide = app.read("先读这里.txt").decode("utf-8")
        assert f"「{APP_SCENE_DIR}」" in offline_guide, "Offline guide must surface the starter folder"
        for scene, title in SCENE_TITLES.items():
            packaged_scene = app.read(f"{APP_SCENE_DIR}/{title}.txt").decode("utf-8")
            assert title in offline_guide, f"Offline guide is missing {title}"
            assert packaged_scene == text(SCENE_FILES[scene]), f"{title} differs from the online starter"
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None, "damaged ZIP contents"
        for path, expected in copies.items():
            assert text(path) == expected, f"{path.name}: App copy text must match the Skill reference"
        tracked_files = [
            "SKILL.md", "references/prompts.md", "references/court.md", "references/planning.md", "references/prompt-sources.md",
            "references/divination.md", "references/guandi-lots.json", "scripts/birth-chart/chart.cjs",
            "scripts/birth-chart/fortune.cjs",
            "scripts/birth-chart/package.json",
            "scripts/birth-chart/package-lock.json",
        ]
        upstream = skill / "vendor" / "ziwei-bazi"
        upstream_files = [
            "LICENSE", "README.md", "SKILL.md", "references/quality-audit-checklist.md",
            "references/translation-dictionary.md", "scripts/dynamic_layer.py", "scripts/paipan_verify.py",
            "scripts/sihua_lookup.py", "scripts/ziwei_chart.py", "tests/test_dynamic_layer.py",
            "tests/test_paipan_verify.py", "tests/test_sihua_lookup.py", "tests/test_ziwei_chart.py",
        ]
        tracked_files.extend((upstream / name).relative_to(skill).as_posix() for name in upstream_files)
        tracked_files.extend(path.relative_to(skill).as_posix() for path in (PLAN_INDEX, *PLAN_FILES))
        lots = json.loads(text(skill / "references" / "guandi-lots.json"))["lots"]
        assert [lot["number"] for lot in lots] == list(range(1, 101))
        assert all(len(lot["verse"]) == 4 and lot["traditionalCommentary"] for lot in lots)
        for path in tracked_files:
            assert bundle.read("xiaodou-skill/" + path).decode().replace("\r\n", "\n") == text(skill / path), path
        archive_paths = set(bundle.namelist())
        for path in ("SKILL.md", "references/planning.md", "references/divination.md"):
            content = text(skill / path)
            directory = posixpath.dirname(f"xiaodou-skill/{path}")
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if "://" not in target and not target.startswith("#"):
                    linked_path = posixpath.normpath(posixpath.join(directory, target.split("#")[0]))
                    assert linked_path in archive_paths, f"{path} refers to missing file: {target}"
        assert bundle.read("xiaodou-skill/LICENSE") == (ROOT / "LICENSE").read_bytes()
        library = bundle.read("xiaodou-skill/references/prompts.md").decode()
        zip_ids = re.findall(r"^### ([A-Z]?\d{2}) · ", library, re.MULTILINE)
        assert zip_ids == full, "ZIP prompt IDs do not match the full copy pack"
        for role in roles:
            name = role["portrait"]
            assert bundle.read(f"xiaodou-skill/assets/roles/{name}") == (ROOT / "docs/studio/portraits" / name).read_bytes(), name
    print(f"README, {len(quick)} quick prompts, {len(full)} full prompts, and {len(roles)} portraits verified.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/check_release.py PATH_TO_SKILL_ZIP")
    verify(Path(sys.argv[1]))
