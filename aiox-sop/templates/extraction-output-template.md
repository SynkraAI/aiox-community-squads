# SOP Extraction Output

> **Template:** extraction-output-template.md | SOP Factory | Synkra AIOX
>
> Produced by @sop-extractor after process extraction. This is the handoff artifact
> consumed by @sop-creator (human SOP) or @sop-ml-architect (ML SOP).
> Fill all `{{placeholders}}` with actual values.

---

## Extraction Header

| Field | Value |
|---|---|
| **Extraction ID** | EXT-{{sequential_number}} |
| **Process Name** | {{process_name}} |
| **Extraction Date** | {{YYYY-MM-DD}} |
| **Extractor** | Ohno (sop-extractor) |
| **Extraction Method** | {{Description / Document / Interview / Observation / Logs / Tribal}} |
| **Source Material** | {{brief description of sources used}} |
| **Target Format** | {{Human-Readable / ML / Both}} |
| **Average Confidence** | {{X.XX}} |

---

## 1. Process Summary

| Field | Value |
|---|---|
| **Name** | {{process_name}} |
| **Purpose** | {{what this process accomplishes}} |
| **Frequency** | {{how often: daily / weekly / on-demand / event-triggered}} |
| **Criticality** | {{low / medium / high / critical}} |
| **Typical Duration** | {{end-to-end time estimate}} |
| **Trigger** | {{what initiates this process}} |
| **Completion Indicator** | {{how you know it is done}} |

---

## 2. Actors & Systems

| Actor/System | Type | Role in Process | Access Required |
|---|---|---|---|
| {{name}} | {{Human / System / Agent}} | {{what they do}} | {{permissions needed}} |

---

## 3. Step Sequence

> Confidence markers: `[OBS] 1.0` | `[DOC] 0.9` | `[REP] 0.8` | `[COR] 0.7` | `[INF] 0.5` | `[ASM] 0.3` | `[UNK] 0.1`

| # | Step | Actor | Tool/System | Expected Result | Conf. | Source |
|---|------|-------|-------------|-----------------|:-----:|--------|
| 1 | {{action in imperative mood}} | {{role}} | {{tool}} | {{what success looks like}} | {{[OBS]/[DOC]/[REP]/[COR]/[INF]/[ASM]/[UNK]}} | {{source reference}} |
| 2 | {{action}} | {{role}} | {{tool}} | {{result}} | {{conf}} | {{source}} |
| 3 | {{action}} | {{role}} | {{tool}} | {{result}} | {{conf}} | {{source}} |

---

## 4. Decision Points

| At Step | Condition | Branch A (if true) | Branch B (if false) | Conf. | Source |
|:-------:|-----------|---------------------|---------------------|:-----:|--------|
| {{#}} | {{condition to evaluate}} | {{action / goto step}} | {{action / goto step}} | {{conf}} | {{source}} |

> If no decision points exist, state: "No decision points identified in this process."

---

## 5. Exceptions & Edge Cases

| ID | Trigger / Symptom | Frequency | Current Workaround | Severity | Conf. |
|----|-------------------|-----------|--------------------|---------:|:-----:|
| EX-01 | {{what goes wrong}} | {{rare / occasional / frequent}} | {{how it is handled today}} | {{low/med/high/critical}} | {{conf}} |

---

## 6. Tools & Systems

| Tool/System | Version | Purpose in Process | Required/Optional | Access Request Method |
|---|---|---|---|---|
| {{name}} | {{version or N/A}} | {{what it does in the process}} | {{Required / Optional}} | {{how to get access}} |

---

## 7. Timing Data

| Step # | Estimated Duration | Variability | Notes |
|:------:|:------------------:|:-----------:|-------|
| {{#}} | {{PTxM}} | {{low / medium / high}} | {{any timing notes}} |

**Total Estimated Duration:** {{sum or range}}

> If timing data is unavailable, state: "Timing data not captured in this extraction. Recommend time-motion study."

---

## 8. Gaps & Verification Needed

> Items below the verification threshold (`0.8` by default) that require validation before SOP creation.

| Item | Current Confidence | What Is Missing | Recommended Verification Method |
|------|:------------------:|-----------------|-------------------------------|
| {{step or fact}} | {{score}} | {{what evidence would raise confidence}} | {{interview / observation / test / document review}} |

---

## 9. Conflicts

> Contradictory information found across sources. Both versions documented for resolution.

| Conflict ID | Topic | Version A | Source A | Version B | Source B | Resolution |
|:-----------:|-------|-----------|----------|-----------|----------|:----------:|
| C-01 | {{what conflicts}} | {{version}} | {{source}} | {{version}} | {{source}} | {{Pending / Resolved: version chosen}} |

> If no conflicts found, state: "No conflicting information identified across sources."

---

## 10. Source Provenance

| Source ID | Type | Description | Date | Reliability |
|:---------:|------|-------------|------|:-----------:|
| SRC-01 | {{Document / Interview / Observation / Log / Tribal}} | {{description}} | {{date}} | {{High / Medium / Low}} |

---

## Handoff Summary

| Check | Status |
|-------|:------:|
| All 10 sections populated | {{Yes / No (list missing)}} |
| Average confidence ≥ 0.7 | {{Yes / No (actual: X.XX)}} |
| All items below 0.8 listed in Gaps | {{Yes / No}} |
| Conflicts resolved or documented | {{Yes / No}} |
| Gaps explicitly listed | {{Yes / No}} |
| Target format identified | {{Human / ML / Both}} |

**Handoff Decision:** {{READY / READY WITH GAPS / INCOMPLETE}}

**Handoff To:** {{@sop-creator / @sop-ml-architect / Both}}

---

**Extractor Signature:** _________________________ **Date:** _______________

---

*Extraction Output Template v1.0. Based on Taiichi Ohno's Gemba methodology.*
*Template: extraction-output-template.md | SOP Factory | Synkra AIOX*
