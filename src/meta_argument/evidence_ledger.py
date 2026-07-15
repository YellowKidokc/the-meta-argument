from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(frozen=True)
class EvidenceItem:
    source_id: str
    claim: str
    source_type: str = "unknown"
    directness: float = 0.5
    independence_group: str | None = None
    supports: list[str] = field(default_factory=list)
    contradicts: list[str] = field(default_factory=list)
    citation: str | None = None


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def normalize_evidence(items: Iterable[dict[str, Any] | EvidenceItem]) -> list[EvidenceItem]:
    normalized: list[EvidenceItem] = []
    for item in items:
        if isinstance(item, EvidenceItem):
            normalized.append(item)
            continue
        normalized.append(EvidenceItem(
            source_id=str(item.get("source_id") or item.get("id") or f"source-{len(normalized) + 1}"),
            claim=str(item.get("claim") or item.get("text") or ""),
            source_type=str(item.get("source_type") or item.get("type") or "unknown"),
            directness=_clamp(float(item.get("directness", item.get("evidence_directness", 0.5)))),
            independence_group=item.get("independence_group"),
            supports=list(item.get("supports", [])),
            contradicts=list(item.get("contradicts", [])),
            citation=item.get("citation") or item.get("url"),
        ))
    return normalized


def ledger_confidence_inputs(items: Iterable[dict[str, Any] | EvidenceItem]) -> dict[str, float]:
    evidence = normalize_evidence(items)
    if not evidence:
        return {}
    source_quality_by_type = {"primary": 1.0, "official": 0.9, "scholarship": 0.85, "reporting": 0.7, "advocate": 0.45, "critic": 0.45, "unknown": 0.5}
    quality = sum(source_quality_by_type.get(item.source_type.lower(), 0.5) for item in evidence) / len(evidence)
    directness = sum(item.directness for item in evidence) / len(evidence)
    groups = {item.independence_group or item.source_id for item in evidence}
    independence = min(1.0, len(groups) / max(1, len(evidence)))
    contradiction_count = sum(1 for item in evidence if item.contradicts)
    causal_certainty = 1.0 - min(0.5, contradiction_count / max(1, len(evidence)))
    return {
        "source_quality": round(_clamp(quality), 3),
        "source_independence": round(_clamp(independence), 3),
        "evidence_directness": round(_clamp(directness), 3),
        "causal_certainty": round(_clamp(causal_certainty), 3),
    }


def attach_evidence(case: dict[str, Any], evidence_items: Iterable[dict[str, Any] | EvidenceItem]) -> dict[str, Any]:
    updated = dict(case)
    evidence = normalize_evidence(evidence_items)
    updated["evidence_ledger"] = [item.__dict__ for item in evidence]
    confidence = dict(updated.get("confidence_inputs", {}))
    confidence.update(ledger_confidence_inputs(evidence))
    updated["confidence_inputs"] = confidence
    return updated
