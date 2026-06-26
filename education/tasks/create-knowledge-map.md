# Task: Create Knowledge Map

**Task ID:** create-knowledge-map
**Version:** 1.0
**Agent:** novak-mapper
**Squad:** education

## Purpose
Generate a hierarchical concept map for the domain using Novak's methodology. This becomes the foundation for all curriculum design decisions.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Domain name |
| research_docs | list | Yes | Paths to diagnose-domain and compare-curricula outputs |
| focus_area | string | No | Specific sub-domain to emphasize |

## Preconditions
- [ ] diagnose-domain.md exists
- [ ] curriculum-matrix/ exists
- [ ] Core concepts identified and validated

## Steps
1. Load all research documents
2. Identify superordinate concepts (top-level categories)
3. Identify subordinate concepts (specific skills/knowledge)
4. Map cross-links (relationships between branches)
5. Define propositions (linking phrases showing relationships)
6. Organize hierarchically (general → specific)
7. Generate visual representation (Mermaid diagram)
8. Document mastery criteria per concept level

## Output
- **Location:** `minds/{domain}/knowledge-map.md`
- **Format:** Concept map with Mermaid diagram + explanations
- **Sections:**
  - Hierarchical structure
  - Cross-links
  - Mastery criteria per level
  - Learning sequences

## Veto Conditions
- Concepts cannot be organized hierarchically (too interconnected)
- No clear superordinate concepts emerge
- Map becomes too complex (>50 nodes)

## Completion Criteria
- [ ] All concepts organized hierarchically
- [ ] Cross-links identified between branches
- [ ] Propositions defined for key relationships
- [ ] Mermaid diagram generated and valid
- [ ] Mastery criteria defined for each level
- [ ] Output saved to knowledge-map.md
