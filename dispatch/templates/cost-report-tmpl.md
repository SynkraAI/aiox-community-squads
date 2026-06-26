# Dispatch Cost Report

> **Run:** {{run_id}}
> **Date:** {{date}}
> **Pricing:** 2026 rates (Haiku $1/$5, Sonnet $3/$15, Opus $5/$25 per MTok)

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Cost** | ${{total_cost_usd}} |
| **Total Tasks** | {{total_tasks}} |
| **Avg Cost/Task** | ${{avg_cost_per_task}} |
| **Opus Equivalent** | ${{opus_equivalent_cost}} |
| **Savings** | **{{savings_pct}}%** (${{savings_usd}} saved) |

---

## Cost by Wave

| Wave | Tasks | Model Mix | Input Tokens | Output Tokens | Cost | Cache Savings |
|------|-------|-----------|-------------|---------------|------|---------------|
{{#each waves}}
| {{this.wave_num}} | {{this.task_count}} | {{this.model_mix}} | {{this.tokens_in}} | {{this.tokens_out}} | ${{this.cost_usd}} | ${{this.cache_savings}} |
{{/each}}
| **Total** | **{{total_tasks}}** | — | **{{total_tokens_in}}** | **{{total_tokens_out}}** | **${{total_cost_usd}}** | **${{total_cache_savings}}** |

---

## Cost by Model

| Model | Tasks | Input Tokens | Output Tokens | Input Cost | Output Cost | Total Cost | % of Total |
|-------|-------|-------------|---------------|------------|-------------|------------|------------|
| Worker | {{worker_count}} | — | — | $0.00 | $0.00 | $0.00 | 0% |
| Haiku | {{haiku_count}} | {{haiku_tokens_in}} | {{haiku_tokens_out}} | ${{haiku_input_cost}} | ${{haiku_output_cost}} | ${{haiku_total_cost}} | {{haiku_pct}}% |
| Sonnet | {{sonnet_count}} | {{sonnet_tokens_in}} | {{sonnet_tokens_out}} | ${{sonnet_input_cost}} | ${{sonnet_output_cost}} | ${{sonnet_total_cost}} | {{sonnet_pct}}% |
| **Total** | **{{total_tasks}}** | **{{total_tokens_in}}** | **{{total_tokens_out}}** | **${{total_input_cost}}** | **${{total_output_cost}}** | **${{total_cost_usd}}** | 100% |

---

## Cost by Domain

| Domain | Tasks | Primary Model | Cost | % of Total |
|--------|-------|---------------|------|------------|
{{#each domains}}
| {{this.name}} | {{this.task_count}} | {{this.primary_model}} | ${{this.cost_usd}} | {{this.pct}}% |
{{/each}}

---

## Prompt Caching Analysis

| Metric | Value |
|--------|-------|
| **Cacheable tokens** | {{cacheable_tokens}} |
| **Cache hits** | {{cache_hits}} |
| **Cache read cost** | ${{cache_read_cost}} |
| **Uncached cost (same tokens)** | ${{uncached_cost}} |
| **Cache savings** | ${{cache_savings}} ({{cache_savings_pct}}%) |

### Cache Efficiency by Wave

| Wave | Same-Domain Tasks | Cache-Eligible | Cache Savings |
|------|-------------------|----------------|---------------|
{{#each waves}}
| {{this.wave_num}} | {{this.same_domain_count}}/{{this.task_count}} | {{this.cache_eligible_pct}}% | ${{this.cache_savings}} |
{{/each}}

---

## Estimate vs Actual

| Metric | Estimated | Actual | Delta | Status |
|--------|-----------|--------|-------|--------|
| Total cost | ${{estimated_cost}} | ${{total_cost_usd}} | {{cost_delta_pct}}% | {{cost_status}} |
| Total tasks | {{estimated_tasks}} | {{actual_tasks}} | {{task_delta}} | {{task_status}} |
| Duration (min) | {{estimated_duration}} | {{actual_duration}} | {{duration_delta_pct}}% | {{duration_status}} |
| Retries | {{estimated_retries}} | {{actual_retries}} | {{retry_delta}} | {{retry_status}} |

**V2.3 Check:** Actual cost {{#if cost_within_budget}}within{{else}}EXCEEDED{{/if}} 3x estimate (threshold: ${{cost_threshold}})

---

## Pricing Reference (2026)

| Model | Input/MTok | Output/MTok | Cache Write | Cache Read |
|-------|-----------|------------|------------|------------|
| Haiku 4.5 | $1.00 | $5.00 | $1.25 | $0.10 |
| Sonnet 4.5 | $3.00 | $15.00 | $3.75 | $0.30 |
| Opus 4.6 | $5.00 | $25.00 | $6.25 | $0.50 |
| Batch (any) | 50% off | 50% off | — | — |

---

## CODE > LLM Efficiency

| Metric | Value |
|--------|-------|
| Worker tasks (scripts) | {{worker_count}} |
| Agent tasks (LLM) | {{agent_count}} |
| CODE > LLM ratio | {{code_llm_ratio}} |
| Cost saved by Workers | ${{worker_savings}} |

**Recommendation:** {{code_llm_recommendation}}
