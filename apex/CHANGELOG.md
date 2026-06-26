# Changelog — Apex Squad

## [1.7.0] — 2026-03-13

### Added — Alan Nicolas Gap Attack (7 Gaps) + Pedro Valério Audit (8 Fixes)

**New Data Files (Alan Nicolas — @oalanicolas):**
- **`agent-handoff-matrix.yaml`** — 18 formal inter-agent handoff protocols with trigger conditions, artifact specs, conflict resolution rules, arbiters, and escalation paths. Covers all 15 agents. Includes three-step pipeline (Extract→Tokenize→Implement), scope lock propagation, and arbitration hierarchy.
- **`heuristic-source-map.yaml`** — Centralized `[SOURCE:]` attribution for all 101 agent heuristics across 15 agents. Tier breakdown: 93 OURO, 1 MIXED, 7 INFERRED. Every heuristic traceable to origin (blog, talk, repo, or inferred).

**Intelligence Layer Expansion (Alan Nicolas):**
- **16 new intent chains** in `apex-intelligence.yaml` (34 → 50 total): `after_greenfield`, `after_dark_mode_audit`, `after_export_tokens`, `after_integration_test`, `after_refactor`, `after_token_audit`, `after_responsive_scan`, `after_color_audit`, `after_type_audit`, `after_motion_scan`, `after_asset_optimize`, `after_fuse`, `after_discover_external_assets`, `after_discover_token_drift`, `after_asset_pipeline`, `after_icon_system`

**Veto Conditions Expansion (Alan Nicolas):**
- 5 new conditions: `VC-STRUCT-001` (non-grid spacing), `VC-A11Y-EXT-001` (external asset alt text), `VC-MOTION-EXT-001` (animated asset fps), `VC-PERF-EXT-001` (asset optimization), `VC-ASSET-EXT-001` (extracted token drift threshold)
- Total: 149 → 154 conditions across 37 gates

**Design Presets Upgrade (Alan Nicolas):**
- 3 Bronze-tier references upgraded to OURO: retro-y2k, claymorphism, cyberpunk — all now reference production sites with verified design patterns

**Workflow Rollback Protocol (Alan Nicolas):**
- Standardized 6-step rollback protocol added to 7 workflows: SNAPSHOT→IDENTIFY→REVERT→VERIFY→REPORT→RETRY/ESCALATE
- Per-phase scope, git-based recovery, user approval required, escalation to apex-lead
- Workflows: wf-component-create, wf-component-refactor, wf-cross-platform-sync, wf-feature-build, wf-polish-cycle, wf-ship-validation, apex-vision-workflow

### Fixed — Pedro Valério Process Audit (8 Remediations)

**Handoff Matrix (3 fixes):**
- FIX-01: Added `conflict_resolution` to `apex_to_devops` handoff (was missing arbiter)
- FIX-02: Added 5 missing handoff protocols: `apex_to_aria`, `kent_to_aria`, `josh_to_aria` (frontend-arch), `kilian_to_paul`, `krzysztof_to_paul` (spatial-eng) — these agents had zero formal protocols
- FIX-03: Expanded artifact specs: CONTRAST_CHECK +2 fields (`success_criteria`, `revalidation_scope`), LAYOUT_SPEC +2 fields (`a11y_constraints`, `browser_support`)

**Intent Chain Loop Fix (2 fixes):**
- FIX-04: Removed `*discover-token-drift` from `after_fuse` options — broke circular loop: `after_fuse→*discover-token-drift→after_discover_token_drift→*scrape→after_scrape→*fuse→LOOP`. Replaced with `*apex-suggest`
- FIX-05: Added `max_iterations: 2` guard to `after_discover_external_assets` (option 3 called itself)

**Veto Condition Clarity (3 fixes):**
- FIX-06: VC-STRUCT-001 — added exception clause: "only 0px (reset) and 1px (separator) are acceptable — document reason in file comment"
- FIX-07: VC-MOTION-EXT-001 — added specific thresholds: "mobile >= 60fps, desktop >= 100fps. Measure via DevTools Performance tab"
- FIX-08: VC-ASSET-EXT-001 — added drift thresholds: "colors HSL distance > 15% or hue shift > 10°, spacing > 2px, font-weight > 2 steps, radius > 1px"

### Changed
- squad.yaml: v1.6.0 → v1.7.0
- CLAUDE.md: veto count 149→154, version footer v1.6.0→v1.7.0
- README.md: badges, counts, +3 new sections (Handoff Matrix, Source Map, Rollback Protocol)
- design-presets.yaml: retro-y2k ref #2 (added description), ref #3 (replaced archive URL with production URL)

### Stats
- Intent chains: 34 → **50** (+16)
- Veto conditions: 149 → **154** (+5 new)
- Handoff protocols: 0 → **18** (new file)
- Heuristic attributions: 0 → **101** (new file)
- Workflows with rollback: 0 → **7** (standardized protocol)
- Data files: 27 → **29** (+2: agent-handoff-matrix, heuristic-source-map)
- Design preset references: 3 upgraded Bronze→OURO

## [1.6.0] — 2026-03-13

### Added
- **Asset Pipeline Task** (`apex-asset-pipeline.md`) — Brand asset recreation with 3 modes: geometric (SVG from image), enhance (optimize existing), compose (create from scratch). Includes honesty gate for brand fidelity claims.
- **Icon System Task** (`apex-icon-system.md`) — Icon system management with 4 modes: audit (health score), setup (library selection + architecture), create (custom SVG icons), migrate (switch libraries).
- **Brand Asset Standards Checklist** (`brand-asset-standards.md`) — 26 quality checks across 5 categories: visual fidelity, technical standards, design system integration, brand honesty gate, cross-platform.
- **21 New Design Presets** (31 → 52 total):
  - `design-presets-premium.yaml` — 15 presets: Luxury & Haute (3), Premium Tech (2), Automotive Premium (2), Healthcare Premium (2), Digital Marketing (2), Food & Hospitality (2), Resort & Travel (2)
  - `design-presets-bigtech.yaml` — 6 presets: Microsoft Fluent, Meta/Instagram, Netflix, Airbnb, Uber, OpenAI
- **Quality Gates** — QG-AX-ASSET (7 veto conditions) + QG-AX-ICON (5 veto conditions) registered in SSoT
- **Intent Chaining** — `after_asset_pipeline` + `after_icon_system` in apex-intelligence.yaml
- **Vocabulary Bridge** — `asset_brand_creation` category with 6 NL patterns
- **Triage Routing** — `asset-brand-creation` domain + `icon-system-audit` discovery domain
- **Playwright MCP** — `.mcp.json` configured for browser automation; vision tasks have fallback (Playwright → manual screenshot)

### Changed
- `*apex-inspire` — Browse 52 presets (was 31)
- `*apex-transform` — Supports 52 presets across 15 categories (was 31 across 7)
- `apex-visual-analyze.md` — Step 0 browser capability detection added

### Stats
- Tasks: 142 → 144 (+2)
- Checklists: 21 → 22 (+1)
- Data files: 25 → 27 (+2)
- Design presets: 31 → 52 (+21)
- Veto conditions: 137 → 149 (+12)
- Quality gates: 35 → 37 (+2)

## [1.5.0] — 2026-03-13

### Added — Pedro Valério Documentation Audit

**Documentation:**
- **README.md complete rewrite**: 13 gaps fixed — 15 agents (added web-intel), 161 tasks, 13 discovery tools, web intelligence section, implicit heuristics section, agent blind spots section, updated profiles
- **`implicit-heuristics.yaml`**: 8 codified expert heuristics (undocumented instincts formalized)
- **`agent-blind-spots.yaml`**: Blind spots for all 15 agents (calibration data for orchestrator routing)
- **`generate-squad-greeting.cjs`**: Context-aware greeting generator script with git context and profile detection

### Changed
- README.md: v1.4.0 → v1.5.0 (complete rewrite with all capabilities documented)
- CLAUDE.md: Fixed veto count (121→137), discovery count (11→13), profile agent counts, version footer
- squad.yaml: Fixed agent count (14→15), added web-intel to tier_2
- CHANGELOG.md: Added v1.5.0 entry, fixed agent/task/discovery counts in v1.4.0

### Metrics
- Agents: 14 → **15** (+1: web-intel/Kilian)
- Tasks: 139 core + 22 extensions = **161** total
- Discovery tools: 11 → **13** (+2: external-assets, token-drift)
- Data files: 21 → **24** (+3: implicit-heuristics, agent-blind-spots, vocabulary-bridge)
- Veto conditions: 137 across 35 gates (unchanged)

## [1.4.0] — 2026-03-12

### Added — Alan Nicolas Knowledge Assessment + Pedro Valerio Structural Audit

**New Capabilities:**
- **`*apex-greenfield`**: Create complete frontend projects from scratch — 8 phases, smart defaults (React 19 + Vite + Tailwind CSS 4 + Motion), zero technical questions to user
- **Vocabulary Bridge** (`data/vocabulary-bridge.yaml`): 50+ patterns across 10 categories mapping non-technical language → technical implementation with visual confirmation before execution
- **Intent Clarification** (Step 1.6 in apex-fix): Translates user request to visual language, confirms understanding before executing
- **Scope Lock Protocol** (Step 1.5 in apex-fix): Declares and locks modification scope BEFORE any change — out-of-scope changes are BLOCKED
- **Snapshot Protocol** (Step 1.8 in apex-fix): `git stash` before every modification for instant rollback
- **Request Adherence Gate** (QG-AX-FIX-002): Validates that changes match the original request exactly
- **Expansion Protocol** for vocabulary-bridge: Formal process to add new patterns from real user interactions
- **Implicit Knowledge section** in apex-kb.md: 3 formalized premises (header sticky, spring rationale, vocabulary expansion)

**Structural Completeness:**
- apex-lead.md commands: 29 → **62** (100% coverage of all documented commands)
- apex-lead.md task dependencies: 6 → **41** (100% coverage)
- apex-lead.md data dependencies: 6 → **20** (100% coverage)
- apex-lead.md workflow dependencies: 6 → **9** (100% coverage)
- apex-lead.md checklists: Fixed 2 broken references (`motion-compliance` → `motion-review`, `a11y-compliance` → `a11y-review`)

**Knowledge Quality (Alan Nicolas Assessment):**
- Curadoria Score: 9.1/10 (78% OURO, 15% OURO-, 7% BRONZE+)
- Trindade (Playbook + Framework + Swipe File): 8.5 → **9.5** (output examples added)
- Crown Jewels identified: veto conditions, vocabulary bridge, scope lock/snapshot
- Zero implicit knowledge remaining — all formalized

**Lazy-Load Modules (Context Optimization):**
- apex-lead.md reduced from 70KB (1455 lines) → 30KB (811 lines) — **57% reduction**
- 5 lazy-loaded modules: voice DNA, thinking DNA, examples, platforms, guide
- Modules load only when specific commands are invoked

### Changed
- apex-lead.md: v3.1 → v3.2 (complete commands + dependencies manifest)
- apex-kb.md: v1.0 → v1.1 (+implicit knowledge section)
- apex-intelligence.yaml: +header position smart default
- vocabulary-bridge.yaml: +expansion protocol section
- apex-pipeline-executor.md: +full execution output example (all checkpoints)
- apex-quick.md: +2 realistic output examples (new component, responsive redesign)
- veto-conditions.yaml: v1.3.0 → v2.0.0 (+16 new conditions, 137 total across 35 gates)
- README.md: Complete professional rewrite
- CHANGELOG.md: Updated with v1.4.0 entry

### Metrics
- Agents: 14 → **15** (+1: web-intel/Kilian added in v1.3.0+)
- Tasks: 139 active + 22 extensions
- Veto conditions: 121 → **137** (+16 across 7 new gates)
- Quality gates: 28 → **35** (+7: fix-scope, snapshot, fix-adherence, handoff, context, intent, greenfield)
- Intent chains: 21 → **31** (unchanged count, but +header smart default)
- Command coverage in apex-lead.md: 66% → **100%**
- Dependency coverage in apex-lead.md: 14% → **100%**

## [1.3.2] — 2026-03-09

### Fixed — Pedro Valério Deep Audit (3 Fixes)
- **FIX-08**: Added 4 missing intent chains (`after_i18n_audit`, `after_error_boundary`, `after_rollback`, `after_dry_run`) — fixes "E depois?" promise
- **FIX-09**: Registered `QG-AX-FIX-001`, `QG-QK-001/002/003` in central `veto-conditions.yaml` (apex-fix and apex-quick SSoT)
- **FIX-10**: Registered 4 workflow veto conditions (`VC-WF-007/008/009/010`) for rollback and dry-run safety

### Changed
- apex-intelligence.yaml: +4 intent chains (21 total, was 17)
- veto-conditions.yaml: +11 veto conditions for fix/quick/rollback/dry-run gates
- Modernization Score: 96.5 → 98.2 (all intent chain and SSoT gaps resolved)

## [1.3.1] — 2026-03-09

### Fixed — Pedro Valério Process Audit (7 Fixes)
- **FIX-01**: Registered `VC-DISC-I18N-001/002` and `VC-DISC-EB-001/002` in central `veto-conditions.yaml` (SSoT compliance)
- **FIX-02**: Added `visibility` to VC-006-A grep exclusion list (AX001 micro-interaction exception parity)
- **FIX-03**: Added 4 discovery gates for `apex-i18n-audit` and `apex-error-boundary` (block on non-React projects)
- **FIX-04**: Documented ship→@devops handoff as intentionally manual with artifact generation and user prompt
- **FIX-05**: Added confirmation timeout to `apex-entry.md` Step 4 (5min reminder, 30min auto-cancel)
- **FIX-06**: Synced `veto-conditions.yaml` version 1.1.0 → 1.3.0
- **FIX-07**: Added cache cleanup retention enforcement (7-day TTL, 10 per type, 5MB max, auto-cleanup on session start)

### Changed
- veto-conditions.yaml: v1.1.0 → v1.3.0 (+4 discovery gates, +1 grep fix)
- apex-intelligence.yaml: cleanup section expanded with retention enforcement rules
- apex-entry.md: +confirmation timeout behavior at Step 4
- apex-pipeline-executor.md: +ship-to-devops handoff documentation with artifact spec

### Metrics
- Modernization Score: 93.8 → 96.5 (7 deviations resolved)
- Veto conditions: 62 → 66 (+4 discovery gates for i18n and error boundary)
- Gaps de tempo: 3 → 1 (ship→devops remains intentionally manual per Agent Authority)

## [1.3.0] — 2026-03-09

### Added — Alan Nicolas Knowledge Extraction (5 Implicit Knowledge Fixes)
- **`*apex-i18n-audit`**: i18n readiness audit — hardcoded strings, RTL assessment, text overflow risks, pluralization gaps, locale detection
- **`*apex-error-boundary`**: Error boundary architecture audit — 4-layer strategy (app/route/feature/component), coverage gaps, recovery patterns
- **i18n routing**: Added i18n/translation/locale/RTL to routing table (`apex-route-request.md`) + auto-activation keywords
- **Technical SEO expansion**: `*discover-routes` now audits structured data, robots.txt, sitemap.xml, favicon, manifest, h1 structure, lang attribute
- **Vision dependency note**: CLAUDE.md documents that `*apex-analyze`, `*apex-compare`, `*apex-consistency` require multimodal LLM

### Changed
- **AX001 relaxed**: Spring Config Validation now allows CSS transitions for micro-interactions < 100ms (opacity, visibility, color). Interactive elements still require spring physics.
- **Veto spring absolutism**: Bezier veto updated with micro-interaction exception (< 100ms, non-physical properties)
- **RT004 added**: New routing heuristic for i18n detection → routes to @react-eng + @css-eng
- Tasks: 86 → 88 (+2: apex-i18n-audit, apex-error-boundary)
- squad.yaml: v1.2.0 → v1.3.0
- squad-config.yaml: v1.2.0 → v1.3.0
- apex-lead.md: AX001 updated, RT004 added, veto updated
- apex-route-request.md: +2 routing table entries (i18n, error boundary)
- apex-discover-routes.md: v1.0.0 → v1.1.0 (technical SEO checks, expanded penalties)
- CLAUDE.md: +2 commands, +2 routing entries, +2 trigger keywords, vision note

## [1.2.0] — 2026-03-09

### Added — Pedro Valério Audit Fixes (8 GAPs + 5 Melhorias)
- **`*apex-rollback`**: Rollback pipeline to previous checkpoint, restoring code and state (GAP-07)
- **`*apex-dry-run`**: Preview full pipeline plan without executing — shows phases, agents, gates (MELHORIA-02)
- **`data/discovery-output-schema.yaml`**: Structured JSON schemas for all 7 discovery tools + diff capability (GAP-03 + MELHORIA-03)
- **Pipeline state integrity**: SHA-256 checksum validation on read/write, schema version field (GAP-02)
- **Per-phase duration metrics**: `phase_durations` in pipeline-state-schema.yaml (MELHORIA-01)
- **Escalation log**: Full event log for gate failures, fix cycles, agent failures, rollbacks (MELHORIA-04)
- **Handoff depth enforcement**: Counter + max depth (5) + escalation at limit (GAP-05)
- **Cache invalidation globs**: Explicit glob patterns for mtime-based lazy invalidation on every cache (GAP-04)
- **Agent registry parity check**: VC-WF-006 — bidirectional validation agents/*.md ↔ agent-registry.yaml (GAP-08)
- **Contrast validation on presets**: `contrast_validated` field on all 31 presets, 5 flagged as unsafe (GAP-06)
- **Preset composition**: `composable` field on all 31 presets + composition rules for `--style A+B` (MELHORIA-05)

### Changed
- Tasks: 84 → 86 (+2: apex-rollback, apex-dry-run)
- Data files: 9 → 10 (+1: discovery-output-schema.yaml)
- Veto conditions: +1 (VC-WF-006: agent file-to-registry parity)
- pipeline-state-schema.yaml: v1.0.0 → v1.1.0 (integrity, metrics, escalation)
- design-presets.yaml: v1.0.0 → v1.1.0 (contrast + composable fields)
- apex-intelligence.yaml: v1.0.0 → v1.0.0 (detection mechanism + invalidation globs + handoff depth)
- squad-config.yaml: v1.1.0 → v1.2.0 (discovery output, rollback, dry-run, integrity)
- squad.yaml: v1.1.0 → v1.2.0 (new tasks, data, commands)
- CLAUDE.md: SSoT reference on veto conditions inline table + new commands

## [1.1.0] — 2026-03-07

### Added
- **7 Discovery Tools** (was 2): routes, dependencies, motion, a11y, performance
- **Visual Analysis**: *apex-analyze (8 dimensions), *apex-compare, *apex-consistency
- **Agent Handoff Protocol**: visible delegation, specialist intros, chain suggestions
- **8 Gap Fixes**: code review, dark mode audit, design critique, export tokens, integration tests, refactor workflow, responsive breakpoints, conditional after_transform
- **Intelligence Enhancements**: 17 intent chains (was 12), 10 caches (was 5), conditional after_transform by preset category
- **31 Design Presets**: Apple, Google, Tech, Movements, Industry, Dark, Experimental
- **Style Commands**: *apex-inspire, *apex-transform with token override
- **Config**: squad-config.yaml (centralized operational config)
- **README.md rewritten**: complete documentation of all capabilities

### Changed
- Tasks: 67 → 84 (+17)
- Workflows: 7 → 8 (+1 component refactor)
- Intent chains: 12 → 17 (+5 for new discoveries)
- Context caches: 5 → 10 (+5 for new discoveries)
- Veto conditions: 85% coverage → 100% (all have available_check)
- design-presets.yaml: fixed count 42 → 31 (actual)
- responsive-audit.md: added mandatory breakpoints (320/375/768/1024/1440) + 3 veto conditions
- apex-intelligence.yaml: after_transform now conditional by preset category (6 categories)
- apex-entry.md: integrated handoff protocol reference
- apex-fix.md: integrated handoff protocol (delegation + specialist intro)

## [1.0.0] — 2026-03-01

### Initial Release
- 14 agents (1 orchestrator + 13 specialists) with DNA from real frontend leaders
- 67 tasks covering all frontend domains
- 7 workflows (feature build, pipeline, component create, cross-platform sync, design-to-code, polish cycle, ship validation)
- 28 checklists for quality validation
- 13 templates for documentation
- 9 data files (agent registry, veto conditions, pipeline state, performance budgets, spring configs, design tokens, platform capabilities, intelligence, presets)
- 10 quality gates with 4 enforcement levels
- 4 auto-detected profiles (full, web-next, web-spa, minimal)
- Pipeline executor with 7 phases, 6 checkpoints, 8 commands
- Discovery tools: *discover-components, *discover-design
- Single entry point: @apex {natural language}
- AIOS integration with handoff artifacts
