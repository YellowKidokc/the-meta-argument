from __future__ import annotations

from statistics import mean
from typing import Any, Iterable

from .models import ANSWER_VALUES, FULL_VARIABLES, PUBLIC_VARIABLES, REFUSAL_STATES, Answer, VariableScore
from .rubric import load_questions


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))

def normalize_answer(label: str) -> Answer:
    token = str(label).strip().upper()
    aliases = {"YES":"YES", "Y":"YES", "NO":"NO", "N":"NO", "MIXED":"MIXED", "UNKNOWN":"UNKNOWN", "NOT_APPLICABLE":"NOT_APPLICABLE", "NA":"NOT_APPLICABLE", "N/A":"NOT_APPLICABLE"}
    if token not in aliases:
        raise ValueError(f"Unsupported answer label: {label}")
    return Answer(aliases[token])

def _answer_value(answer: dict[str, Any]) -> float | None:
    return ANSWER_VALUES[normalize_answer(answer.get("answer", "UNKNOWN"))]

def _answer_weight(answer: dict[str, Any], question_weights: dict[str, float]) -> float:
    return max(0.0, float(answer.get("weight", question_weights.get(str(answer.get("question_id")), 1.0))))

def score_variable(variable: dict[str, Any], question_weights: dict[str, float] | None = None) -> VariableScore:
    question_weights = question_weights or {}
    answers = variable.get("answers", []) if isinstance(variable, dict) else []
    applicable_weight = 0.0
    answered_weight = 0.0
    weighted_sum = 0.0
    qualities: list[float] = []
    numeric_values: list[float] = []
    for answer in answers:
        label = normalize_answer(answer.get("answer", "UNKNOWN"))
        weight = _answer_weight(answer, question_weights)
        if label is Answer.NOT_APPLICABLE:
            continue
        applicable_weight += weight
        value = ANSWER_VALUES[label]
        if value is None:
            continue
        answered_weight += weight
        weighted_sum += value * weight
        numeric_values.append(value)
        qualities.append(_clamp(float(answer.get("evidence_quality", answer.get("confidence", 0.5)))))
    if applicable_weight <= 0:
        return VariableScore(None, None, 0.0, 0.0, 0.0, False, 0.0, 0.0)
    coverage = answered_weight / applicable_weight
    unknown_fraction = 1.0 - coverage
    if answered_weight <= 0:
        return VariableScore(None, None, round(coverage,3), 0.0, round(unknown_fraction,3), False, 0.0, applicable_weight)
    raw = 3.0 * weighted_sum / answered_weight
    agreement = 1.0 - ((max(numeric_values) - min(numeric_values)) / 2.0) if len(numeric_values) > 1 else 1.0
    confidence = _clamp((mean(qualities) if qualities else 0.5) * coverage * agreement)
    return VariableScore(raw, int(round(raw)), round(coverage,3), round(confidence,3), round(unknown_fraction,3), raw <= -2.0, answered_weight, applicable_weight)

def validate_case(case: dict[str, Any]) -> list[str]:
    required = ("case_id","actor","action","target","affected_parties","claimed_objective","mechanism","cost_bearers","beneficiaries","start_date","end_date","measured_outcomes","counterfactual","variables")
    errors=[f"Missing required field: {f}" for f in required if f not in case or case[f] in (None,"",[],{})]
    if not isinstance(case.get("variables", {}), dict): errors.append("variables must be an object")
    elif set(case.get("variables",{}))-set(FULL_VARIABLES): errors.append(f"Unknown variables: {sorted(set(case['variables'])-set(FULL_VARIABLES))}")
    invalid=set(case.get("refusal_states",[]))-REFUSAL_STATES
    if invalid: errors.append(f"Unknown refusal states: {sorted(invalid)}")
    return errors

def _weighted_mean(values: Iterable[tuple[float, float]]) -> float | None:
    items=[(v,w) for v,w in values if w>0]
    if not items: return None
    return round(sum(v*w for v,w in items)/sum(w for _,w in items),3)

def _direction_label(score: float | None) -> str:
    if score is None: return "UNRESOLVED"
    if score >= 1.5: return "STRONGLY_CONSTRUCTIVE"
    if score >= 0.5: return "CONSTRUCTIVE"
    if score > -0.5: return "MIXED"
    if score > -1.5: return "DESTRUCTIVE"
    return "STRONGLY_DESTRUCTIVE"

def _significance(structural: dict[str, Any]) -> dict[str, Any]:
    keys=["population_reach","geographic_reach","resource_scale","institutional_amplification","persistence","reversibility","physical_consequences"]
    vals={k:_clamp(float(structural.get(k,0)),0,3) for k in keys}
    # reversibility is inverse significance: low reversibility increases significance
    adjusted=[vals[k] for k in keys if k!="reversibility"] + [3-vals["reversibility"]]
    raw=sum(adjusted)/(3*len(adjusted)) if adjusted else 0
    return {"raw": round(raw,3), "inputs": vals}

def score_case(case: dict[str, Any]) -> dict[str, Any]:
    errors=validate_case(case)
    if errors: return {"status":"INVALID","errors":errors}
    if case.get("refusal_states"):
        return {"status":"REFUSED","case_id":case["case_id"],"refusal_states":case["refusal_states"]}
    qweights={qid:q.weight for qid,q in load_questions().items()}
    variables={}
    for name in FULL_VARIABLES:
        r=score_variable(case.get("variables",{}).get(name,{}), qweights)
        variables[name]={"raw_score": None if r.raw_score is None else round(r.raw_score,6),"rounded_score":r.rounded_score,"coverage":r.coverage,"confidence":r.confidence,"unknown_fraction":r.unknown_fraction,"veto_candidate":r.veto_candidate,"answered_weight":r.answered_weight,"total_applicable_weight":r.total_applicable_weight}
    known=[(d["raw_score"],d["confidence"]) for d in variables.values() if d["raw_score"] is not None]
    public=[(variables[n]["raw_score"],variables[n]["confidence"]) for n in PUBLIC_VARIABLES if variables[n]["raw_score"] is not None]
    known_scores={n:d["raw_score"] for n,d in variables.items() if d["raw_score"] is not None}
    veto=min(known_scores, key=known_scores.get) if known_scores else None
    conf_inputs=case.get("confidence_inputs",{})
    confidence=round(mean([_clamp(float(conf_inputs.get(k, mean([w for _,w in known]) if known else 0))) for k in ["source_quality","source_independence","evidence_directness","question_coverage","inter_rater_agreement","causal_certainty"]]),3) if known else 0.0
    dscore=_weighted_mean(known)
    return {"status":"SCORED","case_id":case["case_id"],"canonical_unit":f"{case['actor']} + {case['action']} + {case['target']} + {case['mechanism']} + {case['measured_outcomes']} + {case['start_date']}..{case['end_date']}","direction":{"score":dscore,"label":_direction_label(dscore),"public_five_score":_weighted_mean(public)},"structural_significance":_significance(case.get("structural_significance",{})),"veto":{"variable":veto,"score":known_scores.get(veto) if veto else None},"confidence":confidence,"variables":variables,"ontological_dependencies":case.get("ontological_dependencies",[]),"warnings":case.get("warnings",[])}
