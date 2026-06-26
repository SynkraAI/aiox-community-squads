# Task: Compliance Check

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `compliance-check` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-auditor` |
| **Execution Type** | `Hybrid` |

## Metadata
```yaml
id: compliance-check
name: "Compliance Check"
category: audit
agent: sop-auditor
elicit: false
autonomous: true
description: "Validate an SOP against a specific compliance standard (ISO 9001, FDA/GMP, or OSHA) and return requirement-level pass/fail evidence."
```

## Purpose

Run a focused compliance gate without executing the full multi-dimensional audit.
Useful when the main question is: "Does this SOP satisfy standard X right now?"

## Inputs

```yaml
inputs:
  sop_file:
    type: filepath
    required: true
  standard:
    type: enum
    required: true
    options: [iso-9001, fda-gmp, osha]
```

## Workflow / Steps

### 1. Parse SOP

```
ACTION:
  - Read SOP file
  - Extract sections, metadata, controls, and error-handling blocks
```

### 2. Load Requirement Set

```
ACTION:
  - Select requirement set by standard
  - Build checklist with ID + rule + evidence expectations
```

### 3. Evaluate Requirement-by-Requirement

```
ACTION:
  - For each requirement:
    * PASS when explicit evidence exists
    * FAIL when evidence absent
    * PARTIAL when weak/incomplete evidence exists
```

### 4. Output Compliance Report

```
OUTPUT:
  - compliance_score (0-100)
  - pass_count / fail_count / partial_count
  - failed_requirements[]
  - remediation_actions[]
```

## Acceptance Criteria

- [ ] Every requirement has explicit evidence or explicit fail reason
- [ ] Compliance score is reproducible from checklist counts
- [ ] Report includes prioritized remediation actions
