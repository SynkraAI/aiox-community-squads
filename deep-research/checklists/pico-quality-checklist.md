# PICO Quality Checklist

```yaml
checklist:
  id: dr-pico-quality
  version: 1.0.0
  created: 2026-03-06
  purpose: "Validate PICO output from Sackett meets precision standards"
  mode: blocking
  used_by: sackett
  when: "After Sackett completes PICO formulation (QG-001)"
```

---

## Population (P)

```yaml
population_checks:
  - id: P-001
    check: "Population is specific (not generic 'users' or 'companies')"
    type: blocking
    validation: "P includes at least 2 of: size, industry, context, constraints"
    bad_example: "users"
    good_example: "B2B SaaS startups with <$5M ARR and 5-20 engineers"

  - id: P-002
    check: "Inclusion/exclusion criteria defined"
    type: recommended
    validation: "explicit boundaries on who is IN and OUT of scope"

  - id: P-003
    check: "Population is observable (not hypothetical)"
    type: blocking
    validation: "P describes entities that exist or can be identified"
```

---

## Intervention (I)

```yaml
intervention_checks:
  - id: I-001
    check: "Intervention is operationalized (not vague)"
    type: blocking
    validation: "I describes a specific action, tool, method, or change"
    bad_example: "improve onboarding"
    good_example: "implement interactive product tour with 5 guided steps"

  - id: I-002
    check: "Dose/intensity/duration specified where applicable"
    type: recommended
    validation: "I includes implementation details sufficient for replication"

  - id: I-003
    check: "Intervention is actionable (something that can be done)"
    type: blocking
    validation: "I is a verb-driven action, not a state"
```

---

## Comparison (C)

```yaml
comparison_checks:
  - id: C-001
    check: "Comparison is explicitly defined (not 'nothing')"
    type: blocking
    validation: "C describes a realistic baseline or alternative"
    bad_example: "no intervention"
    good_example: "continue with current support-only model"

  - id: C-002
    check: "Comparison is the realistic alternative (what would actually happen without I)"
    type: blocking
    validation: "C represents current practice or next-best option"

  - id: C-003
    check: "Comparison is fair (not straw man)"
    type: recommended
    validation: "C is a credible alternative, not designed to fail"
```

---

## Outcome (O)

```yaml
outcome_checks:
  - id: O-001
    check: "Outcome is measurable (has a metric)"
    type: blocking
    validation: "O includes a quantifiable metric"
    bad_example: "improved"
    good_example: "increased write throughput by >30%"

  - id: O-002
    check: "Magnitude threshold defined"
    type: blocking
    validation: "O specifies what magnitude counts as meaningful (e.g., >20%, >10pp)"

  - id: O-003
    check: "Timeframe specified"
    type: blocking
    validation: "O includes when the outcome is measured (e.g., at 6 months)"
    bad_example: "eventually improves"
    good_example: "measured 3 months post-migration"

  - id: O-004
    check: "Primary vs secondary outcomes distinguished"
    type: recommended
    validation: "if multiple outcomes, one is labeled primary"
```

---

## Question Assembly

```yaml
assembly_checks:
  - id: Q-001
    check: "Well-formed question assembled in standard format"
    type: blocking
    validation: "Question follows: 'In [P], does [I] compared to [C] result in [O]?'"

  - id: Q-002
    check: "Question type classified"
    type: blocking
    validation: "type in [therapeutic, diagnostic, prognostic, etiologic, economic]"

  - id: Q-003
    check: "Evidence level assigned (ideal + realistic)"
    type: blocking
    validation: "evidence_level has ideal (Level I-V) and realistic (Level I-V)"

  - id: Q-004
    check: "Search strategy blueprint derivable from PICO keywords"
    type: blocking
    validation: "search_terms can be extracted from P, I, C, O components"

  - id: Q-005
    check: "If multi-question query, each sub-question has own PICO"
    type: blocking
    validation: "complex queries decomposed into separate PICO formulations"
```

---

## Scoring

| Score | Result | Action |
|-------|--------|--------|
| 100% Blocking (13/13) | PASS | Proceed to Booth |
| >= 85% Blocking (11+/13) | CONDITIONAL | Proceed with documented gaps |
| < 85% Blocking | FAIL | Sackett reformulates |

**Total Checks:** 13 blocking + 4 recommended = 17

---

**Version:** 1.0.0
**Standard:** Deep Research PICO Quality (QG-001)
