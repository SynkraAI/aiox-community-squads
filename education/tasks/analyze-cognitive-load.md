# Task: Analyze Cognitive Load

**Task ID:** analyze-cognitive-load
**Version:** 1.0
**Agent:** sweller-analyst
**Squad:** education

## Purpose
Analyze cognitive load (intrinsic, extraneous, germane) for each lesson using Sweller's Cognitive Load Theory. Prevents overwhelming learners and optimizes instructional design.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lesson_path | string | Yes | Path to lesson design document |
| audience_expertise | string | Yes | "novice", "intermediate", "expert" |
| domain | string | Yes | Course domain |

## Preconditions
- [ ] Lesson design exists
- [ ] Audience expertise level defined
- [ ] Content complexity assessed

## Steps
1. Load lesson design
2. Assess intrinsic load (complexity inherent to content)
3. Assess extraneous load (cognitive effort from poor design)
4. Assess germane load (effort toward schema construction)
5. Calculate total cognitive load per lesson segment
6. Identify overload risks (total load > working memory capacity)
7. Recommend load reduction strategies (worked examples, scaffolding, chunking)
8. Suggest optimal lesson duration based on load

## Output
- **Location:** `minds/{domain}/lessons/{lesson-id}/cognitive-load-report.md`
- **Format:** CLT analysis report
- **Sections:**
  - Intrinsic Load Assessment
  - Extraneous Load Assessment
  - Germane Load Assessment
  - Total Load per Segment
  - Overload Risks
  - Load Reduction Recommendations
  - Optimal Duration

## Veto Conditions
- Total cognitive load exceeds working memory capacity → BLOCK lesson as designed
- Extraneous load > germane load → redesign required
- Intrinsic load too high for audience expertise → split lesson

## Completion Criteria
- [ ] All three load types assessed per segment
- [ ] Total load calculated
- [ ] Overload risks identified
- [ ] Reduction strategies recommended
- [ ] Optimal duration suggested
- [ ] Output saved to cognitive-load-report.md
