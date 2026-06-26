# Audit Decision Quality

**Task ID:** `dr-audit-decisions`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Audit Decision Quality |
| **status** | `pending` |
| **responsible_executor** | kahneman |
| **execution_type** | `Agent` |
| **input** | All pipeline outputs, reliability audit from ioannidis |
| **output** | Decision audit with bias checklist, MAP protocol, pre-mortem, and verdict |
| **action_items** | 4 steps |
| **acceptance_criteria** | 6 criteria |

## Overview
Agent kahneman audits the overall decision quality of the research pipeline output, applying Kahneman's behavioral economics and decision science frameworks. The audit uses the 12-Question Bias Checklist (from "Thinking, Fast and Slow"), the Mediating Assessments Protocol (MAP) to structure judgment, and a structured pre-mortem to stress-test recommendations. The final verdict determines whether the research output is sound enough to inform real decisions.

## Input
- **all_outputs** (object) - Complete pipeline outputs including Tier 0 (PICO, methodology, design), Tier 1 (all agent findings), and the reliability audit from ioannidis
- **reliability_audit** (object) - PPV scores, bias flags, and evidence classifications from ioannidis

## Output
- **decision_audit** (object) - Contains `bias_checklist_results` (12-question checklist with pass/fail per item), `map_protocol` (mediating assessment scores for key decision dimensions), `pre_mortem` (structured failure scenario analysis), `final_verdict` (SOUND/CAUTION/UNSOUND with justification)
- **noise_assessment** (object) - Evaluation of variability and inconsistency across agent outputs that may indicate decision noise

## Action Items
### Step 1: Apply 12-Question Bias Checklist
Evaluate the pipeline's recommendations against Kahneman's bias checklist:
1. Is there reason to suspect self-serving bias in any agent's output?
2. Have the agents fallen in love with a particular conclusion?
3. Were dissenting opinions within the evidence given adequate weight?
4. Is the evidence base anchored too heavily on an initial data point?
5. Are the agents extrapolating from a narrow set of analogies?
6. Is there evidence of halo effect (one positive finding coloring everything)?
7. Are sunk cost considerations influencing recommendations?
8. Were base rates properly considered?
9. Is the confidence level calibrated to the actual evidence strength?
10. Have worst-case scenarios been adequately explored?
11. Is the recommendation overly optimistic about implementation?
12. Are the agents confusing "what is likely" with "what is desirable"?
Score each question as Pass, Partial, or Fail.

### Step 2: Run Mediating Assessments Protocol (MAP)
Decompose the final recommendation into independent assessable dimensions. For each dimension, score it independently before combining into an overall assessment. This prevents the halo effect from one strong dimension contaminating the overall judgment. Typical dimensions: evidence strength, practical feasibility, risk level, time sensitivity, reversibility of decision.

### Step 3: Conduct Structured Pre-Mortem
Assume the recommended course of action was followed and resulted in failure one year later. Generate the three most plausible failure narratives. For each narrative: describe the failure scenario, trace back the root cause, identify which evidence or reasoning gap enabled it, and suggest what mitigation would have prevented it.

### Step 4: Issue Final Verdict
Based on the bias checklist results, MAP scores, and pre-mortem analysis, issue a verdict:
- **SOUND**: Checklist mostly passes, MAP scores consistent, pre-mortem risks are manageable. Research output is suitable for decision-making.
- **CAUTION**: Some checklist failures or MAP inconsistencies detected. Research output usable with specific caveats listed.
- **UNSOUND**: Critical checklist failures, major MAP inconsistencies, or pre-mortem reveals fundamental flaws. Research output should not inform decisions without additional investigation.

## Acceptance Criteria
- [ ] All 12 bias checklist questions are evaluated with Pass/Partial/Fail scoring
- [ ] MAP protocol decomposes the recommendation into at least four independent dimensions
- [ ] Pre-mortem generates at least three distinct failure scenarios with root cause analysis
- [ ] Final verdict is one of SOUND/CAUTION/UNSOUND with written justification
- [ ] Noise assessment evaluates inter-agent consistency and flags significant variability
- [ ] Kahneman's audit does not merely rubber-stamp ioannidis -- it provides independent judgment

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
