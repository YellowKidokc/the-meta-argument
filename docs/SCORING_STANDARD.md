# Theophysics Structural Scoring Standard v0.1

## 1. Unit of analysis

Every scored object must be atomic:

```text
Actor + Action + Target + Mechanism + Outcome + Period
```

Broad labels such as `Trump`, `Democrats`, `capitalism`, `communism`, `abortion`, or `the church` must first be decomposed into specific actions or policies.

## 2. Answer scale

Humans and research agents answer subquestions using:

- `yes` — evidence supports the constructive condition
- `no` — evidence supports its failure or destructive inverse
- `mixed` — material evidence exists on both sides
- `unknown` — insufficient evidence

Deterministic numeric mapping:

```text
yes = +1
mixed = 0
no = -1
unknown = excluded from denominator
```

A zero therefore means balance, not ignorance.

## 3. Public five-variable instrument

### G — Grace / source-bearing

**Question:** Does an actor absorb unresolved cost in a way that restores the affected party's autonomy, or export cost onto nonresponsible people while creating control or dependency?

Subquestions:

1. Was meaningful cost actually absorbed for another party?
2. Was that cost-bearing substantially voluntary?
3. Did the intervention increase the recipient's practical autonomy?
4. Did it avoid creating an unrelated debt, surveillance channel, or control right?
5. Were nonresponsible third parties protected from unjust cost export?

Boundary test: After the intervention, is the recipient more capable of functioning freely without the intervener?

### T — Thermodynamic Justice / ledger

**Question:** Is measurable cost assigned to the actor who caused the damage, with agency, proportionality, and due process established?

Subquestions:

1. Is identifiable damage present?
2. Is a specific causal actor or bounded offender set identified?
3. Is meaningful agency established?
4. Is the remedy proportional to the attributable damage?
5. Is evidence review or due process available?
6. Are victims and non-offenders protected from additional burden?

Boundary test: Can the system name the responsible actor and show why the imposed cost belongs there?

### K — Knowledge / truth access

**Question:** Can relevant claims be independently inspected, challenged, reproduced where feasible, and corrected?

Subquestions:

1. Are primary evidence and governing records accessible?
2. Are methods and material assumptions disclosed?
3. Can qualified independent parties challenge the claim publicly?
4. Are conflicts of interest visible?
5. Do failed predictions or discovered errors produce correction?
6. Are dissenting claims answered with evidence rather than status punishment?

Boundary test: Does authority remain accountable to inspectable evidence?

### F — Faith Network / relational topology

**Question:** Are relationships voluntary, plural, reciprocal, and meaningfully escapable?

Subquestions:

1. Can participants meaningfully refuse or exit?
2. Can alternative networks form?
3. Is disagreement possible without loss of unrelated necessities?
4. Are obligations reciprocal rather than one-directional?
5. Is surveillance limited and disclosed?
6. Does the network preserve direct human association rather than compulsory mediation?

Boundary test: Can a person leave or disagree without losing livelihood, legal identity, healthcare, banking, or basic social existence?

### R — Resurrection / repair

**Question:** Does the intervention repair the original damage, reduce recurrence, restore agency, and preserve a path back?

Subquestions:

1. Is the original damage measurably reduced?
2. Is recurrence risk reduced?
3. Can affected parties reenter ordinary life?
4. Is permanent imposed identity or exclusion avoided?
5. Is there an appeal, correction, or treatment-change mechanism?
6. Can the repaired system function without indefinite intervention?

Boundary test: When intervention ends, is the affected system more capable of healthy independent function?

## 4. Full nine-variable extension

### M — Motion / directed action

1. Did the event convert stated intention into observable action?
2. Was action timely relative to the damage?
3. Did effort remain directed toward the stated constructive outcome?
4. Did implementation avoid uncontrolled mission expansion?

### E — Generator / durable capacity

1. Did the event create durable capacity for constructive production?
2. Could the mechanism continue without escalating extraction?
3. Did it generate correction, learning, or beneficial replication?
4. Did it avoid creating self-reinforcing destructive machinery?

### S — Sin-Entropy / closure

For the common scoring direction, `yes` means entropy-reducing.

1. Did the event reduce irreversible damage?
2. Did it preserve institutional openness to correction?
3. Did it reduce fragmentation and disorder rather than amplify them?
4. Did it avoid normalizing escalating harm?
5. Did it preserve future options?

### Q — Quantum Faith / pre-evidential commitment

1. Was action under uncertainty proportionate to available evidence?
2. Were commitments revisable when evidence changed?
3. Was uncertainty disclosed honestly?
4. Did commitment avoid becoming identity-protected ideology?
5. Were risks borne principally by those choosing the commitment?

## 5. Consciousness/free-will wrapper

`W` is not inferred from hidden motives. Public scoring uses observable proxies only:

- availability of meaningful choice;
- disclosure of uncertainty;
- consistency between stated purpose and mechanism;
- response to correction;
- willingness of decision-makers to bear cost.

Values:

```text
+1 = predominantly constructive observable orientation
 0 = mixed, disputed, or unobservable
-1 = predominantly destructive observable orientation
```

## 6. Derived outputs

For each variable:

```text
raw = sum(answer values) / number of known answers
score = round(raw * 3, 2)
confidence = evidence_quality * coverage * agreement
```

Report four independent outputs:

1. **Direction** — confidence-weighted mean of variable scores
2. **Structural significance** — physical reach × amplification × persistence
3. **Veto profile** — weakest known load-bearing variable
4. **Confidence** — evidence quality, coverage, and inter-rater agreement

Do not collapse these into one moral number.

## 7. Evidence hierarchy

Preferred source classes:

1. primary law, order, judgment, transcript, budget, archival record, or dataset;
2. official outcome data;
3. peer-reviewed or major scholarly synthesis;
4. reputable contemporaneous reporting;
5. explicit advocate and critic sources.

Every factual claim must retain source URL, publication date, source class, quoted or paraphrased support, and confidence.

## 8. Anti-gaming requirements

- **Label-blind pass:** remove actor, party, nation, and ideology names where possible.
- **Symmetry pass:** reverse political identities while preserving the mechanism.
- **Advocate pass:** construct the strongest evidence-based constructive case.
- **Critic pass:** construct the strongest evidence-based destructive case.
- **Arbiter pass:** apply only frozen rules.
- **Counterfactual pass:** state the best-supported outcome without the intervention.
- **Duplicate-penalty check:** one fact cannot silently lower several variables unless each causal connection is separately justified.

## 9. Refusal states

The engine must return one or more of:

- `INSUFFICIENTLY_DEFINED`
- `INSUFFICIENT_EVIDENCE`
- `ONTOLOGICAL_DEPENDENCY`
- `OUTCOME_NOT_YET_OBSERVABLE`
- `CAUSATION_UNRESOLVED`

A refusal is preferable to fabricated precision.

## 10. Interpretation boundary

This instrument measures public structure and observable consequences. It does not measure the complete moral state of a human consciousness. It may compare policies, mechanisms, and records; it may not claim mathematical access to a person's heart.