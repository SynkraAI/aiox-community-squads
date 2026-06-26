# Pipeline Execution Checklist

```yaml
checklist:
  id: dr-pipeline-execution
  version: 1.0.0
  created: 2026-03-06
  purpose: "Validate every pipeline run completes all mandatory stages"
  mode: blocking
  used_by: dr-orchestrator
  when: "After every pipeline run, before delivering final report"
```

---

## Phase 1: Classification

```yaml
classification_checks:
  - id: CLS-001
    check: "Query classified into use case (UC-001 through UC-004)"
    type: blocking
    validation: "use_case field is set and matches UC-001|UC-002|UC-003|UC-004"

  - id: CLS-002
    check: "Agent roster determined (primary + secondary agents selected)"
    type: blocking
    validation: "agent_roster has >= 2 agents from Tier 1"

  - id: CLS-003
    check: "Workflow variant confirmed (deep, quick, or competitive-intel)"
    type: blocking
    validation: "workflow_variant is set"
```

---

## Phase 2: Diagnostic (Tier 0)

```yaml
diagnostic_checks:
  - id: DIAG-001
    check: "Sackett produced PICO with all 4 components (P, I, C, O)"
    type: blocking
    validation: "pico.population AND pico.intervention AND pico.comparison AND pico.outcome are non-empty"

  - id: DIAG-002
    check: "Question type classified (therapeutic, diagnostic, prognostic, etiologic, economic)"
    type: blocking
    validation: "question_type in [therapeutic, diagnostic, prognostic, etiologic, economic]"

  - id: DIAG-003
    check: "Booth selected review methodology from 14 types"
    type: blocking
    validation: "review_type is set with justification"

  - id: DIAG-004
    check: "Creswell produced research design (or explicitly skipped for pure quant)"
    type: recommended
    validation: "research_design is set OR skip_reason documented"

  - id: DIAG-005
    check: "QG-001 (Question Quality) evaluated"
    type: blocking
    validation: "qg_001_result in [pass, fail_with_retry]"

  - id: DIAG-006
    check: "QG-002 (Methodology Fit) evaluated"
    type: blocking
    validation: "qg_002_result in [pass, fail_with_retry]"
```

---

## Phase 3: Execution (Tier 1)

```yaml
execution_checks:
  - id: EXEC-001
    check: "All assigned Tier 1 agents produced at least 1 output artifact"
    type: blocking
    validation: "for each agent in roster: output_artifacts >= 1"

  - id: EXEC-002
    check: "Evidence from >= 5 unique sources cited across all agents"
    type: blocking
    validation: "deduplicated_sources.count >= 5"

  - id: EXEC-003
    check: "Contradictions between agents flagged (not hidden)"
    type: blocking
    validation: "if contradictions_detected: contradictions_list is non-empty"

  - id: EXEC-004
    check: "Failed agents retried max 1 time, then gracefully degraded"
    type: recommended
    validation: "retry_count <= 1 per agent"
```

---

## Phase 4: Quality Assurance

```yaml
qa_checks:
  - id: QA-001
    check: "Ioannidis audited evidence reliability (PPV calculated)"
    type: blocking
    validation: "ppv_calculations exist for all key findings"

  - id: QA-002
    check: "Ioannidis flagged bias patterns"
    type: blocking
    validation: "bias_report is non-empty"

  - id: QA-003
    check: "Kahneman applied 12-Question Bias Checklist"
    type: blocking
    validation: "checklist_score is set (0-12)"

  - id: QA-004
    check: "Kahneman conducted pre-mortem on recommendations"
    type: blocking
    validation: "premortem.failure_scenarios has >= 1 entry"

  - id: QA-005
    check: "QG-003 (Evidence Reliability) evaluated"
    type: blocking
    validation: "qg_003_result is set"

  - id: QA-006
    check: "QG-004 (Decision Quality) evaluated"
    type: blocking
    validation: "qg_004_result is set"
```

---

## Phase 5: Synthesis

```yaml
synthesis_checks:
  - id: SYN-001
    check: "Report has all 8 sections populated"
    type: blocking
    validation: "sections [executive_summary, research_design, findings, quality_assessment, recommendations, limitations, sources, methodology_notes] all non-empty"

  - id: SYN-002
    check: "Confidence levels assigned to all findings (high/medium/low)"
    type: blocking
    validation: "every finding has confidence_level set"

  - id: SYN-003
    check: "Sources listed with credibility ratings"
    type: blocking
    validation: "sources_list has credibility_score for each entry"

  - id: SYN-004
    check: "QA flags surfaced in report (not buried)"
    type: blocking
    validation: "quality_assessment section references Ioannidis and Kahneman outputs"

  - id: SYN-005
    check: "Limitations documented"
    type: blocking
    validation: "limitations section has >= 1 entry"
```

---

## Scoring

| Score | Result | Action |
|-------|--------|--------|
| 100% Blocking (22/22) | PASS | Deliver report |
| >= 85% Blocking (19+/22) | CONDITIONAL | Deliver with documented gaps |
| < 85% Blocking | FAIL | Fix before delivery |

**Total Checks:** 22 blocking + 2 recommended = 24

---

**Version:** 1.0.0
**Standard:** Deep Research Pipeline Quality
