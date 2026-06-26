# Task: Validate MEC Compliance

**Task ID:** validate-mec-compliance
**Version:** 1.0
**Agent:** mec-compliance
**Squad:** education

## Purpose
Validate complete course design (PPC - Projeto Pedagógico de Curso) against MEC requirements. Final compliance gate before course publication.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ppc_path | string | Yes | Path to complete course design document |
| mec_requirements_path | string | Yes | Path to mec-requirements.md |

## Preconditions
- [ ] mec-requirements.md exists
- [ ] Complete course design (PPC) exists
- [ ] All curriculum components finalized

## Steps
1. Load MEC requirements checklist
2. Load complete course design (PPC)
3. Validate each mandatory requirement
4. Check recommended requirements
5. Verify required documentation present
6. Identify compliance gaps
7. Generate compliance report with pass/fail per requirement
8. Provide remediation plan for failures

## Output
- **Location:** `minds/{domain}/mec-compliance-report.md`
- **Format:** Compliance audit report
- **Sections:**
  - Compliance Summary (pass/fail)
  - Mandatory Requirements Validation
  - Recommended Requirements Status
  - Compliance Gaps
  - Remediation Plan
  - Final Verdict (approved/needs-revision)

## Veto Conditions
- Any mandatory requirement failed → BLOCK publication
- Required documentation missing → BLOCK submission
- Domain-specific regulations not met → BLOCK launch

## Completion Criteria
- [ ] All mandatory requirements validated
- [ ] Recommended requirements assessed
- [ ] Compliance gaps documented
- [ ] Remediation plan provided (if gaps exist)
- [ ] Final verdict stated
- [ ] Output saved to mec-compliance-report.md
