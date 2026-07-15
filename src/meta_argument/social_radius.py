from __future__ import annotations

from typing import Any


def social_radius_score(inputs: dict[str, Any]) -> dict[str, Any]:
    keys = ("direct_parties", "families", "institutions", "community", "future_generations")
    values = {key: max(0.0, min(3.0, float(inputs.get(key, 0)))) for key in keys}
    score = sum(values.values()) / (3 * len(keys))
    return {"raw": round(score, 3), "inputs": values}


def attach_social_radius(case: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    updated = dict(case)
    structural = dict(updated.get("structural_significance", {}))
    structural["social_radius"] = social_radius_score(inputs)["raw"]
    updated["structural_significance"] = structural
    updated["social_radius"] = social_radius_score(inputs)
    return updated
