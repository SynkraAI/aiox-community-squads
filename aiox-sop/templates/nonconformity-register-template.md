# Nonconformity Register

> **Template:** nonconformity-register-template.md | SOP Factory | Synkra AIOX
>
> Tracks all nonconformities found during SOP audit by @sop-auditor.
> One register per SOP, persisted across audit cycles for traceability.
> Used by `*audit`, `*re-audit`, and `*certify` commands.

---

## Register Header

| Field | Value |
|---|---|
| **Register ID** | NCR-{{sop_id}} |
| **SOP** | {{sop_id}} — {{sop_title}} |
| **Created** | {{YYYY-MM-DD}} |
| **Last Updated** | {{YYYY-MM-DD}} |
| **Status** | {{Active / All Closed / Archived}} |

---

## Classification Guide

| Class | Definition | SOP Impact | SLA |
|-------|-----------|------------|-----|
| **Critical** | Poses immediate risk to safety, compliance, or business continuity | STOP — Cannot release | 7 days |
| **Major** | Significant gap reducing SOP effectiveness or compliance | HOLD — Release delayed | 14 days |
| **Minor** | Small gap that does not significantly impact execution | NOTE — Release with tracking | 30 days |
| **Observation** | Improvement opportunity, not a nonconformity | LOG — Next revision cycle | N/A |

---

## Findings

| ID | Class | Crosby Point | Audit Date | Description | Evidence | Root Cause | Required Action | Owner | Due Date | Status | Closure Evidence | Closed Date |
|----|:-----:|:------------:|:----------:|-------------|----------|------------|-----------------|-------|:--------:|:------:|-----------------|:-----------:|
| NC-001 | {{class}} | {{#}} | {{date}} | {{description}} | {{where in SOP}} | {{why it exists}} | {{specific fix}} | {{role}} | {{date}} | {{Open/In Progress/Closed/Regressed}} | {{evidence}} | {{date}} |
| NC-002 | {{class}} | {{#}} | {{date}} | {{description}} | {{evidence}} | {{cause}} | {{action}} | {{role}} | {{date}} | {{status}} | {{evidence}} | {{date}} |

---

## Summary Statistics

| Metric | Initial Audit | Re-Audit 1 | Re-Audit 2 |
|--------|:------------:|:----------:|:----------:|
| **Audit Date** | {{date}} | {{date}} | {{date}} |
| Critical Open | {{count}} | {{count}} | {{count}} |
| Major Open | {{count}} | {{count}} | {{count}} |
| Minor Open | {{count}} | {{count}} | {{count}} |
| Observations | {{count}} | {{count}} | {{count}} |
| **Total Open** | {{count}} | {{count}} | {{count}} |
| **Audit Score** | {{score}}% | {{score}}% | {{score}}% |
| **Verdict** | {{verdict}} | {{verdict}} | {{verdict}} |

---

## Trend

```
Audit 1: [{{score}}%] {{verdict}}
         Critical: {{n}} | Major: {{n}} | Minor: {{n}}
              ↓
Audit 2: [{{score}}%] {{verdict}}
         Critical: {{n}} | Major: {{n}} | Minor: {{n}}
         Closed: {{n}} | New: {{n}} | Regressed: {{n}}
```

---

## Closure Rules

- **Critical/Major:** Requires re-audit by @sop-auditor with evidence
- **Minor:** Can be closed by SOP owner with evidence, verified in next periodic audit
- **Observation:** Closed when addressed in next SOP revision
- **Regressed:** Automatically escalated one classification level (Minor → Major)

---

**Register Owner:** _________________________ **Last Review:** _______________

---

*Nonconformity Register Template v1.0. Based on ISO 9001:2015 clause 10.2 and Crosby Zero Defects.*
*Template: nonconformity-register-template.md | SOP Factory | Synkra AIOX*
