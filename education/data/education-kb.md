# Education Engineer Squad — Knowledge Base

> Complete reference for the Education Engineer Squad: mission, architecture, frameworks, compliance, and agent pipeline.

---

## Mission & Philosophy

**What we do:** Transform domain expertise into pedagogically sound, legally compliant online courses using evidence-based instructional design.

**Core Philosophy:**
- **CODE > LLM** — Instructional algorithms, not prompt engineering
- **Evidence-based** — Every decision backed by learning science (Mayer, Rosenshine, Wiggins & McTighe, Bjork, etc.)
- **Compliance-first** — MEC regulations baked into every template and checklist
- **Replicable quality** — Same input = same high-quality output, every time
- **Two-layer architecture** — Permanent pedagogical engine + variable domain minds

**Not a course authoring tool.** We are an instructional design system that produces courses as a byproduct of applying learning science rigorously.

---

## Two-Layer Architecture

```
LAYER 1: PERMANENT ENGINE (never changes)
├── Pedagogical frameworks (Bloom, Mayer, Rosenshine, UbD, CLT, etc.)
├── Instructional algorithms (lesson model, assessment design, engagement tactics)
├── Quality checklists (10 pedagogical + 5 MEC compliance)
└── Templates (11 YAML templates for all deliverables)

LAYER 2: VARIABLE DOMAIN MINDS (changes per course)
├── Domain Expert (subject matter authority)
├── Teaching Voice (tone, examples, analogies)
├── Student Avatar (learner profile, prior knowledge, goals)
└── Context (market, regulations, delivery constraints)
```

**Implication:** Same engine applied to cooking, programming, finance, or leadership → consistently excellent courses in different domains.

---

## Agent Pipeline Overview

**Phase 0: Research & Planning**
- @bloom-analyst → Learning objectives (6 cognitive levels)
- @wiggins-designer → Backward design (UbD framework)
- @schwartz-analyst → Market sophistication & awareness levels
- @keller-motivator → ARCS motivation strategy

**Phase 1: Content Design**
- @mayer-multimedia → Multimedia principles (12 principles)
- @rosenshine-instructor → Direct instruction tactics (10 principles)
- @bjork-memory → Spaced repetition & retrieval (FSFS, interleaving)
- @cathy-moore-action → Action mapping (performance vs. information)
- @clark-engagement → Engagement patterns (cognitive, emotional, behavioral)

**Phase 2: Assessment & Validation**
- @anderson-assessor → Assessment design (aligned to objectives)
- @merrill-validator → First Principles validation (5 principles)

**Phase 3: Orchestration**
- @education-chief → Pipeline orchestration, quality gates, compliance validation

**Phase 4-6: Execution (Tier 2 — Domain-Specific)**
- Domain Expert agents activated per course (cooking, programming, finance, etc.)
- Teaching Voice agents (conversational, academic, motivational)
- Student Avatar agents (beginner, intermediate, professional)

---

## Key Frameworks Summary

| Mind | Framework | What It Does | When to Use |
|------|-----------|--------------|-------------|
| **Bloom** | Revised Bloom's Taxonomy (2001) | Classify objectives by cognitive level (Remember → Create) | Every learning objective |
| **Wiggins & McTighe** | Understanding by Design (UbD) | Backward design: outcomes → assessment → instruction | Course architecture |
| **Mayer** | 12 Multimedia Principles | Reduce extraneous load, manage essential, foster generative | All visual/video content |
| **Rosenshine** | 10 Principles of Instruction | Direct instruction tactics (chunking, modeling, practice) | Lesson structure |
| **Bjork** | Desirable Difficulties | Spaced practice, interleaving, retrieval practice | Assessment design, lesson sequencing |
| **Keller** | ARCS Model | Attention, Relevance, Confidence, Satisfaction | Motivation strategy |
| **Schwartz** | Market Sophistication | Awareness levels (1-5) + sophistication stages | Messaging, hooks, positioning |
| **Cathy Moore** | Action Mapping | Performance-based design (what they DO, not what they know) | Practical courses, corporate training |
| **Clark** | Engagement Taxonomy | Cognitive, emotional, behavioral engagement patterns | Interaction design |
| **Anderson** | Assessment Framework | Align assessments to objectives (knowledge dimensions × cognitive processes) | Quiz design, rubrics |
| **Merrill** | First Principles | Task-centered, activation, demonstration, application, integration | Lesson validation |
| **Ambrose** | 7 Principles of Learning | Prior knowledge, organization, motivation, practice, feedback, climate, self-direction | Quality checklist |
| **Sweller** | Cognitive Load Theory (CLT) | Intrinsic, extraneous, germane load optimization | Content sequencing, multimedia |
| **Piotrowski** | LTEM (8 tiers) | Engagement depth scoring (1-8 scale) | Engagement validation |
| **Wozniak** | FSRS (spaced repetition) | Optimal review intervals based on difficulty & stability | Flashcard systems, review schedules |

---

## MEC Compliance Overview

**5 Course Types (Portaria MEC 2.117/2019):**

| Type | EAD % | Presential % | Approval Required | Key Restrictions |
|------|-------|---------------|-------------------|------------------|
| **100% EAD** | 100% | 0% | Yes (e-MEC) | Health/Engineering forbidden |
| **Semi-presential** | 40% | 60% | No (notify only) | Practical activities presential |
| **Presential with EAD** | 20% | 80% | No | Minimum 80% presential |
| **Extension** | 100% | 0% | No | < 360h, no diploma |
| **Free courses** | 100% | 0% | No | No MEC regulation |

**Critical Compliance Rules:**
- Accessibility mandatory (WCAG 2.1 AA, LIBRAS for videos >5min)
- Virtual library required (3 titles per discipline, digital access)
- Tutoring mandatory (1 tutor per 50 students, max 48h response)
- LMS with attendance tracking, gradebook, student support
- Course project (PPC) with objectives, methodology, evaluation, bibliography
- Final evaluation presential (for diploma courses)

**Output:** Every course generated includes MEC compliance checklist + PPC template.

---

## Replicable Lesson Model

**7-Part Structure (applies to every lesson):**

1. **Hook Initial (2-3 min)** — Keller ARCS (attention) + Schwartz awareness match
2. **Core Concept** — Rosenshine (present small chunks) + Mayer (signaling)
3. **Structured Explanation** — Mayer (coherence, modality) + Bloom (understand level)
4. **Analogies & Examples** — Mayer (personalization) + Rosenshine (provide examples)
5. **Guided Application** — Rosenshine (guided practice) + Bloom (apply level)
6. **Independent Exercise** — Bjork (retrieval practice) + Anderson (assessment alignment)
7. **Strategic Recap** — Bjork (spacing effect) + Rosenshine (weekly/monthly review)

**Timing:** 15-25 min per lesson (research-backed optimal attention span for adults).

---

## Quality Gates (Non-Negotiable)

Every deliverable passes through:

**Pedagogical Validation (10 checklists):**
1. Bloom alignment (objectives → assessments → content)
2. Mayer multimedia compliance (12 principles)
3. Rosenshine instruction tactics (10 principles)
4. UbD backward design coherence
5. CLT optimization (cognitive load managed)
6. Bjork desirable difficulties (spacing, interleaving, retrieval)
7. ARCS motivation presence (all 4 dimensions)
8. Action mapping (performance outcomes clear)
9. Ambrose 7 principles (holistic learning)
10. LTEM engagement depth (tier 5+ target)

**MEC Compliance (5 checklists):**
1. Course type declaration + restrictions check
2. Accessibility (WCAG 2.1 AA, LIBRAS)
3. Tutoring plan (ratio, response time, qualification)
4. LMS requirements (tracking, gradebook, support)
5. PPC completeness (objectives, methodology, evaluation, bibliography)

**Failure at any gate = BLOCK. No exceptions.**

---

## Agent Responsibility Map

| Need | Agent | Tier | Frameworks |
|------|-------|------|------------|
| Define learning objectives | @bloom-analyst | 0 | Bloom Taxonomy |
| Backward design architecture | @wiggins-designer | 0 | UbD |
| Market positioning | @schwartz-analyst | 0 | Awareness/Sophistication |
| Motivation strategy | @keller-motivator | 0 | ARCS |
| Multimedia design | @mayer-multimedia | 1 | 12 Principles |
| Lesson structure | @rosenshine-instructor | 1 | 10 Principles |
| Spaced repetition | @bjork-memory | 1 | Desirable Difficulties |
| Performance outcomes | @cathy-moore-action | 1 | Action Mapping |
| Engagement tactics | @clark-engagement | 1 | Engagement Taxonomy |
| Assessment design | @anderson-assessor | 2 | Assessment Framework |
| Quality validation | @merrill-validator | 2 | First Principles |
| Orchestration | @education-chief | — | All frameworks |

---

## Glossary

**UbD (Understanding by Design):** Backward design framework — start with desired outcomes, then design assessments, then instruction.

**CLT (Cognitive Load Theory):** Optimize intrinsic (inherent difficulty), reduce extraneous (poor design), maximize germane (schema building) load.

**ARCS:** Attention, Relevance, Confidence, Satisfaction — 4 dimensions of learner motivation (Keller).

**LTEM:** Levels of Teaching Engagement Model — 8-tier engagement depth scale (1=passive, 8=creation).

**FSRS (Free Spaced Repetition Scheduler):** Modern algorithm for optimal review intervals (replaces SM-2).

**Action Mapping:** Design courses around what learners DO, not what they know (Cathy Moore).

**Desirable Difficulties:** Learning techniques that feel harder but produce better retention (Bjork) — spacing, interleaving, retrieval.

**Germane Load:** Cognitive load dedicated to schema construction (good load to maximize).

**Extraneous Load:** Cognitive load from poor instructional design (bad load to minimize).

**PPC (Projeto Pedagógico de Curso):** Course pedagogical project — required MEC document with objectives, methodology, evaluation criteria, bibliography.

**WCAG 2.1 AA:** Web Content Accessibility Guidelines — international standard for digital accessibility (MEC requirement).

**LIBRAS:** Brazilian Sign Language — required for videos >5min in MEC-regulated courses.

---

## Quick Start Decision Tree

**I need to...**

| Task | Command | Agent(s) |
|------|---------|----------|
| Create full course from domain | `*create-course {domain}` | @education-chief (orchestrates all) |
| Design learning objectives | `*create-objectives {topic}` | @bloom-analyst |
| Structure course architecture | `*design-course {objectives}` | @wiggins-designer |
| Create one lesson | `*create-lesson {objective}` | @rosenshine-instructor + @mayer-multimedia |
| Design assessment | `*create-assessment {objective}` | @anderson-assessor |
| Validate engagement | `*validate-engagement {lesson}` | @clark-engagement + @merrill-validator |
| Check MEC compliance | `*validate-mec {course-type}` | @education-chief |
| Generate PPC document | `*generate-ppc {course}` | @education-chief |

---

## File Structure Quick Reference

```
squads/education/
├── agents/           # 16 agent definitions (Tier 0-2 + Chief)
├── tasks/            # 21 atomic tasks
├── templates/        # 11 YAML templates
├── checklists/       # 15 quality checklists
├── workflows/        # 4 workflows
├── data/             # This KB + 6 reference files
├── scripts/          # Automation scripts (TBD)
└── docs/             # Research, methodology docs
```

---

## Version

**Education Engineer Squad v1.0.0** (2026-02-14)

Reference: `plan/prd/PRD-squad-education-engineer.md`
