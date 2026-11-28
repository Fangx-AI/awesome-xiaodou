"""Check the staged Skill ZIP, clipboard entry, and README links."""
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

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
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None, "damaged ZIP contents"
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
        lots = json.loads(text(skill / "references" / "guandi-lots.json"))["lots"]
        assert [lot["number"] for lot in lots] == list(range(1, 101))
        assert all(len(lot["verse"]) == 4 and lot["traditionalCommentary"] for lot in lots)
        for path in tracked_files:
            assert bundle.read("xiaodou-skill/" + path).decode().replace("\r\n", "\n") == text(skill / path), path
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
