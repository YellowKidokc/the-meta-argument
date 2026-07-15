from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class Answer(str, Enum):
    YES = "YES"
    NO = "NO"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"

ANSWER_VALUES = {Answer.YES: 1.0, Answer.NO: -1.0, Answer.MIXED: 0.0, Answer.UNKNOWN: None, Answer.NOT_APPLICABLE: None}
PUBLIC_VARIABLES = ("G", "T", "K", "F", "R")
FULL_VARIABLES = ("G", "M", "E", "S", "T", "K", "R", "Q", "F")
REFUSAL_STATES = {"INSUFFICIENTLY_DEFINED", "INSUFFICIENT_EVIDENCE", "ONTOLOGICAL_DEPENDENCY", "OUTCOME_NOT_YET_OBSERVABLE", "CAUSATION_UNRESOLVED"}

@dataclass(frozen=True)
class Question:
    id: str
    variable: str
    text: str
    weight: float = 1.0

@dataclass(frozen=True)
class VariableScore:
    raw_score: float | None
    rounded_score: int | None
    coverage: float
    confidence: float
    unknown_fraction: float
    veto_candidate: bool
    answered_weight: float
    total_applicable_weight: float

@dataclass
class AntiGamingResult:
    name: str
    passed: bool
    notes: list[str] = field(default_factory=list)
    delta: float | None = None
