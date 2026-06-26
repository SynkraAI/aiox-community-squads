# Gerador Pop YOLO Optimization Plan

Date: 2026-03-18
Squad: `aiox-sop`
Status: `pending_approval`

## Preflight Snapshot

- environment contract: `pro + portable_docs_mode + docs_projection`
- projection path: `docs/squad/aiox-sop/operational-projection.yaml` (`present`, `current`, updated `2026-03-10`)
- local baseline: `bash squads/squad-creator/scripts/validate-squad.sh aiox-sop --quick --json` -> `PASS 10/10`
- workflow contracts baseline:
  - relaxed: `PASS`
  - strict: `PASS`
- doc drift baseline: `PASS`
- repo-global baseline: `pass`
- risk profile: `medium`
  - no pre-existing dirty files inside `squads/aiox-sop/`
  - optimization scope touches workflow routing and support-material classification across multiple surfaces
  - no `voice_dna` surface exists in `aiox-sop`, so the voice-dna veto remains inactive

## Optimization Findings

### F1. Extraction workflow ownership drifts from the squad routing contract

`agents/sop-chief.md` routes extraction work to `sop-extractor`, and the
`extract-sop` / `extract-from-video` tasks also frame extraction as the
extractor's domain. But `workflows/wf-sop-extraction-pipeline.yaml` assigns the
runtime extraction phases to `sop-creator`, including raw capture, step
decomposition, role mapping, and structure formation.

Impact:

- runtime behavior is harder to reason about because the workflow disagrees with
  the squad's public routing contract
- future automation can mis-route extraction work to the wrong specialist

### F2. The extraction workflow keeps ML-format generation on the wrong surface

Inside `wf-sop-extraction-pipeline.yaml`, the structure-formation phase includes
`Generate ML Format` under the same creator-owned surface instead of making the
specialist ownership explicit.

Impact:

- human and ML output responsibilities are blurred
- the workflow topology hides where specialist handoffs should happen

### F3. `convert-sop-format` stays Agent-only despite a working deterministic worker

`tasks/convert-sop-format.md` still declares `Execution Type: Agent`, but the
repository already ships `scripts/convert-sop-format-worker.py`. Representative
smoke checks succeeded for both directions:

- `sample-human-sop.md -> yaml`
- `sample-ml-sop.yaml -> human-md`

Impact:

- deterministic work still incurs agent-level overhead
- the task contract underuses the worker surface that already exists and works

### F4. Support materials conflict with the canonical output contract

The squad contract says generated artifacts belong under `outputs/aiox-sop/`,
but the repository still contains slide SOP packages under
`squads/aiox-sop/outputs/`. At least one retained package also embeds the
old squad-local storage path inside its content.

Impact:

- operators can confuse reference packages with canonical publish outputs
- maintenance workflows inherit an avoidable source-of-truth ambiguity

### F5. Workflow backup files are useful for recovery but are not canonical runtime surfaces

The `.bak` workflow files are currently unreferenced support materials.

Impact:

- they should remain available for rollback, but they should be treated as
  archive/support artifacts, not active runtime contract surfaces

## Priority Matrix

| ID | Change | ROI | Risk | Decision |
|----|--------|-----|------|----------|
| F1 | Align extraction workflow specialist ownership | High | Medium | Execute |
| F2 | Make ML handoff explicit in extraction workflow | High | Medium | Execute |
| F3 | Convert `convert-sop-format` to Worker/Hybrid contract and document CLI path | High | Low | Execute |
| F4 | Reclassify squad-local output packages as reference/archive materials | Medium | Medium | Execute |
| F5 | Record `.bak` workflows as archive/support only | Low | Low | Execute if touched by F1/F2/F4 |

## Planned Waves

## Wave 1: Foundation Convergence

Goal: restore a single runtime source of truth for extraction ownership.

Planned changes:

- align `wf-sop-extraction-pipeline.yaml` with `sop-chief` routing and the
  extractor task contracts
- make specialist ownership explicit where ML output generation appears
- preserve `portable_docs_mode` and the current share-safe output contract

Target files:

- `squads/aiox-sop/workflows/wf-sop-extraction-pipeline.yaml`
- `squads/aiox-sop/agents/sop-chief.md` only if the workflow fix exposes any
  wording mismatch that must be corrected

## Wave 2: Deterministic Executor Convergence

Goal: move repeatable conversion work to the worker surface already present in
the repository.

Planned changes:

- update `tasks/convert-sop-format.md` to declare the deterministic worker path
- document the exact command contract for `convert-sop-format-worker.py`
- keep creative generation tasks on Agent; only deterministic conversion moves

Target files:

- `squads/aiox-sop/tasks/convert-sop-format.md`
- `squads/aiox-sop/docs/README.md` if a runner note is needed for local docs

## Wave 3: Material Utility Triage

Goal: remove ambiguity between canonical runtime outputs and squad-local
reference artifacts.

Planned changes:

- classify `squads/aiox-sop/outputs/SOP-SLIDES-*` as reference material, not
  canonical publish outputs
- either relocate them under an explicit reference/examples surface or label
  them clearly as non-canonical support artifacts
- preserve rollback safety for `*.bak` workflow files while keeping them out of
  the active runtime contract narrative

Target files:

- `squads/aiox-sop/outputs/`
- `squads/aiox-sop/examples/README.md`
- `squads/aiox-sop/README.md`
- `squads/aiox-sop/ARCHITECTURE.md`

## Validation After Approval

- `node squads/squad-creator/scripts/detect-environment-contract.cjs --squad=aiox-sop --format=json`
- `bash squads/squad-creator/scripts/validate-squad.sh aiox-sop --quick --json`
- `node infrastructure/scripts/squads/validate_workflow_contracts.cjs --squads aiox-sop --strict --fail-on-warnings --json`
- `node infrastructure/scripts/squads/check_doc_drift.cjs --squad aiox-sop --json`
- runtime smoke for any changed deterministic surface, including representative
  `convert-sop-format-worker.py` arguments
- `npm run lint`
- `npm run typecheck`
- `npm test`

## Commit / Push

- commit: not requested
- push: not requested

## Approval Summary

If approved, execution will continue autonomously through:

1. workflow routing convergence
2. deterministic worker/task hardening
3. material triage
4. runtime smoke
5. validation and evidence reporting

No further confirmation prompts will be requested unless a workflow veto fires.
