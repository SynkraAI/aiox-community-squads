# ═══════════════════════════════════════════════════════════════════════════════
# TASK: Convert Input
# ID: convert-input
# Version: 1.0.0
# Purpose: Convert non-story inputs (PRD, free text, task list) into a
#          temporary story-like structure for dispatch processing.
# Agent: wave-planner (or dispatch-chief for simple conversions)
# Executor: wave-planner
# Phase in Pipeline: Phase 0 (when input is not a story)
# Pattern: DS-QG-002 (Veto Conditions — V0.* Sufficiency)
# ═══════════════════════════════════════════════════════════════════════════════

## Overview

Not all dispatch inputs arrive as well-formed stories with acceptance criteria.
Users may provide PRDs, free text descriptions, or unstructured task lists.
This task converts any non-story input into a temporary story-format file that
`plan-execution` can consume as if it were a story.

This is a CONVERSION task. It adds structure, detects deliverables, and
generates operational acceptance criteria. It NEVER invents content — all
information comes from the original input. If the input lacks sufficient
information for dispatch, this task applies V0.* veto conditions and redirects
the user to the appropriate agent (/pm, /po, or /copy:agents:copy-chief).

**Key distinction:** This task is a SHIM — it exists only to normalize input
format. The real decomposition happens in `plan-execution`. If the input is
already a story with acceptance criteria, this task is SKIPPED entirely.

---

## Inputs

| Parameter   | Type   | Required | Description                                                        |
|------------|--------|----------|--------------------------------------------------------------------|
| raw_input  | string or path | YES | Raw input: inline text string OR path to a file (.md, .yaml, .json, .txt) |
| input_type | enum   | YES      | One of: `prd`, `free_text`, `task_list`. Stories bypass this task. |
| run_id     | string | NO       | Dispatch run ID. Auto-generated if not provided (dispatch-YYYYMMDD-HHMMSS) |

---

## Preconditions

Before starting this task, the following MUST be true:

- [ ] `raw_input` is provided (either non-empty string or valid file path)
- [ ] `input_type` is one of: `prd`, `free_text`, `task_list`
- [ ] If `raw_input` is a file path: file exists and is readable
- [ ] Data file exists: `squads/dispatch/data/enrichment-rules.yaml` (quantity_patterns)
- [ ] Data file exists: `squads/dispatch/data/veto-conditions.yaml` (V0.* conditions)

---

## PHASE 0: Classify and Validate Input

**Checkpoint:** Input classified and passes sufficiency checks.

### Action Items

- [ ] 0.1 — Determine if `raw_input` is a file path or inline text:
  - If path: Read file content into memory
  - If inline text: use as-is
- [ ] 0.2 — Read veto conditions: `squads/dispatch/data/veto-conditions.yaml`
- [ ] 0.3 — Read enrichment rules: `squads/dispatch/data/enrichment-rules.yaml`
- [ ] 0.4 — Count words in input
- [ ] 0.5 — Apply V0.2 check: "Input < 10 words with no deliverables"
  - Count words in raw input
  - Scan for quantity patterns from `enrichment-rules.yaml` (`quantity_patterns` section)
  - IF word_count < 10 AND no quantities detected:
    - **VETO V0.2** — redirect to /pm or /po with message:
      "Input too brief for dispatch. Use /pm for PRD or /po for story with acceptance criteria."
    - BLOCK execution
- [ ] 0.6 — Apply V0.3 check: "No specific deliverables mentioned"
  - Scan for file types (.md, .yaml, .json, .py, etc.)
  - Scan for quantity patterns
  - Scan for output-related keywords (create, generate, write, build, produce)
  - IF no deliverables detected:
    - **VETO V0.3** — ask user for quantities and deliverables
    - BLOCK execution
- [ ] 0.7 — Generate `run_id` if not provided: format `dispatch-YYYYMMDD-HHMMSS`
- [ ] 0.8 — Create run directory: `_temp/dispatch/runs/{run_id}/`

### Phase 0 Checkpoint

- [ ] Input content loaded into memory (from file or inline)
- [ ] V0.2 passed (input has >= 10 words OR contains quantity patterns)
- [ ] V0.3 passed (input mentions specific deliverables)
- [ ] run_id is set
- [ ] Run directory exists

---

## PHASE 1: Extract Structure by Type

**Checkpoint:** Structured task list extracted from input.

### Action Items — PRD Input (`input_type == prd`)

- [ ] 1A.1 — Identify requirements section in PRD (look for "Requirements", "Requisitos", "Must have", "Should have", or numbered lists)
- [ ] 1A.2 — Extract each requirement as a candidate task
- [ ] 1A.3 — For compound requirements (contain "and", "e", or multiple verbs), split into separate tasks
- [ ] 1A.4 — Extract priority if available (must/should/could/won't)
- [ ] 1A.5 — Extract any acceptance criteria already present in PRD
- [ ] 1A.6 — Map PRD sections to task groups (functional requirements = one group, non-functional = another)

### Action Items — Free Text Input (`input_type == free_text`)

- [ ] 1B.1 — **CODE > LLM:** Run `python squads/dispatch/scripts/extract-quantities.py --input "$INPUT" --format json` to extract quantities deterministically. Do NOT use LLM for pattern matching.
  - Script applies ALL quantity patterns from `enrichment-rules.yaml` to detect deliverables:
  - `(\d+)\s+newsletters?` → type: newsletter
  - `(\d+)\s+emails?` → type: email
  - `(\d+)\s+tags?` → type: tag_ac or tag_bh
  - `(\d+)\s+(?:automações?|automations?)` → type: automation
  - `(\d+)\s+(?:agents?|agentes?)` → type: agent
  - `(\d+)\s+(?:tasks?|tarefas?)` → type: task
  - (full list in enrichment-rules.yaml)
- [ ] 1B.2 — For each detected quantity: create N separate tasks (e.g., "3 newsletters" = 3 tasks)
- [ ] 1B.3 — For text without quantity patterns: decompose by sentences. Each sentence with an action verb = 1 candidate task.
- [ ] 1B.4 — Assign default acceptance criteria from `enrichment-rules.yaml` `acceptance_by_type` section based on detected type

### Action Items — Task List Input (`input_type == task_list`)

- [ ] 1C.1 — Parse input as list (look for numbered list, bullet points, or newline-separated items)
- [ ] 1C.2 — For each item: extract description
- [ ] 1C.3 — For each item: check if acceptance criteria are present (look for "criteria:", "acceptance:", "must", "should")
- [ ] 1C.4 — For items WITHOUT acceptance criteria: generate operational criteria from `enrichment-rules.yaml` `acceptance_by_type` based on detected type
- [ ] 1C.5 — For items with vague criteria (V1.2 patterns: "good", "appropriate", "well-written"): replace with measurable alternatives

### Phase 1 Checkpoint

- [ ] At least 1 task extracted from input
- [ ] Each task has a description
- [ ] Quantity patterns applied (no compound deliverables)
- [ ] Each task has acceptance criteria (original or generated)

---

## PHASE 2: Generate Story-Format Output

**Checkpoint:** Temporary story file written in consumable format.

### Action Items

- [ ] 2.1 — Build story-format document with the following structure:
  ```markdown
  # [Converted Input] {brief title from input}

  ## Source
  - Input type: {input_type}
  - Original input: {first 200 chars of raw_input}
  - Converted at: {timestamp}
  - Run ID: {run_id}

  ## Description
  {Full original input text, preserved verbatim}

  ## Acceptance Criteria
  - [ ] {criterion 1 — measurable, binary}
  - [ ] {criterion 2 — measurable, binary}
  ...

  ## Extracted Tasks
  1. {task description} → output: {expected output type}
  2. {task description} → output: {expected output type}
  ...
  ```
- [ ] 2.2 — Validate EVERY acceptance criterion is operational (V1.2):
  - No "good quality", "well-written", "appropriate tone"
  - Each criterion is measurable: contains a number, file path, format, or binary check
  - Each criterion is binary: unambiguously PASS or FAIL
- [ ] 2.3 — Validate no placeholders remain: `[XXX]`, `{TODO}`, `TBD` (V1.3)
- [ ] 2.4 — Preserve original input verbatim in Description section (never modify user content)
- [ ] 2.5 — Write output to: `_temp/dispatch/runs/{run_id}/converted-input.md`
- [ ] 2.6 — Log conversion summary to console:
  - "Converted {input_type} → story format: {task_count} tasks extracted"
  - "Output: _temp/dispatch/runs/{run_id}/converted-input.md"

### Phase 2 Checkpoint

- [ ] File exists at `_temp/dispatch/runs/{run_id}/converted-input.md`
- [ ] File has Source, Description, Acceptance Criteria, and Extracted Tasks sections
- [ ] All acceptance criteria are operational (V1.2)
- [ ] Zero placeholders (V1.3)
- [ ] Original input preserved verbatim in Description

---

## Acceptance Criteria

All criteria are measurable and binary (PASS/FAIL):

1. Output file exists at `_temp/dispatch/runs/{run_id}/converted-input.md`
2. Output file contains `## Acceptance Criteria` section with at least 1 criterion
3. Output file contains `## Extracted Tasks` section with at least 1 task
4. Every acceptance criterion is measurable and binary — no subjective terms (V1.2)
5. Zero placeholders `[XXX]`, `{TODO}`, `TBD` in output (V1.3)
6. Original input text is preserved verbatim in `## Description` section
7. Quantity patterns correctly expanded (e.g., "3 newsletters" = 3 separate tasks)
8. V0.2 enforced: inputs < 10 words without deliverables are VETOED (not converted)
9. V0.3 enforced: inputs without specific deliverables are VETOED (not converted)
10. Conversion adds structure only — zero invented content

---

## Output Specification

| Field         | Value                                                |
|--------------|------------------------------------------------------|
| Format       | Markdown                                              |
| Filename     | `converted-input.md`                                  |
| Location     | `_temp/dispatch/runs/{run_id}/`                       |
| Full path    | `_temp/dispatch/runs/{run_id}/converted-input.md`     |

---

## Dependencies

| File                                               | Purpose                                       |
|---------------------------------------------------|------------------------------------------------|
| `squads/dispatch/data/enrichment-rules.yaml`      | quantity_patterns, acceptance_by_type           |
| `squads/dispatch/data/veto-conditions.yaml`       | V0.* sufficiency conditions                    |
| `scripts/extract-quantities.py`                   | Deterministic quantity extraction (CODE > LLM) |

---

## Error Handling

| Error                                        | Action                                                            |
|---------------------------------------------|-------------------------------------------------------------------|
| raw_input is empty                          | BLOCK — nothing to convert                                        |
| raw_input file path does not exist          | BLOCK — return error with attempted path                          |
| V0.2 triggered (< 10 words, no deliverables) | VETO — redirect to /pm or /po with helpful message              |
| V0.3 triggered (no specific deliverables)   | VETO — ask user for quantities and deliverables                   |
| 0 tasks extracted after parsing             | VETO V0.3 — input lacks actionable content, redirect             |
| Generated criterion is subjective (V1.2)    | Rewrite with measurable alternative before writing output         |
| input_type is "story"                       | SKIP this task entirely — stories go directly to plan-execution  |

---

## Estimated Time

| Scenario                           | Time     |
|-----------------------------------|----------|
| Simple task list (3-5 items)      | 1 min    |
| Free text with quantities         | 1-2 min  |
| PRD with requirements section     | 2-3 min  |
| Ambiguous input requiring veto    | < 30 sec (fast fail) |

---

## Next Step

After this task completes, the converted input flows to:
1. **wave-planner** (plan-execution) — decomposes into atomic tasks with dependency DAG
   - `plan-execution` receives `converted-input.md` as `story_file` with `input_type: story`

**If vetoed (V0.2 or V0.3):**
1. User is redirected to `/pm` (for PRD creation) or `/po` (for story with acceptance criteria)
2. After user creates proper input, dispatch can be re-invoked
