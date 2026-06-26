# Execute Web Search

**Task ID:** `dr-web-search`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0
**Last Updated:** 2026-03-06

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Execute Web Search |
| **status** | `pending` |
| **responsible_executor** | any-agent |
| **execution_type** | `Agent` |
| **input** | Search query, search type, filters |
| **output** | Ranked search results with content and relevance scores |
| **action_items** | 4 steps |
| **acceptance_criteria** | 5 criteria |

## Overview
Utility task available to any Deep Research agent needing to gather information from the web. This task abstracts the three available search mechanisms (EXA web search, WebSearch, and Context7 documentation lookup) behind a unified interface. The calling agent specifies the query and preferred search type, and this task handles tool selection, execution, result filtering, and relevance ranking.

## Input
- **search_query** (string) - The search query to execute, optimized for the target search engine
- **search_type** (enum) - One of: `exa` (EXA deep web search for broad research), `websearch` (WebSearch for current events and general info), `context7` (Context7 for library/framework documentation)
- **filters** (object, optional) - Contains `domain_whitelist` (array of allowed domains), `domain_blacklist` (array of blocked domains), `max_results` (number, default 8), `recency` (date filter for freshness)
- **context** (string, optional) - Brief description of why this search is being conducted, used to improve relevance ranking

## Output
- **search_results** (array) - Each result contains `url` (source URL), `title` (page title), `content` (extracted text content), `relevance_score` (0.0-1.0 estimated relevance to the query), `source_type` (academic/industry/blog/docs/news)
- **search_metadata** (object) - Tool used, query executed, number of results returned, timestamp

## Action Items
### Step 1: Select Search Tool
Based on the search_type parameter, route to the appropriate tool:
- `exa`: Use mcp__exa__web_search_exa for deep web content retrieval. Best for research papers, technical articles, and comprehensive web content.
- `websearch`: Use WebSearch for up-to-date information, news, and general knowledge queries. Include current year (2026) in date-sensitive queries.
- `context7`: Use mcp__context7__resolve-library-id then mcp__context7__query-docs for programming library documentation and code examples.

### Step 2: Execute Search
Run the search with the provided query and any applicable filters. For EXA, set contextMaxCharacters based on expected content depth. For WebSearch, apply domain filters if specified. For Context7, resolve the library ID first, then query documentation.

### Step 3: Filter Results
Remove results that match domain blacklist entries. Remove duplicate content (same URL or substantially similar text). Remove results with insufficient content (less than 100 characters of extractable text). Apply domain whitelist if specified.

### Step 4: Rank by Relevance
Score each remaining result for relevance to the original search query and the provided context. Consider: keyword match density, source authority (academic > industry report > blog), content freshness, and alignment with the calling agent's research objective. Sort results by relevance score descending.

## Acceptance Criteria
- [ ] Correct search tool is selected based on the search_type parameter
- [ ] Results are filtered against blacklist/whitelist when provided
- [ ] Duplicate results are removed before returning
- [ ] Every result includes url, title, content, relevance_score, and source_type
- [ ] Search metadata documents which tool was used and when the search was executed

---
_Task Version: 1.0_
_Pattern: HO-TP-001_
