# RESEARCH PIPELINE

This document is part of the deterministic first milestone for the Meta-Argument scoring engine.

## Implementation plan

1. Preserve the workbook as a design reference and move machine-readable definitions into versioned YAML/JSON.
2. Score only atomic cases with actor, action, target, mechanism, outcome, and period boundaries.
3. Keep evidence, interpretations, rubric answers, and final scores separate.
4. Convert only fixed answers (YES, NO, MIXED, UNKNOWN, NOT_APPLICABLE) into deterministic scores.
5. Preserve UNKNOWN as missing information and exclude NOT_APPLICABLE from denominators.
6. Produce separate direction, structural significance, veto, confidence, and ontological-dependency outputs.
7. Add research and dashboard layers only after deterministic scoring is reproducible.

## Workbook mapping

The workbook sheets inspected are: J-M-FW Diagnostic, Scenario Scorer, Reciprocity Test, Coherence Index, Historical χ Scorer, Convergence Map, 5-Variable Instrument, Historical Baseline, α Resolver, Canonical Equations, and Impossibility Proof. Their first-milestone machine-readable counterparts live in config/, schemas/, src/meta_argument/, and tests/.
