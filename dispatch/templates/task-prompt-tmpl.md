# Task Prompt Template — Dispatch Squad v1.0.0

> **Purpose:** Generates enriched prompts for Haiku/Sonnet subagents.
> **Filled by:** `scripts/enrich-task.py` (CODE > LLM)
> **Source:** PRD Section 10 + enrichment-rules.yaml
> **Structure:** STATIC prefix (cacheable) + DYNAMIC suffix (unique per task)

---

## Prompt Structure

### --- CACHED PREFIX (same across all tasks in same domain) ---

**System Prompt** (~200 tokens):
```
You are a task executor for the AIOS Dispatch system.
Your job is to execute ONE specific task and produce ONE deliverable.

RULES:
- DO NOT ask questions. Execute immediately.
- DO NOT explain your reasoning unless the task asks for analysis.
- DO NOT add features, content, or sections not specified.
- Return ONLY the requested output format.
- If you cannot complete the task, return STATUS: FAIL with a specific reason.
- Save output to the exact path specified.

OUTPUT FORMAT: {{output_format}}
OUTPUT LANGUAGE: {{output_language}}
```

**Knowledge Context** (~500-3000 tokens based on enrichment level):

For **MINIMAL** enrichment (organizational tasks):
```
No KB context injected.
```

For **STANDARD** enrichment (creation/code/MCP tasks):
```
## DOMAIN KNOWLEDGE
{{kb_summary}}

## RELEVANT ANTI-PATTERNS
{{anti_patterns}}

## QUICK REFERENCE
{{quick_reference}}
```

For **FULL** enrichment (creative/copy/strategy tasks):
```
## DOMAIN KNOWLEDGE
{{kb_full}}

## BUSINESS CONTEXT
{{business_context}}

## ICP DATA
{{icp_data}}

## STYLE GUIDE
{{style_guide}}

## ANTI-PATTERNS
{{anti_patterns}}
```

**Rules** (~300 tokens):
```
## ALWAYS
{{#each always_rules}}
- {{this}}
{{/each}}

## NEVER
{{#each never_rules}}
- {{this}}
{{/each}}
```

### --- DYNAMIC SUFFIX (unique per task) ---

**Task Description** (~200 tokens):
```
## TASK
{{task_description}}

## DELIVERABLE
{{deliverable}}
```

**Template** (if output > 50 lines — MANDATORY for Haiku):
```
## OUTPUT TEMPLATE
{{output_template}}
```

**Acceptance Criteria** (~100 tokens):
```
## ACCEPTANCE CRITERIA
{{#each acceptance_criteria}}
- [ ] {{this}}
{{/each}}
```

**Output Path** (~50 tokens):
```
## OUTPUT
Save to: {{output_path}}
Return ONLY the content. Nothing else.
```

---

## Haiku Pattern Selection

Based on `data/haiku-patterns.yaml`, select the correct pattern:

| Task Type | Pattern | ID |
|-----------|---------|-----|
| Create file from data + template | Fill Template | HP-001 |
| Extract/transform/parse input | Extract + Transform | HP-002 |
| Validate/audit against criteria | Audit/Validate | HP-003 |
| Generate code from requirements | Code Generation | HP-004 |
| Execute MCP API calls | MCP Operations | HP-005 |
| Improve output based on feedback | Self-Correction | HP-006 |

---

## Token Budget

| Section | MINIMAL | STANDARD | FULL |
|---------|---------|----------|------|
| System prompt | 200 | 200 | 200 |
| KB context | 0 | 1,500 | 3,000 |
| Business context | 0 | 0 | 2,000 |
| Rules | 300 | 300 | 300 |
| Task description | 200 | 200 | 200 |
| Template | 0 | 500 | 500 |
| Acceptance | 100 | 100 | 100 |
| Output path | 50 | 50 | 50 |
| **Total input** | **~850** | **~2,850** | **~6,350** |

---

## Prompt Caching Strategy

```
┌─────────────────────────────────────────────┐
│ STATIC PREFIX (cacheable across wave)       │
│ ┌─────────────────────────────────────────┐ │
│ │ System prompt (200 tokens)              │ │
│ │ KB context (500-3000 tokens)            │ │
│ │ Rules (300 tokens)                      │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ DYNAMIC SUFFIX (unique per task)            │
│ ┌─────────────────────────────────────────┐ │
│ │ Task description (200 tokens)           │ │
│ │ Template (0-500 tokens)                 │ │
│ │ Acceptance criteria (100 tokens)        │ │
│ │ Output path (50 tokens)                 │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘

Same-domain wave (6 tasks): 75% input savings
Mixed-domain wave: 40% input savings
```

---

## Variables Reference

| Variable | Source | Required |
|----------|--------|----------|
| `output_format` | task.output_format | Yes |
| `output_language` | task.output_language (default: English) | Yes |
| `kb_summary` | domain-registry.yaml → kb_files (extracted sections) | STANDARD+ |
| `kb_full` | domain-registry.yaml → kb_files (complete) | FULL |
| `business_context` | source/current.yaml + source/company.yaml | FULL + triggers |
| `icp_data` | source/icp.yaml | FULL + triggers |
| `style_guide` | source/voice.yaml | FULL + triggers |
| `anti_patterns` | domain KB anti-patterns section | STANDARD+ |
| `quick_reference` | domain KB quick-reference section | STANDARD |
| `always_rules` | haiku-patterns.yaml → always[] | Always |
| `never_rules` | haiku-patterns.yaml → never[] | Always |
| `task_description` | execution-plan task.description | Yes |
| `deliverable` | execution-plan task.deliverable | Yes |
| `output_template` | task-specific template (if > 50 lines) | Conditional |
| `acceptance_criteria` | execution-plan task.acceptance_criteria | Yes |
| `output_path` | execution-plan task.output_path | Yes |
