# Task: Design Lesson

**Task ID:** design-lesson
**Version:** 1.0
**Agent:** merrill-designer, rosenshine-teacher
**Squad:** education

## Purpose
Design a single lesson combining Merrill's First Principles and Rosenshine's Principles of Instruction. Produces detailed lesson plan ready for content production.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lesson_id | string | Yes | Lesson identifier (e.g., "M01L01") |
| module_path | string | Yes | Path to module-design.md |
| domain | string | Yes | Course domain |
| duration_minutes | number | Yes | Lesson duration |

## Preconditions
- [ ] module-design.md exists
- [ ] Lesson scope defined in module breakdown
- [ ] Learning objectives for lesson clear

## Steps
1. **Review & Prime (Rosenshine):**
   - Daily review of prior learning
   - Prime for new content

2. **Present New Material (Rosenshine + Merrill Demonstration):**
   - Teach in small steps
   - Model procedures
   - Use worked examples
   - Ask questions to check understanding

3. **Guided Practice (Rosenshine + Merrill Application):**
   - Practice under supervision
   - Immediate corrective feedback
   - High success rate (80%+)

4. **Check for Understanding:**
   - Formative assessment
   - Address misconceptions

5. **Independent Practice (Merrill Application):**
   - Practice without scaffolding
   - Distributed practice over time

6. **Weekly/Monthly Review (Rosenshine):**
   - Plan spaced review schedule

7. Define lesson materials, media, assessments

## Output
- **Location:** `minds/{domain}/modules/{module-id}/lessons/{lesson-id}.md`
- **Format:** Lesson plan template
- **Sections:**
  - Lesson Overview
  - Learning Objectives
  - Review & Prime (5-10%)
  - New Material Presentation (20-30%)
  - Guided Practice (30-40%)
  - Check for Understanding (10%)
  - Independent Practice (20-30%)
  - Materials List
  - Assessment Criteria

## Veto Conditions
- New material presentation >40% of lesson → too much cognitive load
- Guided practice <30% → insufficient scaffolding
- No formative assessment → cannot check understanding

## Completion Criteria
- [ ] All Rosenshine principles applied
- [ ] Review, present, practice, assess cycle complete
- [ ] Materials list complete
- [ ] Assessment criteria defined
- [ ] Timing allocated per section
- [ ] Output saved to lesson plan
