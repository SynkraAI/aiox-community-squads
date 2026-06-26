# Task: Assess Transfer

**Task ID:** assess-transfer
**Version:** 1.0
**Agent:** thalheimer-assessor
**Squad:** education

## Purpose
Validate learning transfer using Thalheimer's LTEM (Learning-Transfer Evaluation Model). Ensures learners can apply knowledge in real-world contexts, not just recall in assessments.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course domain |
| assessment_plan_path | string | Yes | Path to assessment specifications |
| transfer_context | string | Yes | Real-world context where skill will be used |

## Preconditions
- [ ] Assessment plan exists
- [ ] Transfer context defined (where learners apply skills)
- [ ] Performance criteria specified

## Steps
1. **Classify Transfer Distance (LTEM):**
   - Near transfer: Same context as learning
   - Moderate transfer: Similar context, some adaptation
   - Far transfer: Different context, significant adaptation

2. **Design Transfer Assessments:**
   - **Level 1 (Near):** Recognize/recall in training context
   - **Level 2 (Moderate):** Apply with minor adaptation
   - **Level 3 (Far):** Apply in novel situations
   - **Level 4 (Very Far):** Transfer across domains

3. **Validate Assessment Authenticity:**
   - Does assessment match real-world task?
   - Are conditions realistic (time, resources, constraints)?
   - Is performance criterion job-relevant?

4. **Design Transfer Support:**
   - Job aids for near-transfer tasks
   - Coaching for moderate-transfer tasks
   - Communities of practice for far-transfer tasks

5. Generate transfer assessment specifications

## Output
- **Location:** `minds/{domain}/transfer-assessment.md`
- **Format:** LTEM transfer validation
- **Sections:**
  - Transfer Distance Classification
  - Transfer Assessment Levels (1-4)
  - Authenticity Validation
  - Transfer Support Strategies
  - Assessment Specifications
  - Expected Transfer Rates

## Veto Conditions
- All assessments are Level 1 (near transfer only) → learners won't transfer to job
- Transfer context undefined → cannot design authentic assessments
- Performance criteria don't match job requirements → redesign

## Completion Criteria
- [ ] Transfer distance classified
- [ ] Assessments designed across LTEM levels
- [ ] Authenticity validated
- [ ] Transfer support strategies defined
- [ ] Expected transfer rates estimated
- [ ] Output saved to transfer-assessment.md
