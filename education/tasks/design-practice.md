# Task: Design Practice

**Task ID:** design-practice
**Version:** 1.0
**Agent:** bjork-engineer, ericsson-coach
**Squad:** education

## Purpose
Design practice activities using Bjork's Desirable Difficulties and Ericsson's Deliberate Practice. Optimizes retention and skill acquisition through spacing, interleaving, variation, and feedback.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lesson_path | string | Yes | Path to lesson design |
| skill_type | string | Yes | "cognitive", "motor", "perceptual" |
| target_mastery | number | Yes | Mastery threshold (0.70-0.95) |
| domain | string | Yes | Course domain |

## Preconditions
- [ ] Lesson design exists
- [ ] Learning objectives measurable
- [ ] Mastery criteria defined

## Steps
1. **Apply Bjork's Desirable Difficulties:**
   - **Spacing:** Distribute practice over time (schedule reviews)
   - **Interleaving:** Mix problem types (don't block by category)
   - **Variation:** Vary practice contexts and examples
   - **Generation:** Make learners retrieve vs. re-read
   - **Contextual Interference:** Introduce complexity gradually

2. **Apply Ericsson's Deliberate Practice:**
   - Define well-defined task at appropriate difficulty
   - Provide informative feedback immediately
   - Allow repetition and error correction
   - Ensure focused attention (minimize distractions)
   - Build on existing knowledge incrementally

3. Design practice sequence:
   - Initial practice (massed, focused)
   - Spaced practice (distributed reviews)
   - Interleaved practice (mixed problem types)
   - Variable practice (different contexts)

4. Define feedback mechanisms:
   - Immediate (during practice)
   - Corrective (what's wrong, how to fix)
   - Formative (progress toward mastery)

5. Set mastery criteria and exit conditions

## Output
- **Location:** `minds/{domain}/modules/{module-id}/lessons/{lesson-id}/practice-spec.md`
- **Format:** Practice design specification
- **Sections:**
  - Practice Sequence (initial/spaced/interleaved/variable)
  - Desirable Difficulties Applied
  - Deliberate Practice Components
  - Feedback Mechanisms
  - Mastery Criteria
  - Review Schedule

## Veto Conditions
- All practice is massed (no spacing) → poor retention guaranteed
- No interleaving → learners can't discriminate problem types
- Feedback absent or delayed >24h → slow learning

## Completion Criteria
- [ ] Practice sequence designed with spacing
- [ ] Interleaving and variation included
- [ ] Feedback mechanisms defined
- [ ] Mastery criteria clear
- [ ] Review schedule specified
- [ ] Output saved to practice-spec.md
