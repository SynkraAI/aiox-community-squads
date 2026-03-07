# Deep Research Squad -- Architecture

> Comprehensive architecture reference for the 11-agent evidence-based research pipeline.

---

## 1. Pipeline Overview

Every research query flows through a structured 7-stage pipeline. No stage can be skipped. QA is mandatory for all runs regardless of use case.

```
  ┌──────────┐    ┌────────────────┐    ┌──────────────┐    ┌──────────────┐
  |  QUERY   | -> | CLASSIFICATION | -> |   TIER 0     | -> |   TIER 1     |
  |  (input) |    | dr-orchestrator|    |  Diagnostic  |    |  Execution   |
  |          |    |  UC-001~004    |    |  (sequential)|    |  (parallel)  |
  └──────────┘    └────────────────┘    └──────────────┘    └──────────────┘
                                               |                    |
                                         ┌─────┴─────┐      ┌──────┴──────┐
                                         | Sackett   |      | Selected    |
                                         | Booth     |      | agents per  |
                                         | Creswell  |      | use case    |
                                         └───────────┘      └─────────────┘
                                                                    |
                                                                    v
  ┌──────────┐    ┌────────────────┐    ┌──────────────┐    ┌──────────────┐
  |  REPORT  | <- |   SYNTHESIS    | <- |     QA       | <- |  Tier 1      |
  |  (output)|    | dr-orchestrator|    |  (sequential)|    |  results     |
  |          |    |  final report  |    |  (mandatory) |    |  collected   |
  └──────────┘    └────────────────┘    └──────────────┘    └──────────────┘
                                               |
                                         ┌─────┴─────┐
                                         | Ioannidis |
                                         | Kahneman  |
                                         └───────────┘
```

**Stage Breakdown:**

| # | Stage | Agent(s) | Mode | Duration | Output |
|---|-------|----------|------|----------|--------|
| 1 | Query Intake | dr-orchestrator | Single | Immediate | Classified query + UC assignment |
| 2 | Classification | dr-orchestrator | Single | Immediate | Use case (UC-001~004) + agent selection |
| 3 | Diagnostic | Sackett, Booth, Creswell | Sequential | 3 steps | PICO, methodology, research design |
| 4 | Execution | 2-5 Tier 1 agents | Parallel | Varies | Domain-specific evidence packages |
| 5 | QA Audit | Ioannidis, Kahneman | Sequential | 2 steps | Reliability score + bias report |
| 6 | Synthesis | dr-orchestrator | Single | Post-QA | Integrated findings report |
| 7 | Report | dr-orchestrator | Single | Final | Structured deliverable |

---

## 2. Tier 0 -- Diagnostic Flow

Tier 0 runs **sequentially** for every pipeline execution. Its purpose is to transform a raw research query into a structured research plan before any evidence gathering begins.

```
  Raw Query
      |
      v
  ┌───────────────────────────────────────────────────┐
  |  SACKETT (David Sackett -- EBM Founder)           |
  |                                                   |
  |  Input:  Raw research query                       |
  |  Process: PICO decomposition                      |
  |  Output: Structured PICO question                 |
  |          - P: Population/Problem                   |
  |          - I: Intervention/Indicator               |
  |          - C: Comparison/Control                   |
  |          - O: Outcome/Objective                    |
  |  Gate:   QG-001 (Question Quality)                |
  └─────────────────────┬─────────────────────────────┘
                        |
                        v
  ┌───────────────────────────────────────────────────┐
  |  BOOTH (Andrew Booth -- SALSA Framework)          |
  |                                                   |
  |  Input:  PICO question from Sackett               |
  |  Process: Methodology selection from 14 types     |
  |  Output: Selected review methodology              |
  |          - Review type (scoping, systematic,      |
  |            rapid, umbrella, realist, etc.)         |
  |          - SALSA components (Search, Appraisal,   |
  |            Synthesis, Analysis)                    |
  |          - STARLITE search strategy               |
  |  Gate:   QG-002 (Methodology Fit)                 |
  └─────────────────────┬─────────────────────────────┘
                        |
                        v
  ┌───────────────────────────────────────────────────┐
  |  CRESWELL (John Creswell -- Mixed Methods)        |
  |                                                   |
  |  Input:  PICO + methodology from Booth            |
  |  Process: Research design selection               |
  |  Output: Complete research design                 |
  |          - Approach: qualitative, quantitative,   |
  |            or mixed methods                        |
  |          - Data integration strategy              |
  |          - Sampling and collection plan            |
  |          - Validity/reliability considerations    |
  └─────────────────────┬─────────────────────────────┘
                        |
                        v
              Research Plan Package
              (handed to dr-orchestrator)
```

**Key Constraint:** The diagnostic chain is strictly sequential. Booth cannot begin until Sackett completes the PICO formulation, and Creswell cannot begin until Booth selects the methodology. This ensures each diagnostic step builds on the previous one.

---

## 3. Tier 1 -- Execution Flow

Tier 1 runs **in parallel**. The orchestrator selects which agents participate based on the use case classification. Not all 5 agents run for every query.

```
                    dr-orchestrator
                    (selects agents based on UC)
                           |
          ┌────────┬───────┼────────┬────────┐
          |        |       |        |        |
          v        v       v        v        v
      ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
      |Forsgren||Cochrane||Higgins ||Klein   ||Gilad   |
      |DORA/   ||PRISMA/ ||OSINT/  ||NDM/    ||CI/     |
      |SPACE   ||GRADE   ||Verify  ||RPD     ||SCIP    |
      └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
          |        |       |        |        |
          v        v       v        v        v
                    dr-orchestrator
                    (collects all results)
```

### Agent Specialties

**Forsgren (Nicole Forsgren -- DORA/SPACE)**
- Input: Research plan + technical performance questions
- Process: DORA metrics analysis, SPACE framework application, capability assessment
- Output: Quantitative performance analysis with benchmarks
- Tools: Context7 (for library/framework documentation)
- Collaborates with: Cochrane (for evidence grounding)

**Cochrane (Cochrane Collaboration -- Systematic Reviews)**
- Input: Research plan + evidence synthesis requirements
- Process: Systematic search, PRISMA flow, GRADE evaluation
- Output: Evidence synthesis with quality assessment and hierarchy
- Tools: Exa (web search), Context7 (documentation), WebSearch
- Collaborates with: Forsgren (metrics), Higgins (source verification)

**Higgins (Eliot Higgins -- Bellingcat/OSINT)**
- Input: Research plan + investigation targets
- Process: Open-source intelligence gathering, source triangulation, verification
- Output: Verified findings with source provenance chain
- Tools: Exa (web search), WebSearch
- Collaborates with: Cochrane (evidence standards), Gilad (competitive targets)

**Klein (Gary Klein -- NDM/RPD)**
- Input: Research plan + decision scenarios
- Process: Pattern recognition, Recognition-Primed Decision analysis, pre-mortem
- Output: Decision analysis with pattern matches and failure modes
- Tools: None (reasoning-based)
- Collaborates with: Gilad (strategic context), Forsgren (data patterns)

**Gilad (Ben Gilad -- Competitive Intelligence)**
- Input: Research plan + competitive landscape questions
- Process: CI collection, early warning analysis, blind spot detection
- Output: Competitive landscape map with strategic implications
- Tools: Exa (web search), WebSearch
- Collaborates with: Higgins (OSINT), Klein (strategic sensemaking)

---

## 4. QA Flow

QA runs **sequentially** and is **mandatory for every pipeline run**, regardless of use case. Both agents must process the findings before the report is finalized.

```
  Tier 1 Results (aggregated by dr-orchestrator)
      |
      v
  ┌───────────────────────────────────────────────────┐
  |  IOANNIDIS (John Ioannidis -- Meta-Research)      |
  |                                                   |
  |  Input:  All Tier 1 evidence packages             |
  |  Process: Evidence reliability audit              |
  |          - Positive Predictive Value (PPV)        |
  |          - Bias pattern detection                 |
  |          - Statistical significance review        |
  |          - Source credibility assessment           |
  |          - Reproducibility check                  |
  |  Output: Reliability-scored evidence              |
  |          - Each finding tagged: HIGH/MEDIUM/LOW   |
  |          - Bias flags with specific patterns      |
  |          - Unreliable evidence quarantined         |
  |  Gate:   QG-003 (Evidence Reliability)            |
  └─────────────────────┬─────────────────────────────┘
                        |
                        v
  ┌───────────────────────────────────────────────────┐
  |  KAHNEMAN (Daniel Kahneman -- Behavioral Econ)    |
  |                                                   |
  |  Input:  Reliability-scored evidence from         |
  |          Ioannidis + original query context       |
  |  Process: Decision quality audit                  |
  |          - 12-Question Checklist (from Noise)     |
  |          - System 1/System 2 analysis             |
  |          - Cognitive bias scan (anchoring,        |
  |            availability, confirmation, etc.)      |
  |          - Pre-mortem analysis                    |
  |          - Decision hygiene recommendations       |
  |  Output: Decision-quality report                  |
  |          - Bias warnings for the decision-maker   |
  |          - Confidence calibration                 |
  |          - Alternative framings                   |
  |  Gate:   QG-004 (Decision Quality) -- FINAL      |
  └─────────────────────┬─────────────────────────────┘
                        |
                        v
              QA-Cleared Evidence Package
              (returned to dr-orchestrator for synthesis)
```

**Why QA is mandatory:** Research without bias auditing produces confident-but-wrong conclusions. Ioannidis catches evidence-level problems (bad sources, statistical artifacts). Kahneman catches decision-level problems (cognitive biases in interpretation). Together they form a double-lock on research quality.

---

## 5. Use Case Classification

The dr-orchestrator classifies incoming queries into one of four use cases. Classification determines which Tier 1 agents are activated.

### UC-001: Technical Deep Dive

```
Trigger patterns:
  - "performance of X vs Y"
  - "benchmark", "metrics", "DORA", "throughput"
  - "tech stack evaluation"
  - "migration impact"
  - "DevOps maturity"

Primary:   Forsgren (metrics) + Cochrane (evidence)
Secondary: Klein (decision patterns) + Higgins (verification)

Example: "What are the performance implications of migrating from REST to gRPC?"
```

### UC-002: Strategic Decision Support

```
Trigger patterns:
  - "should we", "build vs buy"
  - "strategic", "decision", "trade-off"
  - "architecture decision record"
  - "risk assessment"

Primary:   Klein (decision analysis) + Gilad (competitive context)
Secondary: Forsgren (quantitative data) + Cochrane (evidence base)

Example: "Should we build our own auth system or adopt a managed solution?"
```

### UC-003: Competitive Intelligence

```
Trigger patterns:
  - "competitor", "market landscape"
  - "competitive analysis"
  - "early warning", "market shift"
  - "company X vs company Y"

Primary:   Gilad (CI methodology) + Higgins (OSINT)
Secondary: Klein (pattern recognition)

Example: "Map the AI code assistant landscape and identify emerging threats."
```

### UC-004: Evidence Synthesis

```
Trigger patterns:
  - "state of the art", "best practices"
  - "systematic review", "literature review"
  - "what does the evidence say"
  - "survey of approaches"

Primary:   Cochrane (systematic review) + Forsgren (technical metrics)
Secondary: Higgins (source verification)

Example: "What does the evidence say about monorepo vs polyrepo at scale?"
```

### Classification Algorithm

```
dr-orchestrator applies this decision tree:

1. Does query mention specific competitors/companies?
   YES -> UC-003 (Competitive Intelligence)

2. Does query involve a binary/multi-option decision?
   YES -> UC-002 (Strategic Decision Support)

3. Does query focus on technical performance/metrics?
   YES -> UC-001 (Technical Deep Dive)

4. Does query seek broad evidence/literature/best practices?
   YES -> UC-004 (Evidence Synthesis)

5. Ambiguous -> Default to UC-004, refine after Tier 0 diagnostic
```

---

## 6. Quality Gates

Four quality gates are placed at critical junctures in the pipeline to prevent low-quality research from propagating downstream.

### QG-001: Question Quality

| Property | Value |
|----------|-------|
| Placement | After Sackett completes PICO formulation |
| Agent | Sackett |
| Criteria | PICO question has all 4 components clearly defined |
| Pass | Proceed to Booth |
| Fail | Sackett reformulates with clarifying questions to user |
| Max retries | 2 (then escalate to dr-orchestrator) |

### QG-002: Methodology Fit

| Property | Value |
|----------|-------|
| Placement | After Booth selects review methodology |
| Agent | Booth |
| Criteria | Review type matches question type and available evidence |
| Pass | Proceed to Creswell |
| Fail | Booth re-evaluates methodology selection |
| Max retries | 2 |

### QG-003: Evidence Reliability

| Property | Value |
|----------|-------|
| Placement | After all Tier 1 agents complete |
| Agent | Ioannidis |
| Criteria | PPV above threshold, bias patterns documented, unreliable evidence flagged |
| Pass | Proceed to Kahneman |
| Fail | Findings flagged as LOW confidence, proceed with warnings |
| Note | Does not block pipeline; adds reliability metadata |

### QG-004: Decision Quality

| Property | Value |
|----------|-------|
| Placement | Final gate before synthesis |
| Agent | Kahneman |
| Criteria | 12-Question Checklist passed, cognitive biases audited, pre-mortem completed |
| Pass | Proceed to synthesis |
| Fail | Pre-mortem exercise required before final report |
| Note | May add "decision warnings" section to final report |

---

## 7. Handoff Data Format

All agents produce structured output that follows a standard data contract. This ensures interoperability between pipeline stages.

### Standard Handoff Envelope

```yaml
handoff:
  from_agent: "<agent-name>"
  to_agent: "<next-agent-name>"
  timestamp: "<ISO 8601>"
  pipeline_id: "<uuid>"
  stage: "<tier-0 | tier-1 | qa | synthesis>"

  input_summary: "<what this agent received>"

  findings:
    - id: "F-001"
      claim: "<factual claim or finding>"
      evidence_level: "<HIGH | MEDIUM | LOW>"
      sources:
        - url: "<source URL>"
          type: "<primary | secondary | grey-literature>"
          credibility: "<score 1-5>"
      confidence: <0.0 - 1.0>
      methodology: "<how this finding was produced>"

  metadata:
    use_case: "<UC-001 | UC-002 | UC-003 | UC-004>"
    quality_gate: "<QG-XXX result if applicable>"
    bias_flags: []
    limitations: []

  recommendations:
    - "<actionable recommendation>"
```

### Tier-Specific Extensions

**Tier 0 (Diagnostic) adds:**
```yaml
diagnostic:
  pico:
    population: "<P>"
    intervention: "<I>"
    comparison: "<C>"
    outcome: "<O>"
  methodology:
    review_type: "<selected type>"
    salsa_components: {}
    search_strategy: {}
  research_design:
    approach: "<qualitative | quantitative | mixed>"
    data_integration: "<strategy>"
```

**Tier 1 (Execution) adds:**
```yaml
execution:
  domain: "<forsgren | cochrane | higgins | klein | gilad>"
  evidence_package:
    total_sources: <n>
    included_sources: <n>
    excluded_sources: <n>
    exclusion_reasons: []
  domain_specific:
    # Forsgren: metrics, benchmarks, scores
    # Cochrane: PRISMA flow, GRADE table
    # Higgins: source chain, verification steps
    # Klein: patterns, analogies, failure modes
    # Gilad: competitor profiles, signals, warnings
```

**QA adds:**
```yaml
qa_audit:
  reliability: # Ioannidis
    ppv_estimate: <0.0 - 1.0>
    bias_patterns:
      - type: "<publication | selection | confirmation | etc.>"
        severity: "<HIGH | MEDIUM | LOW>"
        affected_findings: ["F-001", ...]
    quarantined_evidence: []

  decision_quality: # Kahneman
    checklist_score: <0-12>
    biases_detected:
      - type: "<anchoring | availability | confirmation | etc.>"
        description: "<how it manifests>"
        mitigation: "<recommended action>"
    pre_mortem:
      failure_scenarios: []
      probability_estimates: []
    confidence_calibration: "<overconfident | calibrated | underconfident>"
```

---

## 8. Routing Algorithm

The dr-orchestrator uses a multi-step routing algorithm to transform raw queries into fully-orchestrated pipeline runs.

### Step 1: Query Intake and Normalization

```
Input:  Raw user query (natural language)
Output: Normalized query object

Process:
  1. Extract key entities (technologies, companies, concepts)
  2. Identify query intent (evaluate, compare, investigate, synthesize)
  3. Detect urgency and scope constraints
  4. Check for prior related pipeline runs (context)
```

### Step 2: Use Case Classification

```
Input:  Normalized query
Output: UC assignment (UC-001 through UC-004)

Process:
  1. Pattern match against UC trigger patterns (see Section 5)
  2. If multiple UCs match, select by strongest signal
  3. If ambiguous, default to UC-004 (broadest coverage)
  4. Log classification rationale
```

### Step 3: Agent Selection

```
Input:  UC assignment
Output: Agent roster for this pipeline run

Process:
  1. Always include: all Tier 0 agents (mandatory)
  2. Always include: both QA agents (mandatory)
  3. Include primary agents for classified UC
  4. Evaluate if secondary agents add value:
     - Query complexity > threshold -> include secondaries
     - User requests "deep" or "comprehensive" -> include secondaries
  5. Final roster logged for traceability
```

### Step 4: Pipeline Execution

```
Input:  Agent roster + normalized query
Output: Pipeline run with handoff chain

Process:
  1. Dispatch to Tier 0: Sackett -> Booth -> Creswell (sequential)
  2. Collect Tier 0 output (research plan package)
  3. Dispatch to Tier 1: selected agents (parallel)
  4. Wait for all Tier 1 agents to complete
  5. Aggregate Tier 1 results
  6. Dispatch to QA: Ioannidis -> Kahneman (sequential)
  7. Collect QA-cleared evidence package
  8. Synthesize final report
```

### Step 5: Report Assembly

```
Input:  QA-cleared evidence from all agents
Output: Structured research report

Report sections:
  1. Executive Summary (from synthesis)
  2. PICO Question (from Sackett)
  3. Methodology (from Booth + Creswell)
  4. Findings (from Tier 1 agents, per-domain)
  5. Evidence Quality (from Ioannidis)
  6. Decision Considerations (from Kahneman)
  7. Recommendations (from synthesis)
  8. Sources and References
  9. Appendix: Raw Evidence Tables
```

---

## 9. Tool Integration

Three external tools are integrated into the pipeline. Each tool is assigned to specific agents based on their operational needs.

### Tool Matrix

| Tool | Purpose | Used By | When |
|------|---------|---------|------|
| Exa | Web search with AI-powered results | Higgins, Cochrane, Gilad, dr-orchestrator | Evidence gathering, source discovery |
| Context7 | Library/framework documentation | Forsgren, Cochrane | Technical documentation lookup |
| WebSearch | General web search | Higgins, Gilad, Cochrane | Broad information gathering |

### Tool Usage by Agent

**dr-orchestrator**
- Exa: Quick context gathering during query classification

**Forsgren**
- Context7: Look up framework/library documentation for technical benchmarks

**Cochrane**
- Exa: Systematic search for academic and industry sources
- Context7: Technical documentation for evidence grounding
- WebSearch: Supplementary broad search

**Higgins**
- Exa: OSINT source discovery and verification
- WebSearch: Broad investigation sweeps

**Gilad**
- Exa: Competitive intelligence gathering, company research
- WebSearch: Market and industry news

**Klein, Sackett, Booth, Creswell, Ioannidis, Kahneman**
- No external tools (reasoning-based agents)

### Tool Selection Principles

1. **Exa first** -- Preferred for targeted, AI-enhanced search results
2. **Context7 for code/docs** -- When the query involves specific libraries or frameworks
3. **WebSearch as supplement** -- For broad coverage when Exa results are insufficient
4. **Reasoning agents stay tool-free** -- Diagnostic (Tier 0) and QA agents rely on structured reasoning, not raw search. They process outputs from tool-using agents

---

*Deep Research Squad Architecture v1.0*
*Last updated: 2026-03-06*
