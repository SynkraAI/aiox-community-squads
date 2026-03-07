# Report Completeness Checklist

```yaml
checklist:
  id: dr-report-completeness
  version: 1.0.0
  created: 2026-03-06
  purpose: "Validate final research report before delivery to user"
  mode: blocking
  used_by: dr-orchestrator
  when: "After synthesis (Phase 5), before delivering report"
```

---

## Section 1: Executive Summary

```yaml
executive_summary_checks:
  - id: RPT-ES-001
    check: "Executive summary present with 3-5 bullet points"
    type: blocking
    validation: "executive_summary has 3-5 key findings/recommendations"

  - id: RPT-ES-002
    check: "Summary reflects actual findings (not generic)"
    type: blocking
    validation: "bullets reference specific evidence from Tier 1 agents"

  - id: RPT-ES-003
    check: "Confidence level stated in summary"
    type: blocking
    validation: "overall confidence (high/medium/low) mentioned upfront"
```

---

## Section 2: Research Design

```yaml
research_design_checks:
  - id: RPT-RD-001
    check: "PICO question included (from Sackett)"
    type: blocking
    validation: "P, I, C, O components visible in report"

  - id: RPT-RD-002
    check: "Review methodology stated (from Booth)"
    type: blocking
    validation: "review_type and selection rationale included"

  - id: RPT-RD-003
    check: "Research design described (from Creswell)"
    type: recommended
    validation: "qual/quant/mixed approach stated, or skip reason documented"
```

---

## Section 3: Findings

```yaml
findings_checks:
  - id: RPT-FN-001
    check: "Findings organized by use case or theme"
    type: blocking
    validation: "findings grouped logically, not dumped as flat list"

  - id: RPT-FN-002
    check: "Each finding has confidence level (high/medium/low)"
    type: blocking
    validation: "every finding tagged with confidence_level"

  - id: RPT-FN-003
    check: "Each finding traceable to source(s)"
    type: blocking
    validation: "finding references at least 1 cited source"

  - id: RPT-FN-004
    check: "Contradictions between agents surfaced (not hidden)"
    type: blocking
    validation: "if agents disagree: both positions presented with respective confidence"

  - id: RPT-FN-005
    check: "Agent attribution clear (which agent produced which finding)"
    type: recommended
    validation: "findings labeled with originating agent"
```

---

## Section 4: Quality Assessment

```yaml
quality_assessment_checks:
  - id: RPT-QA-001
    check: "Ioannidis PPV results included"
    type: blocking
    validation: "ppv_table or ppv_summary from Ioannidis audit present"

  - id: RPT-QA-002
    check: "Bias patterns documented"
    type: blocking
    validation: "bias_report from Ioannidis included (types, severity, affected findings)"

  - id: RPT-QA-003
    check: "Kahneman cognitive bias audit included"
    type: blocking
    validation: "12-Question score and detected biases documented"

  - id: RPT-QA-004
    check: "Unreliable findings clearly marked"
    type: blocking
    validation: "findings with ppv < 0.3 or VERY_LOW reliability are flagged visually"
```

---

## Section 5: Recommendations

```yaml
recommendations_checks:
  - id: RPT-RC-001
    check: "Recommendations are actionable (not vague)"
    type: blocking
    validation: "each recommendation starts with a verb and specifies what to do"
    bad_example: "Consider improving the process"
    good_example: "Implement CI/CD pipeline with automated testing before Q3"

  - id: RPT-RC-002
    check: "Each recommendation has confidence level"
    type: blocking
    validation: "recommendation tagged with confidence (high/medium/low)"

  - id: RPT-RC-003
    check: "Pre-mortem failure scenarios included for major recommendations"
    type: blocking
    validation: "top recommendation has >= 2 failure scenarios from Kahneman"

  - id: RPT-RC-004
    check: "Bias warnings attached to flagged recommendations"
    type: blocking
    validation: "recommendations with >= 1 cognitive bias have warning label"
```

---

## Section 6: Limitations

```yaml
limitations_checks:
  - id: RPT-LM-001
    check: "Limitations section present and non-empty"
    type: blocking
    validation: "limitations has >= 1 documented limitation"

  - id: RPT-LM-002
    check: "Evidence gaps identified"
    type: blocking
    validation: "missing evidence areas or unanswered sub-questions documented"

  - id: RPT-LM-003
    check: "Scope boundaries stated"
    type: recommended
    validation: "what was NOT investigated is explicitly stated"
```

---

## Section 7: Sources

```yaml
sources_checks:
  - id: RPT-SR-001
    check: "Full source list present"
    type: blocking
    validation: "sources section has >= 5 entries"

  - id: RPT-SR-002
    check: "Each source has credibility rating"
    type: blocking
    validation: "credibility_score (high/medium/low) assigned per source"

  - id: RPT-SR-003
    check: "Source types labeled (primary/secondary/grey literature)"
    type: recommended
    validation: "source_type field set for each entry"

  - id: RPT-SR-004
    check: "No dead links (URLs accessible)"
    type: recommended
    validation: "spot-check top 3 URLs for accessibility"
```

---

## Section 8: Methodology Notes

```yaml
methodology_checks:
  - id: RPT-MN-001
    check: "PICO formulation documented"
    type: blocking
    validation: "full PICO with all 4 components in methodology section"

  - id: RPT-MN-002
    check: "Review type and search strategy documented"
    type: blocking
    validation: "Booth's methodology selection and Sackett's search blueprint included"

  - id: RPT-MN-003
    check: "Agents used in this run listed"
    type: recommended
    validation: "agent roster for this specific pipeline execution documented"
```

---

## Meta Checks

```yaml
meta_checks:
  - id: RPT-META-001
    check: "Report is self-contained (reader needs no external context)"
    type: blocking
    validation: "all acronyms defined, all references inline"

  - id: RPT-META-002
    check: "Use case classification stated at top of report"
    type: recommended
    validation: "UC-00X label visible in report header or methodology section"
```

---

## Scoring

| Score | Result | Action |
|-------|--------|--------|
| 100% Blocking (26/26) | PASS | Deliver to user |
| >= 85% Blocking (22+/26) | CONDITIONAL | Deliver with noted gaps |
| < 85% Blocking | FAIL | Fix before delivery |

**Total Checks:** 26 blocking + 8 recommended = 34

---

**Version:** 1.0.0
**Standard:** Deep Research Report Completeness
