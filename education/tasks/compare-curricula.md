# Task: Compare Curricula

**Task ID:** compare-curricula
**Version:** 1.0
**Agent:** novak-mapper
**Squad:** education

## Purpose
Cross-reference 5+ existing courses in the domain to identify patterns, gaps, and opportunities. Produces a curriculum matrix showing what competitors teach and what they miss.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Domain being researched |
| competitor_urls | list | No | URLs of existing courses (WebFetch if provided) |
| search_query | string | No | Query to find courses if URLs not provided |

## Preconditions
- [ ] knowledge-map.md exists for this domain
- [ ] At least 5 comparable courses can be found
- [ ] minds/{domain}/curriculum-matrix/ directory exists

## Steps
1. Find 5-10 existing courses (via URLs or WebSearch)
2. For each course, extract: topics covered, sequence, depth level, format
3. Build comparison matrix: rows=concepts, columns=courses, cells=coverage
4. Identify patterns: what ALL courses teach (table stakes)
5. Identify gaps: what NO course teaches well (opportunities)
6. Note pedagogical approaches used by each
7. Assess typical duration and pricing patterns

## Output
- **Location:** `minds/{domain}/curriculum-matrix/`
- **Files:**
  - `comparison-matrix.md` (table of coverage)
  - `patterns.md` (what everyone does)
  - `gaps.md` (what nobody does well)
  - `sources.md` (URLs and references)

## Veto Conditions
- Fewer than 3 comparable courses found
- All courses found are outdated (pre-2024)
- Courses are too varied to compare meaningfully

## Completion Criteria
- [ ] At least 5 courses analyzed
- [ ] Comparison matrix complete with all core concepts
- [ ] Patterns identified (minimum 3)
- [ ] Gaps identified (minimum 2)
- [ ] All sources documented with URLs
- [ ] Output saved to curriculum-matrix/
