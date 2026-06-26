# Protocol: SOP ↔ Workflow Integration

## Protocol Anatomy

| Field | Value |
|-------|-------|
| **Protocol ID** | `sop-workflow-integration` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Owners** | `sop-chief` (analysis), `squad-chief` (implementation) |
| **Created** | `2026-03-25` |

## Purpose

Define the integration protocol between the **SOP Factory** (`aiox-sop` squad) and the **Squad Creator** (`squad-creator` squad) for bidirectional quality management of workflows. This protocol establishes:

1. **When** to use each pipeline
2. **Handoff contracts** between squads
3. **Interface format** (the gap report YAML)
4. **Responsibilities** per squad
5. **PDCA cycle** for continuous improvement

## Scope

| In Scope | Out of Scope |
|----------|-------------|
| Workflow YAML quality analysis | SOP creation from scratch |
| Gap report generation and consumption | Workflow efficiency optimization (see `optimize-workflow`) |
| SOP-to-workflow conversion | Agent creation or modification |
| Cross-squad handoff protocol | Task-level analysis (use `analyze-sop` for tasks) |

## Responsibility Matrix

| Activity | sop-chief | squad-chief | User |
|----------|-----------|-------------|------|
| Analyze workflow quality | **Executes** (via sop-analyst) | — | Requests |
| Generate gap report | **Produces** | **Consumes** | Reviews |
| Implement workflow fixes | — | **Executes** | Approves |
| Re-audit after fixes | **Executes** | — | Reviews |
| Create workflow from SOP | Routes to squad-chief | **Executes** | Provides SOP |
| Version and release workflow | — | **Executes** | Approves |

## Pipelines

### Pipeline A: Analyze & Improve Existing Workflow

**Trigger:** User wants to assess and improve workflow quality.

```
Step 1: User → @sop-chief *analyze-workflow {workflow-path}
  ├─ sop-chief routes to sop-analyst
  ├─ sop-analyst loads workflow-quality-rubric.yaml
  ├─ sop-analyst executes analyze-workflow.md (7 steps)
  └─ OUTPUT: outputs/aiox-sop/workflow-analysis/{name}-gap-report.yaml

Step 2: sop-chief presents scorecard + top gaps to user

Step 3: User → @squad-chief *improve-workflow-from-report {gap-report-path}
  ├─ squad-chief loads gap report
  ├─ squad-chief creates backup
  ├─ squad-chief applies P1/P2 fixes
  ├─ squad-chief validates post-edit workflow
  └─ OUTPUT: Updated workflow + diff report

Step 4 (optional): User → @sop-chief *analyze-workflow {workflow-path}
  └─ Re-audit to confirm score improvement
```

**Handoff Contract (Step 1 → Step 3):**
- **Format:** YAML following `workflow-gap-report-tmpl.yaml`
- **Location:** `outputs/aiox-sop/workflow-analysis/{name}-gap-report.yaml`
- **Contains:** scorecard, gaps[], remediation[] with target_file and target_section
- **Consumer guarantee:** squad-chief reads gaps[] and remediation[] directly

### Pipeline B: Create Workflow from SOP

**Trigger:** User has a documented SOP and wants an executable workflow.

```
Step 1: User → @sop-chief *create-workflow-from-sop {sop-path} {target-squad}
  ├─ sop-chief validates SOP exists
  └─ sop-chief routes to @squad-chief

Step 2: squad-chief executes create-workflow-from-sop.md
  ├─ Extracts phases, steps, quality gates, RACI from SOP
  ├─ Maps to workflow-tmpl.yaml schema
  ├─ Assigns agents from target squad
  ├─ Creates checkpoints from quality gates
  └─ OUTPUT: squads/{target-squad}/workflows/wf-{derived-name}.yaml

Step 3: Auto-QA via analyze-workflow (scoring_mode: quick)
  ├─ sop-analyst scores the generated workflow
  ├─ If score >= 70: PASS
  ├─ If score < 70: squad-chief applies top P1 fixes
  └─ OUTPUT: gap report (for reference)
```

**Handoff Contract (Step 1 → Step 2):**
- **Format:** Plain message with sop_file path and target_squad name
- **Routing:** sop-chief → squad-chief (direct handoff)

### Pipeline C: Continuous Quality Cycle (PDCA)

**Trigger:** Ongoing quality management of all squad workflows.

```
PLAN:   @sop-chief *analyze-workflow {workflow}
        → Identifies current quality level and gaps

DO:     @squad-chief *improve-workflow-from-report {gap-report}
        → Implements improvements based on gap report

CHECK:  @sop-chief *analyze-workflow {workflow}
        → Re-audits to confirm score improvement
        → Compare pre/post scores

ACT:    Version workflow, update changelog
        → Document lessons learned
        → Feed findings into next cycle
```

**Cycle Cadence:**
- **Reactive:** Run Pipeline A when workflow quality issues are reported
- **Proactive:** Run Pipeline C quarterly for all critical workflows
- **On creation:** Run Pipeline B auto-QA for every new workflow from SOP

## Handoff Interface: Gap Report YAML

The gap report is the **formal contract** between the two squads. Its structure is defined in `workflow-gap-report-tmpl.yaml`.

### Key Fields for Handoff

| Field | Producer (sop-analyst) | Consumer (squad-chief) |
|-------|----------------------|----------------------|
| `report.workflow_analyzed` | Sets path to analyzed workflow | Uses to locate target file |
| `report.overall.score` | Calculates weighted composite | Uses as pre-improvement baseline |
| `report.gaps[]` | Detects and categorizes all gaps | Reads to understand what needs fixing |
| `report.gaps[].location` | Specifies phase_id or section | Uses to locate edit target |
| `report.gaps[].suggested_fix` | Proposes fix based on rubric | Uses as fix specification |
| `report.remediation[]` | Prioritizes fixes (P1/P2/P3) | Implements in priority order |
| `report.remediation[].target_file` | Sets path to workflow | Uses to apply edits |
| `report.remediation[].target_section` | Identifies section to modify | Uses to locate edit point |
| `report.remediation[].improvement_source` | Traces to rubric evidence | Preserves in diff report |

### Validation Rules

The gap report MUST satisfy these conditions before handoff:

1. Valid YAML syntax
2. `report.workflow_analyzed` points to an existing file
3. Every `remediation[].improvement_source` is non-empty (VETO-ANL-007)
4. Every `scorecard[].evidence` has at least 1 valid marker citation (VETO-ANL-005)
5. Zero invention red flag phrases without citations (VETO-ANL-006)

## Commands Reference

### sop-chief Commands

| Command | Pipeline | Action |
|---------|----------|--------|
| `*analyze-workflow <path>` | A, C | Route to sop-analyst for 10-dimension quality analysis |
| `*create-workflow-from-sop <sop> <squad>` | B | Route to squad-chief for SOP-to-workflow conversion |

### squad-chief Commands

| Command | Pipeline | Action |
|---------|----------|--------|
| `*improve-workflow-from-report <path>` | A, C | Apply improvements from gap report |
| `*create-workflow-from-sop <sop>` | B | Generate workflow from SOP |

## Quality Standards

### Analysis Quality (sop-analyst)
- Minimum 2 evidence citations per dimension (full mode)
- All citations use `[MARKER] file:section` format
- Zero invention red flags
- Improvement sources traced to rubric dimensions

### Implementation Quality (squad-chief)
- Backup before any modification (VETO-IWR-001)
- Post-edit validation passes (YAML, reachability, no cycles)
- No fixes beyond what the gap report specifies (VETO-IWR-003)
- Version bump with changelog entry

## Artifacts Reference

| Artifact | Squad | Path |
|----------|-------|------|
| Workflow Quality Rubric | aiox-sop | `squads/aiox-sop/data/workflow-quality-rubric.yaml` |
| Gap Report Template | aiox-sop | `squads/aiox-sop/templates/workflow-gap-report-tmpl.yaml` |
| Analyze Workflow Task | aiox-sop | `squads/aiox-sop/tasks/analyze-workflow.md` |
| Improve Workflow Task | squad-creator | `squads/squad-creator/tasks/improve-workflow-from-report.md` |
| Create from SOP Task | squad-creator | `squads/squad-creator/tasks/create-workflow-from-sop.md` |
| Workflow Template | squad-creator | `squads/squad-creator/templates/workflow-tmpl.yaml` |
| Optimize Workflow | squad-creator-pro | `squads/squad-creator-pro/tasks/optimize-workflow.md` |

## Relationship to optimize-workflow

`optimize-workflow` and this integration protocol are **complementary, not overlapping**:

| Aspect | optimize-workflow | sop-workflow-integration |
|--------|-------------------|--------------------------|
| **Focus** | EFFICIENCY (cost, speed, parallelization) | QUALITY (clarity, completeness, compliance) |
| **Dimensions** | 6 efficiency dimensions (D1-D6) | 10 quality dimensions (WD-01 to WD-10) |
| **Output** | Optimization report + applied changes | Gap report YAML + applied fixes |
| **When to use** | Workflow works but costs too much or is slow | Workflow structure is incomplete or unclear |
| **Executor** | squad-chief (single squad) | sop-analyst → squad-chief (cross-squad) |

**Recommended sequence:** Quality first (this protocol), then efficiency (`optimize-workflow`). Fix structural issues before optimizing cost.
