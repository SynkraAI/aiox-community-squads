# Analyze Decision Patterns

**Task ID:** `dr-analyze-decisions`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Analyze Decision Patterns |
| **status** | `pending` |
| **responsible_executor** | klein |
| **execution_type** | `Agent` |
| **input** | PICO question, available evidence from other Tier 1 agents |
| **output** | Pattern analysis with recognized patterns, anomalies, and decision points |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Agent klein applies the Recognition-Primed Decision (RPD) model and SenseMaking framework to analyze decision patterns within the research domain. The agent identifies recurring patterns in the available evidence, detects anomalies that challenge assumptions, maps critical decision points, and conducts a pre-mortem analysis to anticipate failure modes. This provides the strategic reasoning layer that transforms raw evidence into actionable decision intelligence.

## Input
- **pico_question** (object) - Structured PICO question providing the decision context
- **available_evidence** (array) - Outputs from other Tier 1 agents (performance data, systematic review results, OSINT findings, competitive intelligence) available at time of analysis
- **agent_brief** (object) - Research design instructions specifying the analytical focus

## Output
- **pattern_analysis** (object) - Contains `recognized_patterns` (recurring themes with evidence support), `anomalies` (findings that deviate from expected patterns), `decision_points` (critical junctions where different choices lead to different outcomes), `mental_models` (implicit models detected in the evidence), `pre_mortem` (failure mode analysis)
- **sensemaking_map** (object) - Data-Frame relationships showing how evidence maps to interpretive frameworks

## Action Items
### Step 1: Collect Environmental Cues
Scan all available evidence from other Tier 1 agents for situational cues: key data points, trends, outliers, and contextual signals. Organize cues by category (performance indicators, market signals, behavioral patterns, technology trends). Identify which cues are strong (high confidence) versus weak (low confidence or ambiguous).

### Step 2: Match Patterns Using RPD Model
Apply Recognition-Primed Decision pattern matching to the collected cues. Compare the current situation against known archetypes: technology adoption curves, organizational change patterns, market disruption patterns, technical debt accumulation patterns. Document which patterns match and which aspects of the situation are novel (not matching any known pattern).

### Step 3: Identify Anomalies and Challenge Assumptions
Systematically look for evidence that contradicts the recognized patterns. Apply Klein's anomaly detection heuristic: expectation violations, gaps in data where information should exist, and coincidences that may indicate hidden causation. For each anomaly, assess whether it represents noise, a genuine deviation, or a paradigm-shifting signal.

### Step 4: Project Scenarios and Pre-Mortem
Using recognized patterns and identified anomalies, project the most likely scenarios forward. Conduct a pre-mortem analysis: assume the recommended course of action has failed, then work backward to identify the most plausible causes of failure. Document each failure mode with its probability, impact, and early warning indicators.

## Acceptance Criteria
- [ ] At least three distinct patterns are identified with supporting evidence citations
- [ ] Anomalies are documented with explicit assessment of significance (noise, deviation, or paradigm shift)
- [ ] Decision points map at least two alternative paths with projected consequences
- [ ] Pre-mortem identifies at least three failure modes with early warning indicators
- [ ] SenseMaking map shows explicit linkage between evidence data and interpretive frameworks

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
