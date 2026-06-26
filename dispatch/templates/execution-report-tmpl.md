# Dispatch Execution Report

> **Run:** {{run_id}}
> **Started:** {{started_at}} | **Completed:** {{completed_at}}
> **Duration:** {{duration_min}} min
> **Status:** {{status}}

---

## Input

| Field | Value |
|-------|-------|
| **Type** | {{input_type}} |
| **Source** | {{input_path}} |
| **Description** | {{description}} |
| **Tasks** | {{total_tasks}} |
| **Waves** | {{total_waves}} |

---

## Execution Summary

### Wave Results

| Wave | Tasks | Pass | Fail | Retry | Duration | Cost |
|------|-------|------|------|-------|----------|------|
{{#each waves}}
| {{this.wave_num}} | {{this.task_count}} | {{this.pass_count}} | {{this.fail_count}} | {{this.retry_count}} | {{this.duration_sec}}s | ${{this.cost_usd}} |
{{/each}}
| **Total** | **{{total_tasks}}** | **{{total_pass}}** | **{{total_fail}}** | **{{total_retry}}** | **{{total_duration_sec}}s** | **${{total_cost_usd}}** |

### Deming PDSA — Prediction vs Actual

| Wave | Predicted Outputs | Actual Outputs | Predicted Cost | Actual Cost | Delta |
|------|-------------------|----------------|----------------|-------------|-------|
{{#each waves}}
| {{this.wave_num}} | {{this.predicted_outputs}} | {{this.actual_outputs}} | ${{this.predicted_cost}} | ${{this.actual_cost}} | {{this.delta_pct}}% |
{{/each}}

---

## Task Details

{{#each tasks}}
### {{this.task_id}}: {{this.description}}

| Field | Value |
|-------|-------|
| Agent | `{{this.agent}}` |
| Model | {{this.model}} |
| Executor | {{this.executor_type}} |
| Status | {{this.status}} |
| Attempts | {{this.attempts}}/{{this.max_attempts}} |
| Output | `{{this.output_path}}` |
| Cost | ${{this.cost_usd}} |

{{#if this.error}}
**Error:** {{this.error}}
{{/if}}

**Acceptance Criteria:**
{{#each this.acceptance_criteria}}
- [{{#if this.passed}}x{{else}} {{/if}}] {{this.criterion}}
{{/each}}

---
{{/each}}

## Failures & Retries

{{#if has_failures}}
| Task | Error | Attempts | Resolution |
|------|-------|----------|------------|
{{#each failures}}
| {{this.task_id}} | {{this.error}} | {{this.attempts}} | {{this.resolution}} |
{{/each}}
{{else}}
No failures in this run.
{{/if}}

---

## Veto Gate Results

### Pre-Execution Gate (V1.*)

| Veto | Condition | Result |
|------|-----------|--------|
{{#each pre_execution_vetos}}
| {{this.id}} | {{this.condition}} | {{this.result}} |
{{/each}}

### Post-Execution Gate (V2.*)

| Veto | Condition | Result |
|------|-----------|--------|
{{#each post_execution_vetos}}
| {{this.id}} | {{this.condition}} | {{this.result}} |
{{/each}}

---

## Health Score

**Score: {{health_score}}/12 — {{health_rating}}**

| # | Check | Status |
|---|-------|--------|
{{#each health_items}}
| {{this.id}} | {{this.name}} | {{this.status}} |
{{/each}}

---

## Story Update

{{#if is_story_input}}
**Story:** `{{input_path}}`

**Acceptance Criteria Updated:**
{{#each story_acceptance}}
- [{{#if this.passed}}x{{else}} {{/if}}] {{this.criterion}}
{{/each}}
{{else}}
Input was not a story — no story checkboxes to update.
{{/if}}

---

## Cost Breakdown

See detailed cost report: `_temp/dispatch/runs/{{run_id}}/cost-report.md`

| Model | Tasks | Input Tokens | Output Tokens | Cost |
|-------|-------|-------------|---------------|------|
| Worker | {{worker_count}} | — | — | $0.00 |
| Haiku | {{haiku_count}} | {{haiku_tokens_in}} | {{haiku_tokens_out}} | ${{haiku_cost}} |
| Sonnet | {{sonnet_count}} | {{sonnet_tokens_in}} | {{sonnet_tokens_out}} | ${{sonnet_cost}} |
| **Total** | **{{total_tasks}}** | **{{total_tokens_in}}** | **{{total_tokens_out}}** | **${{total_cost_usd}}** |

**Savings vs Opus main context:** ${{opus_equivalent_cost}} → ${{total_cost_usd}} = **{{savings_pct}}% savings**

---

## Learnings (Deming Third Way)

{{#each learnings}}
{{@index}}. {{this}}
{{/each}}

---

## Next Steps

1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}
4. Other
