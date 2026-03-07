# Select Review Methodology

**Task ID:** `dr-select-methodology`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Select Review Methodology |
| **status** | `pending` |
| **responsible_executor** | booth |
| **execution_type** | `Agent` |
| **input** | Structured PICO question |
| **output** | Review methodology with search strategy |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Agent booth selects the most appropriate review methodology from 14 recognized review types based on the PICO question. The selection uses the SALSA framework (Search, AppraisaL, Synthesis, Analysis) and STARLITE criteria (Sampling strategy, Type of study, Approaches, Range of years, Limits, Inclusion/exclusion, Terms used, Electronic sources) to ensure methodological rigor and reproducibility.

## Input
- **pico_question** (object) - The structured PICO question from sackett containing population, intervention, comparison, and outcome
- **question_type** (enum) - The classified question type (therapeutic/diagnostic/prognostic/etiologic)
- **evidence_level_required** (string) - Minimum acceptable evidence level

## Output
- **review_methodology** (object) - Contains `type` (one of 14 review types), `rationale` (why this type fits), `search_strategy` (databases, terms, filters), `inclusion_criteria` (what evidence qualifies), `exclusion_criteria` (what is filtered out)
- **salsa_profile** (object) - Search scope, appraisal method, synthesis approach, analysis technique
- **starlite_specification** (object) - Complete STARLITE criteria for the selected methodology

## Action Items
### Step 1: Map Question to Review Type
Evaluate the PICO question against the 14 review types: systematic review, meta-analysis, rapid review, scoping review, narrative review, umbrella review, realist review, integrative review, critical review, state-of-the-art review, mapping review, mixed-methods review, overview of reviews, and qualitative evidence synthesis. Select based on question complexity, time constraints, and evidence landscape.

### Step 2: Select Search Approach
Define the search strategy using STARLITE criteria. Determine which sources to search (academic databases, grey literature, industry reports, code repositories), search terms derived from PICO components, date ranges, and language filters.

### Step 3: Define Inclusion and Exclusion Criteria
Establish clear boundaries for what evidence will be included in the review. Criteria must align with the PICO components: population match, intervention relevance, outcome measurability, and study quality thresholds.

### Step 4: Document SALSA Profile
For the selected review type, specify the Search scope (comprehensive vs. targeted), Appraisal method (GRADE, CASP, or domain-specific), Synthesis approach (narrative, statistical, framework), and Analysis technique (thematic, meta-analytic, configurative).

## Acceptance Criteria
- [ ] Selected review type is one of the 14 recognized types with documented rationale
- [ ] Search strategy includes specific sources, terms, and filters (not generic placeholders)
- [ ] Inclusion and exclusion criteria are derived from the PICO components
- [ ] SALSA profile covers all four dimensions (Search, Appraisal, Synthesis, Analysis)
- [ ] STARLITE specification is complete with all 8 criteria addressed

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
