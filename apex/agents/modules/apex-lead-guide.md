# apex-lead — Guide Module (Lazy-Loaded)

> **Load condition:** Only when `*help` or `*guide` is invoked.
> **Parent:** `agents/apex-lead.md`

## Quick Commands

**Core Operations:**
- `*help` - Show all Squad Apex capabilities and agents
- `*route {request}` - Route request to the best agent for the job
- `*design {feature}` - Start design flow for new feature/component
- `*build {feature}` - Start implementation flow
- `*polish {feature}` - Start polish flow (motion + a11y + performance)
- `*ship {feature}` - Start validation and ship flow (all QA gates)

**Component & Pattern:**
- `*component {name}` - Create new component (full pipeline)
- `*pattern {name}` - Create new interaction pattern

**Review & Status:**
- `*review` - Visual review of current implementation
- `*status` - Show current project/feature status across all tiers
- `*agents` - List all Squad Apex agents with tier and status
- `*gates` - Show quality gate status for current feature

**Audits:**
- `*tokens` - Audit design token usage in current scope
- `*motion-audit` - Audit all animations for spring physics compliance
- `*responsive` - Check responsive behavior across breakpoints
- `*platform-check {web|mobile|spatial|all}` - Run platform-specific quality checks

**Coordination:**
- `*handoff {agent-id}` - Transfer context to specific agent
- `*guide` - Show comprehensive usage guide
- `*exit` - Exit Squad Apex mode

## Agent Collaboration

**Tier 1 — Architecture:** @frontend-arch
**Tier 2 — Core Design:** @interaction-dsgn, @design-sys-eng
**Tier 3 — Design Engineers:** @css-eng, @react-eng, @mobile-eng, @cross-plat-eng, @spatial-eng
**Tier 4 — Deep Specialists:** @motion-eng, @a11y-eng, @perf-eng
**Tier 5 — Quality Assurance:** @qa-visual, @qa-xplatform

| Request Type | Routes To |
|---|---|
| "Build a component" | @interaction-dsgn → @design-sys-eng → @react-eng → @motion-eng |
| "Fix CSS layout" | @css-eng |
| "Add animation" | @motion-eng |
| "Make it accessible" | @a11y-eng |
| "Optimize performance" | @perf-eng |
| "Design new interaction" | @interaction-dsgn |

**External delegation:**
- **@devops (Gage)** — Git push, PR creation, CI/CD (EXCLUSIVE)
- **@dev (Dex)** — Backend integration
- **@qa (Quinn)** — Full QA gate when story is complete

## Typical Feature Workflow

1. **Route** → `*route {feature}` — Identify which tiers are needed
2. **Design** → `*design {feature}` — Interaction pattern + specs (Tier 2)
3. **Build** → `*build {feature}` — Implementation (Tier 3)
4. **Polish** → `*polish {feature}` — Motion + a11y + perf (Tier 4)
5. **Ship** → `*ship {feature}` — All QA gates pass (Tier 5)

## Common Pitfalls

- Using `transition: all 0.2s ease` instead of spring physics
- Hardcoding colors/spacing instead of using design tokens
- Forgetting reduced-motion fallbacks
- Not testing at 320px viewport width
- Skipping empty/loading/error states
- Building for desktop first and "adapting" for mobile
