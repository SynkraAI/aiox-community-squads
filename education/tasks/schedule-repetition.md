# Task: Schedule Repetition

**Task ID:** schedule-repetition
**Version:** 1.0
**Agent:** fsrs-scheduler
**Squad:** education

## Purpose
Generate spaced repetition schedule using FSRS (Free Spaced Repetition Scheduler) algorithm. Optimizes long-term retention with personalized review intervals.

## Executor
**Type:** Script (deterministic — no LLM needed)
**Command:**
```bash
python squads/education/scripts/fsrs-scheduler.py \
  --domain "{domain}" \
  --concepts "{concepts_file}" \
  --duration {course_duration_days} \
  --retention {target_retention}
```

> When executed via dispatch or automation, run the script directly. The Steps section below documents the algorithm logic for reference only.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Course domain |
| concepts | list | Yes | List of concepts to schedule |
| course_duration_days | number | Yes | Total course duration |
| target_retention | number | No | Desired retention rate (default: 0.90) |

## Preconditions
- [ ] Concepts identified and prioritized
- [ ] Course duration defined
- [ ] FSRS parameters configured (or use defaults)

## Steps
1. Load concepts list with difficulty estimates
2. Initialize FSRS scheduler with parameters:
   - Target retention rate (default: 90%)
   - Maximum interval (default: 365 days)
   - Initial intervals (based on concept difficulty)

3. For each concept:
   - Calculate initial review interval
   - Generate spaced review schedule (Day 1, 3, 7, 14, 30, 60...)
   - Adjust intervals based on concept difficulty

4. Optimize schedule to fit course duration
5. Identify review checkpoints (end of week, module, course)
6. Generate review activity specifications per checkpoint
7. Plan post-course review schedule (optional)

## Output
- **Location:** `minds/{domain}/review-schedule.md`
- **Format:** FSRS review schedule
- **Sections:**
  - Concept Review Intervals (per concept)
  - Review Checkpoints (dates + concepts)
  - Review Activity Specs (format, duration, criteria)
  - Post-Course Schedule (optional)
  - FSRS Parameters Used

## Veto Conditions
- Course duration too short for minimum spacing → extend course or reduce concepts
- Target retention unrealistic (>95%) → adjust expectations
- Too many concepts for available time → prioritize/reduce

## Completion Criteria
- [ ] All concepts scheduled with FSRS intervals
- [ ] Review checkpoints identified
- [ ] Review activities specified
- [ ] Schedule fits within course duration
- [ ] FSRS parameters documented
- [ ] Output saved to review-schedule.md
