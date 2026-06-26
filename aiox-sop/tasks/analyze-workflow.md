# Task: Analyze & Grade Workflow

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `analyze-workflow` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-analyst` |
| **Execution Type** | `Agent` |

## Metadata
```yaml
id: analyze-workflow
name: "Analyze & Grade Workflow"
category: analysis
agent: sop-analyst
elicit: false
autonomous: true
description: "Perform multi-dimensional analysis and scoring of a YAML workflow file across 10 quality dimensions adapted for workflow context. Produces a structured YAML gap report consumable by squad-chief for implementation of improvements."
```

## Purpose

Evaluate an existing YAML workflow against 10 quality dimensions derived from the SOP scoring rubric, adapted for workflow-specific concerns (phase structure, agent assignments, checkpoints, handoffs, error handling). This analysis produces a quantitative score (A through F), identifies specific gaps, and provides actionable remediation recommendations in a structured YAML format.

The output is a **YAML gap report** (not markdown) designed to serve as a machine-readable handoff contract between `@sop-chief` (analysis) and `@squad-chief` (implementation).

For SOP analysis, use `analyze-sop`. For full compliance audit, use `audit-sop`.

## Prerequisites

- [ ] Workflow file exists and is readable
- [ ] Workflow is in YAML format (`.yaml` or `.yml`)
- [ ] Workflow quality rubric (`workflow-quality-rubric.yaml`) accessible
- [ ] Gap report template (`workflow-gap-report-tmpl.yaml`) accessible

## Evidence Format Standard

Every score in the gap report MUST be backed by at least one evidence citation. No exceptions.

**Citation Format:**
```
[MARKER] file:section — "observação ou texto citado"
```

**Examples:**
- `[DOC] brownfield-complete.yaml:sequence — "All 6 phases have explicit agent assignment"` (documented finding)
- `[OBS] wf-squad-fusion.yaml:PHASE-3 — missing outputs field after line 42` (direct observation)
- `[INF] wf-create-squad.yaml:error_handling — no rollback policy defined, likely oversight` (inference)

**Minimum Citations Per Dimension:**
- `scoring_mode: full` → 2 citations minimum per dimension
- `scoring_mode: quick` → 1 citation minimum per dimension

**Confidence Floor for Scoring:**
- `[OBS]`, `[DOC]`, `[REP]`, `[COR]`, `[INF]` → valid for scoring (score >= 0.5)
- `[ASM]`, `[UNK]` → NOT valid for scoring. If only [ASM]/[UNK] evidence exists for a dimension, score it 0 and flag as insufficient evidence.

**Reference:** `workflow-quality-rubric.yaml → evidence_standard`

## Invention Red Flags

The following phrases indicate unsupported claims when they appear in the report WITHOUT an accompanying `[MARKER]` citation. Their presence triggers VETO-ANL-006.

| Red Flag Phrase | Safe Alternative |
|----------------|------------------|
| "Geralmente se recomenda" | Cite the specific recommendation source with [DOC] or [REP] |
| "Best practices sugerem" | Name the standard and cite it: `[DOC] workflow-tmpl.yaml:quality_gate — ...` |
| "Na minha experiência" | Replace with observed evidence: `[OBS] file:section — ...` |
| "É comum fazer" | Cite where this practice was observed: `[OBS]` or `[COR]` |
| "Experts concordam que" | Name the expert or source: `[DOC]` or `[REP]` |
| "Tipicamente" / "Normalmente" | State what was actually found: `[OBS]` or `[DOC]` |

**If you cannot cite it, do not claim it.** Declare `[UNK] — insufficient evidence` instead.

**Reference:** `workflow-quality-rubric.yaml → invention_red_flags`

## Inputs

```yaml
inputs:
  workflow_file:
    type: filepath
    required: true
    description: "Path to the workflow YAML file to analyze"

  scoring_mode:
    type: enum
    required: false
    default: full
    options: [full, quick]
    description: >
      full: Complete 10-dimension analysis with detailed gap report.
      quick: Abbreviated analysis focusing on top 5 dimensions (Clarity, Completeness, Executability, Error Handling, Compliance).
```

## 10-Dimension Scoring Reference

The 10 dimensions and their scoring signals are defined in `workflow-quality-rubric.yaml`. The dimensions are:

| # | Dimension | Weight | Key Signals |
|---|-----------|--------|-------------|
| WD-01 | Clarity | 10% | Phase naming, step descriptions, agent assignment clarity, ambiguity |
| WD-02 | Completeness | 15% | Phase coverage, inputs/outputs, scope, anatomy sections, handoffs |
| WD-03 | Executability | 15% | Sequence validity, task existence, agent existence, no dead ends, dependencies |
| WD-04 | Measurability | 10% | Checkpoint criteria, duration estimates, success criteria, quality metrics |
| WD-05 | Compliance | 10% | Schema compliance, quality gates, governance gate, veto conditions |
| WD-06 | Maintainability | 10% | Version control, orchestrator, modular phases, metadata |
| WD-07 | Accessibility | 10% | Metadata tags, description, phase legibility, navigation |
| WD-08 | Error Handling | 10% | on_error, escalation, rollback, veto prevention |
| WD-09 | Visual Design | 5% | Mermaid diagram, structured YAML, formatting |
| WD-10 | AI-Readiness | 5% | Template variables, parseable conditions, agent-executable steps |

## Workflow / Steps

### 1. Ingest Workflow

```
ACTION: Read and parse the workflow YAML file

DETECT:
  - File format validation (must be valid YAML)
  - Presence of workflow.id, workflow.name, workflow.version
  - workflow.sequence[] presence (canonical executable contract)
  - workflow.phases[] presence (supplemental metadata)
  - Total phase count, task count, agent count

STORE: workflow_content = {
  raw_yaml, id, name, version, orchestrator,
  sequence[], phases[], agents[], checkpoints[],
  phase_count, task_count, has_error_handling,
  has_governance_gate, has_handoff_prompts
}
```

### 2. Structural Analysis

```
ACTION: Check workflow anatomy against workflow-tmpl.yaml required sections

MAP each found section to expected 10 sections:
  1. Header (id, name, version, orchestrator, description)
  2. best_for
  3. decision_matrix_fit
  4. sequence (CANONICAL executable contract)
  5. handoff_prompts
  6. phases (supplemental metadata)
  7. error_handling
  8. checkpoint_config
  9. completion_signals / outputs
  10. metadata

OUTPUT: structural_report = {
  sections_found: <count>/10,
  missing_sections: [<names>],
  extra_sections: [<names>],
  section_quality: { <section>: <brief assessment> }
}
```

### 3. Content Analysis

```
ACTION: Analyze content quality signals specific to workflows

MEASURES:
  a) Sequence Analysis
     - Is workflow.sequence[] present and valid?
     - Are requires/next chains consistent?
     - Are all task references resolvable?
     - Are all agent references valid?

  b) Phase Analysis
     - Does each phase have: id, name, agent, description, checkpoint?
     - Are outputs defined per phase?
     - Are handoff_prompts defined for agent transitions?

  c) Checkpoint Analysis
     - Are checkpoint criteria specific and measurable?
     - Are human_review flags set appropriately?
     - Are veto conditions defined?

  d) Error Handling Analysis
     - Is error_handling section present?
     - Are on_phase_failure and on_checkpoint_failure defined?
     - Are rollback/retry policies specified?

OUTPUT: content_report = {
  sequence_valid, phase_completeness_pct,
  checkpoint_coverage_pct, error_handling_present,
  handoff_coverage_pct, missing_elements[]
}
```

### 4. Dimensional Scoring

```
ACTION: Score across all 10 dimensions using workflow-quality-rubric.yaml

FOR EACH dimension:
  1. Evaluate each scoring signal (1-10 scale)
  2. Calculate dimension average
  3. Apply dimension weight
  4. Record evidence using citation format: [MARKER] file:section — "observation"
     - Minimum citations: full=2, quick=1 per dimension
     - Valid markers: [OBS], [DOC], [REP], [COR], [INF] (score >= 0.5)
     - Invalid for scoring: [ASM], [UNK] — score dimension 0 if only these exist
     - CHECK: VETO-ANL-005 triggers if any dimension has zero citations

CALCULATE:
  total_weighted_score = SUM(dimension_score * weight) * 10 for all dimensions
  grade = map to A+/A/B+/B/C+/C/D/F scale

OUTPUT: Populate scorecard section of gap report template
```

### 5. Gap Detection

```
ACTION: Identify specific gaps, ambiguities, and risks in the workflow

CATEGORIES:
  - MISSING: Required elements that are absent (sections, fields, agents)
  - AMBIGUOUS: Definitions that could be interpreted multiple ways
  - INCOMPLETE: Sections present but insufficient
  - INCONSISTENT: Contradictions between sequence and phases
  - DEAD_END: Process paths with no defined next step
  - RISK: Execution, quality, or safety risks from gaps

FORMAT per gap:
  - id: "GAP-{N}"
    category: "<category>"
    dimension: "<dimension_name>"
    location: "<phase_id or section reference>"
    description: "<what is wrong>"
    impact: "high|medium|low"
    suggested_fix: "<specific fix>"
    effort: "XS|S|M|L|XL"
```

### 6. Remediation Recommendations

```
ACTION: Generate prioritized improvement recommendations

FOR EACH gap:
  - Specific fix description
  - Target file and section to modify
  - Effort estimate (XS/S/M/L/XL)
  - Priority (P1: must fix / P2: should fix / P3: nice to have)
  - improvement_source (MANDATORY — VETO-ANL-007)

PRIORITIZATION:
  P1: Executability, compliance, or error handling gaps (score < 5 on critical dimensions)
  P2: Completeness, measurability, maintainability gaps (score 5-7)
  P3: Visual design, accessibility, AI-readiness improvements (score 5-7)

OUTPUT: Populate remediation section of gap report template

NOTE: improvement_source is REQUIRED for every remediation item.
  Format: [SOURCE: file_path:section] — e.g., [SOURCE: workflow-quality-rubric.yaml:WD-03]
  VETO-ANL-007 blocks report generation if any improvement_source is empty.
```

### 7. Generate Gap Report

```
ACTION: Compile structured YAML gap report using workflow-gap-report-tmpl.yaml

STEPS:
  1. Load template from squads/aiox-sop/templates/workflow-gap-report-tmpl.yaml
  2. Populate all sections:
     - report.overall (score, grade, pass, certification, summary)
     - report.scorecard (10 dimensions with evidence)
     - report.strengths (top 3)
     - report.weaknesses (top 3)
     - report.gaps (all detected gaps)
     - report.remediation (prioritized actions)
     - report.evidence_summary (marker counts)
     - report.metadata (analysis metadata)
  3. Validate all evidence citations present (VETO-ANL-005)
  4. Validate all improvement_source fields populated (VETO-ANL-007)
  5. Validate no red flag phrases without citations (VETO-ANL-006)
  6. Write to output path

FILE: outputs/aiox-sop/workflow-analysis/{workflow-name}-gap-report.yaml
```

## Output

```yaml
outputs:
  primary:
    path: "outputs/aiox-sop/workflow-analysis/{workflow-name}-gap-report.yaml"
    format: yaml
    description: "Structured gap report with scorecard, gaps, and remediation plan. Machine-readable for consumption by squad-chief via improve-workflow-from-report task."

  metadata:
    total_score: "<0-100>"
    grade: "<A+|A|B+|B|C+|C|D|F>"
    gap_count: "<number>"
    p1_issues: "<number>"
    dimensions_analyzed: 10
    scoring_mode: "<full|quick>"
```

## Acceptance Criteria

- [ ] All 10 dimensions are scored (or top 5 in quick mode)
- [ ] Total weighted score is calculated correctly
- [ ] Letter grade is assigned matching the scale
- [ ] Every dimension has specific evidence supporting the score
- [ ] All gaps are categorized and assigned impact levels
- [ ] Remediation recommendations are specific (not generic advice)
- [ ] Each recommendation includes target_file and target_section
- [ ] Priorities are assigned (P1/P2/P3) based on impact
- [ ] Output is valid YAML following workflow-gap-report-tmpl.yaml
- [ ] Report includes metadata (date, phase count, task count)
- [ ] Every evidence citation follows `[MARKER] file:section` format (per `evidence_standard`)
- [ ] Every remediation has non-empty `improvement_source` field (per VETO-ANL-007)
- [ ] Output file written to `outputs/aiox-sop/workflow-analysis/`

## Veto Conditions

- STOP if the input file is not a workflow YAML (e.g., it is a task, agent, or unrelated document)
- STOP if the file is empty or not valid YAML
- STOP if the file has no `workflow` root key or no `sequence`/`phases` section
- STOP if workflow quality rubric is unavailable
- `VETO-ANL-005`: STOP if any scored dimension has zero evidence citations. Every dimension MUST have at least one `[MARKER] file:section` citation. If you cannot find evidence, score the dimension 0 and mark `[UNK]`.
- `VETO-ANL-006`: STOP if the report contains any invention red flag phrase (see `workflow-quality-rubric.yaml → invention_red_flags`) without an accompanying `[MARKER]` citation on the same finding. Remove the phrase or add a citation.
- `VETO-ANL-007`: STOP if the `improvement_source` field of any remediation recommendation is empty. Every recommendation MUST trace to a specific source: `[SOURCE: file_path:section]`.
- `VETO-ANL-008`: STOP if `scoring_mode=full` and more than 3 dimensions have ONLY `[INF]` evidence (no `[OBS]`, `[DOC]`, `[REP]`, or `[COR]`). Escalate to `scoring_mode=quick` or request additional source material from the user.

## Related Documents

- `analyze-sop.md` — SOP analysis task (sibling pattern)
- `workflow-quality-rubric.yaml` — Scoring rubric for workflows
- `workflow-gap-report-tmpl.yaml` — Output template (handoff contract)
- `sop-scoring-rubric.yaml` — Parent rubric (reference)
- `improve-workflow-from-report.md` — Consumer of this task's output (squad-creator)
- `sop-workflow-integration.md` — Integration protocol between squads
