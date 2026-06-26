# Changelog — claude-code-mastery

All notable changes to the Claude Code Mastery squad.

## [3.0.0] - 2026-04-03

### SINKRA-Native Upgrade (STORY-CCM-INT.1)

#### Added
- `accountability_token: TK-CCM-ACC-001` in all 31 task Contrato SINKRA blocks
- `output_schema` specific refs in all 31 tasks (mapping task output to artifact contracts)
- Specific acceptance criteria in 13 tasks that had generic ACs
- CCM tokens registered in central SINKRA token registry (`sinkra-squad/data/token-registry.yaml`)
- `sinkra_refs` in `composition_mapping.atoms` linking atoms to token registry
- `sinkra_refs` in `composition_mapping.molecules` linking journey log + state machines
- 3 missing atoms added to `composition_mapping` (align-memory-context, rebuild-runtime-validator, refresh-runtime-contract)
- `sinkra_native: true` flag in config.yaml
- Injection scripts: `inject-accountability-tokens.js`, `inject-output-schemas.js`

#### Changed
- config.yaml version bumped to 3.0.0
- Baseline score: 6.8/10 -> SINKRA-native compliant

## [1.0.0] - 2026-03-02

### Added
- 8 specialist agents: claude-mastery-chief (Orion), hooks-architect (Latch), mcp-integrator (Piper), swarm-orchestrator (Nexus), config-engineer (Sigil), skill-craftsman (Anvil), project-integrator (Conduit), roadmap-sentinel (Vigil)
- 26 executable tasks across all agents
- 3 multi-phase workflows (wf-project-setup, wf-knowledge-update, wf-audit-complete)
- 5 knowledge base files (quick-ref, project-type-signatures, hook-patterns, ci-cd-patterns, mcp-catalog)
- 7 templates (5 CLAUDE.md project templates + 2 GitHub Actions workflows)
- 8 mind DNA summaries (disler, steipete, kieran-klaassen, reuven-cohen, superclaude-org, bmad-code-org, daniel-miessler, boris-cherny)
- 1 validation script (validate-setup.js)
- Tier architecture: Tier 0 (Diagnosis), Tier 1 (Core Mastery), Tier 2 (Strategic & Context)
- Handoff matrix with full routing between all agents
- AIOX-core integration bridge (agents, tasks, hooks, config mapping)

### Architecture
- Entry agent: claude-mastery-chief (Orion) with 7-domain routing matrix
- Cross-cutting concern: all agents understand AIOX-core architecture
- Knowledge sources: Claude Code changelog, official docs, community resources
