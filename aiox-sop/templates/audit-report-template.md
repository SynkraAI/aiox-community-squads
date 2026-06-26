# SOP Audit Report

> **Template:** audit-report-template.md | SOP Factory | Synkra AIOX
>
> Used by @sop-auditor to produce standardized audit reports after `*audit` execution.
> Fill all `{{placeholders}}` with actual values.

---

## Audit Header

| Field | Value |
|---|---|
| **Report ID** | AUD-{{sequential_number}} |
| **SOP Under Audit** | {{sop_id}} — {{sop_title}} |
| **SOP Version** | {{sop_version}} |
| **Auditor** | Crosby (sop-auditor) |
| **Audit Date** | {{YYYY-MM-DD}} |
| **Audit Type** | {{Initial / Re-Audit / Periodic}} |
| **Previous Audit** | {{previous_report_id or "N/A — Initial Audit"}} |

---

## 14-Point Crosby Assessment

> Reference worksheet: `checklists/14-point-crosby-checklist.md`

| # | Point | Weight | Point Score | Evidence | Finding |
|---|-------|--------|:-----------:|----------|---------|
| 1 | Management Commitment | CRITICAL | {{1/4/7/10}} | {{specific evidence from SOP}} | {{finding or "Conformant"}} |
| 2 | Quality Improvement Team | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 3 | Quality Measurement | CRITICAL | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 4 | Cost of Quality | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 5 | Quality Awareness | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 6 | Corrective Action | CRITICAL | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 7 | Zero Defects Planning | CRITICAL | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 8 | Employee Education | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 9 | Zero Defects Day | MINOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 10 | Goal Setting | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 11 | Error Cause Removal | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 12 | Recognition | MINOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 13 | Quality Councils | MAJOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |
| 14 | Do It Over Again | MINOR | {{1/4/7/10}} | {{evidence}} | {{finding}} |

---

## Nonconformity Register

| ID | Classification | Crosby Point | Description | Required Action | Owner | Due Date |
|----|:-------------:|:------------:|-------------|-----------------|-------|----------|
| NC-001 | {{Critical/Major/Minor/Observation}} | {{#}} | {{description of nonconformity}} | {{specific remediation action}} | {{responsible role}} | {{YYYY-MM-DD}} |
| NC-002 | {{class}} | {{#}} | {{description}} | {{action}} | {{owner}} | {{date}} |

---

## Audit Score

> Source of truth: `data/verdict-thresholds.yaml`

| Component | Weight | Raw Score | Weighted Contribution |
|-----------|:------:|:---------:|:---------------------:|
| Structural | 20% | {{0-100}} | {{score}} |
| Content | 30% | {{0-100}} | {{score}} |
| Compliance | 20% | {{0-100}} | {{score}} |
| Risk | 15% | {{0-100}} | {{score}} |
| Crosby | 15% | {{0-100}} | {{score}} |
| **FINAL SCORE** | **100%** | — | **{{final_score}} / 100** |

| Finding Type | Count |
|---|:---:|
| Critical Open | {{count}} |
| Major Open | {{count}} |
| Minor Open | {{count}} |
| Observations | {{count}} |

---

## VERDICT: {{CERTIFIED / APPROVED / CONDITIONAL / REJECTED}}

{{Verdict explanation. Include:
- Key strengths observed
- Critical gaps requiring attention
- Specific actions required before next stage
- Timeline for remediation if applicable}}

---

## Remediation Tracking

> Complete this section during re-audit or follow-up.

| Finding ID | Original Classification | Status | Closure Evidence | Closed Date |
|:----------:|:----------------------:|:------:|-----------------|:-----------:|
| NC-001 | {{class}} | {{Open/Closed/Regressed}} | {{evidence of fix}} | {{date}} |

---

## Compliance Cross-Reference

> Standards assessed during this audit (if applicable).

| Standard | Clauses Checked | Conformant | Gaps |
|----------|----------------|:----------:|------|
| {{ISO 9001 / FDA / GMP / etc.}} | {{clause numbers}} | {{Yes/Partial/No}} | {{gap description}} |

---

## Auditor Notes

{{Free-form notes, observations not captured in formal findings, recommendations for next revision cycle.}}

---

**Auditor Signature:** _________________________ **Date:** _______________

---

*Audit Report Template v1.0. Based on Philip Crosby's 14-point framework and ISO 19011 audit methodology.*
*Template: audit-report-template.md | SOP Factory | Synkra AIOX*
