# Task: Analyze & Grade SOP

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `analyze-sop` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-analyst` |
| **Execution Type** | `Agent` |

## Metadata
```yaml
id: analyze-sop
name: "Analyze & Grade SOP"
category: analysis
agent: sop-analyst
elicit: false
autonomous: true
description: "Perform multi-dimensional analysis and scoring of an existing SOP across 10 quality dimensions. Produces a comprehensive report with weighted scores, gap detection, and prioritized remediation recommendations."
```

## Purpose

Evaluate an existing SOP against 10 quality dimensions derived from ISO 9001, FDA/GMP, Six Sigma, and Gawande's principles. This analysis produces a quantitative score (A through F), identifies specific gaps, and provides actionable remediation recommendations. The analysis is autonomous and does not require user input beyond the SOP file.

This is the foundational analysis task. For benchmarking against specific standards, use `benchmark-sop`. For full compliance audit, use `audit-sop`.

## Prerequisites

- [ ] SOP file exists and is readable
- [ ] SOP is in Markdown, YAML, or JSON format
- [ ] Scoring rubric (`sop-scoring-rubric.yaml`) accessible
- [ ] Confidence levels (`confidence-levels.yaml`) accessible

## Evidence Format Standard

Every score in the analysis report MUST be backed by at least one evidence citation. No exceptions.

**Citation Format:**
```
[MARKER] file:section — "observação ou texto citado"
```

**Examples:**
- `[DOC] create-sop.md:Procedure — "Step 3 uses passive voice: 'the form should be submitted'"` (documented finding)
- `[OBS] benchmark-sop.md:Prerequisites — missing compliance standard reference after line 12` (direct observation)
- `[INF] extract-sop.md:Error Handling — no escalation path defined, likely oversight given complexity` (inference)

**Minimum Citations Per Dimension:**
- `scoring_mode: full` → 2 citations minimum per dimension
- `scoring_mode: quick` → 1 citation minimum per dimension

**Confidence Floor for Scoring:**
- `[OBS]`, `[DOC]`, `[REP]`, `[COR]`, `[INF]` → valid for scoring (score >= 0.5)
- `[ASM]`, `[UNK]` → NOT valid for scoring. If only [ASM]/[UNK] evidence exists for a dimension, score it 0 and flag as insufficient evidence.

**Reference:** `sop-scoring-rubric.yaml → evidence_standard`, `confidence-levels.yaml`

## Invention Red Flags

The following phrases indicate unsupported claims when they appear in the report WITHOUT an accompanying `[MARKER]` citation. Their presence triggers VETO-ANL-006.

| Red Flag Phrase | Safe Alternative |
|----------------|------------------|
| "Geralmente se recomenda" | Cite the specific recommendation source with [DOC] or [REP] |
| "Best practices sugerem" | Name the standard and cite it: `[DOC] ISO-9001:7.5 — ...` |
| "Na minha experiência" | Replace with observed evidence: `[OBS] file:section — ...` |
| "É comum fazer" | Cite where this practice was observed: `[OBS]` or `[COR]` |
| "Experts concordam que" | Name the expert or source: `[DOC]` or `[REP]` |
| "Tipicamente" / "Normalmente" | State what was actually found: `[OBS]` or `[DOC]` |

**If you cannot cite it, do not claim it.** Declare `[UNK] — insufficient evidence` instead.

**Reference:** `sop-scoring-rubric.yaml → invention_red_flags`

## Inputs

```yaml
inputs:
  sop_file:
    type: filepath
    required: true
    description: "Path to the SOP file to analyze"

  scoring_mode:
    type: enum
    required: false
    default: full
    options: [full, quick]
    description: >
      full: Complete 10-dimension analysis with detailed report.
      quick: Abbreviated analysis focusing on top 5 dimensions (Clarity, Completeness, Executability, Error Handling, Compliance).
```

## 10-Dimension Scoring Rubric

```yaml
dimensions:
  1_clarity:
    name: "Clarity"
    weight: 0.10
    description: "How clear and understandable is the SOP?"
    signals:
      - flesch_kincaid_grade: "Target <= 8. Score: <=6=10, 7-8=8, 9-10=6, 11-12=4, >12=2"
      - jargon_density: "Undefined terms per 100 words. Score: 0=10, 1-2=8, 3-5=5, >5=2"
      - passive_voice_pct: "% of passive voice sentences. Score: 0-5%=10, 6-15%=7, 16-30%=4, >30%=1"
      - sentence_length: "Avg words per sentence. Score: <=15=10, 16-20=7, 21-25=4, >25=1"
      - action_verb_usage: "% of procedure steps starting with action verb. Score: 100%=10, 90-99%=8, 70-89%=5, <70%=2"

  2_completeness:
    name: "Completeness"
    weight: 0.15
    description: "Are all expected sections and information present?"
    signals:
      - sections_present: "FDA/GMP sections present / 11 total. Score proportional."
      - edge_cases: "Exception paths documented. Score: all=10, most=7, some=4, none=1"
      - inputs_outputs: "Defined and typed. Score: both complete=10, partial=5, missing=1"
      - roles_defined: "All actors identified with responsibilities. Score: RACI=10, roles only=6, none=1"
      - scope_boundaries: "Scope + out-of-scope defined. Score: both=10, scope only=5, neither=1"

  3_executability:
    name: "Executability"
    weight: 0.15
    description: "Can someone execute this SOP without additional information?"
    signals:
      - action_verbs: "Every step starts with verb. Score: 100%=10, 90%=8, 70%=5, <70%=2"
      - atomic_steps: "One action per step. Score: 100%=10, 90%=8, 70%=5, <70%=2"
      - expected_outcomes: "Steps include expected result. Score: all critical=10, most=7, few=3, none=1"
      - tools_specified: "Required tools/systems named. Score: all=10, most=7, some=4, none=1"
      - sequence_clarity: "Step ordering is unambiguous. Score: numbered+logical=10, numbered=7, bullets=4, prose=1"

  4_measurability:
    name: "Measurability"
    weight: 0.10
    description: "Can process performance be measured?"
    signals:
      - kpis_defined: "Performance indicators present. Score: >=3 KPIs=10, 1-2=6, none=1"
      - success_criteria: "Defined completion conditions. Score: quantitative=10, qualitative=5, none=1"
      - time_estimates: "Duration per step or phase. Score: per step=10, per phase=7, total only=4, none=1"
      - quality_metrics: "Acceptance thresholds defined. Score: quantitative=10, qualitative=5, none=1"

  5_compliance:
    name: "Compliance"
    weight: 0.10
    description: "Does the SOP meet regulatory and standard requirements?"
    signals:
      - standard_alignment: "Aligned to stated standard. Score: fully=10, mostly=7, partially=4, not=1"
      - document_control: "Version, date, author, approver. Score: all 4=10, 3=7, 2=4, <2=1"
      - review_cycle: "Scheduled review defined. Score: specific date=10, general policy=5, none=1"
      - training_requirements: "Training documented. Score: detailed plan=10, mentioned=5, none=1"
      - record_keeping: "Documentation requirements stated. Score: detailed=10, mentioned=5, none=1"

  6_maintainability:
    name: "Maintainability"
    weight: 0.10
    description: "How easy is this SOP to update and manage?"
    signals:
      - version_history: "Change log present. Score: detailed=10, basic=5, none=1"
      - review_date: "Next review date specified. Score: specific=10, policy ref=5, none=1"
      - owner_defined: "Process owner identified. Score: named person=10, role=7, department=4, none=1"
      - modular_structure: "Sections independent and reusable. Score: highly modular=10, somewhat=5, monolithic=1"
      - change_process: "How to propose changes documented. Score: detailed=10, mentioned=5, none=1"

  7_accessibility:
    name: "Accessibility"
    weight: 0.10
    description: "How easy is the SOP to find, navigate, and use?"
    signals:
      - table_of_contents: "TOC or navigation aids. Score: linked TOC=10, TOC=7, headings only=4, none=1"
      - formatting: "Consistent headings, lists, tables. Score: excellent=10, good=7, fair=4, poor=1"
      - searchability: "Keywords, tags, metadata. Score: rich metadata=10, some=5, none=1"
      - length_appropriateness: "Not too long, not too short. Score: right-sized=10, slightly off=7, too long/short=3"
      - visual_hierarchy: "Information priority clear. Score: excellent=10, good=7, fair=4, poor=1"

  8_error_handling:
    name: "Error Handling"
    weight: 0.10
    description: "How well does the SOP handle exceptions and failures?"
    signals:
      - exception_paths: "Error scenarios documented. Score: comprehensive=10, common errors=7, minimal=4, none=1"
      - troubleshooting: "Troubleshooting section present. Score: detailed table=10, section=7, inline=4, none=1"
      - escalation: "Escalation path defined. Score: with contacts+criteria=10, general=5, none=1"
      - recovery: "Recovery procedures. Score: per error type=10, general=5, none=1"
      - prevention: "Preventive measures documented. Score: detailed=10, mentioned=5, none=1"

  9_visual_design:
    name: "Visual Design"
    weight: 0.05
    description: "Does the SOP use visual aids effectively?"
    signals:
      - flowcharts: "Process flowchart present. Score: detailed+clear=10, basic=7, none=1"
      - decision_trees: "Decision logic visualized. Score: for all decisions=10, some=5, none=1"
      - tables: "Data in tables vs prose. Score: all tabular data in tables=10, some=5, all prose=1"
      - diagrams: "Supporting diagrams. Score: relevant diagrams=10, some=5, none=1"
      - consistent_style: "Visual consistency. Score: uniform style=10, mostly=7, inconsistent=3"

  10_ai_readiness:
    name: "AI-Readiness"
    weight: 0.05
    description: "Could this SOP be converted to ML format without major rewrite?"
    signals:
      - structured_data: "Inputs/outputs as typed data. Score: fully typed=10, partially=5, prose only=1"
      - decision_logic: "Decision points as explicit conditions. Score: IF/THEN=10, implied=5, narrative=1"
      - tool_references: "Tools named specifically. Score: tool+action=10, tool only=5, vague=1"
      - step_atomicity: "Steps are atomic/parseable. Score: all atomic=10, most=7, few=3"
      - metadata_present: "YAML front matter or structured header. Score: rich=10, basic=5, none=1"

grade_scale:
  A: { min: 90, max: 100, label: "Excellent - Production ready" }
  B: { min: 80, max: 89, label: "Good - Minor improvements needed" }
  C: { min: 70, max: 79, label: "Acceptable - Significant improvements recommended" }
  D: { min: 60, max: 69, label: "Below Standard - Major revision required" }
  F: { min: 0, max: 59, label: "Failing - Complete rewrite recommended" }
```

## Workflow / Steps

### 1. Ingest SOP

```
ACTION: Read and parse the SOP file

DETECT:
  - File format (Markdown, YAML, JSON)
  - Presence of YAML front matter
  - Section structure and hierarchy
  - Total word count and step count

STORE: sop_content = {
  raw_text, format, sections[], steps[],
  word_count, step_count, has_front_matter
}
```

### 2. Structural Analysis

```
ACTION: Check all expected sections against FDA/GMP template

MAP each found section to expected 11 sections:
  1. Header Block
  2. Purpose
  3. Scope
  4. Definitions
  5. Responsibilities (RACI)
  6. Materials & Equipment
  7. Procedure
  8. Error Handling
  9. Quality Control
  10. References
  11. Revision History

OUTPUT: structural_report = {
  sections_found: <count>/11,
  missing_sections: [<names>],
  extra_sections: [<names>],
  section_quality: { <section>: <brief assessment> }
}
```

### 3. Content Analysis

```
ACTION: Analyze content quality signals

MEASURES:
  a) Readability
     - Calculate Flesch-Kincaid grade level (approximate)
     - Count average sentence length
     - Identify passive voice instances
     - Count undefined jargon/acronyms

  b) Action Verb Analysis
     - Check each procedure step for leading action verb
     - List steps without action verbs
     - Identify compound steps (multiple actions)

  c) Completeness Check
     - Are inputs defined?
     - Are outputs defined?
     - Are roles assigned?
     - Are tools specified?
     - Are time estimates present?
     - Are edge cases covered?

OUTPUT: content_report = {
  readability_grade, passive_voice_pct,
  action_verb_pct, compound_step_count,
  completeness_score, missing_elements[]
}
```

### 4. Dimensional Scoring

```
ACTION: Score across all 10 dimensions using the rubric above

FOR EACH dimension:
  1. Evaluate each signal (1-10 scale)
  2. Calculate dimension average
  3. Apply dimension weight
  4. Record evidence using citation format: [MARKER] file:section — "observation"
     - Minimum citations: full=2, quick=1 per dimension
     - Valid markers: [OBS], [DOC], [REP], [COR], [INF] (score >= 0.5)
     - Invalid for scoring: [ASM], [UNK] — score dimension 0 if only these exist
     - CHECK: VETO-ANL-005 triggers if any dimension has zero citations

CALCULATE:
  total_weighted_score = SUM(dimension_score * weight) for all 10 dimensions
  grade = map to A/B/C/D/F scale

OUTPUT: scores = {
  dimensions: {
    clarity: { score: X, weighted: X, evidence: "..." },
    completeness: { score: X, weighted: X, evidence: "..." },
    ...
  },
  total_score: <0-100>,
  grade: "<A|B|C|D|F>",
  grade_label: "<description>"
}
```

### 5. Gap Detection

```
ACTION: Identify specific gaps, ambiguities, and risks

CATEGORIES:
  - MISSING: Required elements that are absent
  - AMBIGUOUS: Statements that could be interpreted multiple ways
  - INCOMPLETE: Sections present but insufficient
  - INCONSISTENT: Contradictions between sections
  - DEAD_END: Process paths with no defined outcome
  - RISK: Safety, compliance, or quality risks from gaps

FORMAT per gap:
  - id: "GAP-{N}"
    category: "<category>"
    location: "<section/step reference>"
    description: "<what is wrong>"
    impact: "high|medium|low"
    dimension_affected: "<dimension name>"
```

### 6. Remediation Recommendations

```
ACTION: Generate prioritized improvement recommendations

FOR EACH gap:
  - Specific fix description
  - Example of correct implementation
  - Effort estimate (quick-fix / moderate / major)
  - Priority (P1: must fix / P2: should fix / P3: nice to have)

PRIORITIZATION:
  P1: Safety, compliance, or executability gaps (score < 5 on critical dimensions)
  P2: Completeness, measurability, error handling gaps (score 5-7)
  P3: Visual design, accessibility, AI-readiness improvements (score 5-7)

OUTPUT: remediation_plan = [
  { priority, gap_id, fix_description, example, effort, improvement_source }
]

NOTE: improvement_source is REQUIRED for every remediation item.
  Format: [SOURCE: file_path:section] — e.g., [SOURCE: sop-scoring-rubric.yaml:DIM-03]
  VETO-ANL-007 blocks report generation if any improvement_source is empty.
```

### 7. Generate Report

```
ACTION: Compile full analysis report

STRUCTURE:
  # SOP Analysis Report: {SOP Name}

  ## Executive Summary
  - Overall Grade: {grade} ({score}/100)
  - Key Strengths (top 3 dimensions)
  - Critical Gaps (top 3 issues)

  ## Scorecard
  | Dimension | Weight | Score | Weighted | Grade |
  |-----------|--------|-------|----------|-------|
  | Clarity | 10% | X/10 | X.X | A-F |
  | ... | ... | ... | ... | ... |
  | **TOTAL** | **100%** | | **X.X** | **{grade}** |

  ## Dimensional Analysis
  ### 1. Clarity (Score: X/10)
  - Evidence: ...
  - Gaps: ...
  - Recommendation: ...
  [repeat for all 10 dimensions]

  ## Gap Inventory
  | ID | Category | Location | Impact | Fix Priority |
  [all gaps]

  ## Remediation Plan
  ### Priority 1 (Must Fix)
  ...
  ### Priority 2 (Should Fix)
  ...
  ### Priority 3 (Nice to Have)
  ...

  ## Metadata
  - Analyzed: {date}
  - Analyzer: sop-analyst
  - Scoring Mode: {full|quick}
  - SOP Word Count: {count}
  - SOP Step Count: {count}

FILE: outputs/aiox-sop/analysis/{sop-name}-analysis.md
```

## Output

```yaml
outputs:
  primary:
    path: "outputs/aiox-sop/analysis/{sop-name}-analysis.md"
    format: markdown
    description: "Comprehensive analysis report with scorecard, gaps, and remediation plan"

  metadata:
    total_score: "<0-100>"
    grade: "<A|B|C|D|F>"
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
- [ ] Each recommendation includes a concrete example
- [ ] Priorities are assigned (P1/P2/P3) based on impact
- [ ] Executive summary highlights top 3 strengths and top 3 gaps
- [ ] Report includes metadata (date, word count, step count)
- [ ] Every evidence citation follows `[MARKER] file:section` format (per `evidence_standard`)
- [ ] Every remediation has non-empty `improvement_source` field (per VETO-ANL-007)

## Veto Conditions

- STOP if the input file is not an SOP (e.g., it is code, configuration, or unrelated document)
- STOP if the file is empty or contains fewer than 50 words
- STOP if the file format cannot be parsed (corrupted or binary)
- STOP if scoring rubric data file is unavailable and cannot be applied from embedded rubric
- `VETO-ANL-005`: STOP if any scored dimension has zero evidence citations. Every dimension MUST have at least one `[MARKER] file:section` citation. Mirror of `WF-AUDIT-VETO-002`. If you cannot find evidence, score the dimension 0 and mark `[UNK]`.
- `VETO-ANL-006`: STOP if the report contains any invention red flag phrase (see `sop-scoring-rubric.yaml → invention_red_flags`) without an accompanying `[MARKER]` citation on the same finding. Remove the phrase or add a citation.
- `VETO-ANL-007`: STOP if the `improvement_source` field of any remediation recommendation is empty. Every recommendation MUST trace to a specific source: `[SOURCE: file_path:section]`.
- `VETO-ANL-008`: STOP if `scoring_mode=full` and more than 3 dimensions have ONLY `[INF]` evidence (no `[OBS]`, `[DOC]`, `[REP]`, or `[COR]`). Escalate to `scoring_mode=quick` or request additional source material from the user.
