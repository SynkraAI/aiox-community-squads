# Task: Design Curriculum

**Task ID:** design-curriculum
**Version:** 1.0
**Agent:** wiggins-architect
**Squad:** education

## Purpose
Apply Understanding by Design (backward design) to create Curriculum Master Architecture. Starts with desired results, determines acceptable evidence, then plans learning experiences.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course domain |
| competency_matrix_path | string | Yes | Path to competency-matrix.md |
| knowledge_map_path | string | Yes | Path to knowledge-map.md |
| duration_hours | number | Yes | Total course hours |

## Preconditions
- [ ] competency-matrix.md exists
- [ ] knowledge-map.md exists
- [ ] Learning objectives defined and measurable

## Steps
1. **Stage 1 - Identify Desired Results:**
   - Load competency matrix and knowledge map
   - Define enduring understandings (big ideas that persist)
   - Define essential questions (drive inquiry)
   - List knowledge and skills students will acquire

2. **Stage 2 - Determine Acceptable Evidence:**
   - Design performance tasks (authentic assessments)
   - Design other evidence (quizzes, observations, work samples)
   - Set evaluation criteria per task

3. **Stage 3 - Plan Learning Experiences:**
   - Organize into modules (logical chunks)
   - Sequence modules (prerequisites, dependencies)
   - Allocate hours per module
   - Define learning activities (WHERETO framework)

4. Generate Curriculum Master Architecture document

## Output
- **Location:** `minds/{domain}/curriculum-master-architecture.md`
- **Format:** UbD-structured curriculum plan
- **Sections:**
  - Stage 1: Desired Results
  - Stage 2: Acceptable Evidence
  - Stage 3: Learning Plan
  - Module Overview Table
  - Hour Allocation
  - Assessment Map

## Veto Conditions
- Learning objectives not measurable → cannot design evidence
- Total hours insufficient for competency matrix → reduce scope
- Module sequence has circular dependencies → redesign structure

## Completion Criteria
- [ ] Enduring understandings defined
- [ ] Essential questions stated
- [ ] Performance tasks designed
- [ ] Evidence types mapped to objectives
- [ ] Modules sequenced logically
- [ ] Hours allocated per module
- [ ] Output saved to curriculum-master-architecture.md
