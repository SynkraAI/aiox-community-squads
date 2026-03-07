# Assess Technical Performance

**Task ID:** `dr-assess-performance`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Assess Technical Performance |
| **status** | `pending` |
| **responsible_executor** | forsgren |
| **execution_type** | `Agent` |
| **input** | PICO question, research design |
| **output** | Performance assessment with metrics, benchmarks, and tier classification |
| **action_items** | 4 steps |
| **acceptance_criteria** | 6 criteria |

## Overview
Agent forsgren conducts a technical performance assessment using the DORA (DevOps Research and Assessment) four key metrics and the SPACE framework (Satisfaction, Performance, Activity, Communication, Efficiency). The assessment benchmarks the target population against industry data, classifies performance into tiers (Elite, High, Medium, Low), and identifies specific gaps with actionable improvement paths.

## Input
- **pico_question** (object) - Structured PICO question defining the target population, intervention, comparison baseline, and measurable outcomes
- **research_design** (object) - Research approach and data collection methods assigned to forsgren by creswell
- **agent_brief** (object) - Specific instructions from the research design on what data to collect and in what format

## Output
- **performance_assessment** (object) - Contains `metrics` (DORA four keys + SPACE dimensions with values), `benchmarks` (industry comparison data), `tier_classification` (Elite/High/Medium/Low per metric), `gaps` (areas below comparison baseline), `improvement_paths` (ranked recommendations)
- **data_quality_notes** (object) - Confidence level in each metric, data sources used, any proxy measures employed

## Action Items
### Step 1: Identify Relevant Metrics
Map the PICO outcome to specific DORA metrics (deployment frequency, lead time for changes, change failure rate, time to restore service) and SPACE dimensions. Not all metrics apply to every question -- select those that directly measure the stated outcome. Document why excluded metrics are not relevant.

### Step 2: Gather Performance Data
Collect quantitative data from available sources: web searches for published benchmarks (State of DevOps reports, industry surveys), code repository analysis if applicable, and any data provided in the query context. Use the execute-web-search utility task for external data gathering.

### Step 3: Benchmark Against Industry Data
Compare gathered metrics against the DORA benchmark tiers from the most recent State of DevOps Report. Classify each metric into Elite (top quartile), High (second quartile), Medium (third quartile), or Low (bottom quartile). Note the specific thresholds used for classification.

### Step 4: Identify Gaps and Recommend Improvements
Calculate the delta between current performance and the comparison baseline from the PICO question. Rank gaps by impact (which improvements would most affect the stated outcome). Produce concrete, actionable improvement recommendations grounded in the Accelerate research findings.

## Acceptance Criteria
- [ ] At least two DORA metrics are evaluated with quantitative values
- [ ] SPACE framework dimensions are assessed where sufficient data exists
- [ ] Tier classification uses published DORA benchmark thresholds with citations
- [ ] Gaps are quantified as deltas against the PICO comparison baseline
- [ ] Improvement recommendations are specific and actionable, not generic advice
- [ ] Data quality notes document confidence level and source for each metric

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
