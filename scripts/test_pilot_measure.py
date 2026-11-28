import unittest

from pilot_measure import summarize, summarize_comparisons


class PilotMeasurementTests(unittest.TestCase):
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
