# ETL Process

## Contrato SINKRA

Domain: `Operational`
executor: etl-chief
atomic_layer: Organism
Input: process.schema payload, desired_output, constraints
Output: output-contract envelope, checkpoints, persisted artifacts
Pre-condition: schema de entrada válido e preflight concluído
Post-condition: extração, transformação e entrega concluídas com checkpoints
Performance: bloquear source inválida, extração vazia ou contract drift


## Metadata

| Field | Value |
|---|---|
| **task_name** | Process Source Into Usable Content |
| **status** | Active |
| **responsible_executor** | `@etl-chief` |
| **execution_type** | `Hybrid` |
| **input** | `process.schema.json` payload with `source`, `desired_output`, `mode`, `constraints` |
| **output** | Contract envelope from `output-contract.yaml` |
| **action_items** | 8-phase unidirectional flow with workspace preflight + veto conditions |
| **acceptance_criteria** | 14 measurable criteria |

## Purpose

Single entry point for ETL operations. The chief diagnoses the source, routes execution to extractor/transformer, and enforces checkpoints until delivery.

## Inputs

Use the JSON schema in `squads/etl-ops/data/process.schema.json`.

Minimum input:

```json
{
  "source": {
    "kind": "url",
    "value": "https://example.com/post"
  },
  "desired_output": "chunks",
  "mode": "single"
}
```

Workspace-aware optional constraints:

```json
{
  "constraints": {
    "business_slug": "acme",
    "workspace_mode": "auto"
  }
}
```

## Execution Flow

0. Workspace preflight (required)
- If `constraints.business_slug` is present:
  - `bash squads/etl-ops/scripts/bootstrap-etl-workspace.sh {business_slug}`
- Always run:
  - `bash squads/etl-ops/scripts/validate-etl-essentials.sh`
- Always load:
  - `tasks/load-workspace-context.md`
- VETO if workspace route is `blocked`.

1. Diagnose
- Detect source profile via `routing-profiles.yaml`.
- Resolve execution path (CLI or API).
- VETO if source kind is unknown.

2. Validate prerequisites
- Verify source accessibility (`ls`, URL format, required env vars).
- VETO if required precondition fails.

3. Extract
- Execute routed extractor command/API.
- Validate non-empty extraction.
- VETO on extraction error or empty/minimal payload.

4. Structure
- If `constraints.document_strategy=book_progressive`, build structural manifest first.
- Prefer EPUB-derived markdown for books.
- VETO if book manifest is required and no chapters are detected.

5. Context pack
- If `desired_output=book_summary`, assemble `book_context` before any chapter summary.
- `context_sources` may include URLs or inline text.
- If no external context exists, emit deterministic fallback context from the manifest.

6. Transform
- Decide transform path from `desired_output`.
- For `chunks`: select strategy and apply chunking.
- For `clean`/`filtered`: run deterministic path first; LLM only when needed.
- For `book_summary`: summarize one chapter at a time using `book_context` + rolling chapter continuity.
- VETO if transformation fidelity is below threshold for `clean`/`chunks`.
- For `filtered`, VETO on speaker-integrity failure (wrong speaker leakage).

7. Deliver
- Emit standardized output envelope.
- Persist artifacts when requested.
- Include metrics, checkpoints, and warnings.

## Output Routing Policy

- `workspace_mode=auto` (default):
  - with valid `business_slug` -> canonical path:
    - `workspace/businesses/{business_slug}/etl/runs/{run_id}/`
  - without slug -> legacy fallback:
    - `outputs/etl/{run_id}/`
- `workspace_mode=canonical`:
  - requires valid `business_slug`, otherwise VETO.
- `workspace_mode=legacy`:
  - force `outputs/etl/{run_id}/` (no workspace write).
- Custom reports and notes can be written in:
  - `docs/etl/{business_slug|global}/`

## Mode Policy

- `single`: process one source end-to-end.
- `batch`: validate first item fully before processing the remainder.
- `rag`: force chunk-friendly transform and include chunk metadata.

## Book Policy

- `desired_output=book_summary` requires `constraints.document_strategy=book_progressive`
- Prefer `.epub` -> `.md`
- Treat PDF as fallback with warning, not as ideal path
- Build `manifest` and `book_context` before chapter summaries
- Final synthesis must derive from `chapter_summary` artifacts, not from the full book blob

## Checkpoint Rules

Use `squads/etl-ops/data/checkpoints.yaml` as source of truth.

Mandatory:
- Checkpoint after diagnose
- Checkpoint after validate
- Checkpoint after extract
- Checkpoint after structure
- Checkpoint after context_pack
- Checkpoint after transform
- Final delivery integrity checkpoint

## Local Quality Gate

Before marking the process as completed, run:

```bash
bash squads/etl-ops/scripts/validate-etl-essentials.sh
npm run validate:etl-ops
```

If the command fails:
- STOP delivery
- report contract drift or missing artifacts
- fix contracts/agents/wrappers first, then re-run

If the command reports WARN:
- continue execution (non-blocking advisory)
- include warnings in final envelope for follow-up hardening

## Acceptance Criteria

1. Input conforms to `process.schema.json`.
2. Source is classified to a valid routing profile.
3. Prerequisite failures produce explicit veto messages.
4. Extraction output is non-empty and format-valid.
5. Transformation preserves fidelity threshold rules.
6. Output follows `output-contract.yaml`.
7. `batch` mode validates first item before full run.
8. Execution includes per-phase checkpoint records.
9. Workspace preflight runs before diagnose.
10. `load-workspace-context` decides output route before extraction.
11. Local quality gates (`validate-etl-essentials` + `validate:etl-ops`) pass before completion.
12. `book_summary` only runs after manifest generation.
13. `book_summary` emits `book_context` before chapter loop.
14. Final book synthesis is derived from staged artifacts, not the raw full-book prompt.


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
