"""Prepare group-free review packets and restore scores to anonymous comparison rows."""
import argparse
import hashlib
import json
import re
import secrets
from pathlib import Path

from pilot_measure import (
    COMPARISON_ARMS, check_carryover, check_comparison_scenario, check_ids, check_keys, summarize_comparisons,
)

ROLE_FILE = Path(__file__).resolve().parents[1] / "docs/studio/roles.json"


def group_labels():
    roles = json.loads(ROLE_FILE.read_text(encoding="utf-8"))
    words = ["普通小豆", "皇帝模式", "皇帝模拟器", "陛下", "皇上", "朕", "三省六部",
             "中书拟案", "门下核对", "尚书交付", "展开朝议", "准奏", "回奏"]
    words.extend(role[field] for role in roles for field in ("department", "name"))
    return re.compile("|".join(map(re.escape, words)))


def redacted(text, label, labels):
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{label} needs a redacted text excerpt")
    if labels.search(text):
        raise ValueError(f"{label} still contains an identifiable role or group label")


def material_digest(task, excerpt):
    if not all(isinstance(value, str) for value in (task, excerpt)):
        raise ValueError("review needs the original task and excerpt")
    material = json.dumps([task, excerpt], ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def anonymize(records):
    check_ids(records, "source comparisons")
    labels = group_labels()
    reviewer, key = [], []
    for record in records:
        check_keys(record, ("id", "order", "task", "carryover", "scenario", *COMPARISON_ARMS), "source comparison")
        if record.get("order") not in COMPARISON_ARMS:
            raise ValueError("order must name the first arm")
        check_carryover(record)
        check_comparison_scenario(record)
        task = record.get("task")
        redacted(task, "common task", labels)
        links = {"id": record["id"], "order": record["order"], "digests": {}}
        links.update({field: record[field] for field in ("carryover", "scenario") if field in record})
        for arm in COMPARISON_ARMS:
            excerpt = record.get(arm)
            if excerpt is None:
                continue
            redacted(excerpt, "observed arm", labels)
            code = secrets.token_hex(12)
            links[arm] = code
            links["digests"][arm] = material_digest(task, excerpt)
            reviewer.append({"code": code, "task": task, "excerpt": excerpt, "scores": {}})
        key.append(links)
    secrets.SystemRandom().shuffle(reviewer)
    return reviewer, key


def restore(key, reviewer):
    check_ids(key, "private key")
    digests = {}
    for item in key:
        check_keys(item, ("id", "order", "digests", "carryover", "scenario", *COMPARISON_ARMS), "private key row")
    codes = [item[arm] for item in key for arm in COMPARISON_ARMS if arm in item]
    if any(not isinstance(code, str) for code in codes) or len(set(codes)) != len(codes):
        raise ValueError("invalid or duplicate review codes in the private key")
    for item in key:
        if "digests" in item:
            arms = {arm for arm in COMPARISON_ARMS if arm in item}
            checksums = item["digests"]
            check_keys(checksums, arms, "private key digests")
            if arms != checksums.keys() or any(
                not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
                for value in checksums.values()
            ):
                raise ValueError("private key needs one material digest per observed arm")
            digests.update({item[arm]: checksums[arm] for arm in arms})
    unknown = set(codes)
    scores = {}
    if not isinstance(reviewer, list):
        raise ValueError("review must be an array")
    for item in reviewer:
        check_keys(item, ("code", "scores", "task", "excerpt"), "review")
        code = item.get("code")
        if not isinstance(code, str) or code not in unknown:
            raise ValueError("review contains an unknown or duplicate code")
        if code in digests and material_digest(item.get("task"), item.get("excerpt")) != digests[code]:
            raise ValueError("review material does not match its original task and excerpt")
        unknown.remove(code)
        scores[code] = item.get("scores", {})

    rows = []
    for item in key:
        result = {"id": item["id"], "order": item["order"]}
        result.update({field: item[field] for field in ("carryover", "scenario") if field in item})
        for arm in COMPARISON_ARMS:
            if item.get(arm) in scores:
                result[arm] = scores[item[arm]]
        rows.append(result)
    summarize_comparisons(rows)
    return rows


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def serialize(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    prepare = subcommands.add_parser("prepare")
    prepare.add_argument("source", type=Path)
    prepare.add_argument("output_directory", type=Path)
    unblind = subcommands.add_parser("restore")
    unblind.add_argument("private_key", type=Path)
    unblind.add_argument("review", type=Path)
    unblind.add_argument("output_file", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            reviewer, key = anonymize(read(args.source))
            args.output_directory.mkdir()
            (args.output_directory / "review.json").write_text(serialize(reviewer), encoding="utf-8")
            (args.output_directory / "private-key.json").write_text(serialize(key), encoding="utf-8")
        else:
            rows = restore(read(args.private_key), read(args.review))
            with args.output_file.open("x", encoding="utf-8") as output:
                output.write(serialize(rows))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Invalid review data or output path: {exc}\n")


if __name__ == "__main__":
    main()
