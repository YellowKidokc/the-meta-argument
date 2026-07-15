from __future__ import annotations

from statistics import mean
from typing import Any, Iterable

from .models import FULL_VARIABLES
from .scoring import score_case


def convergence_summary(cases: Iterable[dict[str, Any]]) -> dict[str, Any]:
    scored = [score_case(case) for case in cases]
    valid = [result for result in scored if result.get("status") == "SCORED"]
    if not valid:
        return {"status": "NO_SCORED_CASES", "rater_count": 0, "results": scored}
    variable_ranges: dict[str, float | None] = {}
    variable_means: dict[str, float | None] = {}
    for variable in FULL_VARIABLES:
        values = [result["variables"][variable]["raw_score"] for result in valid if result["variables"][variable]["raw_score"] is not None]
        variable_ranges[variable] = round(max(values) - min(values), 3) if values else None
        variable_means[variable] = round(mean(values), 3) if values else None
    direction_scores = [result["direction"]["score"] for result in valid if result.get("direction", {}).get("score") is not None]
    return {
        "status": "CONVERGED" if all(value is None or value <= 1.0 for value in variable_ranges.values()) else "DIVERGED",
        "rater_count": len(valid),
        "direction_mean": round(mean(direction_scores), 3) if direction_scores else None,
        "variable_means": variable_means,
        "variable_ranges": variable_ranges,
        "results": scored,
    }
