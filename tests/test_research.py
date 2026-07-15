from meta_argument.research import build_research_bundle, bundle_to_markdown


def test_research_bundle_markdown_records_evidence_and_places_looked():
    case = {"case_id": "demo", "actor": "A", "action": "acts", "target": "T", "mechanism": "M", "start_date": "1", "end_date": "2"}
    result = {"direction": {"label": "MIXED", "score": 0, "public_five_score": 0}, "veto": {"variable": "T"}}
    bundle = build_research_bundle(
        case,
        result,
        evidence_items=[{"source_id": "s1", "claim": "A thing happened", "source_url": "https://example.test/source"}],
        looked_at=[{"source_id": "w1", "url": "https://example.test", "title": "Example", "status": "200", "excerpt": "Looked here"}],
    )

    markdown = bundle_to_markdown(bundle)

    assert "## Evidence Ledger" in markdown
    assert "A thing happened" in markdown
    assert "## Places Looked / Research Snapshots" in markdown
    assert "Looked here" in markdown


def test_write_research_bundle_creates_json_and_markdown(tmp_path):
    case = {"case_id": "Demo Case", "actor": "A", "action": "acts", "target": "T", "mechanism": "M", "start_date": "1", "end_date": "2"}
    result = {"direction": {"label": "MIXED", "score": 0}, "veto": {"variable": "T"}}
    bundle = build_research_bundle(case, result)

    from meta_argument.research import write_research_bundle

    paths = write_research_bundle(bundle, tmp_path)

    assert paths["json"].exists()
    assert paths["markdown"].exists()
    assert "# Demo Case" in paths["markdown"].read_text(encoding="utf-8")
