# Task: Analyze Squad SOPs

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `analyze-squad` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-analyst` |
| **Execution Type** | `Agent` |

## Metadata
```yaml
id: analyze-squad
name: "Analyze Squad SOPs"
category: analysis
agent: sop-analyst
elicit: false
autonomous: true
description: "Squad-level SOP analysis: discovers all SOPs in a squad, runs individual analyses, detects cross-SOP patterns, and produces a squad health dashboard with aggregated scores and systemic recommendations."
```

## Purpose

Evaluate the overall SOP quality of a squad by analyzing its tasks and workflows as a collection. Unlike `analyze-sop` (single document) or `audit-batch` (compliance audit), this task focuses on cross-SOP pattern detection, systemic gaps, and squad-level health metrics.

This is the task that should have existed when the analyst was asked "analyze the copy squad." Without it, the analyst improvised without structure. This task provides that structure.

## Prerequisites

- [ ] Squad directory exists and contains at least one SOP (task or workflow)
- [ ] Scoring rubric (`sop-scoring-rubric.yaml`) accessible
- [ ] Confidence levels (`confidence-levels.yaml`) accessible
- [ ] `analyze-sop` task definition accessible (used for individual analyses)

## Evidence Format Standard

All evidence rules from `analyze-sop.md` apply here. Every score MUST have citations.

**Citation Format:** `[MARKER] file:section — "observação ou texto citado"`

**Valid markers:** `[OBS]`, `[DOC]`, `[REP]`, `[COR]`, `[INF]` (score >= 0.5)
**Invalid for scoring:** `[ASM]`, `[UNK]`
**Minimum per dimension:** full=2, quick=1

**Reference:** `sop-scoring-rubric.yaml → evidence_standard`

## Invention Red Flags

Same rules as `analyze-sop.md`. No red flag phrase without `[MARKER]` citation.

**Reference:** `sop-scoring-rubric.yaml → invention_red_flags`

## Inputs

```yaml
inputs:
  squad_path:
    type: filepath
    required: true
    description: "Path to the squad root directory (e.g., squads/copy/)"

  scan_scope:
    type: enum
    required: false
    default: all
    options: [tasks, workflows, all]
    description: >
      tasks: Only scan tasks/ directory.
      workflows: Only scan workflows/ directory.
      all: Scan both tasks/ and workflows/.

  sampling:
    type: enum
    required: false
    default: full
    options: [full, stratified]
    description: >
      full: Analyze every SOP found.
      stratified: Select 1 SOP per artifact type (the one with highest word count).
```

## Workflow / Steps

### 1. Discover Squad Artifacts

```
ACTION: Scan squad directory for analyzable SOPs

SCAN directories based on scan_scope:
  - tasks/    → *.md files
  - workflows/ → *.yaml, *.yml files

EXCLUDE:
  - README.md, README files
  - Files < 100 bytes (stubs, placeholders)
  - Files starting with underscore (_) or dot (.)
  - Non-SOP files (pure data, config, schemas)

DETECT per file:
  - word_count
  - format (markdown, yaml)
  - category (task, workflow, checklist)

OUTPUT: artifact_inventory = {
  total_found: <count>,
  included: [{ path, word_count, format, category }],
  excluded: [{ path, reason }]
}

CHECK: VETO-SQD-001 if total included == 0
```

### 2. Apply Sampling Strategy

```
ACTION: Select SOPs for analysis based on sampling mode

IF sampling == "full":
  selected = all included artifacts

IF sampling == "stratified":
  FOR EACH category (task, workflow, checklist):
    selected += artifact with highest word_count in that category

OUTPUT: analysis_queue = [{ path, word_count, format, category }]
```

### 3. Individual Analysis Loop

```
ACTION: Run analyze-sop (quick mode) on each selected SOP

FOR EACH sop in analysis_queue:
  1. Execute analyze-sop with scoring_mode=quick
  2. All VETO conditions (005-008) apply per individual analysis
  3. Record: { sop_path, scores, grade, gap_count, evidence_citations }

IF any individual analysis triggers VETO-ANL-005:
  - Mark that SOP as "VETO: score without evidence"
  - Do NOT include its scores in aggregation (VETO-SQD-002)
  - Log the VETO in the final report

OUTPUT: individual_results = [{
  sop_path, dimension_scores, total_score, grade,
  gaps[], evidence_citations[], veto_triggered: bool
}]
```

### 4. Cross-SOP Pattern Detection

```
ACTION: Identify systemic patterns across all individual results

ANALYZE:
  a) Consistently Low Dimensions
     - Dimensions scoring < 5 in > 50% of SOPs
     - These indicate systemic squad-level issues

  b) Missing Sections Across SOPs
     - Sections absent in > 50% of analyzed SOPs
     - E.g., no Error Handling in any task

  c) Systemic Red Flags
     - invention_red_flag phrases found across multiple SOPs
     - Recurring gap categories (MISSING, AMBIGUOUS, etc.)

  d) Evidence Quality Distribution
     - Count of [OBS], [DOC], [REP], [COR], [INF] across all analyses
     - Percentage of high-confidence ([OBS]+[DOC]) vs low-confidence ([INF])

IMPORTANT: Every cross-SOP claim MUST list which specific SOPs were verified.
  Format: "Dimension X scores < 5 in: sop-a.md (3.2), sop-b.md (4.1), sop-c.md (2.8)"
  CHECK: VETO-SQD-003 if any cross-SOP claim lacks specific SOP references.

OUTPUT: patterns = {
  weak_dimensions: [{ dimension, avg_score, affected_sops[] }],
  missing_sections: [{ section, affected_sops[] }],
  red_flags: [{ phrase, occurrences, sops[] }],
  evidence_distribution: { obs: N, doc: N, rep: N, cor: N, inf: N }
}
```

### 5. Squad Health Aggregation

```
ACTION: Calculate squad-level health metrics

CALCULATE:
  - squad_average_score: mean of all non-vetoed individual scores
  - dimension_heatmap: per-dimension average across all SOPs
  - strongest_dimension: highest average
  - weakest_dimension: lowest average
  - grade_distribution: { A: N, B: N, C: N, D: N, F: N }
  - sop_count_analyzed: total analyzed (excluding vetoed)
  - sop_count_vetoed: total that triggered VETOs

OUTPUT: health = {
  squad_average_score, squad_grade,
  dimension_heatmap, strongest, weakest,
  grade_distribution, analyzed_count, vetoed_count
}
```

### 6. Squad-Level Recommendations

```
ACTION: Generate prioritized recommendations for squad improvement

PRIORITIZE by systemic impact:
  P1: Issues affecting > 75% of SOPs (systemic, fix template/process)
  P2: Issues affecting 50-75% of SOPs (common, fix in batch)
  P3: Issues affecting < 50% of SOPs (individual, fix per SOP)

FOR EACH recommendation:
  - Specific action description
  - Affected SOPs list
  - Expected score impact
  - improvement_source: [SOURCE: file_path:section] (REQUIRED, VETO-ANL-007)

OUTPUT: recommendations = [{
  priority, description, affected_sops[],
  expected_impact, improvement_source
}]
```

### 7. Generate Squad Report

```
ACTION: Compile full squad analysis report

STRUCTURE:
  # Squad Analysis Report: {squad_name}

  ## Executive Summary
  - Squad Health Score: {score}/100 ({grade})
  - SOPs Analyzed: {count} of {total_found}
  - SOPs Vetoed (insufficient evidence): {vetoed_count}
  - Strongest Dimension: {name} ({score})
  - Weakest Dimension: {name} ({score})

  ## Squad Health Dashboard
  | Dimension | Avg Score | Strongest SOP | Weakest SOP |
  [heatmap data]

  ## Grade Distribution
  | Grade | Count | SOPs |
  [distribution data]

  ## Individual SOP Scores
  | SOP | Score | Grade | Top Gap | Evidence Count |
  [per-SOP summary]

  ## Cross-SOP Patterns
  ### Systemic Weaknesses
  [patterns with specific SOP references]
  ### Missing Sections
  [common gaps]

  ## Recommendations
  ### P1 — Systemic (Fix process/template)
  [with improvement_source]
  ### P2 — Common (Batch fix)
  [with improvement_source]
  ### P3 — Individual (Per-SOP fix)
  [with improvement_source]

  ## Evidence Summary
  [marker distribution across all analyses]

  ## Metadata
  - Squad Path: {path}
  - Scan Scope: {scope}
  - Sampling: {mode}
  - Date: {date}
  - Analyst: sop-analyst

FILE: outputs/aiox-sop/analysis/{squad-name}-squad-analysis.md
```

## Output

```yaml
outputs:
  primary:
    path: "outputs/aiox-sop/analysis/{squad-name}-squad-analysis.md"
    format: markdown
    description: "Squad-level analysis report with health dashboard, cross-SOP patterns, and systemic recommendations"

  metadata:
    squad_average_score: "<0-100>"
    squad_grade: "<A|B|C|D|F>"
    sops_analyzed: "<number>"
    sops_vetoed: "<number>"
    total_gaps: "<number>"
    systemic_issues: "<number>"
```

## Acceptance Criteria

- [ ] All discovered SOPs are listed (included and excluded with reasons)
- [ ] Each individual SOP analysis follows `analyze-sop` task rules
- [ ] Every dimension score has evidence citations in `[MARKER] file:section` format
- [ ] Cross-SOP pattern claims reference specific SOPs by name
- [ ] Squad health score is calculated as mean of non-vetoed individual scores
- [ ] Dimension heatmap shows per-dimension averages across all SOPs
- [ ] Every recommendation has non-empty `improvement_source`
- [ ] Vetoed SOPs are logged but excluded from aggregated scores
- [ ] Report includes evidence summary with marker distribution
- [ ] Grade distribution matches individual SOP grades

## Veto Conditions

- `VETO-SQD-001`: STOP if zero analyzable SOPs are found in the scan. The squad path may be wrong or the directory may contain only non-SOP files.
- `VETO-SQD-002`: STOP if any individual analysis triggers `VETO-ANL-005` (score without evidence). That SOP's scores MUST NOT enter the aggregated report. Log the VETO and continue with remaining SOPs. If ALL SOPs are vetoed, HALT entirely.
- `VETO-SQD-003`: STOP if any cross-SOP claim (pattern, systemic weakness, missing section) does not list which specific SOPs were verified. Every aggregate claim requires explicit SOP references.
