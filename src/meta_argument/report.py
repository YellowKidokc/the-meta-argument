from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def write_json_report(result: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def render_markdown(case: dict[str, Any], result: dict[str, Any]) -> str:
    lines=[f"# Structural Report: {case.get('case_id')}", "", f"Status: `{result.get('status')}`", ""]
    if result.get("status") != "SCORED":
        lines.append(json.dumps(result, indent=2)); return "\n".join(lines)+"\n"
    lines += ["## Atomic Case", f"- Actor: {case.get('actor')}", f"- Action: {case.get('action')}", f"- Target: {case.get('target')}", f"- Mechanism: {case.get('mechanism')}", f"- Period: {case.get('start_date')} to {case.get('end_date')}", "", "## Direction", f"- Label: `{result['direction']['label']}`", f"- Score: `{result['direction']['score']}`", f"- Public five score: `{result['direction']['public_five_score']}`", "", "## Variables", "| Variable | Raw | Rounded | Coverage | Confidence | Unknown | Veto? |", "|---|---:|---:|---:|---:|---:|---|"]
    for name, data in result["variables"].items():
        lines.append(f"| {name} | {data['raw_score']} | {data['rounded_score']} | {data['coverage']} | {data['confidence']} | {data['unknown_fraction']} | {data['veto_candidate']} |")
    lines += ["", "## Veto", f"- Weakest variable: `{result['veto']['variable']}` ({result['veto']['score']})", "", "## Confidence", f"- Overall confidence: `{result['confidence']}`", "", "## Ontological Dependencies"]
    lines += [f"- {x}" for x in result.get("ontological_dependencies", [])] or ["- None declared"]
    return "\n".join(lines)+"\n"

def write_markdown_report(case: dict[str, Any], result: dict[str, Any], path: Path) -> None:
    path.write_text(render_markdown(case, result), encoding="utf-8")
