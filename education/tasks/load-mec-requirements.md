# Task: Load MEC Requirements

**Task ID:** load-mec-requirements
**Version:** 1.0
**Agent:** mec-compliance
**Squad:** education

## Purpose
Load and document all MEC requirements for the classified course type. Provides complete checklist for compliance validation.

## Executor
**Type:** Script (deterministic — no LLM needed)
**Command:**
```bash
python squads/education/scripts/load-mec-reqs.py \
  --category "{mec_category}" \
  --domain "{domain}" \
  [--ead]
```

> When executed via dispatch or automation, run the script directly. The Steps section below documents the compilation logic for reference only.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| mec_category | string | Yes | livre/FIC/técnico/graduação/pós |
| domain | string | Yes | Course domain |

## Preconditions
- [ ] mec-classification.md exists
- [ ] MEC category determined
- [ ] squads/education/data/mec-requirements/ contains reference docs

## Steps
1. Load MEC requirements document for category
2. Extract mandatory requirements (non-negotiable)
3. Extract recommended requirements (best practices)
4. Identify domain-specific requirements (if regulated profession)
5. Generate compliance checklist
6. Document required documentation for MEC submission (if applicable)

## Output
- **Location:** `minds/{domain}/mec-requirements.md`
- **Format:** Structured requirements document
- **Sections:**
  - Mandatory Requirements
  - Recommended Requirements
  - Domain-Specific Requirements
  - Required Documentation
  - Compliance Checklist

## Veto Conditions
- MEC category not recognized
- Domain is regulated profession but no authorization to operate
- Requirements cannot be met with available resources

## Completion Criteria
- [ ] All mandatory requirements listed
- [ ] Recommended requirements listed
- [ ] Domain-specific requirements identified
- [ ] Required documentation enumerated
- [ ] Compliance checklist complete
- [ ] Output saved to mec-requirements.md
