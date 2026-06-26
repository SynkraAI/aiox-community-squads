# Changelog -- deep-research

All notable changes to the Deep Research Squad will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-06

### Added
- 11 specialist agents across 3-tier pipeline (Diagnostic, Execution, QA)
- 17 executable tasks covering pipeline, diagnostic, execution, QA, and utility operations
- 3 multi-phase workflows (full research, quick research, competitive intel)
- 4 quality gates (QG-001 through QG-004)
- Pipeline architecture with use case classification (UC-001 through UC-004)
- Handoff matrix with full routing between all agents
- Tool integration: Exa, Context7, WebSearch
- Mind DNA extractions for all 10 research personas
- Search orchestration scripts (deep-search.ts, search-providers.ts)

### Architecture
- Entry agent: dr-orchestrator with 4-use-case routing
- Tier 0 (Diagnostic): Sackett -> Booth -> Creswell (sequential)
- Tier 1 (Execution): Forsgren, Cochrane, Higgins, Klein, Gilad (parallel)
- QA: Ioannidis -> Kahneman (sequential, mandatory)
- Synthesis: dr-orchestrator aggregates all findings into final report

### Agents
- **dr-orchestrator** (541 lines) -- Pipeline coordinator, query classification, quality gates
- **sackett** (595 lines) -- PICO question formulation, evidence levels, EBM 5-step workflow
- **booth** (682 lines) -- Review methodology selection, SALSA/STARLITE frameworks
- **creswell** (698 lines) -- Qualitative/quantitative/mixed methods design
- **forsgren** (363 lines) -- DORA metrics, SPACE framework, DevOps assessment
- **cochrane** (456 lines) -- Systematic literature reviews, PRISMA, GRADE
- **higgins** (367 lines) -- OSINT investigations, source verification, geolocation
- **klein** (430 lines) -- Pattern recognition, NDM/RPD, sensemaking
- **gilad** (385 lines) -- Competitive intelligence, early warning, blind spot detection
- **ioannidis** (408 lines) -- Evidence reliability audit, PPV calculation, bias detection
- **kahneman** (461 lines) -- Cognitive bias audit, System 1/2, decision hygiene

### Quality Gates
- QG-001: Question Quality (Sackett, after Tier 0)
- QG-002: Methodology Fit (Booth, after Tier 0)
- QG-003: Evidence Reliability (Ioannidis, after Tier 1)
- QG-004: Decision Quality (Kahneman, final gate)

### Use Cases
- UC-001: Technical Deep Dive (Forsgren + Cochrane)
- UC-002: Strategic Decision Support (Klein + Gilad)
- UC-003: Competitive Intelligence (Gilad + Higgins)
- UC-004: Evidence Synthesis (Cochrane + Forsgren)

### Documentation
- README.md with full squad overview and quick start guide
- ARCHITECTURE.md with pipeline deep dive and data contracts
- CHANGELOG.md (this file)
