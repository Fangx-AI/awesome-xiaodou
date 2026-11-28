"""Build the prompt library, mobile paste pack and portable Agent Skill."""
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_life_plans import APP_PACK_NAME, PLAN_FILES, PLAN_INDEX, app_pack_files, copy_packs

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "xiaodou-skill"
LIBRARY = SKILL / "references" / "prompts.md"
PASTE_PACK = ROOT / "prompts" / "xiaodou-paste-pack.txt"
QUICK_PACK = ROOT / "prompts" / "xiaodou-quick-pack.txt"
STARTER = ROOT / "prompts" / "xiaodou-start.txt"
PILOT_STARTER = ROOT / "prompts" / "xiaodou-pilot-start.txt"
PILOT_GUIDE = ROOT / "docs" / "field-tests" / "pilot-s0.md"
QUICK_IDS = ("G01", "H01", "09", "11", "36", "01", "07", "41", "42")
COURT_ROLES = ROOT / "docs" / "studio" / "roles.json"
COURT_REFERENCE = LIBRARY.parent / "court.md"
PLANNING_REFERENCE = LIBRARY.parent / "planning.md"
DIVINATION_REFERENCE = LIBRARY.parent / "divination.md"
CHART_TOOLS = SKILL / "scripts" / "birth-chart"
DIVINATION_UPSTREAM = SKILL / "vendor" / "ziwei-bazi"
DIVINATION_FILES = (
    DIVINATION_REFERENCE, LIBRARY.parent / "guandi-lots.json", CHART_TOOLS / "chart.cjs",
    CHART_TOOLS / "fortune.cjs", CHART_TOOLS / "package.json", CHART_TOOLS / "package-lock.json",
)


def build_court():
    roles = json.loads(COURT_ROLES.read_text(encoding="utf-8"))
    departments = {role["department"] for role in roles}
    expected = {"中书省", "门下省", "尚书省", "吏部", "户部", "礼部", "兵部", "刑部", "工部"}
    portraits = [COURT_ROLES.parent / "portraits" / role["portrait"] for role in roles]
    if departments != expected or len(roles) != len(expected):
        raise ValueError("The court must contain one profile per department")
    if len(set(portraits)) != len(roles) or not all(path.is_file() for path in portraits):
        raise ValueError("Each department must have its own portrait file")
    lines = ["# 三省六部人物志", "", "用户要求了解分工时再打开。人物均为虚构设计。", ""]
    for role in roles:
        lines.extend([
            f"## {role['department']} · {role['name']}", "",
            f"![{role['name']}](https://raw.githubusercontent.com/Fangx-AI/awesome-xiaodou/main/docs/studio/portraits/{role['portrait']})", "",
            f"- 职责：{role['duty']}。{role['deliverable']}。",
            f"- 性格：{role['personality']}。",
            f"- 举例：{role['example']}。", "",
        ])
    COURT_REFERENCE.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return portraits


def read_prompt(path):
    body = path.read_text(encoding="utf-8")
    blocks = re.findall(r"^\x60{3}text\n(.*?)\n\x60{3}$", body, re.M | re.S)
    if len(blocks) != 1 or not blocks[0].strip():
        raise ValueError(f"Expected one non-empty text prompt: {path}")
    return blocks[0].strip()


def main(output_folder):
    copies = copy_packs()
    for path, content in copies.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    cases = json.loads((ROOT / "data/playbooks.json").read_text(encoding="utf-8"))
    cases.append({"id": "H01", "path": "prompts/41-weight-plan.md",
                  "title": "一个月减肥计划与每周复盘", "category": "健康与习惯"})
    cases.append({"id": "G01", "path": "prompts/emperor-simulator.md",
                  "title": "小豆皇帝模拟器", "category": "个人治理"})
    groups = {}
    for case in cases:
        groups.setdefault(case["category"], []).append(case)

    markdown = ["# 小豆提示词库", "", f"共 {len(cases)} 条。可按场景或编号选用。", ""]
    routing = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[2].strip()
    routing = routing.replace("[提示词库](references/prompts.md)", "下方的提示词库")
    routing = routing.replace("[30 个生活计划](references/life-plans/README.md)", "当前对话已加载的生活计划资料（如有）")
    routing = routing.replace("[三省六部人物志](references/court.md)", "G01 中的角色分工")
    routing = routing.replace("[计划手册](references/planning.md)", "G01 的常见奏请")
    routing = routing.replace("[礼部 · 传统术数](references/divination.md)", "G01 的「御前问签」规则")
    intro = [
        "请在本次对话中启用下面的小豆 Skill。",
        routing,
        "已经收到目标就直接按 G01 办理。没有目标时问：皇上，今天想先办哪件事？",
        "以下是提示词库：",
    ]
    paste = intro.copy()
    by_id = {}
    for category, entries in groups.items():
        markdown.extend([f"## {category}", ""])
        paste.append(f"【{category}】")
        for case in entries:
            heading = f"{case['id']} · {case['title']}"
            prompt = read_prompt(ROOT / case["path"])
            markdown.extend([f"### {heading}", "", "\x60\x60\x60text", prompt, "\x60\x60\x60", ""])
            entry = f"{heading}\n{prompt}"
            paste.append(entry)
            if case["id"] in by_id:
                raise ValueError(f"Duplicate prompt ID: {case['id']}")
            by_id[case["id"]] = entry

    LIBRARY.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY.write_text("\n".join(markdown), encoding="utf-8", newline="\n")
    PASTE_PACK.write_text("\n\n".join(paste) + "\n", encoding="utf-8", newline="\n")
    quick = intro + [by_id[prompt_id] for prompt_id in QUICK_IDS]
    QUICK_PACK.write_text("\n\n".join(quick) + "\n", encoding="utf-8", newline="\n")
    example = re.search(r"^```text\n(.*?)\n```$", PILOT_GUIDE.read_text(encoding="utf-8"), re.M | re.S)
    if not example or not example[1].strip():
        raise ValueError("Missing first message in the S0 guide")
    pilot_text = example[1].strip()
    if not pilot_text.startswith(STARTER.read_text(encoding="utf-8").strip() + "\n\n"):
        raise ValueError("The first message in the S0 guide must start with the current starter")
    PILOT_STARTER.write_text(pilot_text + "\n", encoding="utf-8", newline="\n")
    output_folder.mkdir(parents=True, exist_ok=True)
    portraits = build_court()
    archive = output_folder / "xiaodou-skill.zip"
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        upstream_files = sorted(path for path in DIVINATION_UPSTREAM.rglob("*")
                                if path.is_file() and (path.suffix in {".md", ".py"} or path.name == "LICENSE"))
        if not (DIVINATION_UPSTREAM / "SKILL.md").is_file():
            raise ValueError("Missing vendored ziwei-bazi Skill")
        for path in (SKILL / "SKILL.md", LIBRARY, LIBRARY.parent / "prompt-sources.md", COURT_REFERENCE, PLANNING_REFERENCE,
                     PLAN_INDEX, *PLAN_FILES, *DIVINATION_FILES, *upstream_files):
            bundle.write(path, path.relative_to(SKILL.parent).as_posix())
        for portrait in portraits:
            bundle.write(portrait, f"xiaodou-skill/assets/roles/{portrait.name}")
        bundle.write(ROOT / "LICENSE", "xiaodou-skill/LICENSE")
    app_archive = output_folder / APP_PACK_NAME
    with ZipFile(app_archive, "w", compression=ZIP_DEFLATED) as bundle:
        for name, content in app_pack_files(copies).items():
            bundle.writestr(name, content)
    print(f"{len(cases)} prompts; archives: {archive}, {app_archive}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/build_skill.py OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]))
