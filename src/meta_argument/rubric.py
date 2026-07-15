from __future__ import annotations
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from .models import Question

def _minimal_yaml(text: str) -> dict[str, Any]:
    # Purpose-built fallback for config/questions.yaml when PyYAML is unavailable.
    import re
    variables: dict[str, list[dict[str, Any]]] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^  ([A-Z]):\s*$", line)
        if m:
            current = m.group(1); variables[current] = []; continue
        m = re.match(r"^    - \{id: ([^,]+), weight: ([^,]+), text: (.*)\}\s*$", line)
        if m and current:
            variables[current].append({"id": m.group(1).strip(), "weight": float(m.group(2)), "text": m.group(3).strip()})
    return {"variables": variables}

ROOT = Path(__file__).resolve().parents[2]

def load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return _minimal_yaml(text)

def load_questions(path: Path | None = None) -> dict[str, Question]:
    path = path or ROOT / "config" / "questions.yaml"
    data = load_yaml(path)
    questions: dict[str, Question] = {}
    for variable, items in data.get("variables", {}).items():
        for item in items:
            q = Question(id=item["id"], variable=variable, text=item["text"], weight=float(item.get("weight", 1)))
            questions[q.id] = q
    return questions

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
