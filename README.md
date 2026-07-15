# The Meta-Argument

A reproducible research and scoring system for evaluating atomic historical events, laws, policies, institutions, technologies, and public actions through the Theophysics Master Equation.

```text
χ(W) = C_W[ ∭(G · M · E · S · T · K · R · Q · F) dx dy dt ]
```

`C_W` is the consciousness/free-will wrapper, not a tenth factor. The first deterministic milestone implements the public five-variable diagnostic subset: `G`, `T`, `K`, `F`, and `R`, while preserving the nine-variable schema.

## Current milestone

The local engine can:

1. load an atomic case JSON file;
2. validate required atomic-case fields;
3. load fixed rubric questions from `config/questions.yaml`;
4. convert fixed answers into deterministic scores;
5. preserve `UNKNOWN` and exclude `NOT_APPLICABLE`;
6. calculate direction, structural significance, veto, confidence, and dependencies;
7. run anti-gaming comparisons when alternate packets are supplied;
8. export JSON and Markdown reports;
9. run unit tests; and
10. encode the workbook logic as versioned config/docs rather than hidden spreadsheet formulas.

## Run locally

```bash
python -m pip install -e .
meta-score examples/fixture.json --anti-gaming --output /tmp/score.json --markdown /tmp/score.md
meta-excel-sync "GMF 3 the Trilima (1).xlsx" --research-dir knowledge_base/drafts
python -m unittest discover -s tests
```

## Knowledge-base workflow

The Excel sync can now emit a research bundle: a JSON record plus a Markdown note containing the case, score, evidence ledger, places looked, source snapshots, and review notes. Use this as the draft layer for a growing wiki-style corpus before promoting reviewed cases into `cases/`. See `docs/KNOWLEDGE_BASE.md` for the operating workflow.

## Integrity rules

The system must be able to refuse false precision with `INSUFFICIENTLY_DEFINED`, `INSUFFICIENT_EVIDENCE`, `ONTOLOGICAL_DEPENDENCY`, `CAUSATION_UNRESOLVED`, or `OUTCOME_NOT_YET_OBSERVABLE`. It never infers hidden moral intent as observable fact.
