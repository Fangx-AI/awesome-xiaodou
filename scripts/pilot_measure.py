"""Summarize anonymous pilot records without publishing individual data."""
import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path
from statistics import median

from build_life_plans import PLAN_FILES, PLAN_PACK, PLAN_STARTER_FILES, SCENE_FILES
from render_pilot_report import render

READ_ANSWERS = ("identity", "where", "how", "confirmation")
CHANGE_SCORES = ("preserved", "affected_only", "actionable")
COMPARISON_ARMS = ("regular", "emperor")
COMPARISON_REPLAN_FIELDS = ("preserved", "affected_only", "replan_actionable")
COMPARISON_FIELDS = ("first_action", *COMPARISON_REPLAN_FIELDS)
CARRYOVER_STAGES = ("none", "first_action", "replan")
COMPARISON_SCENARIOS = {
    "pilot-reschedule": "英语练习改期",
    "monthly-partial-intake": "减肥计划补问",
    "comparison-reading-threshold": "阅读改完成标准",
    "comparison-event-budget": "读书会改物料预算",
}
TRIAL_STARTERS = ("xiaodou-start.txt", PLAN_PACK.name,
                  *(f"life-plans/{path.stem}.txt" for path in PLAN_FILES),
                  *(f"life-plans/{path.name}" for path in SCENE_FILES.values()),
                  *(f"life-plans/{path.name}" for path in PLAN_STARTER_FILES.values()))
SHARED_SCENES = ("weight", "fitness", "reading", "english", "study-abroad")
ACCESS_STAGES = ("find", "install", "login", "activate", "send", "other")


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


def summarize_groups(groups):
    return {
        label: {"started": counts["started"],
                "completion": ratio(counts["finished"], counts["eligible"])}
        for label, counts in sorted(groups.items())
    }


def summarize_first_action_timing(observations):
    rounds = [row["response_round"] for row in observations if "response_round" in row]
    seconds = [row["elapsed_seconds"] for row in observations if "elapsed_seconds" in row]
    return {
        "qualified": len(observations),
        "on_first_reply": ratio(rounds.count(1), len(rounds)),
        "median_response_round": median(rounds) if rounds else None,
        "elapsed_observed": len(seconds),
        "median_elapsed_seconds": median(seconds) if seconds else None,
    }


def score_required_checks(scores, checks):
    grades = [scores.get(check) for check in checks]
    if False in grades:
        return False
    return None if None in grades else True


def score_comparison_pairs(records):
    outcomes = {(True, True): "both", (True, False): "regular_only",
                (False, True): "emperor_only", (False, False): "neither"}
    criteria = {
        "first_action": ("first_action",),
        "replan": COMPARISON_REPLAN_FIELDS,
        **{field: (field,) for field in COMPARISON_REPLAN_FIELDS},
    }
    scores = {
        name: {"pairs": 0, "emperor_only": 0, "regular_only": 0, "both": 0, "neither": 0}
        for name in criteria
    }
    follow_ups = {"pairs": 0, "regular_total": 0, "emperor_total": 0,
                  "emperor_fewer": 0, "regular_fewer": 0, "equal": 0}
    for item in records:
        arms = [item.get(arm, {}) for arm in COMPARISON_ARMS]
        if all("follow_up_questions" in arm and "first_action" in arm for arm in arms):
            regular, emperor = (arm["follow_up_questions"] for arm in arms)
            follow_ups["pairs"] += 1
            follow_ups["regular_total"] += regular
            follow_ups["emperor_total"] += emperor
            if emperor < regular:
                follow_ups["emperor_fewer"] += 1
            elif regular < emperor:
                follow_ups["regular_fewer"] += 1
            else:
                follow_ups["equal"] += 1

        for name, fields in criteria.items():
            pair = tuple(score_required_checks(arm, fields) for arm in arms)
            if None not in pair:
                result = scores[name]
                result["pairs"] += 1
                result[outcomes[pair]] += 1

    for values in scores.values():
        count = values["pairs"]
        values["unscored_pairs"] = len(records) - count
        delta = values["emperor_only"] - values["regular_only"]
        values["emperor_minus_regular_pp"] = round(100 * delta / count, 1) if count else None
    count = follow_ups["pairs"]
    follow_ups["unscored_pairs"] = len(records) - count
    follow_ups["emperor_minus_regular_mean"] = (
        round((follow_ups["emperor_total"] - follow_ups["regular_total"]) / count, 2) if count else None
    )
    return {
        "enrolled": len(records),
        "outcomes": {name: scores[name] for name in ("first_action", "replan")},
        "replan_checks": {name: scores[name] for name in COMPARISON_REPLAN_FIELDS},
        "follow_up_questions": follow_ups,
    }


def check_carryover(item):
    if "carryover" in item and item["carryover"] not in CARRYOVER_STAGES:
        raise ValueError("carryover must be none, first_action or replan")


def check_comparison_scenario(item):
    if "scenario" in item:
        value = item["scenario"]
        if not isinstance(value, str) or value not in COMPARISON_SCENARIOS:
            raise ValueError("scenario must name a supported comparison task")


def comparison_report(records):
    counts = dict.fromkeys((*CARRYOVER_STAGES, "unknown"), 0)
    screened = []
    for item in records:
        value = item.get("carryover", "unknown")
        counts[value] += 1
        if value == "none":
            screened.append(item)
        elif value == "replan":
            # The first action and its follow-ups preceded the conflicting information.
            screened.append({
                arm: {key: score for key, score in item.get(arm, {}).items() if key not in COMPARISON_REPLAN_FIELDS}
                for arm in COMPARISON_ARMS
            })
    return {
        **score_comparison_pairs(records),
        "carryover_counts": counts,
        "carryover_screened": score_comparison_pairs(screened),
    }


def summarize_comparisons(records):
    check_ids(records, "comparisons")
    by_order = {arm: [] for arm in COMPARISON_ARMS}
    scenario_counts = dict.fromkeys((*COMPARISON_SCENARIOS, "unspecified"), 0)
    for item in records:
        check_keys(item, ("id", "order", "carryover", "scenario", *COMPARISON_ARMS), "comparison")
        if item.get("order") not in COMPARISON_ARMS:
            raise ValueError("comparison order must name the first arm: regular or emperor")
        check_carryover(item)
        check_comparison_scenario(item)
        scenario_counts[item.get("scenario", "unspecified")] += 1
        for result in (item.get(arm, {}) for arm in COMPARISON_ARMS):
            check_keys(result, (*COMPARISON_FIELDS, "follow_up_questions"), "comparison arm")
            check_flags({key: result[key] for key in COMPARISON_FIELDS if key in result},
                        COMPARISON_FIELDS, "comparison arm")
            if "follow_up_questions" in result:
                count = result["follow_up_questions"]
                if type(count) is not int or count < 0:
                    raise ValueError("follow_up_questions must be a non-negative integer")
        by_order[item["order"]].append(item)

    return {
        **comparison_report(records),
        "order_counts": {arm: len(items) for arm, items in by_order.items()},
        "scenario_counts": {COMPARISON_SCENARIOS.get(key, "场景未登记"): count
                            for key, count in scenario_counts.items() if count},
        "by_order": {arm: comparison_report(items) for arm, items in by_order.items()},
    }


def summarize_access(records, starts, as_of):
    check_ids(records, "access_blocks")
    by_stage = {stage: {"reported": 0, "recovered": 0, "started_trial": 0} for stage in ACCESS_STAGES}
    for item in records:
        check_keys(item, ("id", "stage", "observed_on", "recovered_on"), "access block")
        stage = item.get("stage")
        if stage not in ACCESS_STAGES:
            raise ValueError("access block stage must name a supported pre-start step")
        observed = read_day(item.get("observed_on"), "observed_on")
        start = starts.get(item["id"])
        if observed > as_of or (start is not None and observed > start):
            raise ValueError("access block must be observed by as_of and no later than trial start")
        if "recovered_on" in item:
            recovered = read_day(item["recovered_on"], "recovered_on")
            if not observed <= recovered <= (start or as_of):
                raise ValueError("recovered_on is outside the observed pre-start interval")
        counts = by_stage[stage]
        counts["reported"] += 1
        counts["recovered"] += "recovered_on" in item or start is not None
        counts["started_trial"] += start is not None

    for counts in by_stage.values():
        counts["recovery_unconfirmed"] = counts["reported"] - counts["recovered"]
    return {"by_stage": by_stage, "people": len(records)}


def summarize(data):
    check_keys(data, ("as_of", "cohort", "candidate_commit", "public_readme_commit",
                      "cold_reads", "trials", "comparisons", "access_blocks"), "report")
    as_of = read_day(data.get("as_of"), "as_of")
    cohort = data.get("cohort")
    if "cohort" in data and (not isinstance(cohort, str) or not re.fullmatch(r"[a-z0-9-]{1,40}", cohort)):
        raise ValueError("cohort must be a stable anonymous batch label")
    for field in ("candidate_commit", "public_readme_commit"):
        if field in data and (not isinstance(data[field], str) or not re.fullmatch(r"[0-9a-f]{40}", data[field])):
            raise ValueError(f"{field} must be the full lowercase Git commit ID")
    candidate_commit = data.get("candidate_commit")
    reads, trials = data.get("cold_reads", []), data.get("trials", [])
    check_ids(reads, "cold_reads")
    check_ids(trials, "trials")

    understood = scored_reads = assisted_reads = 0
    read_checks = dict.fromkeys((*READ_ANSWERS, "found_start"), 0)
    for item in reads:
        check_keys(item, ("id", "answers", "found_start", "assisted"), "cold read")
        answers = item.get("answers", {})
        check_flags(answers, READ_ANSWERS, "cold read answers")
        flags = ("found_start", "assisted")
        check_flags({key: item[key] for key in flags if key in item}, flags, "cold read")
        if item.get("assisted"):
            assisted_reads += 1
            continue
        if item.get("assisted") is not False or "found_start" not in item:
            continue
        if not all(key in answers for key in READ_ANSWERS):
            continue
        scored_reads += 1
        for key, correct in answers.items():
            read_checks[key] += correct
        read_checks["found_start"] += item["found_start"]
        understood += item["found_start"] and all(answers.values())

    ready = first_action_observed = 0
    seven_day_eligible = finished = reported_incomplete = changes = good_changes = 0
    unscored_changes = 0
    returned = prompted_returns = return_eligible = 0
    channels, starters, shared_scenes = {}, {}, {}
    first_action_timing = {}
    starts = {}
    for item in trials:
        check_keys(item, ("id", "channel", "starter", "shared_scene", "started_on", "first_action", "first_action_observation", "finished_on",
                          "no_completion_reported_on", "change", "return"), "trial")
        channel = item.get("channel", "unspecified")
        if not isinstance(channel, str) or not re.fullmatch(r"[a-z0-9-]{1,32}", channel):
            raise ValueError("trial channel must be an anonymous label")
        starter = item.get("starter", "unspecified")
        if "starter" in item and starter not in TRIAL_STARTERS:
            raise ValueError("trial starter must name a supported file from STARTERS.tsv")
        shared_scene = item.get("shared_scene", "unspecified")
        if "shared_scene" in item and shared_scene not in SHARED_SCENES:
            raise ValueError("trial shared_scene must name one of the five public share cards")
        check_flags({key: item[key] for key in ("first_action",) if key in item}, ("first_action",), "trial")
        start = read_day(item.get("started_on"), "started_on")
        if start > as_of:
            raise ValueError("started_on is after as_of")
        starts[item["id"]] = start
        first_action_observed += "first_action" in item
        ready += item.get("first_action", False)
        timing = item.get("first_action_observation", {})
        if "first_action_observation" in item:
            check_keys(timing, ("response_round", "elapsed_seconds"), "first action observation")
            if not timing or item.get("first_action") is not True:
                raise ValueError("first action observation needs a qualified first action and at least one measurement")
            for key, minimum in (("response_round", 1), ("elapsed_seconds", 0)):
                if key in timing and (type(timing[key]) is not int or timing[key] < minimum):
                    raise ValueError(f"{key} must be an integer of at least {minimum}")
        if item.get("first_action") is True:
            first_action_timing.setdefault(starter, []).append(timing)
        due = start + timedelta(days=7)
        matured = due <= as_of
        seven_day_eligible += matured
        end = None
        if "finished_on" in item:
            end = read_day(item["finished_on"], "finished_on")
            if not start <= end <= as_of:
                raise ValueError("finished_on is outside the observed interval")

        reported_no_completion = "no_completion_reported_on" in item
        if reported_no_completion:
            report_day = read_day(item["no_completion_reported_on"], "no_completion_reported_on")
            if not due <= report_day <= as_of:
                raise ValueError("no_completion_reported_on must fall between the seven-day cutoff and as_of")
            if end is not None and end <= due:
                raise ValueError("no_completion_reported_on conflicts with on-time completion")

        on_time = end is not None and end <= due
        for groups, label in ((channels, channel), (starters, starter), (shared_scenes, shared_scene)):
            counts = groups.setdefault(label, {"started": 0, "eligible": 0, "finished": 0})
            counts["started"] += 1
            counts["eligible"] += matured
            counts["finished"] += matured and on_time
        if matured:
            finished += on_time
            reported_incomplete += reported_no_completion or (end is not None and end > due)

        if "change" in item:
            change = item["change"]
            check_flags(change, CHANGE_SCORES, "change")
            changes += 1
            outcome = score_required_checks(change, CHANGE_SCORES)
            good_changes += outcome is True
            unscored_changes += outcome is None

        return_matured = start + timedelta(days=8) <= as_of
        return_eligible += return_matured
        if "return" in item:
            back = item["return"]
            check_keys(back, ("day", "prompted"), "return")
            check_flags({"prompted": back.get("prompted")}, ("prompted",), "return")
            day = read_day(back.get("day"), "return day")
            if not start <= day <= as_of:
                raise ValueError("return day is outside the observed interval")
            if return_matured and 6 <= (day - start).days <= 8:
                if back["prompted"]:
                    prompted_returns += 1
                else:
                    returned += 1

    return {
        "as_of": as_of.isoformat(),
        "candidate_commit": candidate_commit,
        "public_readme_commit": data.get("public_readme_commit"),
        "cold_read": ratio(understood, scored_reads),
        "cold_read_assisted": assisted_reads,
        "cold_read_incomplete": len(reads) - scored_reads - assisted_reads,
        "cold_read_checks": {key: ratio(correct, scored_reads) for key, correct in read_checks.items()},
        "app_access": summarize_access(data["access_blocks"], starts, as_of) if "access_blocks" in data else None,
        "first_action": ratio(ready, len(trials)),
        "first_action_observed_not_ready": first_action_observed - ready,
        "first_action_unobserved": len(trials) - first_action_observed,
        "first_action_timing": summarize_first_action_timing([
            row for group in first_action_timing.values() for row in group
        ]),
        "first_action_timing_by_starter": {
            starter: summarize_first_action_timing(group) for starter, group in sorted(first_action_timing.items())
        },
        "seven_day_completion": ratio(finished, seven_day_eligible),
        "seven_day_reported_incomplete": reported_incomplete,
        "seven_day_unreported": seven_day_eligible - finished - reported_incomplete,
        "pending_seven_day_window": len(trials) - seven_day_eligible,
        "seven_day_by_channel": summarize_groups(channels),
        "seven_day_by_starter": summarize_groups(starters),
        "seven_day_by_shared_scene": summarize_groups(shared_scenes),
        "replanning": ratio(good_changes, changes),
        "replanning_unscored": unscored_changes,
        "unprompted_return": ratio(returned, return_eligible),
        "prompted_return": ratio(prompted_returns, return_eligible),
        "matched_comparison": summarize_comparisons(data.get("comparisons", [])),
        "thresholds": {
            "cold_read": "public_readme_commit" in data and scored_reads >= 12 and 12 * understood >= 10 * scored_reads,
            "first_action": candidate_commit is not None and len(trials) >= 100 and 100 * ready >= 80 * len(trials),
            "seven_day_completion": (candidate_commit is not None and seven_day_eligible >= 100
                                     and 100 * finished >= 60 * seven_day_eligible),
            "replanning": candidate_commit is not None and changes >= 30 and 100 * good_changes >= 85 * changes,
        },
    }


def summarize_cumulative(sources):
    cohorts = {}
    participant_channels = {}
    first_completions = {}
    trial_rows = 0
    for source in sources:
        report = summarize(source)
        cohort = source.get("cohort")
        if cohort is None or report["candidate_commit"] is None:
            raise ValueError("cumulative records need a cohort label and candidate commit")
        if cohort in cohorts:
            raise ValueError("supply only one authoritative snapshot for each cohort")
        cohorts[cohort] = {"as_of": report["as_of"], "candidate_commit": report["candidate_commit"]}
        for trial in source.get("trials", []):
            trial_rows += 1
            participant = trial["id"]
            channels = participant_channels.setdefault(participant, set())
            channel = trial.get("channel", "unspecified")
            if channel != "unspecified":
                channels.add(channel)
            if "finished_on" in trial:
                end = trial["finished_on"]
                first_completions[participant] = min(end, first_completions.get(participant, end))

    by_channel = {}
    attribution_conflicts = 0
    for participant, channels in participant_channels.items():
        attribution_conflicts += len(channels) > 1
        channel = next(iter(channels)) if len(channels) == 1 else "unspecified"
        counts = by_channel.setdefault(channel, {"unique_started": 0, "unique_completed": 0})
        counts["unique_started"] += 1
        counts["unique_completed"] += participant in first_completions

    by_month = {}
    for end in first_completions.values():
        month = end[:7]
        by_month[month] = by_month.get(month, 0) + 1

    return {
        "cohorts": dict(sorted(cohorts.items())),
        "unique_started": len(participant_channels),
        "unique_completed": len(first_completions),
        "first_completions_by_month": dict(sorted(by_month.items())),
        "duplicate_trial_rows": trial_rows - len(participant_channels),
        "attribution_conflicts": attribution_conflicts,
        "by_channel": dict(sorted(by_channel.items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, nargs="+")
    parser.add_argument("--cumulative", action="store_true", help="Count unique people across cohort snapshots")
    parser.add_argument("--public-markdown", action="store_true", help="Render one cohort as aggregate Markdown")
    args = parser.parse_args()
    if not args.cumulative and len(args.records) != 1:
        parser.error("supply one records file or use --cumulative")
    if args.cumulative and args.public_markdown:
        parser.error("--public-markdown requires one cohort, without --cumulative")
    try:
        sources = (json.loads(path.read_text(encoding="utf-8-sig")) for path in args.records)
        report = summarize_cumulative(sources) if args.cumulative else summarize(next(sources))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Invalid pilot data: {exc}\n")
    if args.public_markdown:
        print(render(report), end="")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
