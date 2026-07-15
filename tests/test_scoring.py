import copy
import unittest

from meta_argument.scoring import score_case, score_variable


class VariableScoringTests(unittest.TestCase):
    def test_unknown_is_not_zero(self):
        result = score_variable({"answers": [
            {"question_id": "x", "answer": "unknown", "evidence_quality": 1.0},
            {"question_id": "y", "answer": "yes", "evidence_quality": 1.0},
        ]})
        self.assertEqual(result.score, 3.0)
        self.assertEqual(result.coverage, 0.5)

    def test_mixed_is_zero(self):
        result = score_variable({"answers": [
            {"question_id": "x", "answer": "mixed", "evidence_quality": 1.0}
        ]})
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.coverage, 1.0)


class CaseScoringTests(unittest.TestCase):
    def base_case(self):
        return {
            "case_id": "TEST-1",
            "actor": "Actor A",
            "action": "Performed action X",
            "target": "Target B",
            "mechanism": "Mechanism C",
            "period": "2000",
            "variables": {
                "G": {"answers": [{"question_id": "G1", "answer": "yes", "evidence_quality": 1.0}]},
                "T": {"answers": [{"question_id": "T1", "answer": "no", "evidence_quality": 1.0}]},
                "K": {"answers": [{"question_id": "K1", "answer": "mixed", "evidence_quality": 1.0}]},
                "F": {"answers": [{"question_id": "F1", "answer": "yes", "evidence_quality": 1.0}]},
                "R": {"answers": [{"question_id": "R1", "answer": "yes", "evidence_quality": 1.0}]}
            },
            "wrapper": {"W": 0, "confidence": 0.5},
            "structural": {"physical_reach": 2, "amplification": 2, "persistence": 2}
        }

    def test_veto_exposes_weakest_factor(self):
        result = score_case(self.base_case())
        self.assertEqual(result["status"], "SCORED")
        self.assertEqual(result["veto"]["variable"], "T")
        self.assertEqual(result["veto"]["score"], -3.0)

    def test_label_swap_does_not_change_score(self):
        first = self.base_case()
        second = copy.deepcopy(first)
        second["actor"] = "Opposing Party"
        second["target"] = "Different Named Group"
        self.assertEqual(
            score_case(first)["direction"],
            score_case(second)["direction"],
        )

    def test_refusal_state_prevents_false_precision(self):
        case = self.base_case()
        case["refusal_states"] = ["CAUSATION_UNRESOLVED"]
        result = score_case(case)
        self.assertEqual(result["status"], "REFUSED")


if __name__ == "__main__":
    unittest.main()
