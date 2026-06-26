# Task: Adapt Progression

**Task ID:** adapt-progression
**Version:** 1.0
**Agent:** education-chief
**Squad:** education

## Purpose
Adjust learning path based on diagnostic results. Creates personalized curriculum progression that skips mastered content and reinforces weak areas.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| diagnostic_results | object | Yes | Learner's diagnostic assessment results |
| curriculum_path | string | Yes | Path to curriculum-master-architecture.md |
| placement_level | string | Yes | Recommended placement level |
| domain | string | Yes | Course domain |

## Preconditions
- [ ] diagnostic-assessment.md exists
- [ ] Diagnostic completed and scored
- [ ] curriculum-master-architecture.md exists

## Steps
1. Load diagnostic results and curriculum architecture
2. Identify mastered concepts (no instruction needed)
3. Identify weak areas (need reinforcement)
4. Identify gaps (concepts not yet assessed)
5. Generate adapted curriculum:
   - Skip modules for mastered concepts
   - Add practice/review for weak areas
   - Adjust sequence if prerequisites missing

6. Recalculate course duration based on adaptations
7. Create personalized learning path document
8. Define checkpoints for reassessment

## Output
- **Location:** `minds/{domain}/learners/{learner-id}/adapted-curriculum.md`
- **Format:** Personalized curriculum plan
- **Sections:**
  - Diagnostic Summary
  - Mastered Concepts (skipped)
  - Weak Areas (reinforcement plan)
  - Adapted Module Sequence
  - Adjusted Duration
  - Reassessment Checkpoints
  - Personalized Learning Path

## Veto Conditions
- Diagnostic results incomplete → cannot adapt
- Too many gaps (>50% concepts unknown) → recommend prerequisite course
- Placement level conflicts with diagnostic → reassess placement

## Completion Criteria
- [ ] Mastered concepts identified and skipped
- [ ] Weak areas identified with reinforcement plan
- [ ] Module sequence adapted
- [ ] Duration recalculated
- [ ] Reassessment checkpoints defined
- [ ] Output saved to adapted-curriculum.md
