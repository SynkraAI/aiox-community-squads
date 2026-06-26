# Brand YOLO Optimization Plan

Date: 2026-03-10
Squad: `brand`
Status: `executed`

## Wave 1: Foundation convergence

Goal: align the canonical workspace contract everywhere it is executed.

Changes:

- add `COO` readiness resolver to `workspace_contract.required_preflight` in
  all 8 brand workflows
- add `validate-brand-essentials.sh` to the 2 workflows that still skip it
- preserve current `context_task: load-workspace-context`

Result:

- completed

Target files:

- `squads/brand/workflows/wf-naming-to-domain.yaml`
- `squads/brand/workflows/wf-brand-foundations.yaml`
- `squads/brand/workflows/wf-brand-positioning-narrative.yaml`
- `squads/brand/workflows/wf-brand-activation-system.yaml`
- `squads/brand/workflows/wf-brand-complete.yaml`
- `squads/brand/workflows/wf-brand-all-hands.yaml`
- `squads/brand/workflows/wf-logo-brainstorm.yaml`
- `squads/brand/workflows/wf-brand-mockup-generation.yaml`

## Wave 2: Cross-squad executor convergence

Goal: make the workflow runtime match the declared design executor.

Changes:

- replace `agent: aiox-master` with `agent: nano-banana-generator` in image
  generation/refinement steps
- keep the existing cross-squad design routing and handoff prompts aligned with
  that executor
- add a local validation bridge for `nano-banana-generator` under
  `squads/brand/agents/` while keeping Design as canonical owner

Result:

- completed

Target files:

- `squads/brand/workflows/wf-logo-brainstorm.yaml`
- `squads/brand/workflows/wf-brand-mockup-generation.yaml`

## Wave 3: Validation and self-heal

Goal: confirm the squad still passes structural and workflow checks after the
convergence waves.

Validation:

- `bash squads/squad-creator/scripts/validate-squad.sh brand --quick --json`
- targeted drift scan on `required_preflight`
- targeted drift scan on image workflow executors

Result:

- completed with `PASS`

## Commit / Push

- commit: not requested
- push: not requested

## Stop Conditions

- any new validation failure
- any unexpected drift beyond the planned edit scope
- any evidence that `nano-banana-generator` should remain abstracted through
  `aiox-master`
