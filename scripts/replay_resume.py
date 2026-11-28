"""Export a two-plan summary and paste the actual reply into a fresh Codex session."""
import argparse
import hashlib
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from replay_court import ROOT, STARTER, replay


REQUEST = (
    "今天是北京时间 2026 年 11 月 28 日。以后称我小林。英语会议开场已经写好第一句，也读过一次。"
    "下一步是明天晚上七点半留十五分钟练第二句。之前我同意设这条提醒，提交时超时了，没拿到回执，也没查到是否创建。"
    "读书这周完成了两次，已暂停，等我主动说继续。那次旧的留学材料整理已经结案，不带到新对话。"
    "我要换对话，把英语和读书的进度一起带过去，先接英语。请只输出一段能整段复制到新对话的摘要。"
)
COMMON = (
    "小林", "英语|英文|会议开场", "第二句", "读书|阅读", "暂停", r"两次|2\s*次", r"一(?:次|遍)|1\s*(?:次|遍)",
    r"11\s*月\s*29\s*日|2026-11-29", r"19[:：]30|7[:：]30|七点半", "北京时间|UTC[+]0?8",
    "核对|查看|确认", "提醒", "超时|无回执|未见回执|结果未知|创建.{0,10}待核",
    r"重新.{0,12}确认|新对话.{0,24}确认|等.{0,12}确认|再行确认|再次确认",
)
FORBIDDEN = (
    "皇上|朕", "已设置提醒|提醒已创建|补建成功|已重新创建", "留学材料",
    "此前已获.{0,5}确认|已获.{0,5}同意|此前已明确同意",
)
LATER_UPDATE = (
    "现在是北京时间 2026 年 11 月 30 日，原定的时间已经过了。我没有练第二句。"
    "今天只有五分钟，现在就练第二句，先别查或设置任何提醒。读书继续暂停。"
    "沿用已经做过的事，只给今天能做的一步。"
)
LATER_REQUIRED = (
    "小林", "第一句", r"一(?:次|遍)|1\s*(?:次|遍)", "第二句", r"五分钟|5\s*分钟",
)


def round_trip(args, source, prompts):
    export = replay(args, (f"{source}-export", source, REQUEST, COMMON, FORBIDDEN), prompts)
    if not export["turn_completed"] or not export["output"]:
        return [export]
    # Use the complete reply as the only user message. No starter or history is reloaded.
    imported = replay(args, (f"{source}-import", "fresh", export["output"], COMMON, FORBIDDEN), prompts)
    if not args.resume_later:
        return [export, imported]
    later = replay(
        args,
        (f"{source}-late-import", "fresh", f"{export['output']}\n\n当前更新：{LATER_UPDATE}", LATER_REQUIRED,
         (*FORBIDDEN, "第二句已经练完|第二句已完成|今晚七点半练|今天19:30练|已核对提醒|重新设好了|恢复读书计划")),
        prompts,
    )
    return [export, imported, later]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--codex", default=shutil.which("codex") or "codex")
    parser.add_argument("--model")
    parser.add_argument("--resume-later", action="store_true", help="Also resume after the old time has passed")
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.compare = False
    prompts = {
        "starter": STARTER.read_text(encoding="utf-8").strip(),
        "learning": (ROOT / "prompts/life-plans/learning.txt").read_text(encoding="utf-8").strip(),
        "fresh": "",
    }
    with ThreadPoolExecutor(max_workers=2) as pool:
        groups = pool.map(lambda source: round_trip(args, source, prompts), ("starter", "learning"))
        records = [record for group in groups for record in group]
    report = {
        "environment": "Codex CLI, independent sessions, no platform connectors",
        "model": args.model or "Codex CLI default",
        "instruction_sha256": {name: hashlib.sha256(prompt.encode()).hexdigest() for name, prompt in prompts.items()},
        "records": records,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for record in records:
        print(f"{record['case']} {'PASS' if record['passed'] else 'REVIEW'}")
    expected_count = 6 if args.resume_later else 4
    return 0 if len(records) == expected_count and all(record["passed"] for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
