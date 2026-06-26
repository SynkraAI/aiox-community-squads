# Task: Re-Audit SOP

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `re-audit` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-auditor` |
| **Execution Type** | `Hybrid` |

## Metadata
```yaml
id: re-audit
name: "Re-Audit SOP"
category: audit
agent: sop-auditor
elicit: false
autonomous: true
description: "Re-run SOP audit after remediation, compare before/after findings, and determine closure status."
```

## Purpose

Verify whether remediation actions closed previous nonconformities.
This task compares a fresh audit with a baseline audit and confirms if the SOP can move forward.

## Inputs

```yaml
inputs:
  sop_file:
    type: filepath
    required: true
  previous_audit_report:
    type: filepath
    required: true
  strict_mode:
    type: boolean
    required: false
    default: true
```

## Workflow / Steps

### 1. Load Baseline

```
ACTION:
  - Read previous audit report
  - Extract open findings, severity, and prior score
```

### 2. Execute Current Audit Snapshot

```
ACTION:
  - Re-run audit checks on current SOP version
  - Capture new score, verdict, and open findings
```

### 3. Compare Delta

```
ACTION:
  - For each previous finding:
    * CLOSED when evidence now satisfies requirement
    * OPEN when issue remains
    * REGRESSED when quality worsened
  - Identify new findings introduced after remediation
```

### 4. Determine Re-Audit Outcome

```
OUTCOME:
  - PASS when all critical+major findings are closed
  - CONDITIONAL when only minor findings remain
  - FAIL when critical/major findings remain or regressions appear
```

### 5. Produce Re-Audit Report

```
OUTPUT:
  - before_after_score
  - findings_closed/open/regressed
  - final_outcome
  - remaining_actions
```

## Acceptance Criteria

- [ ] Every baseline finding has explicit closure/open/regression status
- [ ] Final outcome is consistent with severity rules
- [ ] Report includes before/after traceability to both audit artifacts
