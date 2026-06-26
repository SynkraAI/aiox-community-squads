# Changelog - Brand Squad

All notable changes to this squad will be documented in this file.

## [1.1.1] - 2026-03-10

### Fixed
- Added explicit `COO`/`c-level` readiness contract to the Brand squad workspace integration
- Added native `brand` readiness resolution in `workspace/scripts/resolve-squad-workspace-readiness.cjs`
- Updated all 8 workflows to require `resolve-squad-workspace-readiness.cjs` during preflight
- Added missing `validate-brand-essentials.sh` preflight to `wf-logo-brainstorm.yaml` and `wf-brand-mockup-generation.yaml`
- Aligned visual workflow runtime steps with `nano-banana-generator` instead of mixed `aiox-master` routing
- Added a local validation bridge for `nano-banana-generator` so workflow contract validation passes without warnings

## [1.1.0] - 2026-03-06

### Fixed
- Added `entry_agent: brand-chief` to config.yaml (was missing)
- Added `activation-instructions` to brand-chief.md
- Added `tested: true` to config.yaml
- Created missing `wf-brand-mockup-generation.yaml` workflow
- Removed legacy `squad.yaml` (canonical is `config.yaml`)
- Added `*help` command to brand-chief
- Added `voice_dna`, `output_examples`, `objection_algorithms` to all 15 agents
- Created CHANGELOG.md, ARCHITECTURE.md
- Created lifecycle tasks: update-brand.md, delete-brand.md
- Created brand-naming-checklist.md

## [1.0.0] - 2026-02-18

### Added
- Initial squad creation with 15 agents (Brasil-first)
- SNP (Igor Pinterich) + E/F/F (Ana Couto) as primary methodologies
- 11 global specialists for foundations, positioning, narrative, activation
- 7 workflows: naming-to-domain, foundations, positioning-narrative, activation-system, all-hands, logo-brainstorm, brand-complete
- 16 tasks covering naming, domain, branding, logo, and epic management
- workspace-first integration with bootstrap and essentials validation
- Cross-squad integration with Design squad for logo/mockup generation
