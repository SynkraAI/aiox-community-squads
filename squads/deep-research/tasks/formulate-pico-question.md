# Formulate PICO Question

**Task ID:** `dr-formulate-pico`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Formulate PICO Question |
| **status** | `pending` |
| **responsible_executor** | sackett |
| **execution_type** | `Agent` |
| **input** | Raw user query |
| **output** | Structured PICO question with question type and evidence level |
| **action_items** | 5 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Agent sackett transforms the raw research query into a structured PICO (Population, Intervention, Comparison, Outcome) question. This formalization is the foundation for all downstream research -- it ensures that the investigation has a clear scope, measurable outcomes, and a defined comparison baseline. PICO is adapted for non-clinical domains: Population becomes the target system/team/market, Intervention becomes the technology/practice/strategy under investigation.

## Input
- **raw_query** (string) - The original research question as submitted by the user
- **use_case_classification** (object) - The classified use case from the orchestrator, providing domain context

## Output
- **pico_question** (object) - Contains `population` (who/what is being studied), `intervention` (the practice or technology under investigation), `comparison` (the baseline or alternative), `outcome` (measurable result criteria)
- **question_type** (enum) - One of: therapeutic (does X work?), diagnostic (can we detect X?), prognostic (what will happen?), etiologic (what causes X?)
- **evidence_level_required** (string) - Minimum acceptable evidence level (e.g., systematic review, RCT equivalent, observational, expert opinion)

## Action Items
### Step 1: Identify Population
Extract the target population, system, or domain from the query. In technical contexts, this may be a software team, a codebase, a market segment, or an organization. Be specific: "enterprise SaaS teams with >50 engineers" is better than "software teams."

### Step 2: Extract Intervention
Identify the practice, technology, tool, or strategy being investigated. Frame it as an actionable variable that can be measured. Example: "adoption of trunk-based development" rather than "branching strategy."

### Step 3: Define Comparison
Determine the baseline or alternative against which the intervention is measured. If no explicit comparison exists in the query, establish a reasonable default (e.g., "current state" or "industry median").

### Step 4: Specify Measurable Outcome
Define concrete, measurable outcomes that would answer the research question. Outcomes must be observable and quantifiable where possible: deployment frequency, defect rate, time-to-market, revenue impact.

### Step 5: Classify Question Type
Categorize the PICO question into one of the four types (therapeutic, diagnostic, prognostic, etiologic) and determine the minimum evidence level needed to answer it credibly.

## Acceptance Criteria
- [ ] All four PICO components (Population, Intervention, Comparison, Outcome) are explicitly defined
- [ ] Population is specific enough to guide targeted evidence collection
- [ ] Outcome includes at least one measurable or observable criterion
- [ ] Question type is classified into one of the four valid categories
- [ ] Evidence level required is stated and justified based on question type

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
