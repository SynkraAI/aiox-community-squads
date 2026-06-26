# Synthesize Final Report

**Task ID:** `dr-synthesize-report`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Synthesize Final Report |
| **status** | `pending` |
| **responsible_executor** | dr-orchestrator |
| **execution_type** | `Agent` |
| **input** | Tier 0 outputs, Tier 1 outputs, QA audit results |
| **output** | Consolidated final research report |
| **action_items** | 5 steps |
| **acceptance_criteria** | 6 criteria |

## Overview
The orchestrator consolidates all outputs from the diagnostic, execution, and quality assurance tiers into a single coherent research report. The report resolves contradictions between agents, highlights consensus findings, presents evidence with GRADE ratings, and includes full citation trails. This is the primary deliverable the user receives.

## Input
- **tier_0_outputs** (object) - PICO question from sackett, review methodology from booth, research design from creswell
- **tier_1_outputs** (array) - Variable set of agent outputs depending on activated use case (performance assessment, evidence synthesis, OSINT report, pattern analysis, CI report)
- **qa_outputs** (object) - Reliability audit from ioannidis, decision quality audit from kahneman

## Output
- **final_research_report** (document) - Structured report containing executive summary, methodology description, key findings, evidence quality assessment, limitations, recommendations, and citation list
- **confidence_metadata** (object) - Overall confidence score, per-finding confidence, and dissent notes where agents disagreed

## Action Items
### Step 1: Collect and Inventory Outputs
Gather all agent outputs, verify completeness against the activation plan. Flag any missing outputs and note which findings may be incomplete as a result.

### Step 2: Identify Key Findings
Extract the top findings from each Tier 1 agent output. Rank findings by evidence strength (using GRADE ratings from cochrane where available) and cross-agent corroboration.

### Step 3: Resolve Contradictions
When two or more agents produce conflicting findings, document both positions, note the evidence basis for each, and apply the QA audit results to determine which position has stronger support. Do not silently discard minority findings.

### Step 4: Structure Report
Organize content into standard sections: Executive Summary (max 300 words), Methodology, Findings (grouped by theme), Evidence Quality, Limitations and Bias Warnings, Recommendations, and References.

### Step 5: Add Citations and Traceability
Every factual claim in the report must trace back to a specific agent output and, where applicable, to an external source. Use inline citation format [agent-id:finding-ref] and expand in the References section.

## Acceptance Criteria
- [ ] Report contains all mandatory sections (Executive Summary, Methodology, Findings, Evidence Quality, Limitations, Recommendations, References)
- [ ] Every finding includes at least one citation traceable to an agent output
- [ ] Contradictions between agents are explicitly documented, not silently resolved
- [ ] QA audit flags (bias warnings, unreliable evidence) are surfaced in the Limitations section
- [ ] Executive summary does not exceed 300 words
- [ ] Confidence metadata includes per-finding scores and overall research confidence

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
