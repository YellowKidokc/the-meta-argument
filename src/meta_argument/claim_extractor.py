from __future__ import annotations

from typing import Any

CLAIM_TYPE_TO_VARIABLES = {
    "cost": ("G",),
    "autonomy": ("G", "F"),
    "causation": ("T",),
    "proportionality": ("T",),
    "knowledge": ("K",),
    "transparency": ("K",),
    "voluntary_relation": ("F",),
    "repair": ("R",),
    "recurrence": ("R",),
}


def route_claim(claim: dict[str, Any] | str) -> dict[str, Any]:
    text = claim if isinstance(claim, str) else str(claim.get("claim") or claim.get("text") or "")
    lowered = text.lower()
    matches = []
    for claim_type, variables in CLAIM_TYPE_TO_VARIABLES.items():
        tokens = claim_type.replace("_", " ").split()
        if any(token in lowered for token in tokens):
            matches.append({"claim_type": claim_type, "variables": list(variables)})
    return {"claim": text, "routes": matches or [{"claim_type": "unclassified", "variables": []}]}
