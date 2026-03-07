# Evidence Reliability Checklist

```yaml
checklist:
  id: dr-evidence-reliability
  version: 1.0.0
  created: 2026-03-06
  purpose: "Validate Ioannidis evidence audit meets meta-research standards"
  mode: blocking
  used_by: ioannidis
  when: "After Ioannidis completes evidence reliability audit (QG-003)"
```

---

## PPV Calculation

```yaml
ppv_checks:
  - id: PPV-001
    check: "PPV calculated for every key finding"
    type: blocking
    validation: "each finding tagged with ppv_estimate (0.0-1.0)"

  - id: PPV-002
    check: "Pre-study odds (R) estimated with justification"
    type: blocking
    validation: "R value stated with 1-sentence rationale per finding"

  - id: PPV-003
    check: "Statistical power (1-beta) assessed"
    type: blocking
    validation: "power estimate based on study design and sample size"

  - id: PPV-004
    check: "Bias factor (u) estimated"
    type: blocking
    validation: "u value stated based on field characteristics and conflicts"

  - id: PPV-005
    check: "Reliability tier assigned per finding"
    type: blocking
    validation: "tier in [high (>0.85), moderate (0.50-0.85), low (0.20-0.50), very_low (<0.20)]"

  - id: PPV-006
    check: "No finding with PPV < 0.3 presented as strong evidence"
    type: blocking
    validation: "findings with ppv < 0.3 are labeled LOW or VERY_LOW confidence"
```

---

## Bias Detection

```yaml
bias_checks:
  - id: BIAS-001
    check: "Bias scan executed against top 8 categories"
    type: blocking
    validation: "each finding checked for: selection, publication, confirmation, reporting, funding, citation, language, time-lag bias"

  - id: BIAS-002
    check: "Each detected bias has severity rating"
    type: blocking
    validation: "severity in [CRITICAL, HIGH, MEDIUM, LOW] for each bias found"

  - id: BIAS-003
    check: "Affected findings linked to bias patterns"
    type: blocking
    validation: "each bias entry has affected_findings list"

  - id: BIAS-004
    check: "Publication bias assessed (funnel plot asymmetry or equivalent)"
    type: recommended
    validation: "publication_bias_assessment is present for meta-analyses"

  - id: BIAS-005
    check: "Conflicts of interest flagged"
    type: blocking
    validation: "funding_source and conflicts checked for each primary source"
```

---

## 5-Pillar Assessment

```yaml
pillar_checks:
  - id: PIL-001
    check: "Methods pillar graded (study design adequacy)"
    type: blocking
    validation: "methods_grade in [A, B, C, D, F] with justification"

  - id: PIL-002
    check: "Reporting pillar graded (selective reporting check)"
    type: blocking
    validation: "reporting_grade set with check for outcome completeness"

  - id: PIL-003
    check: "Reproducibility pillar graded (replication status)"
    type: blocking
    validation: "reproducibility_grade set with replication count or status"

  - id: PIL-004
    check: "Evaluation pillar graded (peer review rigor)"
    type: recommended
    validation: "evaluation_grade set or N/A with reason"

  - id: PIL-005
    check: "Incentives pillar graded (reward alignment)"
    type: recommended
    validation: "incentives_grade set or N/A with reason"
```

---

## Reliability Verdict

```yaml
verdict_checks:
  - id: VRD-001
    check: "Overall reliability grade assigned"
    type: blocking
    validation: "reliability_grade in [HIGH, MODERATE, LOW, VERY_LOW]"

  - id: VRD-002
    check: "Unreliable findings clearly quarantined"
    type: blocking
    validation: "findings with ppv < 0.20 moved to quarantined_evidence list"

  - id: VRD-003
    check: "Recommendation per finding: trust, verify, or discard"
    type: blocking
    validation: "each finding has action in [trust, verify, discard]"

  - id: VRD-004
    check: "Audit summary ready for Kahneman handoff"
    type: blocking
    validation: "structured output with ppv_table, bias_report, and reliability_grades"
```

---

## Scoring

| Score | Result | Action |
|-------|--------|--------|
| 100% Blocking (18/18) | PASS | Proceed to Kahneman |
| >= 85% Blocking (16+/18) | CONDITIONAL | Proceed with gaps documented |
| < 85% Blocking | FAIL | Ioannidis re-audits |

**Total Checks:** 18 blocking + 3 recommended = 21

---

**Version:** 1.0.0
**Standard:** Deep Research Evidence Reliability (QG-003)
