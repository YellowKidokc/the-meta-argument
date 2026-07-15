from __future__ import annotations
from typing import Any
from .scoring import score_case

CHECKS = ("label_blind", "identity_swap", "same_radius", "counterfactual", "intent_separation", "unknown_preservation", "duplicate_penalty", "symmetry")

def compare_scores(a: dict[str, Any], b: dict[str, Any], tolerance: float = 0.01) -> tuple[bool, float | None]:
    sa, sb = score_case(a), score_case(b)
    if sa.get("status") != "SCORED" or sb.get("status") != "SCORED":
        return False, None
    va, vb = sa["direction"]["score"], sb["direction"]["score"]
    if va is None or vb is None: return False, None
    delta = abs(va - vb)
    return delta <= tolerance, round(delta, 6)

def run_anti_gaming(case: dict[str, Any]) -> dict[str, Any]:
    results = {}
    alternates = case.get("anti_gaming", {})
    for name in CHECKS:
        packet = alternates.get(name)
        if isinstance(packet, dict) and "case" in packet:
            passed, delta = compare_scores(case, packet["case"], float(packet.get("tolerance", 0.01)))
            results[name] = {"passed": passed, "delta": delta, "notes": packet.get("notes", [])}
        else:
            supplied = bool(packet is True)
            results[name] = {"passed": supplied, "delta": None, "notes": [] if supplied else ["No alternate packet supplied"]}
    return results
