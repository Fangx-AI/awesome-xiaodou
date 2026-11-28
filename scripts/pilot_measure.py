"""Summarize anonymous pilot records without publishing individual data."""
import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path

READ_ANSWERS = ("identity", "where", "how", "confirmation")
CHANGE_SCORES = ("preserved", "affected_only", "actionable")
COMPARISON_ARMS = ("regular", "emperor")
COMPARISON_FIELDS = ("first_action", "preserved", "affected_only", "replan_actionable")


def check_keys(value, allowed, label):
    if not isinstance(value, dict) or value.keys() - set(allowed):
        raise ValueError(f"{label}: expected only {', '.join(allowed)}")


def check_flags(value, allowed, label):
    check_keys(value, allowed, label)
    if any(type(flag) is not bool for flag in value.values()):
        raise ValueError(f"{label}: scores must be true or false")


def read_day(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label}: expected YYYY-MM-DD")
    return date.fromisoformat(value)


def check_ids(records, label):
    if not isinstance(records, list):
        raise ValueError(f"{label}: expected an array")
    seen = set()
    for index, record in enumerate(records, 1):
        uid = record.get("id") if isinstance(record, dict) else None
        if not isinstance(uid, str) or not re.fullmatch(r"P-[0-9]{4,12}", uid):
            raise ValueError(f"{label} row {index}: expected an anonymous ID (e.g. P-0001)")
        if uid in seen:
            raise ValueError(f"{label} row {index}: duplicate participant")
        seen.add(uid)


def ratio(numerator, denominator):
    return {
        "numerator": numerator, "denominator": denominator,
        "percent": round(100 * numerator / denominator, 1) if denominator else None,
    }


def summarize_comparisons(records):
    check_ids(records, "comparisons")
    arm_counts = dict.fromkeys(COMPARISON_ARMS, 0)
    outcomes = {(True, True): "both", (True, False): "regular_only",
                (False, True): "emperor_only", (False, False): "neither"}
    scores = {
        mode: {"pairs": 0, "emperor_only": 0, "regular_only": 0, "both": 0, "neither": 0}
        for mode in ("first_action", "replan")
    }
    for item in records:
        check_keys(item, ("id", "order", *COMPARISON_ARMS), "comparison")
        if item.get("order") not in COMPARISON_ARMS:
            raise ValueError("comparison order must name the first arm: regular or emperor")
        arm_counts[item["order"]] += 1
        arms = [item.get(arm, {}) for arm in COMPARISON_ARMS]
        for result in arms:
            check_flags(result, COMPARISON_FIELDS, "comparison arm")

        for name, fields in (("first_action", ("first_action",)), ("replan", COMPARISON_FIELDS[1:])):
            if not all(field in arm for arm in arms for field in fields):
                continue
            regular, emperor = (all(arm[field] for field in fields) for arm in arms)
            result = scores[name]
            result["pairs"] += 1
            result[outcomes[regular, emperor]] += 1

    for values in scores.values():
        count = values["pairs"]
        values["unscored_pairs"] = len(records) - count
        delta = values["emperor_only"] - values["regular_only"]
        values["emperor_minus_regular_pp"] = round(100 * delta / count, 1) if count else None
    return {"enrolled": len(records), "order_counts": arm_counts, "outcomes": scores}


def summarize(data):
    check_keys(data, ("as_of", "cold_reads", "trials", "comparisons"), "report")
    as_of = read_day(data.get("as_of"), "as_of")
    reads, trials = data.get("cold_reads", []), data.get("trials", [])
    check_ids(reads, "cold_reads")
    check_ids(trials, "trials")

    understood = 0
    for item in reads:
        check_keys(item, ("id", "answers", "found_start"), "cold read")
        answers = item.get("answers", {})
        check_flags(answers, READ_ANSWERS, "cold read answers")
        check_flags({key: item[key] for key in ("found_start",) if key in item}, ("found_start",), "cold read")
        understood += bool(item.get("found_start") and all(answers.get(key) for key in READ_ANSWERS))

    ready = seven_day_eligible = finished = changes = good_changes = returned = return_eligible = 0
    for item in trials:
        check_keys(item, ("id", "channel", "started_on", "first_action", "finished_on", "change", "return"), "trial")
        channel = item.get("channel", "")
        if "channel" in item and (not isinstance(channel, str) or not re.fullmatch(r"[a-z0-9-]{1,32}", channel)):
            raise ValueError("trial channel must be an anonymous label")
        check_flags({key: item[key] for key in ("first_action",) if key in item}, ("first_action",), "trial")
        start = read_day(item.get("started_on"), "started_on")
        if start > as_of:
            raise ValueError("started_on is after as_of")
        ready += item.get("first_action", False)
        due = start + timedelta(days=7)
        matured = due <= as_of
        seven_day_eligible += matured
        if "finished_on" in item:
            end = read_day(item["finished_on"], "finished_on")
            if not start <= end <= as_of:
                raise ValueError("finished_on is outside the observed interval")
            finished += matured and end <= due

        change = item.get("change", {})
        check_flags(change, CHANGE_SCORES, "change")
        if all(key in change for key in CHANGE_SCORES):
            changes += 1
            good_changes += all(change.values())

        return_matured = start + timedelta(days=8) <= as_of
        return_eligible += return_matured
        if "return" in item:
            back = item["return"]
            check_keys(back, ("day", "prompted"), "return")
            check_flags({"prompted": back.get("prompted")}, ("prompted",), "return")
            day = read_day(back.get("day"), "return day")
            if not start <= day <= as_of:
                raise ValueError("return day is outside the observed interval")
            returned += return_matured and 6 <= (day - start).days <= 8 and not back["prompted"]

    return {
        "as_of": as_of.isoformat(),
        "cold_read": ratio(understood, len(reads)),
        "first_action": ratio(ready, len(trials)),
        "seven_day_completion": ratio(finished, seven_day_eligible),
        "pending_seven_day_window": len(trials) - seven_day_eligible,
        "replanning": ratio(good_changes, changes),
        "unprompted_return": ratio(returned, return_eligible),
        "matched_comparison": summarize_comparisons(data.get("comparisons", [])),
        "thresholds": {
            "cold_read": len(reads) >= 12 and 12 * understood >= 10 * len(reads),
            "first_action": len(trials) >= 100 and 100 * ready >= 80 * len(trials),
            "seven_day_completion": seven_day_eligible >= 100 and 100 * finished >= 60 * seven_day_eligible,
            "replanning": changes >= 30 and 100 * good_changes >= 85 * changes,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path)
    args = parser.parse_args()
    try:
        source = json.loads(args.records.read_text(encoding="utf-8-sig"))
        report = summarize(source)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Invalid pilot data: {exc}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
