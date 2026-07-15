# The Meta-Argument

A reproducible research and scoring system for evaluating historical events, laws, policies, institutions, technologies, and public actions through the Theophysics Master Equation.

## Purpose

The project converts broad moral and political claims into auditable structural questions. It does not ask a language model to intuit whether a person, party, or event is good. It:

1. defines an atomic case;
2. collects evidence from multiple source classes;
3. separates facts from interpretations;
4. answers fixed, observable subquestions;
5. derives scores deterministically;
6. preserves unknowns and confidence;
7. exposes the exact point of disagreement.

## Master Equation

The canonical structure is:

```text
χ(W) = C_W[ ∭(G · M · E · S · T · K · R · Q · F) dx dy dt ]
```

The nine internal factors are:

- `G` — Grace / external cost-bearing and autonomy-restoring repair
- `M` — Motion / directed action
- `E` — Generator / durable productive capacity
- `S` — Sin-Entropy / closure, disorder, and irreversible damage
- `T` — Thermodynamic Justice / causal ledger and proportional cost assignment
- `K` — Knowledge-Revelation / truth access, challenge, and correction
- `R` — Resurrection / repair, reintegration, and recovery
- `Q` — Quantum Faith / commitment before full certainty
- `F` — Faith Network / relational connectivity, trust, and exit

`C_W` is the consciousness/free-will wrapper. It is not a tenth factor.

## Public Diagnostic

A five-variable public instrument provides the first pass:

```text
G · T · K · F · R
```

These factors answer:

- Who bears unresolved cost, and does the intervention restore autonomy?
- Does cost land on the actual responsible actor?
- Can claims be independently inspected, challenged, and corrected?
- Are relationships voluntary, plural, reciprocal, and escapable?
- Is damage actually repaired, with a path back to ordinary life?

The full nine-factor profile then explains motion, replication, entropy, and pre-evidential commitment.

## Non-negotiable rules

- Score atomic actions, not entire people, parties, religions, or ideologies.
- Never infer hidden consciousness or motive as established fact.
- `unknown` is not `zero`.
- Store evidence and reasoning for every answer.
- Separate direction, structural significance, confidence, and veto weakness.
- Run advocate, critic, arbiter, label-blind, symmetry, and counterfactual passes.
- A high total cannot hide a catastrophic load-bearing failure.

## Repository layout

```text
docs/                 Canonical scoring specification and research notes
schemas/              JSON schemas for cases and results
src/meta_argument/    Deterministic Python scoring engine
examples/             Pilot cases and example outputs
tests/                Repeatability and anti-gaming tests
```

## Run locally

```bash
python -m pip install -e .
meta-score examples/hiroshima-1945.json
python -m unittest discover -s tests
```

No AI key is required for the scoring engine. Internet research and AI-assisted extraction are intentionally separate from deterministic scoring.

## Current status

`v0.1.0` establishes the scoring contract, data model, public five-variable instrument, full nine-variable extension, confidence handling, and pilot-case format. The formulas are provisional research instruments and must be calibrated through blind inter-rater testing.