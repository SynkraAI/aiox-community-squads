# Design Research Plan

**Task ID:** `dr-design-plan`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Design Research Plan |
| **status** | `pending` |
| **responsible_executor** | creswell |
| **execution_type** | `Agent` |
| **input** | PICO question, review methodology |
| **output** | Research design with data collection and integration strategy |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Agent creswell designs the overarching research plan that guides Tier 1 execution agents. Drawing from Creswell's research design taxonomy, the agent determines whether the investigation requires a qualitative, quantitative, or mixed-methods approach. The plan specifies data collection methods, integration strategies for combining evidence from multiple agents, and validity procedures to ensure research trustworthiness.

## Input
- **pico_question** (object) - Structured PICO question from sackett with all four components
- **review_methodology** (object) - Selected review type and search strategy from booth
- **use_case_classification** (object) - Use case ID and agent routing from the orchestrator

## Output
- **research_design** (object) - Contains `approach` (qualitative/quantitative/mixed), `data_collection_methods` (array of methods per Tier 1 agent), `integration_strategy` (how outputs from different agents will be combined), `validity_procedures` (checks for credibility, transferability, dependability, confirmability)
- **agent_briefs** (array) - Per-agent instruction packets that translate the research design into specific guidance for each Tier 1 agent

## Action Items
### Step 1: Assess Question Nature
Analyze the PICO question and review methodology to determine the dominant research paradigm. Quantitative emphasis when outcomes are numeric and comparative. Qualitative emphasis when exploring patterns, experiences, or meanings. Mixed methods when the question demands both measurement and interpretation.

### Step 2: Select Research Approach
Choose the specific design within the selected paradigm. For quantitative: correlational, quasi-experimental, or descriptive survey. For qualitative: phenomenological, grounded theory, case study, or ethnographic. For mixed: convergent parallel, explanatory sequential, or exploratory sequential.

### Step 3: Plan Data Collection Methods
Map each Tier 1 agent to specific data collection responsibilities. Example: forsgren collects quantitative metrics, cochrane collects published evidence, higgins collects open-source intelligence, klein collects decision pattern data, gilad collects competitive intelligence. Define the format and schema each agent should produce.

### Step 4: Design Integration Strategy
Specify how outputs from multiple agents will be merged. For convergent designs, plan side-by-side comparison. For sequential designs, define handoff points. Establish conflict resolution rules when agents produce contradictory data. Define validity procedures: triangulation across agents, member checking against PICO, audit trail through the pipeline.

## Acceptance Criteria
- [ ] Research approach is explicitly stated as qualitative, quantitative, or mixed with justification
- [ ] Data collection methods are assigned to each activated Tier 1 agent
- [ ] Integration strategy addresses how multi-agent outputs will be combined
- [ ] Validity procedures include at least two of: triangulation, audit trail, member checking, peer debriefing
- [ ] Agent briefs are generated for every Tier 1 agent in the activation plan

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
