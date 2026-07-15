from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.request import Request, urlopen

from .evidence_ledger import EvidenceItem, normalize_evidence


@dataclass(frozen=True)
class ResearchSnapshot:
    source_id: str
    url: str
    title: str = ""
    fetched_at: str = ""
    status: str = ""
    excerpt: str = ""
    error: str = ""


@dataclass(frozen=True)
class ResearchBundle:
    case_id: str
    created_at: str
    case: dict[str, Any]
    result: dict[str, Any]
    evidence: list[dict[str, Any]] = field(default_factory=list)
    looked_at: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _safe_name(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-").lower()
    return slug or "case"


def _html_title(text: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def snapshot_url(url: str, source_id: str | None = None, timeout: int = 20, max_chars: int = 4000) -> ResearchSnapshot:
    fetched_at = _utc_now()
    request = Request(url, headers={"User-Agent": "meta-argument-research/0.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(max_chars)
            charset = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
            status = str(getattr(response, "status", ""))
    except Exception as exc:
        return ResearchSnapshot(source_id=source_id or url, url=url, fetched_at=fetched_at, error=str(exc))
    excerpt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()[:1000]
    return ResearchSnapshot(source_id=source_id or url, url=url, title=_html_title(text), fetched_at=fetched_at, status=status, excerpt=excerpt)


def build_research_bundle(
    case: dict[str, Any],
    result: dict[str, Any],
    evidence_items: Iterable[dict[str, Any] | EvidenceItem] = (),
    looked_at: Iterable[dict[str, Any] | ResearchSnapshot] = (),
    notes: Iterable[str] = (),
) -> ResearchBundle:
    evidence = [asdict(item) for item in normalize_evidence(evidence_items)]
    snapshots = [asdict(item) if isinstance(item, ResearchSnapshot) else dict(item) for item in looked_at]
    return ResearchBundle(
        case_id=str(case.get("case_id") or result.get("case_id") or "case"),
        created_at=_utc_now(),
        case=case,
        result=result,
        evidence=evidence,
        looked_at=snapshots,
        notes=list(notes),
    )


def bundle_to_markdown(bundle: ResearchBundle) -> str:
    direction = bundle.result.get("direction", {}) if isinstance(bundle.result, dict) else {}
    lines = [
        "---",
        f"case_id: {bundle.case_id}",
        f"created_at: {bundle.created_at}",
        f"direction_label: {direction.get('label', '')}",
        f"direction_score: {direction.get('score', '')}",
        f"veto: {bundle.result.get('veto', {}).get('variable', '') if isinstance(bundle.result, dict) else ''}",
        "---",
        "",
        f"# {bundle.case_id}",
        "",
        "## Case",
        "",
        f"- Actor: {bundle.case.get('actor', '')}",
        f"- Action: {bundle.case.get('action', '')}",
        f"- Target: {bundle.case.get('target', '')}",
        f"- Mechanism: {bundle.case.get('mechanism', '')}",
        f"- Period: {bundle.case.get('start_date', '')}..{bundle.case.get('end_date', '')}",
        "",
        "## Score",
        "",
        f"- Direction: {direction.get('label', '')} ({direction.get('score', '')})",
        f"- Public five score: {direction.get('public_five_score', '')}",
        f"- Veto: {bundle.result.get('veto', {}).get('variable', '') if isinstance(bundle.result, dict) else ''}",
        "",
        "## Evidence Ledger",
        "",
    ]
    if bundle.evidence:
        for item in bundle.evidence:
            lines.append(f"- `{item.get('source_id', '')}` {item.get('claim', '')}")
            citation = item.get("citation") or item.get("source_url")
            if citation:
                lines.append(f"  - Source: {citation}")
            if item.get("source_type"):
                lines.append(f"  - Type: {item.get('source_type')}; directness: {item.get('directness')}")
    else:
        lines.append("- No evidence ledger entries were attached.")
    lines.extend(["", "## Places Looked / Research Snapshots", ""])
    if bundle.looked_at:
        for item in bundle.looked_at:
            lines.append(f"- `{item.get('source_id', '')}` {item.get('title') or item.get('url', '')}")
            if item.get("url"):
                lines.append(f"  - URL: {item.get('url')}")
            if item.get("status"):
                lines.append(f"  - Status: {item.get('status')}")
            if item.get("error"):
                lines.append(f"  - Error: {item.get('error')}")
            if item.get("excerpt"):
                lines.append(f"  - Excerpt: {item.get('excerpt')}")
    else:
        lines.append("- No web/source snapshots were attached.")
    lines.extend(["", "## Notes", ""])
    lines.extend([f"- {note}" for note in bundle.notes] or ["- No notes."])
    lines.append("")
    return "\n".join(lines)


def write_research_bundle(bundle: ResearchBundle, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    base = _safe_name(bundle.case_id)
    json_path = output_dir / f"{base}.research.json"
    md_path = output_dir / f"{base}.md"
    json_path.write_text(json.dumps(asdict(bundle), indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(bundle_to_markdown(bundle), encoding="utf-8")
    return {"json": json_path, "markdown": md_path}
