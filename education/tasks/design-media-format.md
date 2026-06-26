# Task: Design Media Format

**Task ID:** design-media-format
**Version:** 1.0
**Agent:** mayer-presenter
**Squad:** education

## Purpose
Apply Mayer's Cognitive Theory of Multimedia Learning to make media format decisions. Determines video vs. text vs. interactive, prevents split-attention and redundancy effects.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lesson_path | string | Yes | Path to lesson design |
| content_type | string | Yes | "procedural", "conceptual", "factual", "metacognitive" |
| domain | string | Yes | Course domain |

## Preconditions
- [ ] Lesson design exists
- [ ] Content type classified
- [ ] Cognitive load analysis complete

## Steps
1. **Apply Mayer's Principles:**
   - Multimedia: Use words + pictures (not words alone)
   - Spatial Contiguity: Place text near graphics
   - Temporal Contiguity: Present narration and animation simultaneously
   - Coherence: Exclude extraneous material
   - Modality: Narration + animation > text + animation
   - Redundancy: Avoid narration + on-screen text duplication
   - Signaling: Highlight essential material
   - Personalization: Use conversational style
   - Voice: Human voice > machine voice
   - Image: Don't need instructor's image on screen

2. **Select Format per Content Type:**
   - Procedural → Video demonstration with narration
   - Conceptual → Animated diagrams with narration
   - Factual → Text with supporting images
   - Metacognitive → Reflective text prompts

3. **Design Layout:**
   - Avoid split-attention (integrate text and graphics)
   - Segment complex content
   - Pre-train component knowledge

4. Generate media specifications

## Output
- **Location:** `minds/{domain}/modules/{module-id}/lessons/{lesson-id}/media-spec.md`
- **Format:** Media design specifications
- **Sections:**
  - Format Recommendations (video/text/interactive per segment)
  - Mayer Principles Applied
  - Layout Specifications
  - Production Guidelines
  - Accessibility Considerations

## Veto Conditions
- Violates redundancy principle (narration duplicates on-screen text) → redesign
- Split-attention effect present → integrate text/graphics
- Extraneous content >20% → violates coherence principle

## Completion Criteria
- [ ] Format selected per content type
- [ ] All applicable Mayer principles applied
- [ ] Layout prevents split-attention
- [ ] Production guidelines clear
- [ ] Accessibility considered
- [ ] Output saved to media-spec.md
