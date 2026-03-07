# Audit Evidence Reliability

**Task ID:** `dr-audit-reliability`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Audit Evidence Reliability |
| **status** | `pending` |
| **responsible_executor** | ioannidis |
| **execution_type** | `Agent` |
| **input** | All Tier 1 agent outputs |
| **output** | Reliability audit with PPV scores, bias flags, and recommendations |
| **action_items** | 4 steps |
| **acceptance_criteria** | 6 criteria |

## Overview
Agent ioannidis audits the reliability of all evidence produced by Tier 1 agents, applying the principles from "Why Most Published Research Findings Are False." The audit calculates Positive Predictive Value (PPV) estimates for key findings, detects systematic biases (confirmation bias, survivorship bias, publication bias, selection bias), flags unreliable evidence that should not inform decisions, and produces recommendations for interpreting the evidence base with appropriate skepticism.

## Input
- **all_tier_1_outputs** (array) - Complete outputs from every activated Tier 1 agent: performance assessment (forsgren), evidence synthesis (cochrane), OSINT report (higgins), pattern analysis (klein), CI report (gilad)
- **research_design** (object) - Original research design from creswell for context on intended methodology

## Output
- **reliability_audit** (object) - Contains `ppv_scores` (per-finding estimated positive predictive value), `bias_flags` (detected biases with severity rating), `unreliable_evidence` (findings that should be discounted or removed), `reliable_evidence` (findings that withstand scrutiny), `recommendations` (guidance on interpreting the evidence base)
- **audit_methodology** (object) - Documentation of criteria and thresholds used for the audit

## Action Items
### Step 1: Calculate PPV for Key Findings
For each major finding from Tier 1 agents, estimate the Positive Predictive Value using the Ioannidis framework. Consider: pre-study probability (how likely was this finding before the research?), statistical power equivalent (how strong is the evidence?), bias factor (what biases might inflate the result?), number of independent tests (how many things were tested?). PPV below 0.5 flags a finding as more likely false than true.

### Step 2: Detect Systematic Biases
Scan all Tier 1 outputs for evidence of systematic biases:
- **Confirmation bias**: Did agents only seek evidence supporting initial hypotheses?
- **Survivorship bias**: Are failed cases/projects underrepresented?
- **Publication bias**: Is the evidence skewed toward positive results?
- **Selection bias**: Is the sample unrepresentative of the population?
- **Recency bias**: Is older but relevant evidence underweighted?
Rate each detected bias as Critical, High, Medium, or Low severity.

### Step 3: Flag Unreliable Evidence
Based on PPV scores and bias detection, classify each finding as Reliable (PPV >= 0.7, no critical biases), Uncertain (PPV 0.4-0.7 or medium biases), or Unreliable (PPV < 0.4 or critical biases). Unreliable findings must include specific reasons and should not be used in the final report without explicit caveats.

### Step 4: Produce Audit Report and Recommendations
Compile the complete reliability audit with actionable recommendations. For uncertain findings, suggest additional evidence that would resolve uncertainty. For reliable findings, note any caveats. Produce an overall evidence base quality rating (Strong, Moderate, Weak, Insufficient) that the orchestrator will use in the final report.

## Acceptance Criteria
- [ ] PPV is estimated for every major finding from Tier 1 agents
- [ ] At least five bias types are systematically checked across all outputs
- [ ] Every finding is classified as Reliable, Uncertain, or Unreliable with justification
- [ ] Unreliable findings include specific reasons for the classification
- [ ] Overall evidence base quality rating is provided (Strong/Moderate/Weak/Insufficient)
- [ ] Audit methodology is documented so the assessment itself is transparent and reproducible

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
