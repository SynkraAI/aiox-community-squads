# Task: Generate Deliverables

**Task ID:** generate-deliverables
**Version:** 1.0
**Agent:** education-chief
**Squad:** education

## Purpose
Assemble all course components into final deliverable package. Produces complete course ready for production, LMS upload, or MEC submission.

## Executor
**Type:** Script (deterministic — no LLM needed)
**Command:**
```bash
python squads/education/scripts/assemble-deliverables.py \
  --domain "{domain}" \
  --type "{deliverable_type}" \
  --minds-path "{minds_path}"
```

> When executed via dispatch or automation, run the script directly. The Steps section below documents the assembly logic for reference only.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course domain |
| deliverable_type | string | Yes | "production", "lms", "mec-submission", "all" |
| minds_path | string | Yes | Path to minds/{domain}/ directory |

## Preconditions
- [ ] All design documents complete (curriculum, modules, lessons)
- [ ] All validations passed (evidence, compliance, transfer)
- [ ] All schedules generated (practice, review, assessment)

## Steps
1. **Collect All Components:**
   - Curriculum Master Architecture
   - Module designs (all modules)
   - Lesson plans (all lessons)
   - Assessment specifications
   - Practice specifications
   - Review schedules
   - Media specifications
   - ARCS analyses
   - Cognitive load reports
   - Validation reports
   - Compliance reports (if applicable)

2. **Generate Deliverable per Type:**

   **Production Package:**
   - Master curriculum document
   - Lesson-by-lesson production specs
   - Media asset list
   - Assessment items
   - Instructor guides (if applicable)

   **LMS Package:**
   - SCORM/xAPI structure
   - Content sequencing rules
   - Assessment configuration
   - Completion criteria
   - Certificate templates

   **MEC Submission Package:**
   - PPC (Projeto Pedagógico de Curso)
   - Compliance documentation
   - Faculty credentials
   - Facility requirements
   - Assessment plan

3. Create deliverable index (what's included, where to find)
4. Generate quality checklist for deliverable review
5. Package all files into organized structure

## Output
- **Location:** `output/courses/{domain}/`
- **Structure:**
  ```
  {domain}/
  ├── deliverables/
  │   ├── production/
  │   ├── lms/
  │   └── mec-submission/
  ├── source/
  │   ├── curriculum/
  │   ├── modules/
  │   └── lessons/
  ├── assessments/
  ├── media-specs/
  ├── reports/
  └── INDEX.md
  ```

## Veto Conditions
- Any validation failed and not remediated → BLOCK delivery
- MEC compliance report shows failures → BLOCK submission
- Curriculum incomplete (missing modules/lessons) → complete design first

## Completion Criteria
- [ ] All components collected
- [ ] Deliverable packages generated per type
- [ ] INDEX.md complete with all file locations
- [ ] Quality checklist passed
- [ ] Output organized in deliverables/ structure
- [ ] Ready for handoff to production/LMS/MEC
