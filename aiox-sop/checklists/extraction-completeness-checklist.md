# Extraction Completeness Checklist

> **Purpose:** Verify that a process extraction by @sop-extractor captured all required sections before handoff to @sop-creator or @sop-ml-architect. This is the quality gate between EXTRACTION and CREATION stages.
>
> **Scoring:** All 10 sections must be present. Items below the verification threshold (`0.8`) are flagged in the Gaps section, while average handoff readiness is evaluated at `0.7`.
> - **10/10 sections present:** Ready for handoff
> - **8-9 sections:** Handoff with gaps documented
> - **<8 sections:** Return to extraction -- incomplete

| Field | Value |
|---|---|
| **Checklist ID** | QC-EXTRACT-001 |
| **Purpose** | Verify extraction output completeness before handoff |
| **Process Extracted** | ________________________ |
| **Extraction Method** | Description / Document / Interview / Observation / Logs / Tribal |
| **Extractor** | ________________________ |
| **Extraction Date** | ________________________ |
| **Total Sections** | 10 |

---

## Section Verification

| # | Section | Present | Min Items | Confidence Contract Applied | Notes |
|---|---------|:-------:|:---------:|:---------------------------:|-------|
| 1 | **Process Summary** — Name, purpose, frequency, criticality | [ ] | 4 fields | [ ] | |
| 2 | **Actors & Systems** — Who and what is involved, with roles | [ ] | 1 actor | [ ] | |
| 3 | **Step Sequence** — Numbered steps with confidence scores | [ ] | 3 steps | [ ] | |
| 4 | **Decision Points** — Branching logic with conditions | [ ] | 0 (may not apply) | [ ] | |
| 5 | **Exceptions & Edge Cases** — Known failure modes and workarounds | [ ] | 1 exception | [ ] | |
| 6 | **Tools & Systems** — Required software, hardware, access | [ ] | 1 tool | [ ] | |
| 7 | **Timing Data** — Duration estimates per step (where available) | [ ] | 0 (best effort) | [ ] | |
| 8 | **Gaps & Verification Needed** — Items below confidence threshold | [ ] | 0 (may be empty) | N/A | |
| 9 | **Conflicts** — Contradictory information with sources noted | [ ] | 0 (may be empty) | N/A | |
| 10 | **Source Provenance** — Where each fact came from | [ ] | 1 source | [ ] | |

---

## Confidence Distribution

| Level | Icon | Score | Count | % of Steps |
|-------|:----:|:-----:|:-----:|:----------:|
| Observed | [OBS] | 1.0 | _____ | _____% |
| Documented | [DOC] | 0.9 | _____ | _____% |
| Reported | [REP] | 0.8 | _____ | _____% |
| Corroborated | [COR] | 0.7 | _____ | _____% |
| Inferred | [INF] | 0.5 | _____ | _____% |
| Assumed | [ASM] | 0.3 | _____ | _____% |
| Unknown | [UNK] | 0.1 | _____ | _____% |

**Average Confidence:** _____

> **Rules:** If average confidence is below `0.7`, or if more than `30%` of steps are below `0.8`, recommend additional extraction before handoff.

---

## Handoff Readiness

| Check | Pass | Fail |
|-------|:----:|:----:|
| All 10 sections present (or justified N/A) | [ ] | [ ] |
| Average confidence is at least 0.7 | [ ] | [ ] |
| Every item below 0.8 is listed in Gaps & Verification Needed | [ ] | [ ] |
| All conflicts have both sources documented | [ ] | [ ] |
| Gaps section explicitly lists what needs verification | [ ] | [ ] |
| Target format identified (human-readable / ML / both) | [ ] | [ ] |

**Handoff Decision:**
- [ ] **READY** — Proceed to @sop-creator or @sop-ml-architect
- [ ] **READY WITH GAPS** — Proceed, but gaps must be resolved during creation
- [ ] **INCOMPLETE** — Return to extraction for additional pass

**Extractor Signature:** _________________________ **Date:** _______________

---

*Extraction Completeness Checklist v1.0. Based on Taiichi Ohno's Gemba methodology.*
*Checklist: extraction-completeness-checklist.md | SOP Factory | Synkra AIOX*
