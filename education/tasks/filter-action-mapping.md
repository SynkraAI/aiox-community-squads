# Task: Filter Action Mapping

**Task ID:** filter-action-mapping
**Version:** 1.0
**Agent:** moore-filter
**Squad:** education

## Purpose
Decision gate: "Does this need a course?" Apply Geoffrey Moore's Crossing the Chasm framework to determine if formal education is the right solution or if other interventions work better.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Domain or skill to evaluate |
| business_goal | string | Yes | What outcome is needed |
| audience_profile | string | Yes | Who needs to learn |
| current_state | string | Yes | Current performance/knowledge level |

## Preconditions
- [ ] Business goal is measurable
- [ ] Audience profile is defined
- [ ] Current state documented

## Steps
1. Assess if gap is knowledge vs. motivation vs. environmental
2. Evaluate adoption curve position (innovators, early adopters, majority, laggards)
3. Determine if skill is disruptive or sustaining innovation
4. Check if formal course is best intervention or if job aids/coaching suffice
5. Assess ROI: cost of course development vs. business impact
6. Make recommendation: course, workshop, job aid, or no intervention

## Output
- **Location:** `minds/{domain}/triage-report.md`
- **Format:** Structured recommendation
- **Sections:**
  - Gap Analysis (knowledge/motivation/environment)
  - Adoption Curve Position
  - Recommended Intervention
  - ROI Estimate
  - Go/No-Go Decision

## Veto Conditions
- Gap is primarily motivational, not knowledge-based → recommend incentives instead
- Audience too small to justify course development → recommend coaching
- Skill changes too rapidly for structured course → recommend communities of practice

## Completion Criteria
- [ ] Gap type identified (knowledge/motivation/environment)
- [ ] Adoption curve position assessed
- [ ] Clear recommendation made with justification
- [ ] ROI estimated
- [ ] Go/No-Go decision stated
- [ ] Output saved to triage-report.md
