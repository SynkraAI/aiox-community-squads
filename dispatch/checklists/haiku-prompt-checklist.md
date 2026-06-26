# Haiku Prompt Checklist — ALWAYS/NEVER Rules + 6 Patterns

> **Phase:** 4.5 (Pre-Execution Gate) — applied to Haiku tasks
> **Agent:** quality-gate
> **Source:** haiku-patterns.yaml + PRD Section 10
> **Validated:** 94 tests, 100% success rate
> **Script:** `scripts/validate-dispatch-gate.sh --phase haiku-prompt`

---

## Purpose

Ensures every Haiku prompt follows validated patterns that guarantee consistent, high-quality output. These rules are extracted from 94 real-world tests with 100% success rate.

**Core insight:** Haiku is extremely capable when constrained correctly. Without constraints, output quality drops from 9/10 to 5/10.

---

## ALWAYS Rules (Veto If Absent)

| # | Rule | Veto ID | Check |
|---|------|---------|-------|
| 1 | Instructions in **ENGLISH** | V1.6 | `detect_language(instructions) == "en"` |
| 2 | Template/structure for outputs > 50 lines | V1.5 | `expected_lines > 50 → has_template` |
| 3 | `"DO NOT ask questions. Execute immediately."` present | — | `grep -c "DO NOT ask"` |
| 4 | `"Return ONLY [format]. Nothing else."` for structured output | — | `grep -c "Return ONLY"` |
| 5 | 1 task = 1 deliverable | V1.7 | `count_deliverables == 1` |
| 6 | Output format explicit (`yaml`, `json`, `markdown`) | — | `has_format_marker` |
| 7 | Output language specified explicitly if not English | — | `has_language_spec OR output_lang == "en"` |

---

## NEVER Rules (Veto If Present)

| # | Rule | Veto ID | Check |
|---|------|---------|-------|
| 1 | Prompts without context | — | `word_count(context) > 0` |
| 2 | "Generate document" without template | V1.5 | `no generate_without_template` |
| 3 | Code-switching (EN+PT mixed in same prompt) | V1.6 | `no language_mixing` |
| 4 | Outputs > 300 lines without template | V1.5 | `expected_lines > 300 → has_template` |
| 5 | Multiple deliverables in 1 task | V1.7 | `deliverable_count == 1` |
| 6 | Implicit instructions ("continue from last time") | — | `no implicit_refs` |
| 7 | Inherit model from parent (always set explicitly) | V1.10 | `model is not None` |

---

## 6 Validated Haiku Patterns

### HP-001: Fill Template

**Use when:** Output has a defined structure to fill.
**Task types:** create_file, generate_config, create_agent, create_task

```
## DATA
{context data to use}

## TEMPLATE
{template structure with placeholders}

## INSTRUCTIONS
Fill ALL placeholders in the template using the DATA above.
DO NOT ask questions. Execute immediately.
Write output in {language}.
Save to: {output_path}

## ACCEPTANCE CRITERIA
{criteria list}
```

### HP-002: Extract + Transform

**Use when:** Input data needs to be extracted and restructured.
**Task types:** extract, transform, parse, convert

```
## INPUT
{source data}

## OUTPUT FORMAT
```{format}
{expected output structure}
```

## INSTRUCTIONS
Extract ONLY the fields shown in OUTPUT FORMAT from the INPUT.
DO NOT ask questions. Execute immediately.
Return ONLY the {format} block. Nothing else.
Save to: {output_path}
```

### HP-003: Audit/Validate

**Use when:** Check input against criteria or checklist.
**Task types:** validate, audit, check, verify

```
## INPUT TO VALIDATE
{file or content to check}

## CHECKLIST
{criteria list — each must be PASS or FAIL}

## INSTRUCTIONS
Check each criterion against the input.
Status is binary: PASS or FAIL. No "partial" or "maybe".
DO NOT ask questions. Execute immediately.

## OUTPUT FORMAT
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | {criterion} | PASS/FAIL | {why} |

Save to: {output_path}
```

### HP-004: Code Generation

**Use when:** Generate code from requirements.
**Task types:** create_script, create_component, generate_code

```
## REQUIREMENTS
{what the code should do}

## CONSTRAINTS
- Language: {language}
- Max lines: {limit}
- Dependencies: {allowed libraries}
- Style: {coding conventions}

## INSTRUCTIONS
Generate code that meets ALL requirements.
DO NOT ask questions. Execute immediately.
Return ONLY the code block.
Save to: {output_path}
```

### HP-005: MCP Operations

**Use when:** Execute API calls via MCP tools.
**Task types:** mcp_create, mcp_update, mcp_delete, mcp_query
**Constraint:** MUST run foreground — MCP unavailable in background tasks.

```
## OBJECTIVE
{what to achieve}

## STEPS
1. {step 1 — specific MCP tool call}
2. {step 2 — specific MCP tool call}
3. Verify result

## MCP TOOLS AVAILABLE
{list of relevant MCP tools}

## INSTRUCTIONS
Execute tools in order shown.
DO NOT ask questions. Execute immediately.
If step fails, retry once. If still fails, report error.

## ACCEPTANCE CRITERIA
{verification steps}
```

### HP-006: Self-Correction

**Use when:** Improve existing output based on feedback.
**Task types:** improve, correct, rewrite, fix

```
## ORIGINAL OUTPUT (V1)
{output from previous attempt}

## FEEDBACK
{specific issues to fix}

## CRITERIA FOR V2
{what V2 must satisfy}

## INSTRUCTIONS
Read the original output and feedback.
Create V2 that addresses ALL issues in feedback.
DO NOT ask questions. Execute immediately.
Save V2 to: {output_path}
```

---

## Pattern Selection Guide

| Task Type | Pattern | ID |
|-----------|---------|-----|
| Create file from data + template | Fill Template | HP-001 |
| Extract/transform/parse input | Extract + Transform | HP-002 |
| Validate/audit against criteria | Audit/Validate | HP-003 |
| Generate code from requirements | Code Generation | HP-004 |
| Execute MCP API calls | MCP Operations | HP-005 |
| Improve output based on feedback | Self-Correction | HP-006 |

---

## Quick Validation Checklist

Before dispatching a Haiku task, verify:

- [ ] Instructions are in English (V1.6)
- [ ] "DO NOT ask questions. Execute immediately." is present
- [ ] Output format is explicit (yaml/json/markdown/code)
- [ ] 1 task = 1 deliverable (V1.7)
- [ ] If output > 50 lines: template included (V1.5)
- [ ] If output language != English: explicitly specified
- [ ] No code-switching in prompt (V1.6)
- [ ] No placeholders [XXX], {TODO}, TBD (V1.3)
- [ ] Correct pattern selected (HP-001 through HP-006)
- [ ] If MCP task: running foreground (not background)
