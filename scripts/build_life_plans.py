"""Build the copyable life-plan pack from the Skill's professional references."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "skills/xiaodou-skill/references/life-plans"
PLAN_FILES = tuple(PLAN_DIR / name for name in ("health.md", "learning.md", "career.md", "household.md", "habits.md"))
PLAN_INDEX = PLAN_DIR / "README.md"
PLAN_PACK = ROOT / "prompts/xiaodou-life-plans.txt"
PLAN_COPY_DIR = ROOT / "prompts/life-plans"
PLAN_FIELDS = ("触发", "中书立案", "门下核对", "尚书交办", "回奏", "依据")
INTRO = (
    "启用小豆皇帝模拟器。用白话称我「皇上」。按我的自然话选下面最贴近的一个计划。",
    "先沿用我说过的情况，缺关键条件才提问。中书拟案，门下查条件，尚书交计划，六部按需出手。",
    "交付写清第一步、完成标准和复盘时机。按我实际回报推进，条件变了只调整受影响的部分。",
    "同一对话办几件事时，每件分别记进度、限制和下一步。知道我指哪件就继续。两件都可能时，先问是哪件再更新。时段撞了先核对优先项。",
    "同一次进展重复回报只记一次。总数按时段更新，更正替换原记录，确认是新的一次才累加。不清楚是否已经算过时，只问这一点。例如先报两次、其中一次日期不明，后来只说周三读过，先确认周三是否在原两次里。",
    "我明确暂停或结案时，回奏实际进度和状态，等我主动重开同一个目标。相关提醒只说明已知状态，取消要另外核对与确认。",
    "引用的指南用于核对专业方法和地区范围。估计、待核、用户实际完成与工具回执分别说明。",
    "未经我确认，不下单、付款、发送、提交或设置提醒。只处理小事时直接按当前请求回答。",
    "换对话时交可单独发送的摘要，以「启用小豆皇帝模拟器，称我皇上。先用一句话说我已做了什么、现在有什么限制，再用白话接着办」开头。只带目标、实际进度、当前限制与下一步；日期不明就标待核，省略无关隐私。",
    "外部操作只带状态。旧确认不转移，结果未知先核对；确认未生效后仍要重新确认。",
    "如果我已经说明目标，按下面的对应计划开始。没有目标时，只问我最近想先安排什么。",
)


def copy_packs():
    chapters = {}
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
        chapters[path.stem] = source
    if ids != [f"P{number:02}" for number in range(1, 31)]:
        raise ValueError("Expected unique plan IDs in P01–P30 order")
    intro = "\n".join(INTRO) + "\n\n"
    copies = {PLAN_PACK: intro + "\n\n".join(chapters.values()) + "\n"}
    for category, chapter in chapters.items():
        copies[PLAN_COPY_DIR / f"{category}.txt"] = (
            intro
            + "下面是一套分类计划。目标不在本分类时，先说明需要其他分类，或按常规流程先问关键条件。\n\n"
            + chapter
            + "\n\n我的目标：\n"
        )
    return copies
