# Knowledge Base Workflow

The project should grow like an auditable encyclopedia, not like a pile of one-off scores.

## Intended pipeline

```text
Excel workbook input
→ Python case JSON
→ deterministic score result
→ evidence ledger and source snapshots
→ JSON + Markdown research bundle
→ reviewed case promoted into cases/
```

The scoring engine must stay deterministic. Research can be assisted by humans or external tools, but every claim that affects a score should be written down as evidence with enough source metadata to audit it later.

## Running from Excel

```bash
meta-excel-sync \
  "GMF 3 the Trilima (1).xlsx" \
  --case-json knowledge_base/drafts/current.case.json \
  --result-json knowledge_base/drafts/current.result.json \
  --research-dir knowledge_base/drafts
```

This writes:

- the constructed case JSON;
- the score result JSON;
- a research JSON bundle;
- a Markdown note that can be dropped into Obsidian or any static-site/wiki tool.

## What belongs in a research bundle

A strong bundle should contain:

1. **Case definition** — actor, action, target, mechanism, period, measured outcomes, and counterfactual.
2. **Evidence ledger** — factual claims separated from interpretation, with source URL/title/publisher/date where available.
3. **Places looked** — sources searched or fetched, including sources that did not support the claim.
4. **Rubric answers** — the frozen yes/no/mixed/unknown answers that drive the score.
5. **Score result** — direction, public-five score, veto, confidence, and variable-level details.
6. **Notes** — unresolved disputes, missing evidence, ontology issues, and reasons for `UNKNOWN` answers.

## Promotion rule

Draft bundles are not automatically authoritative. Promote a draft into `cases/` only after review confirms that:

- the event is atomic enough to score;
- every non-`UNKNOWN` answer has evidence;
- conflicting evidence is visible instead of hidden;
- identity-swap and duplicate-penalty anti-gaming rules still pass;
- a human reviewer can reproduce the score from the bundle alone.

## Why this matters

The academically defensible claim is not “the model knows morality.” The defensible claim is narrower and stronger: given the same atomic case definition, frozen subquestions, visible evidence, and deterministic scoring code, independent raters can converge or expose exactly where they diverge.
