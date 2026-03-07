# Conduct Systematic Review

**Task ID:** `dr-systematic-review`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Conduct Systematic Review |
| **status** | `pending` |
| **responsible_executor** | cochrane |
| **execution_type** | `Agent` |
| **input** | PICO question, review methodology |
| **output** | Evidence synthesis with quality ratings and GRADE assessment |
| **action_items** | 5 steps |
| **acceptance_criteria** | 6 criteria |

## Overview
Agent cochrane performs a systematic evidence review following PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) protocol. The agent searches for published evidence, screens results against inclusion criteria, extracts data from qualifying sources, assesses study quality, and synthesizes findings using the GRADE (Grading of Recommendations, Assessment, Development and Evaluations) framework. This produces the highest-rigor evidence base for the research question.

## Input
- **pico_question** (object) - Structured PICO question with all four components defined
- **review_methodology** (object) - Selected review type, search strategy, inclusion/exclusion criteria, and SALSA profile from booth
- **agent_brief** (object) - Data collection instructions from the research design

## Output
- **evidence_synthesis** (object) - Contains `included_studies` (array of qualifying sources with metadata), `excluded_studies` (array with exclusion reasons), `quality_ratings` (per-study quality assessment), `grade_assessment` (overall GRADE rating: High/Moderate/Low/Very Low), `narrative_synthesis` (thematic summary of findings), `forest_plot_data` (quantitative data for meta-analytic display if applicable)
- **prisma_flow** (object) - PRISMA flow diagram data: records identified, screened, eligible, included

## Action Items
### Step 1: Execute Systematic Search
Run the search strategy defined by booth across specified sources. Use the execute-web-search utility task for web-based sources. Record total records identified per source. Remove duplicates. Document the complete search string and date of search for reproducibility.

### Step 2: Screen Results
Apply inclusion and exclusion criteria in two phases. Phase 1 (title/abstract screening): quickly filter obviously irrelevant results. Phase 2 (full-text screening): evaluate remaining sources against all criteria. Record reasons for exclusion at each phase.

### Step 3: Extract Data
From included sources, extract structured data aligned with the PICO components: population characteristics, intervention details, comparison conditions, and outcome measurements. Use a standardized extraction form to ensure consistency across sources.

### Step 4: Assess Study Quality
Evaluate each included source using the appropriate quality assessment tool: CASP (Critical Appraisal Skills Programme) for qualitative studies, Cochrane Risk of Bias tool for experimental studies, Newcastle-Ottawa Scale for observational studies. Rate each source as high, moderate, or low quality.

### Step 5: Synthesize Evidence
Combine findings using the approach specified in the SALSA profile. For narrative synthesis, organize by theme and identify convergence/divergence. For quantitative synthesis, calculate effect sizes and confidence intervals. Apply GRADE to produce an overall evidence quality rating accounting for risk of bias, inconsistency, indirectness, imprecision, and publication bias.

## Acceptance Criteria
- [ ] Search strategy is documented with reproducible search strings and source list
- [ ] PRISMA flow data captures counts at every stage (identified, screened, eligible, included)
- [ ] Every excluded source has a documented exclusion reason
- [ ] Quality ratings are applied to each included source using a recognized assessment tool
- [ ] GRADE assessment produces an overall rating with justification for each domain
- [ ] Narrative synthesis organizes findings by theme and notes areas of convergence and divergence

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
