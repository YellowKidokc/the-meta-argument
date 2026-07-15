from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Iterable

ANSWER_VALUES = {
    "yes": 1.0,
    "mixed": 0.0,
    "no": -1.0,
    "unknown": None,
}

PUBLIC_VARIABLES = ("G", "T", "K", "F", "R")
FULL_VARIABLES = ("G", "M", "E", "S", "T", "K", "R", "Q", "F")
REFUSAL_STATES = {
    "INSUFFICIENTLY_DEFINED",
    "INSUFFICIENT_EVIDENCE",
    "ONTOLOGICAL_DEPENDENCY",
    "OUTCOME_NOT_YET_OBSERVABLE",
    "CAUSATION_UNRESOLVED",
}


@dataclass(frozen=True)
class VariableResult:
    score: float | None
    confidence: float
    coverage: float
    known_answers: int
    total_answers: int


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _answer_value(answer: dict[str, Any]) -> float | None:
    label = str(answer.get("answer", "unknown")).strip().lower()
    if label not in ANSWER_VALUES:
        raise ValueError(f"Unsupported answer label: {label}")
    return ANSWER_VALUES[label]


def score_variable(variable: dict[str, Any]) -> VariableResult:
    answers = variable.get("answers", [])
    if not isinstance(answers, list) or not answers:
        return VariableResult(None, 0.0, 0.0, 0, 0)

    known: list[float] = []
    evidence_weights: list[float] = []
    for answer in answers:
        value = _answer_value(answer)
        if value is None:
            continue
        weight = _clamp(float(answer.get("evidence_quality", 0.5)))
        known.append(value)
        evidence_weights.append(weight)

    total = len(answers)
    if not known:
        return VariableResult(None, 0.0, 0.0, 0, total)

    coverage = len(known) / total
    agreement = 1.0 - (max(known) - min(known)) / 2.0 if len(known) > 1 else 1.0
    evidence_quality = mean(evidence_weights) if evidence_weights else 0.0
    confidence = _clamp(evidence_quality * coverage * agreement)
    score = round(mean(known) * 3.0, 2)
    return VariableResult(score, round(confidence, 3), round(coverage, 3), len(known), total)


def _weighted_mean(values: Iterable[tuple[float, float]]) -> float | None:
    items = [(value, weight) for value, weight in values if weight > 0]
    if not items:
        return None
    numerator = sum(value * weight for value, weight in items)
    denominator = sum(weight for _, weight in items)
    return round(numerator / denominator, 3)


def _direction_label(score: float | None) -> str:
    if score is None:
        return "UNRESOLVED"
    if score >= 1.5:
        return "STRONGLY_CONSTRUCTIVE"
    if score >= 0.5:
        return "CONSTRUCTIVE"
    if score > -0.5:
        return "MIXED"
    if score > -1.5:
        return "DESTRUCTIVE"
    return "STRONGLY_DESTRUCTIVE"


def validate_case(case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("case_id", "actor", "action", "target", "mechanism", "period", "variables")
    for field in required:
        if field not in case or case[field] in (None, "", [], {}):
            errors.append(f"Missing required field: {field}")

    variables = case.get("variables", {})
    if isinstance(variables, dict):
        unknown = set(variables) - set(FULL_VARIABLES)
        if unknown:
            errors.append(f"Unknown variables: {sorted(unknown)}")
    else:
        errors.append("variables must be an object")

    refusal_states = set(case.get("refusal_states", []))
    invalid_refusals = refusal_states - REFUSAL_STATES
    if invalid_refusals:
        errors.append(f"Unknown refusal states: {sorted(invalid_refusals)}")
    return errors


def score_case(case: dict[str, Any]) -> dict[str, Any]:
    errors = validate_case(case)
    if errors:
        return {"status": "INVALID", "errors": errors}

    refusal_states = case.get("refusal_states", [])
    if refusal_states:
        return {
            "status": "REFUSED",
            "case_id": case["case_id"],
            "refusal_states": refusal_states,
        }

    variable_results: dict[str, dict[str, Any]] = {}
    for name in FULL_VARIABLES:
        result = score_variable(case.get("variables", {}).get(name, {}))
        variable_results[name] = {
            "score": result.score,
            "confidence": result.confidence,
            "coverage": result.coverage,
            "known_answers": result.known_answers,
            "total_answers": result.total_answers,
        }

    known = [
        (data["score"], data["confidence"])
        for data in variable_results.values()
        if data["score"] is not None
    ]
    direction_score = _weighted_mean(known)

    public_known = [
        (variable_results[name]["score"], variable_results[name]["confidence"])
        for name in PUBLIC_VARIABLES
        if variable_results[name]["score"] is not None
    ]
    public_score = _weighted_mean(public_known)

    known_scores = {
        name: data["score"]
        for name, data in variable_results.items()
        if data["score"] is not None
    }
    veto_variable = min(known_scores, key=known_scores.get) if known_scores else None

    reach = _clamp(float(case.get("structural", {}).get("physical_reach", 0.0)), 0.0, 3.0)
    amplification = _clamp(float(case.get("structural", {}).get("amplification", 0.0)), 0.0, 3.0)
    persistence = _clamp(float(case.get("structural", {}).get("persistence", 0.0)), 0.0, 3.0)
    significance = round((reach * amplification * persistence) / 9.0, 3)

    wrapper = case.get("wrapper", {})
    w_value = float(wrapper.get("W", 0.0))
    if w_value not in (-1.0, 0.0, 1.0):
        raise ValueError("wrapper.W must be -1, 0, or 1")

    overall_confidence = round(mean([weight for _, weight in known]), 3) if known else 0.0

    return {
        "status": "SCORED",
        "case_id": case["case_id"],
        "direction": {
            "score": direction_score,
            "label": _direction_label(direction_score),
            "public_five_score": public_score,
        },
        "structural_significance": significance,
        "veto": {
            "variable": veto_variable,
            "score": known_scores.get(veto_variable) if veto_variable else None,
        },
        "wrapper": {
            "W": w_value,
            "confidence": _clamp(float(wrapper.get("confidence", 0.0))),
            "note": wrapper.get("note", ""),
        },
        "confidence": overall_confidence,
        "variables": variable_results,
        "warnings": case.get("warnings", []),
    }
