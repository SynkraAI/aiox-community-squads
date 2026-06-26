# Task: Diagnose Domain

**Task ID:** diagnose-domain
**Version:** 1.0
**Agent:** novak-mapper
**Squad:** education

## Purpose
Research an unknown domain and map the complete field of knowledge to understand what learners need to master. Produces a comprehensive knowledge map showing concepts, relationships, and dependencies.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Domain name (e.g., "Google Ads", "Python", "SEO") |
| target_audience | string | Yes | Who will learn this (e.g., "beginners", "professionals") |
| business_context | string | No | Why this course exists (e.g., "internal training", "product") |

## Preconditions
- [ ] Domain name is specific enough to scope (not "marketing" but "Facebook Ads")
- [ ] Target audience profile exists or can be inferred
- [ ] minds/{domain}/ directory created

## Steps
1. Research domain fundamentals via WebSearch (2026 current practices)
2. Identify core concepts and sub-concepts (hierarchical structure)
3. Map concept relationships (prerequisites, dependencies, co-requisites)
4. Identify common learning paths in the field
5. Note what experts consider "mastery" vs "competence"
6. Document knowledge boundaries (what's in scope, what's adjacent)
7. Generate knowledge map using Novak's concept mapping methodology

## Output
- **Location:** `minds/{domain}/knowledge-map.md`
- **Format:** Markdown with hierarchical concept structure
- **Sections:** Core Concepts, Dependencies, Learning Paths, Mastery Criteria, Boundaries

## Veto Conditions
- Domain too broad to map coherently (e.g., "business")
- No credible sources found for current practices
- Domain overlaps 80%+ with existing mapped domain

## Completion Criteria
- [ ] All core concepts identified and defined
- [ ] Dependencies mapped between concepts
- [ ] At least 2 credible sources cited per major concept
- [ ] Knowledge boundaries clearly stated
- [ ] Output saved to minds/{domain}/knowledge-map.md
