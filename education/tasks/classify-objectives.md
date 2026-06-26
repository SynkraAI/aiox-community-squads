# Task: Classify Objectives

**Task ID:** classify-objectives
**Version:** 1.0
**Agent:** bloom-diagnostician
**Squad:** education

## Purpose
Classify learning objectives using Bloom's Taxonomy (revised) and set mastery thresholds per cognitive level. Produces competency matrix for assessment design.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course domain |
| knowledge_map_path | string | Yes | Path to knowledge-map.md |
| target_mastery_level | string | Yes | "remember", "understand", "apply", "analyze", "evaluate", "create" |

## Preconditions
- [ ] knowledge-map.md exists
- [ ] Core concepts identified
- [ ] Target mastery level realistic for audience and duration

## Steps
1. Load knowledge map
2. For each concept, write learning objective with measurable verb
3. Classify objective into Bloom level (Remember → Create)
4. Set mastery threshold per level (e.g., Remember=90%, Create=70%)
5. Align assessment types to levels (Remember=quiz, Apply=task, Create=project)
6. Generate competency matrix: concept × Bloom level × mastery threshold
7. Validate progression is logical (don't skip levels)

## Output
- **Location:** `minds/{domain}/competency-matrix.md`
- **Format:** Table + explanations
- **Sections:**
  - Learning Objectives (with measurable verbs)
  - Bloom Classification per objective
  - Mastery Thresholds
  - Assessment Alignment
  - Competency Matrix Table

## Veto Conditions
- Objectives not measurable (e.g., "understand" without behavior)
- Target mastery level unrealistic for audience (beginners → "create")
- Mastery thresholds set too low (<70%) or too high (>95%)

## Completion Criteria
- [ ] All objectives written with measurable verbs
- [ ] Each objective classified into Bloom level
- [ ] Mastery thresholds set per level
- [ ] Assessment types aligned
- [ ] Competency matrix complete
- [ ] Output saved to competency-matrix.md
