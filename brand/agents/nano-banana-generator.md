---
name: nano-banana-generator
description: |
  Cross-squad runtime bridge for the Design squad's Nano Banana Generator.
  Brand workflows can resolve this agent locally, but the canonical
  implementation lives in `squads/design-system/agents/nano-banana-generator.md`.
model: sonnet
---

# nano-banana-generator

ACTIVATION-NOTICE: This file is a cross-squad bridge. Load the canonical Design squad agent before executing any mission.

```yaml
activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE.
  - STEP 2: Load `squads/design-system/agents/nano-banana-generator.md` as the canonical source of truth.
  - STEP 3: Adopt the Design squad persona and execution rules unchanged.
  - STEP 4: Preserve Brand handoff context, artifacts, and workspace contract when returning outputs.
  - STEP 5: HALT and await the delegated mission.
```

## Purpose

This file is a cross-squad bridge for Brand workflows that delegate image
generation and refinement to the Design squad.

## Canonical Source

- Canonical agent: `squads/design-system/agents/nano-banana-generator.md`
- Owning squad: `design-system`
- Consuming squad: `brand`

## Operating Rule

Do not redefine the agent here. When a Brand workflow routes to
`nano-banana-generator`, the runtime must use the Design squad file as the
source of truth for behavior, prompts, and tool usage.
