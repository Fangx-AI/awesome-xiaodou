import unittest

from pilot_blind import anonymize, restore
from pilot_measure import summarize, summarize_comparisons, summarize_cumulative


class PilotMeasurementTests(unittest.TestCase):
    def test_cumulative_counts_people_once_across_verified_cohorts(self):
        first = {"as_of": "2026-12-12", "cohort": "first", "candidate_commit": "a" * 40, "trials": [
            {"id": "P-0001", "channel": "github", "started_on": "2026-12-01", "finished_on": "2026-12-10"},
            {"id": "P-0002", "started_on": "2026-12-01"},
            {"id": "P-0003", "channel": "github", "started_on": "2026-12-01", "finished_on": "2026-12-03"},
        ]}
        second = {"as_of": "2026-12-20", "cohort": "second", "candidate_commit": "b" * 40, "trials": [
            {"id": "P-0001", "started_on": "2026-12-13", "finished_on": "2026-12-14"},
            {"id": "P-0002", "channel": "referral", "started_on": "2026-12-13", "finished_on": "2026-12-15"},
            {"id": "P-0003", "channel": "community", "started_on": "2026-12-13"},
            {"id": "P-0004", "channel": "community", "started_on": "2026-12-15"},
        ]}
        report = summarize_cumulative([first, second])
        self.assertEqual(report, summarize_cumulative([second, first]))
        self.assertEqual(report["unique_started"], 4)
        self.assertEqual(report["unique_completed"], 3)
        self.assertEqual(report["duplicate_trial_rows"], 3)
        self.assertEqual(report["attribution_conflicts"], 1)
        self.assertEqual(report["by_channel"], {
            "community": {"unique_started": 1, "unique_completed": 0},
            "github": {"unique_started": 1, "unique_completed": 1},
            "referral": {"unique_started": 1, "unique_completed": 1},
            "unspecified": {"unique_started": 1, "unique_completed": 1},
        })
        self.assertEqual(summarize(first)["seven_day_completion"]["numerator"], 1)

    def test_cumulative_dates_use_earliest_completion_and_recompute_corrections(self):
        december = {"cohort": "december", "candidate_commit": "a" * 40, "as_of": "2027-01-15", "trials": [
            {"id": "P-0001", "started_on": "2026-12-20", "finished_on": "2026-12-30"},
            {"id": "P-0002", "started_on": "2026-12-20", "finished_on": "2026-12-31"},
            {"id": "P-0003", "started_on": "2026-12-25"},
        ]}
        january = {"cohort": "january", "candidate_commit": "b" * 40, "as_of": "2027-01-20", "trials": [
            {"id": "P-0001", "started_on": "2027-01-01", "finished_on": "2027-01-02"},
            {"id": "P-0003", "started_on": "2027-01-01", "finished_on": "2027-01-04"},
        ]}
        initial = summarize_cumulative([january, december])
        self.assertEqual(initial["first_completions_by_month"], {"2026-12": 2, "2027-01": 1})
        self.assertEqual(initial["unique_completed"], 3)
        self.assertEqual(summarize(december)["seven_day_completion"]["numerator"], 0)

        corrected = {**december, "as_of": "2027-01-21", "trials": [
            {key: value for key, value in trial.items() if key != "finished_on"}
            for trial in december["trials"]
        ]}
        revised = summarize_cumulative([corrected, january])
        self.assertEqual(revised["first_completions_by_month"], {"2027-01": 2})
        self.assertEqual(revised["unique_started"], 3)
        self.assertEqual(revised["unique_completed"], 2)
        self.assertNotIn("P-0001", str(revised))

    def test_cumulative_rejects_duplicate_snapshots_and_unversioned_batches(self):
        source = {"as_of": "2026-12-12", "cohort": "first", "candidate_commit": "a" * 40}
        with self.assertRaisesRegex(ValueError, "one authoritative snapshot"):
            summarize_cumulative([source, {**source, "as_of": "2026-12-20"}])
        for field in ("cohort", "candidate_commit"):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "cohort label and candidate commit"):
                summarize_cumulative([{key: value for key, value in source.items() if key != field}])

    def test_blind_packet_round_trip_preserves_missing_arms(self):
        reviewer, key = anonymize([
            {"id": "P-0001", "order": "emperor", "task": "练会议开场",
             "regular": "请先写一句。", "emperor": "先读已经写好的一句。"},
            {"id": "P-0002", "order": "regular", "task": "练会议开场", "regular": "请先写一句。"},
        ])
        self.assertTrue(all(set(row) == {"code", "task", "excerpt", "scores"} for row in reviewer))
        for row in reviewer:
            row["scores"]["first_action"] = row["excerpt"].startswith("先读")
        rows = restore(key, reviewer)
        report = summarize_comparisons(rows)
        self.assertEqual(report["order_counts"], {"emperor": 1, "regular": 1})
        self.assertEqual(report["outcomes"]["first_action"]["emperor_only"], 1)
        self.assertEqual(report["outcomes"]["first_action"]["unscored_pairs"], 1)
        self.assertNotIn("emperor", rows[1])

    def test_blind_review_rejects_role_labels_and_unmatched_codes(self):
        for excerpt in ("皇上，请先读一句。", "礼部建议先读一句。", "顾砚安排先读一句。", "回奏：已读一句。"):
            with self.subTest(excerpt=excerpt), self.assertRaisesRegex(ValueError, "role or group"):
                anonymize([{"id": "P-0001", "order": "regular", "task": "练英语", "emperor": excerpt}])
        reviewer, key = anonymize([{"id": "P-0001", "order": "regular", "task": "练英语", "regular": "请先读一句。"}])
        for invalid in (reviewer * 2, [{"code": "unmatched"}]):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, "unknown or duplicate"):
                restore(key, invalid)
        reviewer[0]["scores"] = {"first_action": "yes"}
        with self.assertRaisesRegex(ValueError, "scores must be true or false"):
            restore(key, reviewer)

    def test_blind_restore_checks_material_without_requiring_every_score(self):
        review, key = anonymize([{"id": "P-0001", "order": "regular", "task": "练英语",
                                  "regular": "写一句。", "emperor": "读第一句。"}])
        first, second = review
        for row in ({**first, "task": "读纸书"}, {**first, "excerpt": second["excerpt"]},
                    {**first, "code": second["code"]}):
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, "does not match"):
                restore(key, [row])
        with self.assertRaisesRegex(ValueError, "original task and excerpt"):
            restore(key, [{"code": first["code"], "scores": {}}])
        self.assertEqual(restore(key, []), [{"id": "P-0001", "order": "regular"}])

    def test_legacy_blind_key_can_still_restore_scores(self):
        key = [{"id": "P-0001", "order": "regular", "regular": "legacy"}]
        review = [{"code": "legacy", "scores": {"first_action": False}}]
        restored = restore(key, review)
        self.assertEqual(restored[0]["regular"], {"first_action": False})

    def test_candidate_is_retained_and_must_identify_an_immutable_commit(self):
        commit = "91a7020c67480107c7e7f499d5993abb3cc92f11"
        report = summarize({"as_of": "2026-12-09", "candidate_commit": commit})
        self.assertEqual(report["candidate_commit"], commit)
        for invalid in (None, "main", "91a7020"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                summarize({"as_of": "2026-12-09", "candidate_commit": invalid})

    def test_cold_read_threshold_uses_observed_public_readme_version(self):
        report_input = {"as_of": "2026-12-09", "candidate_commit": "a" * 40, "cold_reads": [
            {"id": f"P-{index:04}", "found_start": index < 10, "assisted": False,
             "answers": dict.fromkeys(("identity", "where", "how", "confirmation"), True)}
            for index in range(12)
        ]}
        unversioned = summarize(report_input)
        self.assertEqual(unversioned["cold_read"]["numerator"], 10)
        self.assertFalse(unversioned["thresholds"]["cold_read"])
        versioned = summarize({**report_input, "public_readme_commit": "b" * 40})
        self.assertEqual(versioned["public_readme_commit"], "b" * 40)
        self.assertTrue(versioned["thresholds"]["cold_read"])
        with self.assertRaises(ValueError):
            summarize({**report_input, "public_readme_commit": "main"})

    def test_cold_read_requires_twelve_complete_unaided_observations(self):
        all_correct = dict.fromkeys(("identity", "where", "how", "confirmation"), True)
        reads = [{"id": f"P-{index:04}", "answers": all_correct, "found_start": True, "assisted": False}
                 for index in range(10)]
        reads.extend([
            {"id": "P-0010", "answers": all_correct, "found_start": True},
            {"id": "P-0011", "answers": all_correct, "found_start": True, "assisted": True},
        ])
        source = {"as_of": "2026-12-09", "public_readme_commit": "b" * 40, "cold_reads": reads}
        report = summarize(source)
        self.assertEqual(report["cold_read"], {"numerator": 10, "denominator": 10, "percent": 100.0})
        self.assertEqual(report["cold_read_incomplete"], 1)
        self.assertEqual(report["cold_read_assisted"], 1)
        self.assertFalse(report["thresholds"]["cold_read"])

        reads.extend([{"id": "P-0098", "answers": all_correct, "found_start": True},
                      {"id": "P-0099", "answers": all_correct, "found_start": True}])
        self.assertFalse(summarize(source)["thresholds"]["cold_read"])

        reads.extend([
            {"id": "P-0012", "answers": {**all_correct, "confirmation": False}, "found_start": True, "assisted": False},
            {"id": "P-0013", "answers": all_correct, "found_start": False, "assisted": False},
        ])
        report = summarize(source)
        self.assertEqual(report["cold_read"]["numerator"], 10)
        self.assertEqual(report["cold_read"]["denominator"], 12)
        self.assertEqual(report["cold_read_checks"]["confirmation"]["numerator"], 11)
        self.assertEqual(report["cold_read_checks"]["found_start"]["numerator"], 11)
        self.assertTrue(report["thresholds"]["cold_read"])

    def test_trial_gates_require_a_candidate_version_and_keep_unobserved_users(self):
        trials = [
            {"id": f"P-{i:04}", "started_on": "2026-12-01"}
            for i in range(100)
        ]
        for i, trial in enumerate(trials):
            if i < 80:
                trial["first_action"] = True
            elif i < 85:
                trial["first_action"] = False
            if i < 60:
                trial["finished_on"] = "2026-12-08"
            if i < 30:
                trial["change"] = {"preserved": True, "affected_only": True, "actionable": i < 26}
        data = {"as_of": "2026-12-08", "trials": trials}
        gates = ("first_action", "seven_day_completion", "replanning")

        unversioned = summarize(data)
        self.assertEqual(unversioned["first_action"], {"numerator": 80, "denominator": 100, "percent": 80.0})
        self.assertEqual(unversioned["first_action_observed_not_ready"], 5)
        self.assertEqual(unversioned["first_action_unobserved"], 15)
        self.assertEqual(unversioned["seven_day_completion"]["numerator"], 60)
        self.assertEqual(unversioned["replanning"]["numerator"], 26)
        self.assertTrue(all(not unversioned["thresholds"][gate] for gate in gates))

        versioned = summarize({**data, "candidate_commit": "c" * 40})
        self.assertTrue(all(versioned["thresholds"][gate] for gate in gates))

    def test_explicit_incompletion_and_missing_reports_keep_the_same_denominator(self):
        report = summarize({"as_of": "2026-12-10", "trials": [
            {"id": "P-0001", "channel": "github", "started_on": "2026-12-01", "finished_on": "2026-12-08"},
            {"id": "P-0002", "channel": "github", "started_on": "2026-12-01", "no_completion_reported_on": "2026-12-08"},
            {"id": "P-0003", "started_on": "2026-12-01", "finished_on": "2026-12-09"},
            {"id": "P-0004", "started_on": "2026-12-01"},
            {"id": "P-0005", "started_on": "2026-12-05"},
        ]})
        self.assertEqual(report["seven_day_completion"], {"numerator": 1, "denominator": 4, "percent": 25.0})
        self.assertEqual(report["seven_day_reported_incomplete"], 2)
        self.assertEqual(report["seven_day_unreported"], 1)
        self.assertEqual(report["pending_seven_day_window"], 1)
        self.assertEqual(report["seven_day_by_channel"], {
            "github": {"started": 2, "completion": {"numerator": 1, "denominator": 2, "percent": 50.0}},
            "unspecified": {"started": 3, "completion": {"numerator": 0, "denominator": 2, "percent": 0.0}},
        })

    def test_explicit_incompletion_requires_the_completed_window_and_consistent_result(self):
        for evidence in ({"no_completion_reported_on": "2026-12-07"},
                         {"no_completion_reported_on": "2026-12-08", "finished_on": "2026-12-08"}):
            with self.subTest(evidence=evidence), self.assertRaises(ValueError):
                summarize({"as_of": "2026-12-10", "trials": [
                    {"id": "P-0001", "started_on": "2026-12-01", **evidence},
                ]})

    def test_starter_groups_keep_pending_windows_and_unknown_files_distinct(self):
        entries = [
            {"id": "P-0001", "started_on": "2026-12-01", "finished_on": "2026-12-03",
             "starter": "life-plans/health.txt"},
            {"id": "P-0002", "started_on": "2026-12-06", "starter": "life-plans/health.txt"},
            {"id": "P-0003", "started_on": "2026-12-01", "starter": "xiaodou-start.txt"},
            {"id": "P-0004", "started_on": "2026-12-01"},
        ]
        report = summarize({"as_of": "2026-12-10", "trials": entries})
        self.assertEqual(report["seven_day_by_starter"], {
            "life-plans/health.txt": {"started": 2, "completion": {"numerator": 1, "denominator": 1, "percent": 100.0}},
            "unspecified": {"started": 1, "completion": {"numerator": 0, "denominator": 1, "percent": 0.0}},
            "xiaodou-start.txt": {"started": 1, "completion": {"numerator": 0, "denominator": 1, "percent": 0.0}},
        })
        for invalid in (None, "xiaodou-pilot-start.txt", "life-plans/typo.txt"):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, "supported file"):
                summarize({"as_of": "2026-12-10", "trials": [{**entries[0], "starter": invalid}]})

    def test_shared_scene_comes_from_reported_exposure_not_the_starter(self):
        common = {"started_on": "2026-12-01", "starter": "life-plans/health.txt", "channel": "referral"}
        entries = [
            {**common, "id": "P-0001", "shared_scene": "fitness", "finished_on": "2026-12-03"},
            {**common, "id": "P-0002", "shared_scene": "weight"},
            {**common, "id": "P-0003", "finished_on": "2026-12-05"},
        ]
        report = summarize({"as_of": "2026-12-10", "trials": entries})
        self.assertEqual(report["seven_day_by_shared_scene"], {
            "fitness": {"started": 1, "completion": {"numerator": 1, "denominator": 1, "percent": 100.0}},
            "unspecified": {"started": 1, "completion": {"numerator": 1, "denominator": 1, "percent": 100.0}},
            "weight": {"started": 1, "completion": {"numerator": 0, "denominator": 1, "percent": 0.0}},
        })
        self.assertEqual(report["seven_day_by_starter"]["life-plans/health.txt"]["started"], 3)
        self.assertEqual(report["seven_day_by_channel"]["referral"]["completion"]["numerator"], 2)
        with self.assertRaisesRegex(ValueError, "one of the five"):
            summarize({"as_of": "2026-12-10", "trials": [{**entries[0], "shared_scene": "health"}]})

    def test_paired_report_exposes_opposing_results_by_first_mode(self):
        records = [
            {"id": "P-0001", "order": "regular",
             "regular": {"first_action": False, "follow_up_questions": 3},
             "emperor": {"first_action": True, "follow_up_questions": 1}},
            {"id": "P-0002", "order": "emperor",
             "regular": {"first_action": True, "follow_up_questions": 1},
             "emperor": {"first_action": False, "follow_up_questions": 3}},
            {"id": "P-0003", "order": "regular", "regular": {"first_action": True}},
        ]
        report = summarize_comparisons(records)
        self.assertEqual(report["outcomes"]["first_action"]["emperor_minus_regular_pp"], 0)
        self.assertEqual(report["follow_up_questions"]["emperor_minus_regular_mean"], 0)
        regular_first = report["by_order"]["regular"]
        emperor_first = report["by_order"]["emperor"]
        self.assertEqual(regular_first["enrolled"], 2)
        self.assertEqual(regular_first["outcomes"]["first_action"]["unscored_pairs"], 1)
        self.assertEqual(regular_first["outcomes"]["first_action"]["emperor_minus_regular_pp"], 100)
        self.assertEqual(regular_first["follow_up_questions"]["emperor_minus_regular_mean"], -2)
        self.assertEqual(emperor_first["enrolled"], 1)
        self.assertEqual(emperor_first["outcomes"]["first_action"]["emperor_minus_regular_pp"], -100)
        self.assertEqual(emperor_first["follow_up_questions"]["emperor_minus_regular_mean"], 2)

    def test_zero_questions_and_a_failed_first_action_are_observed(self):
        report = summarize_comparisons([
            {"id": "P-0001", "order": "regular",
             "regular": {"first_action": False, "follow_up_questions": 0},
             "emperor": {"first_action": True, "follow_up_questions": 2}},
            {"id": "P-0002", "order": "emperor",
             "regular": {"first_action": True, "follow_up_questions": 2},
             "emperor": {"first_action": True, "follow_up_questions": 1}},
            {"id": "P-0003", "order": "regular",
             "regular": {"first_action": True},
             "emperor": {"first_action": True, "follow_up_questions": 0}},
            {"id": "P-0004", "order": "emperor",
             "regular": {"follow_up_questions": 0},
             "emperor": {"first_action": True, "follow_up_questions": 0}},
        ])
        self.assertEqual(report["outcomes"]["first_action"]["pairs"], 3)
        self.assertEqual(report["outcomes"]["first_action"]["emperor_only"], 1)
        self.assertEqual(report["follow_up_questions"], {
            "pairs": 2, "unscored_pairs": 2, "regular_total": 2, "emperor_total": 3,
            "emperor_fewer": 1, "regular_fewer": 1, "equal": 0, "emperor_minus_regular_mean": 0.5,
        })

    def test_replanning_keeps_observed_changes_with_missing_evidence(self):
        passed = {"preserved": True, "affected_only": True, "actionable": True}
        scores = [passed] * 26 + [{"preserved": False}, {}, {"actionable": True}] + [passed]
        trials = [{"id": f"P-{index:04}", "started_on": "2026-12-01", "change": change}
                  for index, change in enumerate(scores)]
        trials.append({"id": "P-0100", "started_on": "2026-12-01"})
        report = summarize({"as_of": "2026-12-10", "candidate_commit": "c" * 40, "trials": trials})
        self.assertEqual(report["replanning"], {"numerator": 27, "denominator": 30, "percent": 90.0})
        self.assertEqual(report["replanning_unscored"], 2)
        self.assertTrue(report["thresholds"]["replanning"])

        trials.extend({"id": f"P-{index:04}", "started_on": "2026-12-01", "change": {}}
                      for index in (101, 102))
        report = summarize({"as_of": "2026-12-10", "candidate_commit": "c" * 40, "trials": trials})
        self.assertEqual(report["replanning"], {"numerator": 27, "denominator": 32, "percent": 84.4})
        self.assertFalse(report["thresholds"]["replanning"])

    def test_counts_are_nonnegative_integers(self):
        for invalid in (-1, True, 1.5, None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                summarize_comparisons([{"id": "P-0001", "order": "regular",
                                        "regular": {"follow_up_questions": invalid}}])

    def test_returns_share_the_same_completed_window_denominator(self):
        report = summarize({"as_of": "2026-12-09", "trials": [
            {"id": "P-0001", "started_on": "2026-12-01",
             "return": {"day": "2026-12-07", "prompted": False}},
            {"id": "P-0002", "started_on": "2026-12-01",
             "return": {"day": "2026-12-09", "prompted": True}},
            {"id": "P-0003", "started_on": "2026-12-01"},
            {"id": "P-0004", "started_on": "2026-12-02",
             "return": {"day": "2026-12-09", "prompted": True}},
        ]})
        for key in ("unprompted_return", "prompted_return"):
            self.assertEqual(report[key], {"numerator": 1, "denominator": 3, "percent": 33.3})


if __name__ == "__main__":
    unittest.main()
