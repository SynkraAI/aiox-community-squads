# Classify Research Query

**Task ID:** `dr-classify-query`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Classify Research Query |
| **status** | `pending` |
| **responsible_executor** | dr-orchestrator |
| **execution_type** | `Agent` |
| **input** | Raw user query string |
| **output** | Use case classification with agent routing |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
The orchestrator receives a raw research query from the user and classifies it into one or more of the four supported use cases (UC-001 Technical Assessment, UC-002 Systematic Review, UC-003 OSINT Investigation, UC-004 Strategic Analysis). This classification drives all downstream agent activation and pipeline construction.

## Input
- **raw_query** (string) - The unprocessed research question or topic submitted by the user
- **context_hints** (object, optional) - Any prior conversation context or domain hints that refine classification

## Output
- **use_case_classification** (object) - Contains `id` (UC-001~004), `label`, `primary_agents` (array of agent IDs activated in Tier 1), `secondary_agents` (array of optional supporting agents), `confidence` (0.0-1.0 score)
- **ambiguity_flags** (array) - List of signals indicating the query may span multiple use cases

## Action Items
### Step 1: Parse Query Structure
Tokenize the raw query, extract key entities, intent verbs, and domain signals. Identify whether the query is a question, directive, or exploratory prompt.

### Step 2: Match Trigger Patterns
Compare extracted signals against the trigger pattern registry for each use case:
- UC-001: performance, metrics, DORA, throughput, reliability, deployment frequency
- UC-002: evidence, systematic, studies, effectiveness, compare treatments, literature
- UC-003: investigate, track, verify, source, attribution, open-source intelligence
- UC-004: competitive, market, strategy, landscape, early warning, blind spots

### Step 3: Assign Use Case(s)
Select the primary use case with highest pattern match confidence. If confidence delta between top two is less than 0.15, flag as multi-use-case query and assign both.

### Step 4: Determine Agent Routing
Map the selected use case(s) to the agent activation table:
- UC-001: primary=[forsgren], secondary=[cochrane, klein]
- UC-002: primary=[cochrane], secondary=[higgins, klein]
- UC-003: primary=[higgins], secondary=[gilad, klein]
- UC-004: primary=[gilad], secondary=[forsgren, cochrane]

Tier 0 agents (sackett, booth, creswell) are always activated regardless of classification.

## Acceptance Criteria
- [ ] Every query receives exactly one primary use case classification
- [ ] Confidence score is computed and falls within 0.0-1.0 range
- [ ] Multi-use-case queries are flagged when confidence delta is below threshold
- [ ] Agent routing output contains valid agent IDs from the squad roster
- [ ] Classification completes within a single orchestrator turn without user re-prompting

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
