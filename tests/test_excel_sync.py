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


class _Cell:
    def __init__(self, value):
        self.value = value


class _SeedSheet:
    def __getitem__(self, cell):
        if cell == "B12":
            return _Cell("Modern conflict escalated after a cross-border strike")
        return _Cell(None)


def test_seed_statement_starts_draft_case_when_event_rows_are_unlabelled():
    from meta_argument.excel_sync import _read_event_fields

    fields = _read_event_fields(_SeedSheet())

    assert fields["seed_statement"] == "Modern conflict escalated after a cross-border strike"
    assert fields["action"] == "Modern conflict escalated after a cross-border strike"
    assert fields["case_id"].startswith("excel-seed-modern-conflict")
