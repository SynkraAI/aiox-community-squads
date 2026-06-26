# Changelog

All notable changes to the Education Engineer Squad will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-14

### Added

**Core Architecture**
- Two-layer architecture (permanent pedagogical engine + variable domain minds)
- 6-phase pipeline: Research → Planning → Content → Assessment → Validation → Delivery
- Quality gate system (15 checklists: 10 pedagogical + 5 MEC compliance)

**Agents (16 total)**
- **Tier 0 (Research & Planning):** @bloom-analyst, @wiggins-designer, @schwartz-analyst, @keller-motivator
- **Tier 1 (Content Design):** @mayer-multimedia, @rosenshine-instructor, @bjork-memory, @cathy-moore-action, @clark-engagement
- **Tier 2 (Assessment):** @anderson-assessor, @merrill-validator
- **Tier 3 (Domain):** Domain agent template, Voice template, Avatar template
- **Orchestrator:** @education-chief

**Tasks (21 atomic tasks)**
- `create-course.md` — Full course pipeline
- `create-objectives.md` — Bloom-aligned learning objectives
- `design-architecture.md` — UbD backward design
- `analyze-market.md` — Schwartz awareness/sophistication analysis
- `design-arcs.md` — ARCS motivation strategy
- `create-multimedia.md` — Mayer-compliant multimedia design
- `structure-lesson.md` — Rosenshine lesson plan
- `design-spaced-practice.md` — Bjork spaced repetition schedule
- `create-action-map.md` — Cathy Moore action mapping
- `design-engagement.md` — Clark engagement tactics + LTEM scoring
- `create-assessment.md` — Anderson assessment design
- `validate-lesson.md` — Merrill First Principles validation
- `validate-course.md` — Full pedagogical + compliance audit
- `validate-mec.md` — MEC compliance check
- `generate-ppc.md` — PPC document generation
- `accessibility-audit.md` — WCAG 2.1 AA audit
- `create-domain-agent.md` — Domain expert creation
- `load-domain.md` — Activate existing domain
- `list-domains.md` — Show available domains
- `create-voice-agent.md` — Teaching voice creation
- `create-avatar-agent.md` — Student avatar creation

**Templates (11 YAML templates)**
- `course-tmpl.yaml` — Complete course structure
- `lesson-tmpl.yaml` — Single lesson (7-part model)
- `objectives-tmpl.yaml` — Learning objectives (Bloom 2D matrix)
- `assessment-tmpl.yaml` — Quiz/rubric design
- `arcs-strategy-tmpl.yaml` — ARCS motivation plan
- `action-map-tmpl.yaml` — Performance-based outcomes
- `spaced-schedule-tmpl.yaml` — Review intervals (FSRS algorithm)
- `ppc-tmpl.yaml` — MEC PPC document
- `domain-agent-tmpl.yaml` — Domain expert definition
- `voice-tmpl.yaml` — Teaching voice profile
- `avatar-tmpl.yaml` — Student avatar profile

**Checklists (15 quality checklists)**

*Pedagogical (10):*
- `bloom-alignment.md` — Objectives → Assessments → Content alignment
- `mayer-multimedia.md` — 12 multimedia principles compliance
- `rosenshine-instruction.md` — 10 instruction principles compliance
- `ubd-coherence.md` — Backward design coherence
- `clt-optimization.md` — Cognitive load management
- `bjork-desirable.md` — Spacing, interleaving, retrieval practice
- `arcs-motivation.md` — 4 ARCS dimensions presence
- `action-mapping.md` — Performance outcomes clarity
- `ambrose-7principles.md` — 7 principles of learning
- `ltem-engagement.md` — LTEM tier 5+ validation

*MEC Compliance (5):*
- `mec-course-type.md` — Course type declaration + restrictions
- `mec-accessibility.md` — WCAG 2.1 AA + LIBRAS for videos >5min
- `mec-tutoring.md` — Tutor ratio (1:50), response time (48h max)
- `mec-lms.md` — LMS requirements (tracking, gradebook, support)
- `mec-ppc.md` — PPC completeness validation

**Workflows (4 workflows)**
- `wf-full-pipeline.yaml` — Complete 6-phase course creation (2-4 hours)
- `wf-research-planning.yaml` — Phase 0-1 only (objectives + architecture)
- `wf-lesson-creation.yaml` — Single lesson workflow (15-30 min)
- `wf-validation.yaml` — Quality + compliance audit (10-20 min)

**Knowledge Base (7 files)**
- `education-kb.md` — Complete knowledge base (mission, architecture, frameworks, compliance)
- `lesson-model.md` — 7-part replicable lesson structure
- `bloom-taxonomy-reference.md` — Revised Bloom's Taxonomy (6 levels + 2D matrix + verbs)
- `mayer-12-principles.md` — 12 Multimedia Learning Principles
- `rosenshine-10-principles.md` — 10 Principles of Instruction
- `ltem-8-tiers.md` — LTEM engagement depth scoring
- `README.md` — Squad documentation

**MEC Compliance System**
- Support for 5 course types (100% EAD, Semi-presential, Presential+EAD, Extension, Free)
- Automatic PPC generation (Projeto Pedagógico de Curso)
- WCAG 2.1 AA accessibility validation
- LIBRAS requirement enforcement (videos >5min)
- Tutoring plan validation (1:50 ratio, 48h response time)
- LMS requirements checklist

**Frameworks Integrated (15 total)**
1. Revised Bloom's Taxonomy (Anderson & Krathwohl, 2001)
2. Understanding by Design / UbD (Wiggins & McTighe, 2005)
3. 12 Multimedia Learning Principles (Mayer, 2021)
4. 10 Principles of Instruction (Rosenshine, 2012)
5. Desirable Difficulties (Bjork, 1994)
6. ARCS Model (Keller, 1987)
7. Awareness Levels (Schwartz, 1966)
8. Action Mapping (Cathy Moore, 2008)
9. Engagement Taxonomy (Clark, 2008)
10. Assessment Framework (Anderson, 2001)
11. First Principles of Instruction (Merrill, 2002)
12. 7 Principles of Learning (Ambrose et al., 2010)
13. Cognitive Load Theory (Sweller, 1988)
14. LTEM — Levels of Teaching Engagement (Piotrowski, 2010)
15. FSRS — Free Spaced Repetition Scheduler (Wozniak, 2024)

**Documentation**
- Complete README.md with architecture, agent list, quick start, commands, file structure
- Knowledge base with mission, philosophy, frameworks, glossary, decision trees
- 6 reference files (lesson model, Bloom, Mayer, Rosenshine, LTEM, MEC compliance)
- PRD: `plan/prd/PRD-squad-education-engineer.md`

### Implementation Notes

**Design Principles Applied:**
- CODE > LLM — Instructional design as algorithmic system, not prompt engineering
- Evidence-based — Every decision backed by learning science research
- Compliance-first — MEC regulations embedded in templates and checklists
- Replicable quality — Same input → same output (no variability)
- Two-layer architecture — Permanent engine + variable domain minds

**Quality Standards:**
- 15 quality gates (10 pedagogical + 5 compliance)
- Minimum LTEM score 5.0 (50%+ high-engagement activities)
- Bloom alignment mandatory (objectives → assessments → content)
- All multimedia must pass Mayer's 12 principles
- All lessons must implement Rosenshine's 10 principles

**MEC Compliance:**
- Portaria MEC 2.117/2019 compliance built into system
- 5 course types supported with automatic restriction checking
- PPC template with all required sections
- Accessibility (WCAG 2.1 AA) + LIBRAS enforcement
- Tutoring plan validation (ratio, response time, qualification)

### Known Limitations

- Scripts folder empty (automation scripts planned for v1.1)
- Domain agents must be created manually (no pre-built domains yet)
- MEC compliance specific to Brazilian regulation (international versions planned)
- No LMS integration yet (manual export only)

### Migration Notes

- New squad, no migration needed
- Based on PRD: `plan/prd/PRD-squad-education-engineer.md` (2026-02-14)
- Follows AIOS Framework v3.0 standards

---

## [Unreleased]

### Planned for v1.1
- Automation scripts for batch lesson creation
- Pre-built domain agents (cooking, programming, finance, leadership)
- LMS integration (Moodle, Canvas, Blackboard)
- Analytics dashboard (engagement metrics, completion rates)
- International compliance templates (US accreditation, EU regulations)

### Planned for v1.2
- AI voice cloning for consistent narration
- Automated video editing (Mayer principles compliance)
- Adaptive learning paths (personalized sequencing)
- Gamification layer (achievements, progress tracking)

### Planned for v2.0
- Real-time learner analytics integration
- A/B testing framework for instructional approaches
- Community of practice features (peer teaching, discussion forums)
- Mobile-first lesson templates

---

**Reference:**
- PRD: `plan/prd/PRD-squad-education-engineer.md`
- AIOS Framework: `.aios-core/constitution.md`, `.aios-core/SYSTEM-SPEC.md`
- Squad Standards: `.aios-core/development/agents/README.md`
