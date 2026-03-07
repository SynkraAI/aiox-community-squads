# Deep Research Squad

> 11-agent evidence-based research pipeline: from question formulation to bias-audited synthesis, every conclusion earns its confidence level.

**Version:** 1.0.0 | **Created:** 2026-02-07 | **Total:** 11 agents, 5,386 lines

## Squad Architecture

```
                         dr-orchestrator (Pipeline Coordinator)
                                    [Orchestrator]
                                         |
                    ┌────────────────────┼────────────────────┐
                    |                    |                    |
           ┌────────────────┐    ┌──────────────┐    ┌──────────────┐
           |   TIER 0       |    |   TIER 1     |    |     QA       |
           |  Diagnostic    |    |  Execution   |    |   Audit      |
           |  (sequential)  |    |  (parallel)  |    |  (sequential)|
           └────────────────┘    └──────────────┘    └──────────────┘
                    |                    |                    |
            ┌───────────┐       ┌───────────────┐    ┌───────────┐
            |  Sackett  |       |   Forsgren    |    | Ioannidis |
            |   PICO    |       |   DORA/SPACE  |    |  Evidence  |
            └─────┬─────┘       ├───────────────┤    |  Reliability|
                  |             |   Cochrane    |    └─────┬─────┘
            ┌─────┴─────┐      |   PRISMA      |          |
            |   Booth   |      ├───────────────┤    ┌─────┴─────┐
            |   SALSA   |      |   Higgins     |    | Kahneman  |
            └─────┬─────┘      |   OSINT       |    |  Cognitive |
                  |             ├───────────────┤    |  Bias Audit|
            ┌─────┴─────┐      |    Klein      |    └───────────┘
            | Creswell  |      |   NDM/RPD     |
            |  Mixed    |      ├───────────────┤
            |  Methods  |      |    Gilad      |
            └───────────┘      |   CI/SCIP     |
                               └───────────────┘

  Flow: Query → Classification → Tier 0 → Tier 1 → QA → Synthesis → Report
```

## Agents

| Tier | Agent | Persona | Based On | Lines | Focus |
|------|-------|---------|----------|-------|-------|
| Orch | dr-orchestrator | DR Orchestrator | Original | 541 | Query classification, pipeline routing, quality gates |
| 0 | sackett | David Sackett | EBM founder | 595 | PICO question formulation, evidence levels |
| 0 | booth | Andrew Booth | SALSA framework | 682 | Review methodology selection (14 types) |
| 0 | creswell | John Creswell | Mixed methods pioneer | 698 | Qual/quant/mixed research design |
| 1 | forsgren | Nicole Forsgren | DORA/SPACE | 363 | Technical performance measurement |
| 1 | cochrane | Cochrane Collaboration | Systematic reviews | 456 | Evidence synthesis, PRISMA, GRADE |
| 1 | higgins | Eliot Higgins | Bellingcat/OSINT | 367 | Open-source investigations, verification |
| 1 | klein | Gary Klein | NDM/RPD | 430 | Pattern recognition, sensemaking |
| 1 | gilad | Ben Gilad | Competitive Intelligence | 385 | CI, strategic early warning, blind spots |
| QA | ioannidis | John Ioannidis | Meta-research | 408 | Evidence reliability, PPV, bias detection |
| QA | kahneman | Daniel Kahneman | Behavioral Economics | 461 | Cognitive bias audit, decision hygiene |

## Use Cases

| ID | Use Case | Primary Agents | Secondary Agents | When to Use |
|----|----------|---------------|-----------------|-------------|
| UC-001 | Technical Deep Dive | Forsgren + Cochrane | Klein, Higgins | Performance metrics, tech stack evaluation, DevOps assessment |
| UC-002 | Strategic Decision Support | Klein + Gilad | Forsgren, Cochrane | Build vs buy, architecture decisions, strategic pivots |
| UC-003 | Competitive Intelligence | Gilad + Higgins | Klein | Market analysis, competitor tracking, early warning signals |
| UC-004 | Evidence Synthesis | Cochrane + Forsgren | Higgins | Literature reviews, state-of-the-art surveys, best practices |

## Quick Start

### Activate the Orchestrator
```
@deep-research:dr-orchestrator
```
Or use the AIOX activation:
```
/AIOX:agents:dr-orchestrator
```

### Direct Specialist Access
```
/AIOX:agents:sackett              # PICO question formulation
/AIOX:agents:booth                # Review methodology selection
/AIOX:agents:creswell             # Research design (qual/quant/mixed)
/AIOX:agents:forsgren             # Technical metrics (DORA/SPACE)
/AIOX:agents:cochrane             # Systematic reviews (PRISMA)
/AIOX:agents:higgins              # OSINT investigations
/AIOX:agents:klein                # Pattern recognition / sensemaking
/AIOX:agents:gilad                # Competitive intelligence
/AIOX:agents:ioannidis            # Evidence reliability audit
/AIOX:agents:kahneman             # Cognitive bias audit
```

### Example Research Queries
```
# UC-001: Technical Deep Dive
"What are the performance implications of migrating from REST to gRPC for our microservices?"

# UC-002: Strategic Decision Support
"Should we build our own auth system or adopt Auth0/Clerk?"

# UC-003: Competitive Intelligence
"Map the AI code assistant landscape: Cursor, Windsurf, Claude Code, GitHub Copilot."

# UC-004: Evidence Synthesis
"What does the evidence say about monorepo vs polyrepo for teams of 20-50 engineers?"
```

## Quality Gates

| ID | Gate | Agent | Placement | Criteria | On Failure |
|----|------|-------|-----------|----------|------------|
| QG-001 | Question Quality | Sackett | After Tier 0 | PICO question well-formed with all 4 components | Return to Sackett for reformulation |
| QG-002 | Methodology Fit | Booth | After Tier 0 | Review type matches question type and available evidence | Booth re-selects methodology |
| QG-003 | Evidence Reliability | Ioannidis | After Tier 1 | PPV > threshold, bias patterns flagged, unreliable evidence identified | Flag low-confidence findings |
| QG-004 | Decision Quality | Kahneman | Final | 12-Question Checklist passed, cognitive biases audited | Pre-mortem required before approval |

## Elite Minds Research Attribution

This squad was created through iterative research with devil's advocate validation. Each agent is based on real researchers, frameworks, or organizations with documented methodologies:

| Mind | Contribution | Domain |
|------|-------------|--------|
| **David Sackett** | Evidence-Based Medicine founder, PICO framework, 5-step EBM | Clinical epidemiology |
| **Andrew Booth** | SALSA framework, STARLITE, review type classification (14 types) | Information science |
| **John Creswell** | Mixed methods research design, qual/quant integration strategies | Research methodology |
| **Nicole Forsgren** | DORA metrics, SPACE framework, Accelerate book | DevOps research |
| **Cochrane Collaboration** | Systematic review standards, PRISMA, GRADE evidence hierarchy | Healthcare research |
| **Eliot Higgins** | Bellingcat, open-source investigation methodology, OSINT | Digital forensics |
| **Gary Klein** | Naturalistic Decision Making, Recognition-Primed Decision model | Cognitive science |
| **Ben Gilad** | Competitive Intelligence, SCIP, strategic early warning systems | Business strategy |
| **John Ioannidis** | "Why Most Published Research Findings Are False", PPV, meta-research | Research integrity |
| **Daniel Kahneman** | System 1/System 2, cognitive biases, Noise, decision hygiene | Behavioral economics |

## Directory Structure

```
squads/deep-research/
├── config.yaml                    # Squad configuration and pipeline architecture
├── README.md                      # This file
├── CHANGELOG.md                   # Version history
├── ARCHITECTURE.md                # Pipeline architecture deep dive
├── HEADLINE.md                    # Squad value proposition
├── agents/
│   ├── dr-orchestrator.md         # Orchestrator: Pipeline Coordinator
│   ├── sackett.md                 # Tier 0: PICO question formulation
│   ├── booth.md                   # Tier 0: Methodology selection (SALSA)
│   ├── creswell.md                # Tier 0: Research design (mixed methods)
│   ├── forsgren.md                # Tier 1: Technical metrics (DORA/SPACE)
│   ├── cochrane.md                # Tier 1: Systematic reviews (PRISMA)
│   ├── higgins.md                 # Tier 1: OSINT investigations
│   ├── klein.md                   # Tier 1: Sensemaking (NDM/RPD)
│   ├── gilad.md                   # Tier 1: Competitive Intelligence
│   ├── ioannidis.md               # QA: Evidence reliability audit
│   └── kahneman.md                # QA: Cognitive bias audit
├── tasks/                         # 17 executable task definitions
├── workflows/                     # Multi-phase research workflows
├── scripts/
│   ├── deep-search.ts             # Search orchestration
│   └── search-providers.ts        # Provider integration
└── data/
    └── minds/                     # Mind DNA extractions (10 files)
```

## Statistics

| Metric | Value |
|--------|-------|
| Total agents | 11 |
| Total lines | 5,386 |
| Avg lines/agent | 490 |
| Orchestrator | 1 (Pipeline Coordinator) |
| Tier 0 (Diagnostic) | 3 agents (sequential) |
| Tier 1 (Execution) | 5 agents (parallel) |
| QA agents | 2 (sequential, mandatory) |
| Total tasks | 17 |
| Total workflows | 3 |
| Use cases | 4 (UC-001 through UC-004) |
| Quality gates | 4 (QG-001 through QG-004) |
| Minds cloned | 10 (from 10 distinct sources) |
| Tool integrations | 3 (Exa, Context7, WebSearch) |

---

*Deep Research Squad v1.0 -- Created by Squad Creator Pro*
*Philosophy: "Every research question deserves a structured, evidence-based answer."*
