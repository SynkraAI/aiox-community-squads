# Task: Design Motivation

**Task ID:** design-motivation
**Version:** 1.0
**Agent:** keller-motivator
**Squad:** education

## Purpose
Apply Keller's ARCS Model (Attention, Relevance, Confidence, Satisfaction) to each module. Ensures learner motivation is designed in, not assumed.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| module_path | string | Yes | Path to module-design.md |
| domain | string | Yes | Course domain |
| audience_profile | string | Yes | Learner characteristics |

## Preconditions
- [ ] module-design.md exists
- [ ] Audience profile includes motivational factors
- [ ] Module content finalized

## Steps
1. **Attention Strategies:**
   - Perceptual arousal (surprise, incongruity, conflict)
   - Inquiry arousal (questions, problem-solving)
   - Variability (format changes, unpredictability)

2. **Relevance Strategies:**
   - Goal orientation (link to learner goals)
   - Motive matching (achievement, affiliation, power)
   - Familiarity (use learner experiences)

3. **Confidence Strategies:**
   - Learning requirements (clear expectations)
   - Success opportunities (achievable challenges)
   - Personal control (learner choice, autonomy)

4. **Satisfaction Strategies:**
   - Natural consequences (authentic outcomes)
   - Positive consequences (praise, recognition)
   - Equity (fair treatment, consistent standards)

5. Map ARCS strategies to specific module moments

## Output
- **Location:** `minds/{domain}/modules/{module-id}/arcs-analysis.md`
- **Format:** ARCS strategy mapping
- **Sections:**
  - Attention Strategies (with specific tactics)
  - Relevance Strategies (with examples)
  - Confidence Strategies (with scaffolding plan)
  - Satisfaction Strategies (with rewards)
  - ARCS Integration Map (when each strategy activates)

## Veto Conditions
- No relevance strategy identified → learners won't see value
- Confidence strategies absent → learners will feel overwhelmed
- Satisfaction only extrinsic → no intrinsic motivation

## Completion Criteria
- [ ] All four ARCS components addressed
- [ ] Specific tactics defined per component
- [ ] Strategies mapped to module timeline
- [ ] Balance of intrinsic/extrinsic motivation
- [ ] Output saved to arcs-analysis.md
