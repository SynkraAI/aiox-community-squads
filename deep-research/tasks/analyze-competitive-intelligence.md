# Analyze Competitive Intelligence

**Task ID:** `dr-analyze-ci`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Analyze Competitive Intelligence |
| **status** | `pending` |
| **responsible_executor** | gilad |
| **execution_type** | `Agent` |
| **input** | PICO question, research design |
| **output** | CI report with landscape analysis, early warnings, and strategic recommendations |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Agent gilad conducts competitive intelligence analysis using the CI Cycle (Planning, Collection, Analysis, Dissemination) and Early Warning methodology. The agent maps the competitive landscape relevant to the research question, identifies strategic blind spots, generates early warning signals for emerging threats and opportunities, and produces actionable strategic recommendations. CI is adapted beyond traditional business competitors to include technology alternatives, methodological approaches, and ecosystem dynamics.

## Input
- **pico_question** (object) - Structured PICO question defining the competitive context (the intervention vs. comparison inherently frames a competitive dynamic)
- **research_design** (object) - Research approach and data collection methods assigned to gilad
- **agent_brief** (object) - Intelligence priorities and focus areas from the research design

## Output
- **ci_report** (object) - Contains `landscape` (map of competitors/alternatives with positioning), `early_warnings` (signals of emerging changes with impact assessment), `blind_spots` (areas where intelligence gaps create risk), `strategic_recommendations` (ranked actionable recommendations with confidence)
- **intelligence_gaps** (array) - Questions that could not be answered with available data, with suggested collection strategies

## Action Items
### Step 1: Define Intelligence Needs
Translate the PICO question into specific intelligence requirements. What do we need to know about the competitive landscape to answer the research question? Define Key Intelligence Topics (KITs) and Key Intelligence Questions (KIQs) that focus collection efforts.

### Step 2: Collect Competitive Data
Execute targeted searches using the execute-web-search utility task across multiple source types: industry reports, analyst coverage, product documentation, technical blogs, conference presentations, job postings (as signals of strategic direction), patent filings, and open-source project activity. Focus on signals relevant to the KITs and KIQs defined in Step 1.

### Step 3: Analyze Landscape and Generate Early Warnings
Map the competitive landscape using frameworks appropriate to the domain: technology radar (adopt/trial/assess/hold), market positioning matrix, feature comparison grid, or ecosystem map. Identify early warning signals by detecting weak signals of change: new entrants, technology shifts, regulatory changes, talent movement patterns, and funding flows. Assess each signal for probability and potential impact.

### Step 4: Identify Blind Spots and Formulate Recommendations
Systematically evaluate what the analysis cannot see: areas with insufficient data, perspectives not represented, assumptions not tested. Document these as blind spots with risk assessment. Produce strategic recommendations that address the PICO question, ranked by confidence and impact. Each recommendation must cite supporting intelligence and acknowledge relevant blind spots.

## Acceptance Criteria
- [ ] Landscape map covers at least three competitors or alternatives with differentiated positioning
- [ ] Early warning signals include probability and impact ratings
- [ ] Blind spots are explicitly documented with associated risk levels
- [ ] Strategic recommendations are ranked and tied to specific intelligence findings
- [ ] Intelligence gaps identify at least two unanswered questions with suggested collection approaches

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
