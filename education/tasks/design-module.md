# Task: Design Module

**Task ID:** design-module
**Version:** 1.0
**Agent:** merrill-designer
**Squad:** education

## Purpose
Design a single module using Merrill's First Principles of Instruction (problem-centered, activation, demonstration, application, integration). Produces detailed module design ready for lesson breakdown.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| module_id | string | Yes | Module identifier (e.g., "M01") |
| domain | string | Yes | Course domain |
| curriculum_path | string | Yes | Path to curriculum-master-architecture.md |
| module_scope | string | Yes | Topics covered in this module |

## Preconditions
- [ ] curriculum-master-architecture.md exists
- [ ] Module identified in curriculum plan
- [ ] Learning objectives for module defined

## Steps
1. **Principle 1 - Problem-Centered:**
   - Define real-world problem module solves
   - Show task progression (simple → complex)

2. **Principle 2 - Activation:**
   - Identify prior knowledge to activate
   - Design activation activity (recall, experience, demonstration)

3. **Principle 3 - Demonstration:**
   - Plan what to demonstrate (concepts, procedures)
   - Define demonstration format (video, walkthrough, case study)
   - Include worked examples

4. **Principle 4 - Application:**
   - Design practice tasks (guided → independent)
   - Include corrective feedback mechanisms
   - Define mastery criteria

5. **Principle 5 - Integration:**
   - Plan reflection activities
   - Design creation/sharing tasks (learner demonstrates to peers)
   - Connect to next module

6. Organize into lesson breakdown

## Output
- **Location:** `minds/{domain}/modules/{module-id}/module-design.md`
- **Format:** First Principles structured design
- **Sections:**
  - Problem-Centered (real-world task)
  - Activation (prior knowledge)
  - Demonstration (what to show)
  - Application (practice tasks)
  - Integration (reflection/creation)
  - Lesson Breakdown

## Veto Conditions
- No real-world problem identified → module lacks relevance
- No prior knowledge to activate → need prerequisite module
- Application tasks not aligned to demonstrations → redesign

## Completion Criteria
- [ ] Real-world problem defined
- [ ] Activation activity designed
- [ ] Demonstrations planned
- [ ] Practice tasks created with feedback
- [ ] Integration activities designed
- [ ] Lesson breakdown complete
- [ ] Output saved to module-design.md
