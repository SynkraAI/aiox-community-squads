# Validate Source Credibility

**Task ID:** `dr-validate-source`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Validate Source Credibility |
| **status** | `pending` |
| **responsible_executor** | any-agent |
| **execution_type** | `Agent` |
| **input** | List of sources to evaluate |
| **output** | Per-source credibility ratings |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Utility task for rating the credibility of information sources used across the research pipeline. Any agent can invoke this task when it needs to assess whether a source is trustworthy enough to cite in findings. The evaluation considers four dimensions: authority (who published it), recency (when was it published), bias (is the source neutral), and methodological rigor (how was the information produced). Each source receives an overall credibility score that downstream tasks use for weighting evidence.

## Input
- **source_list** (array) - Each source contains `url` (string), `title` (string), `author_or_publisher` (string), `publication_date` (string, ISO format), `content_type` (academic/industry/blog/news/government/docs)

## Output
- **credibility_ratings** (array) - Per-source rating containing `source_url`, `authority_score` (0.0-1.0), `recency_score` (0.0-1.0), `bias_assessment` (neutral/lean/biased with direction), `methodological_score` (0.0-1.0), `overall_score` (0.0-1.0 weighted composite), `credibility_tier` (Tier 1 High / Tier 2 Moderate / Tier 3 Low)
- **flagged_sources** (array) - Sources scoring below 0.3 overall, with specific concerns noted

## Action Items
### Step 1: Check Authority
Evaluate the source's authority based on publisher reputation, author credentials, and domain expertise. Scoring guide: peer-reviewed journal or established research institution (0.8-1.0), industry report from recognized firm (0.6-0.8), established news outlet or official documentation (0.5-0.7), professional blog or conference presentation (0.3-0.5), anonymous or unverifiable source (0.0-0.3).

### Step 2: Check Recency
Assess the timeliness of the source relative to the research question. Scoring guide: published within last 12 months (0.8-1.0), within 1-3 years (0.5-0.8), within 3-5 years (0.3-0.5), older than 5 years (0.1-0.3). Adjust for domain: foundational research and standards may retain high recency scores regardless of age. Sources with no discernible publication date score 0.2.

### Step 3: Detect Bias
Evaluate the source for potential bias: funding conflicts (who paid for the research?), commercial interest (is the publisher selling a product?), ideological positioning (does the source have a known stance?), and methodological transparency (does the source show its work?). Rate as Neutral (no detected bias), Lean (minor bias that does not invalidate findings), or Biased (significant bias that must be noted in any citation).

### Step 4: Calculate Composite Score
Compute the overall credibility score as a weighted average: authority (35%), recency (20%), bias inverse (25%), methodological rigor (20%). Classify into tiers: Tier 1 High (0.7-1.0), Tier 2 Moderate (0.4-0.69), Tier 3 Low (0.0-0.39). Flag any source below 0.3 for explicit review before inclusion in findings.

## Acceptance Criteria
- [ ] All four dimensions (authority, recency, bias, methodology) are evaluated for every source
- [ ] Overall score uses the specified weighting formula
- [ ] Sources are classified into credibility tiers (High, Moderate, Low)
- [ ] Sources scoring below 0.3 are explicitly flagged with specific concerns
- [ ] Bias assessment includes direction of bias, not just presence/absence

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
