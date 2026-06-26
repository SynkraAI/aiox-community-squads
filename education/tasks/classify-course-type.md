# Task: Classify Course Type

**Task ID:** classify-course-type
**Version:** 1.0
**Agent:** mec-compliance
**Squad:** education

## Purpose
Classify course into MEC categories (livre, FIC, técnico, graduação, pós-graduação) to determine regulatory requirements. Brazil-specific compliance gate.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course subject matter |
| duration_hours | number | Yes | Total course hours |
| certification_intent | string | Yes | "none", "completion", "professional", "academic" |
| target_audience | string | Yes | Audience education level |

## Preconditions
- [ ] Course scope defined
- [ ] Duration estimated
- [ ] Certification intent clear

## Steps
1. Load MEC classification criteria
2. Check duration thresholds (livre <160h, FIC 160h+, técnico 800h+, etc.)
3. Check certification requirements (livre=certificate of completion, FIC=professional qualification, etc.)
4. Determine regulatory category
5. Load applicable requirements for that category
6. Document classification rationale

## Output
- **Location:** `minds/{domain}/mec-classification.md`
- **Format:** Classification + requirements checklist
- **Sections:**
  - MEC Category
  - Classification Rationale
  - Regulatory Requirements
  - Compliance Checklist

## Veto Conditions
- Course duration ambiguous or undefined
- Certification intent conflicts with duration (e.g., wants diploma but <160h)
- Domain requires specific accreditation not available

## Completion Criteria
- [ ] MEC category determined (livre/FIC/técnico/graduação/pós)
- [ ] Classification rationale documented
- [ ] Regulatory requirements listed
- [ ] Compliance checklist generated
- [ ] Output saved to mec-classification.md
