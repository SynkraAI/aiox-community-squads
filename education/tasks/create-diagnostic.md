# Task: Create Diagnostic

**Task ID:** create-diagnostic
**Version:** 1.0
**Agent:** bloom-diagnostician
**Squad:** education

## Purpose
Create diagnostic assessment to determine learner's current level and place them in appropriate course path. Uses Bloom taxonomy to assess existing competencies.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course domain |
| competency_matrix_path | string | Yes | Path to competency-matrix.md |
| placement_levels | list | Yes | Available course paths (e.g., ["beginner", "intermediate", "advanced"]) |

## Preconditions
- [ ] competency-matrix.md exists
- [ ] Placement levels defined
- [ ] Placement criteria per level specified

## Steps
1. Load competency matrix
2. Select key concepts that discriminate between levels
3. Design diagnostic items per concept:
   - Test at lowest Bloom level needed for each placement
   - Beginner track: Remember/Understand
   - Intermediate track: Apply/Analyze
   - Advanced track: Evaluate/Create

4. Create placement algorithm:
   - Define passing scores per level
   - Handle edge cases (between levels)
   - Provide placement recommendations with confidence

5. Design diagnostic format (quiz, task, interview)
6. Set time limits and administration rules
7. Generate diagnostic assessment document

## Output
- **Location:** `minds/{domain}/diagnostic-assessment.md`
- **Format:** Diagnostic assessment specification
- **Sections:**
  - Diagnostic Items (questions/tasks)
  - Bloom Level per Item
  - Placement Algorithm
  - Scoring Rubric
  - Placement Criteria
  - Administration Instructions

## Veto Conditions
- Diagnostic cannot discriminate between levels → redesign items
- Placement criteria overlap → clarify boundaries
- Diagnostic too long (>30min) → reduce scope

## Completion Criteria
- [ ] Diagnostic items designed for key concepts
- [ ] Items test appropriate Bloom levels
- [ ] Placement algorithm defined
- [ ] Scoring rubric complete
- [ ] Administration instructions clear
- [ ] Output saved to diagnostic-assessment.md
