# Changelog

## 2026-03-18

- Migrated markdown SOP publication to root `docs/sops/`.
- Migrated machine-readable SOP publication to `workspace/businesses/{business}/sops/` behind the existing business-aware workspace gate.
- Kept `outputs/aiox-sop/` as the auxiliary root for audits, analysis, checklists, and operational reports.
- Realigned extraction workflow ownership so `sop-extractor` owns raw capture, decomposition, and role mapping, while `sop-chief` coordinates structure formation.
- Converted `convert-sop-format` to a worker-first hybrid contract and documented the deterministic CLI runner.
- Classified `squads/aiox-sop/outputs/` as retained reference packages instead of canonical runtime output surfaces.
- Recorded the `*optimize-yolo aiox-sop` execution evidence under `squads/aiox-sop/docs/`.
- Added optional workspace business-context loading via `load-workspace-context` for business-aware analysis in `full_workspace_mode`.

## 2026-03-10

- Registered `aiox-sop` in COO workspace readiness with canonical `operations` context.
- Upgraded `workspace_integration.level` from `none` to `controlled_runtime_consumer`.
- Enabled `full_workspace_mode` when explicit business context and COO readiness are both proven.
- Updated runtime and architecture docs to describe canonical operations readiness.
- Updated tests that previously assumed `aiox-sop` was unsupported by the COO.
- Added enterprise-aware `environment_contract` detection for `aiox-sop`.
- Aligned enterprise proof with the canonical marker `workspace/license/enterprise-runtime.capability.yaml`.
- Added structural squad docs: `README.md`, `ARCHITECTURE.md`, and `CHANGELOG.md`.
- Added maintenance tasks for update and delete flows.
- Added portable operational projection under `docs/squad/aiox-sop/`.
- Corrected output path drift between extraction/audit tasks and workflows.
- Corrected `HEADLINE.md` identity for SOP Factory.
