import unittest

from scripts.estimate_usage import calculate, normalize_model


class EstimateUsageTests(unittest.TestCase):
    def test_sol_example_with_luna56_workers(self) -> None:
        result = calculate("sol", 3000, 1000, 24000, 8000, worker_model="luna5.6")

        self.assertEqual(result["main_model"], "gpt-5.6-sol")
        self.assertEqual(result["worker_model"], "gpt-5.6-luna")
        self.assertEqual(result["estimated_main_model_tokens_offloaded"], 32000)
        self.assertEqual(result["estimated_main_workload_reduction_percent"], 88.89)
        self.assertEqual(result["baseline_weighted_credits"], 7.2)
        self.assertEqual(result["actual_weighted_credits"], 1.16)
        self.assertEqual(result["estimated_weighted_saving_percent"], 83.89)
        self.assertIsNone(result["raw_total_token_saving"])

    def test_sol61_example_defaults_to_luna6_workers(self) -> None:
        result = calculate("gpt-6.1", 3000, 1000, 24000, 8000)

        self.assertEqual(result["main_model"], "gpt-6.1-sol")
        self.assertEqual(result["worker_model"], "gpt-6-luna")
        self.assertEqual(result["estimated_main_model_tokens_offloaded"], 32000)
        self.assertEqual(result["estimated_main_workload_reduction_percent"], 88.89)
        self.assertEqual(result["baseline_weighted_credits"], 3.6)
        self.assertEqual(result["actual_weighted_credits"], 0.56)
        self.assertEqual(result["estimated_weighted_saving_percent"], 84.44)

    def test_luna_coordinator_has_no_weighted_saving(self) -> None:
        result = calculate("luna", 100, 50, 500, 200)

        self.assertEqual(result["estimated_weighted_credits_saved"], 0.0)
        self.assertEqual(result["estimated_weighted_saving_percent"], 0.0)

    def test_negative_counts_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            calculate("sol", -1, 0, 0, 0)

    def test_aliases_are_normalized(self) -> None:
        self.assertEqual(normalize_model("ASTRA"), "gpt-6-astra")
        self.assertEqual(normalize_model("gpt-5.6"), "gpt-5.6-sol")
        self.assertEqual(normalize_model("luna"), "gpt-6-luna")
        self.assertEqual(normalize_model("luna5.6"), "gpt-5.6-luna")
        self.assertEqual(normalize_model("gpt-6.1"), "gpt-6.1-sol")
        self.assertEqual(normalize_model("sol6"), "gpt-6-sol")

    def test_unsupported_model_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported main model"):
            normalize_model("unknown")


if __name__ == "__main__":
    unittest.main()
