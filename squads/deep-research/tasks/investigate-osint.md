# Investigate OSINT

**Task ID:** `dr-investigate-osint`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Investigate OSINT |
| **status** | `pending` |
| **responsible_executor** | higgins |
| **execution_type** | `Agent` |
| **input** | PICO question, research design |
| **output** | OSINT report with verified sources, timeline, and geolocation data |
| **action_items** | 5 steps |
| **acceptance_criteria** | 6 criteria |

## Overview
Agent higgins gathers Open Source Intelligence (OSINT) to build an evidence base from publicly available information. This includes web content, social media, public records, technical infrastructure data, code repositories, and domain registration information. All collected intelligence is verified through triangulation (minimum two independent sources) and graded by reliability. The agent follows ethical OSINT practices: only publicly available data, no unauthorized access, no social engineering.

## Input
- **pico_question** (object) - Structured PICO question defining the investigation scope and targets
- **research_design** (object) - Research approach and data collection methods assigned to higgins
- **agent_brief** (object) - Specific intelligence requirements and priority areas from creswell

## Output
- **osint_report** (object) - Contains `sources` (array of discovered sources with metadata), `verification_status` (per-source: verified/unverified/contradicted), `geolocation_data` (geographic context if relevant), `timeline` (chronological event sequence), `entity_graph` (relationships between discovered entities), `confidence_levels` (per-finding confidence rating)
- **collection_log** (object) - Audit trail of all searches conducted, tools used, and timestamps

## Action Items
### Step 1: Identify Intelligence Sources
Based on the PICO question, determine which OSINT source categories are relevant: web content and news, social media profiles and posts, public code repositories, domain and infrastructure records, corporate filings, patent databases, job postings, and technical documentation. Prioritize sources by expected intelligence value.

### Step 2: Collect Raw Intelligence
Execute searches across identified source categories using the execute-web-search utility task. For each source, capture: URL, access timestamp, content snapshot, author/publisher, publication date, and initial relevance assessment. Maintain a structured collection log.

### Step 3: Verify and Triangulate
Apply the two-source minimum rule: every significant finding must be corroborated by at least two independent sources. Cross-reference facts across different source types (e.g., a claim in a blog post verified against a public record). Flag unverified findings explicitly.

### Step 4: Build Timeline and Entity Graph
Organize verified findings chronologically to reveal patterns, trends, and causal sequences. Map relationships between entities (people, organizations, technologies, events) to expose connections not obvious from individual sources.

### Step 5: Assess and Document Confidence
Rate each finding on a confidence scale: Confirmed (3+ independent sources), Probable (2 sources), Possible (1 credible source), Unconfirmed (single source with caveats). Document the basis for each rating and any conflicting information discovered.

## Acceptance Criteria
- [ ] All sources are publicly available -- no data obtained through unauthorized access
- [ ] Every significant finding has verification status documented (verified/unverified/contradicted)
- [ ] Two-source minimum rule is applied for findings rated Confirmed or Probable
- [ ] Collection log provides a complete audit trail of searches and tools used
- [ ] Timeline captures chronological sequence of events with dates and sources
- [ ] Confidence levels are assigned to every finding using the defined scale

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
