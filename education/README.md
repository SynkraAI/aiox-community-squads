# 🎓 Education Engineer Squad

> Transform domain expertise into pedagogically sound, legally compliant online courses using evidence-based instructional design.

**Version:** 1.0.0
**Status:** Production
**PRD:** `plan/prd/PRD-squad-education-engineer.md`

---

## What This Squad Does

The Education Engineer Squad is an **instructional design system** that produces online courses by applying learning science rigorously and systematically.

**Core Philosophy:**
- **CODE > LLM** — Instructional algorithms, not prompt engineering
- **Evidence-based** — Every decision backed by research (Mayer, Rosenshine, Wiggins & McTighe, Bjork, Keller)
- **Compliance-first** — MEC regulations baked into templates and checklists
- **Replicable quality** — Same input = same high-quality output, every time

**Not just course authoring.** This squad applies 15 specialized pedagogical frameworks through a systematic pipeline to guarantee learning outcomes.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: PERMANENT ENGINE (pedagogical frameworks)         │
│  ├── Bloom, Mayer, Rosenshine, UbD, CLT, ARCS, Bjork...    │
│  ├── Quality checklists (15 total)                          │
│  └── Templates (11 YAML)                                     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: VARIABLE DOMAIN MINDS (per course)                │
│  ├── Domain Expert (subject matter)                         │
│  ├── Teaching Voice (tone, examples)                        │
│  ├── Student Avatar (learner profile)                       │
│  └── Context (market, regulations)                          │
└─────────────────────────────────────────────────────────────┘

PIPELINE: Research → Design → Validate → Execute → Deliver
```

**Two-layer design:** Permanent pedagogical engine (Layer 1) + variable domain minds (Layer 2) = consistent excellence across any subject.

---

## Agents (16 Total)

### Tier 0: Research & Planning (4 agents)

| Agent | Mind | Role | Primary Framework |
|-------|------|------|-------------------|
| **@bloom-analyst** | Benjamin Bloom | Learning objectives design | Revised Bloom's Taxonomy (2001) |
| **@wiggins-designer** | Grant Wiggins | Course architecture (backward design) | Understanding by Design (UbD) |
| **@schwartz-analyst** | Eugene Schwartz | Market sophistication & awareness | Awareness Levels (1-5) |
| **@keller-motivator** | John Keller | Motivation strategy | ARCS Model |

### Tier 1: Content Design (5 agents)

| Agent | Mind | Role | Primary Framework |
|-------|------|------|-------------------|
| **@mayer-multimedia** | Richard Mayer | Multimedia learning design | 12 Multimedia Principles |
| **@rosenshine-instructor** | Barak Rosenshine | Direct instruction tactics | 10 Principles of Instruction |
| **@bjork-memory** | Robert Bjork | Spaced repetition & retrieval | Desirable Difficulties |
| **@cathy-moore-action** | Cathy Moore | Performance-based design | Action Mapping |
| **@clark-engagement** | Ruth Clark | Engagement patterns | Cognitive/Emotional/Behavioral |

### Tier 2: Assessment & Validation (2 agents)

| Agent | Mind | Role | Primary Framework |
|-------|------|------|-------------------|
| **@anderson-assessor** | Lorin Anderson | Assessment design | Assessment Framework (Bloom 2D) |
| **@merrill-validator** | M. David Merrill | Instructional validation | First Principles of Instruction |

### Tier 3: Domain Specialists (6 agents — examples)

| Agent | Domain | Role |
|-------|--------|------|
| **@domain-cooking** | Culinary Arts | Cooking courses |
| **@domain-programming** | Software Development | Programming courses |
| **@domain-finance** | Personal Finance | Finance courses |
| **@domain-leadership** | Management | Leadership courses |
| **@voice-conversational** | Conversational | Friendly, relatable tone |
| **@avatar-beginner** | Beginner Learner | No prior knowledge, high anxiety |

*(Domain agents created per course using `*create-domain-agent` task)*

### Orchestrator

| Agent | Role | Frameworks |
|-------|------|------------|
| **@education-chief** | Pipeline orchestration, quality gates, compliance validation | All 15 frameworks |

---

## Quick Start

### Create Full Course (Recommended)

```bash
/education
*create-course programming  # Creates course in programming domain
```

**Process:**
1. Activates @education-chief
2. Loads domain expert (or creates if new)
3. Runs 6-phase pipeline (Research → Design → Content → Assess → Validate → Deliver)
4. Outputs complete course + MEC compliance docs

**Duration:** 2-4 hours (Opus) for 10-lesson course

---

### Create Single Lesson

```bash
/education
*create-lesson "Explain Cognitive Load Theory"
```

**Agents involved:** @rosenshine-instructor + @mayer-multimedia + @bjork-memory

**Output:** 20-minute lesson following 7-part model

---

### Design Learning Objectives

```bash
/education
*create-objectives "Personal Finance Fundamentals"
```

**Agent:** @bloom-analyst

**Output:** 8-12 objectives across Bloom levels (Remember → Create)

---

### Validate Course Quality

```bash
/education
*validate-course output/courses/programming-fundamentals/
```

**Process:**
- Runs 10 pedagogical checklists
- Runs 5 MEC compliance checklists
- Generates quality report with scores and recommendations

---

## Available Commands

### Core Workflows

| Command | Description | Duration |
|---------|-------------|----------|
| `*create-course {domain}` | Complete course pipeline (research → delivery) | 2-4 hours |
| `*research-domain {domain}` | Phase 0-1 only (objectives + architecture) | 30-60 min |
| `*create-lesson {objective}` | Single lesson design | 15-30 min |
| `*validate-course {path}` | Quality + compliance audit | 10-20 min |

### Agent-Specific Tasks

| Command | Agent | Output |
|---------|-------|--------|
| `*create-objectives {topic}` | @bloom-analyst | Learning objectives (Bloom-aligned) |
| `*design-architecture {objectives}` | @wiggins-designer | Course structure (UbD backward design) |
| `*analyze-market {domain}` | @schwartz-analyst | Awareness/sophistication analysis |
| `*design-arcs {course}` | @keller-motivator | Motivation strategy (4 dimensions) |
| `*create-multimedia {content}` | @mayer-multimedia | Video/slide design (12 principles) |
| `*structure-lesson {objective}` | @rosenshine-instructor | Lesson plan (10 principles) |
| `*design-spaced-practice {content}` | @bjork-memory | Review schedule (FSRS) |
| `*create-action-map {performance}` | @cathy-moore-action | Performance-based design |
| `*design-engagement {lesson}` | @clark-engagement | Engagement tactics (LTEM scoring) |
| `*create-assessment {objective}` | @anderson-assessor | Quiz/rubric (Bloom 2D aligned) |
| `*validate-lesson {lesson}` | @merrill-validator | First Principles audit |

### Domain Management

| Command | Description |
|---------|-------------|
| `*create-domain-agent {domain}` | Create new domain expert |
| `*load-domain {domain}` | Activate existing domain |
| `*list-domains` | Show available domains |

### MEC Compliance

| Command | Description |
|---------|-------------|
| `*validate-mec {course-type}` | MEC compliance check |
| `*generate-ppc {course}` | Generate PPC document |
| `*accessibility-audit {course}` | WCAG 2.1 AA audit |

---

## File Structure

```
squads/education/
├── agents/
│   ├── tier0-bloom-analyst.md          # Learning objectives
│   ├── tier0-wiggins-designer.md       # UbD backward design
│   ├── tier0-schwartz-analyst.md       # Market sophistication
│   ├── tier0-keller-motivator.md       # ARCS motivation
│   ├── tier1-mayer-multimedia.md       # 12 multimedia principles
│   ├── tier1-rosenshine-instructor.md  # 10 instruction principles
│   ├── tier1-bjork-memory.md           # Spaced repetition
│   ├── tier1-cathy-moore-action.md     # Action mapping
│   ├── tier1-clark-engagement.md       # Engagement taxonomy
│   ├── tier2-anderson-assessor.md      # Assessment design
│   ├── tier2-merrill-validator.md      # First principles
│   ├── tier3-domain-template.md        # Domain agent template
│   ├── tier3-voice-template.md         # Teaching voice template
│   ├── tier3-avatar-template.md        # Student avatar template
│   └── education-chief.md              # Orchestrator
│
├── tasks/
│   ├── create-course.md                # Full pipeline
│   ├── create-objectives.md            # Bloom objectives
│   ├── design-architecture.md          # UbD structure
│   ├── analyze-market.md               # Schwartz analysis
│   ├── design-arcs.md                  # ARCS strategy
│   ├── create-multimedia.md            # Mayer-compliant media
│   ├── structure-lesson.md             # Rosenshine lesson plan
│   ├── design-spaced-practice.md       # Bjork review schedule
│   ├── create-action-map.md            # Action mapping
│   ├── design-engagement.md            # Clark engagement
│   ├── create-assessment.md            # Anderson assessments
│   ├── validate-lesson.md              # Merrill validation
│   ├── validate-course.md              # Full quality audit
│   ├── validate-mec.md                 # MEC compliance
│   ├── generate-ppc.md                 # PPC document
│   ├── create-domain-agent.md          # Domain expert creation
│   └── (15 more tasks...)
│
├── templates/
│   ├── course-tmpl.yaml                # Complete course
│   ├── lesson-tmpl.yaml                # Single lesson
│   ├── objectives-tmpl.yaml            # Learning objectives
│   ├── assessment-tmpl.yaml            # Quiz/rubric
│   ├── arcs-strategy-tmpl.yaml         # Motivation plan
│   ├── action-map-tmpl.yaml            # Performance outcomes
│   ├── spaced-schedule-tmpl.yaml       # Review intervals
│   ├── ppc-tmpl.yaml                   # MEC PPC document
│   ├── domain-agent-tmpl.yaml          # Domain expert
│   ├── voice-tmpl.yaml                 # Teaching voice
│   └── avatar-tmpl.yaml                # Student profile
│
├── checklists/
│   ├── pedagogical/
│   │   ├── bloom-alignment.md          # Objectives → Assessments → Content
│   │   ├── mayer-multimedia.md         # 12 principles
│   │   ├── rosenshine-instruction.md   # 10 principles
│   │   ├── ubd-coherence.md            # Backward design
│   │   ├── clt-optimization.md         # Cognitive load
│   │   ├── bjork-desirable.md          # Spacing, interleaving, retrieval
│   │   ├── arcs-motivation.md          # 4 dimensions
│   │   ├── action-mapping.md           # Performance outcomes
│   │   ├── ambrose-7principles.md      # Holistic learning
│   │   └── ltem-engagement.md          # Tier 5+ target
│   └── compliance/
│       ├── mec-course-type.md          # Type declaration + restrictions
│       ├── mec-accessibility.md        # WCAG 2.1 AA + LIBRAS
│       ├── mec-tutoring.md             # Tutor ratio, response time
│       ├── mec-lms.md                  # Tracking, gradebook, support
│       └── mec-ppc.md                  # PPC completeness
│
├── workflows/
│   ├── wf-full-pipeline.yaml           # Complete course (6 phases)
│   ├── wf-research-planning.yaml       # Phase 0-1 only
│   ├── wf-lesson-creation.yaml         # Single lesson workflow
│   └── wf-validation.yaml              # Quality + compliance audit
│
├── data/
│   ├── education-kb.md                 # THIS FILE — Complete KB
│   ├── lesson-model.md                 # 7-part replicable structure
│   ├── bloom-taxonomy-reference.md     # 6 levels + verbs + 2D matrix
│   ├── mayer-12-principles.md          # Multimedia learning
│   ├── rosenshine-10-principles.md     # Direct instruction
│   └── ltem-8-tiers.md                 # Engagement depth scoring
│
├── scripts/                            # (Future: automation scripts)
│
└── docs/
    ├── research/                       # Source research papers
    └── methodology/                    # Extended methodology docs
```

---

## Workflows

### 1. Full Course Pipeline (`wf-full-pipeline.yaml`)

**Duration:** 2-4 hours (Opus)

**Phases:**
1. **Research (Phase 0)** — Market analysis (Schwartz) + ICP + Domain loading
2. **Planning (Phase 1)** — Learning objectives (Bloom) + Architecture (UbD) + Motivation (ARCS)
3. **Content Design (Phase 2)** — Lessons (Rosenshine + Mayer) + Multimedia + Engagement (Clark)
4. **Assessment (Phase 3)** — Quizzes/Rubrics (Anderson) + Spaced practice (Bjork)
5. **Validation (Phase 4)** — Pedagogical audit (10 checklists) + MEC compliance (5 checklists)
6. **Delivery (Phase 5)** — Final course package + PPC + Tutoring plan

**Agents involved:** All 16

---

### 2. Research & Planning (`wf-research-planning.yaml`)

**Duration:** 30-60 min

**Phases:** 0-1 only (before content creation)

**Output:** Objectives, architecture, motivation strategy (ready for execution)

---

### 3. Lesson Creation (`wf-lesson-creation.yaml`)

**Duration:** 15-30 min per lesson

**Process:** Hook → Concept → Explanation → Examples → Guided → Independent → Recap

**Agents:** @rosenshine-instructor + @mayer-multimedia + @bjork-memory + @clark-engagement

---

### 4. Validation (`wf-validation.yaml`)

**Duration:** 10-20 min

**Process:** 15 checklists (10 pedagogical + 5 MEC compliance) + scoring + recommendations

**Agent:** @merrill-validator + @education-chief

---

## MEC Compliance System

**5 Course Types Supported:**

| Type | EAD % | Approval | Key Restrictions |
|------|-------|----------|------------------|
| 100% EAD | 100% | Required (e-MEC) | Health/Engineering forbidden |
| Semi-presential | 40% | No (notify only) | Practical activities presential |
| Presential + EAD | 20% | No | Min 80% presential |
| Extension | 100% | No | < 360h, no diploma |
| Free courses | 100% | No | No MEC regulation |

**Automatic compliance:** Every course includes MEC checklist validation + PPC generation.

**Reference:** Portaria MEC 2.117/2019

---

## Quality Standards

**Every deliverable passes:**

1. **Bloom Alignment** — Objectives → Assessments → Content (same cognitive level)
2. **Mayer Multimedia** — All 12 principles applied to visuals
3. **Rosenshine Instruction** — All 10 principles in lesson structure
4. **UbD Coherence** — Backward design (outcomes → assessment → instruction)
5. **CLT Optimization** — Cognitive load managed (intrinsic/extraneous/germane)
6. **Bjork Desirable Difficulties** — Spacing, interleaving, retrieval present
7. **ARCS Motivation** — All 4 dimensions (Attention, Relevance, Confidence, Satisfaction)
8. **Action Mapping** — Performance outcomes clear (what they DO, not just know)
9. **Ambrose 7 Principles** — Holistic learning (prior knowledge, motivation, practice, feedback, climate, self-direction, organization)
10. **LTEM Engagement** — Average tier 5+ (minimum 50% high-engagement activities)

**Plus:**
11. **MEC Compliance** — 5 checklists for regulated courses
12. **Accessibility** — WCAG 2.1 AA + LIBRAS for videos >5min

**Failure at any gate = BLOCK. No exceptions.**

---

## Key Frameworks Summary

| Framework | Creator | What It Does | When to Use |
|-----------|---------|--------------|-------------|
| **Bloom's Taxonomy (Revised)** | Anderson & Krathwohl | 6 cognitive levels (Remember → Create) | Every learning objective |
| **UbD (Understanding by Design)** | Wiggins & McTighe | Backward design (outcomes first) | Course architecture |
| **12 Multimedia Principles** | Mayer | Optimize visual learning | All videos, slides, diagrams |
| **10 Principles of Instruction** | Rosenshine | Direct instruction tactics | Lesson structure |
| **Desirable Difficulties** | Bjork | Spacing, interleaving, retrieval | Assessment design, review schedules |
| **ARCS Model** | Keller | Motivation (Attention, Relevance, Confidence, Satisfaction) | Engagement strategy |
| **Action Mapping** | Cathy Moore | Performance-based design | Practical courses |
| **LTEM (8 Tiers)** | Piotrowski | Engagement depth scoring | Quality validation |
| **Cognitive Load Theory** | Sweller | Manage intrinsic/extraneous/germane load | Content sequencing |
| **First Principles** | Merrill | Task-centered instruction | Lesson validation |

---

## Links

- **PRD:** `plan/prd/PRD-squad-education-engineer.md`
- **Knowledge Base:** `squads/education/data/education-kb.md`
- **Lesson Model:** `squads/education/data/lesson-model.md`
- **Bloom Reference:** `squads/education/data/bloom-taxonomy-reference.md`
- **Mayer Principles:** `squads/education/data/mayer-12-principles.md`
- **Rosenshine Principles:** `squads/education/data/rosenshine-10-principles.md`
- **LTEM Reference:** `squads/education/data/ltem-8-tiers.md`

---

## Version History

See `squads/education/CHANGELOG.md`

---

**Education Engineer Squad v1.0.0** — Evidence-based instructional design at scale.
