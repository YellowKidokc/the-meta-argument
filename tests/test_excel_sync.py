from meta_argument.excel_sync import _unknown_count, _weakest_public_factor


def test_unknown_count_counts_public_subquestion_unknowns():
    case = {
        "variables": {
            "G": {"answers": [{"answer": "UNKNOWN"}, {"answer": "YES"}]},
            "T": {"answers": [{"answer": "unknown"}]},
            "M": {"answers": [{"answer": "UNKNOWN"}]},
        }
    }
    assert _unknown_count(case) == 2


def test_weakest_public_factor_uses_public_five_not_full_veto():
    result = {
        "variables": {
            "G": {"raw_score": 1.0},
            "T": {"raw_score": -1.0},
            "K": {"raw_score": 0.0},
            "M": {"raw_score": -3.0},
        }
    }
    assert _weakest_public_factor(result) == "T"
