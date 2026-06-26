# Gerador Pop Optimization Economy

Date: 2026-03-18
Squad: `aiox-sop`

## Before

- extraction ownership was split between the public routing contract and the
  actual workflow topology
- `convert-sop-format` still presented deterministic conversion as an Agent-only
  surface even though a working worker script already existed
- retained reference packages in `squads/aiox-sop/outputs/` visually competed
  with the canonical runtime root `outputs/aiox-sop/`

## After

- extraction workflow ownership now converges on `sop-extractor` for capture,
  decomposition, and role mapping
- structure formation is explicitly coordinated by `sop-chief`, with
  `sop-creator` and `sop-ml-architect` receiving clear handoffs
- `convert-sop-format` is now a worker-first hybrid contract anchored to
  `convert-sop-format-worker.py`
- retained slide SOP packages are explicitly marked as reference/archive
  materials rather than active runtime outputs

## Economy Readout

- deterministic conversion can now bypass an agent turn when the worker script
  succeeds without escalation
- operator review overhead is lower because extraction ownership no longer
  contradicts the squad's public routing contract
- maintenance overhead is lower because canonical publish outputs and retained
  in-repo reference packages are no longer presented as equivalent surfaces

## Limits

No numeric token telemetry is emitted by `aiox-sop`, so the economy verdict
remains qualitative. The strongest measurable change in this run is executor
surface reduction for deterministic conversion and reduced contract ambiguity
for extraction/runtime maintenance.
