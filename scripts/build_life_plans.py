"""Build the copyable life-plan pack from the Skill's professional references."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "skills/xiaodou-skill/references/life-plans"
PLAN_FILES = tuple(PLAN_DIR / name for name in ("health.md", "learning.md", "career.md", "household.md", "habits.md"))
PLAN_INDEX = PLAN_DIR / "README.md"
PLAN_PACK = ROOT / "prompts/xiaodou-life-plans.txt"
PLAN_FIELDS = ("触发", "中书立案", "门下核对", "尚书交办", "回奏", "依据")
INTRO = (
    "启用小豆皇帝模拟器。用白话称我「皇上」。按我的自然话选下面最贴近的一个计划。",
    "先沿用我说过的情况，缺关键条件才提问。中书拟案，门下查条件，尚书交计划，六部按需出手。",
    "交付写清第一步、完成标准和复盘时机。按我实际回报推进，条件变了只调整受影响的部分。",
    "引用的指南用于核对专业方法和地区范围。估计、待核、用户实际完成与工具回执分别说明。",
    "未经我确认，不下单、付款、发送、提交或设置提醒。只处理小事时直接按当前请求回答。",
    "如果我已经说明目标，按下面的对应计划开始。没有目标时，只问我最近想先安排什么。",
)


def plan_content():
    chapters = []
    ids = []
    for path in PLAN_FILES:
        source = path.read_text(encoding="utf-8").strip()
        blocks = re.split(r"^## (P\d{2}) · ", source, flags=re.MULTILINE)
        if len(blocks) != 13:
            raise ValueError(f"{path.name}: expected six plans")
        for plan_id, body in zip(blocks[1::2], blocks[2::2], strict=True):
            fields = re.findall(r"^- \*\*([^*]+)\*\*\s+\S", body, re.MULTILINE)
            if tuple(fields) != PLAN_FIELDS or "https://" not in body:
                raise ValueError(f"{plan_id}: expected the six plan fields and an external source")
            ids.append(plan_id)
        chapters.append(source)
    if ids != [f"P{number:02}" for number in range(1, 31)]:
        raise ValueError("Expected unique plan IDs in P01–P30 order")
    return "\n".join(INTRO) + "\n\n" + "\n\n".join(chapters) + "\n"
