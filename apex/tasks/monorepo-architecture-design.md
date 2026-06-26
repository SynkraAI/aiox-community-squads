---
id: monorepo-architecture-design
version: "1.0.0"
title: "Monorepo Architecture Decision & Design"
description: "Evaluate monorepo vs polyrepo, design package boundaries, dependency constraints, versioning strategy, and build graph for frontend projects"
elicit: true
owner: frontend-arch
executor: frontend-arch
outputs:
  - monorepo-adr.md
  - package-boundary-spec.yaml
---

# Monorepo Architecture Decision & Design

## When This Task Runs

- Project needs architectural decision: monorepo vs polyrepo
- Existing monorepo needs package boundary redesign
- New packages need to be added with clear boundaries
- Dependency constraint violations detected

## Execution Steps

### Step 1: Evaluate Monorepo Need

**elicit: true** — Gather project context:

| Factor | Monorepo | Polyrepo |
|--------|----------|----------|
| **Team size** | 1-3 teams, shared codebase | 4+ teams, independent releases |
| **Code sharing** | High (>40% shared) | Low (<20% shared) |
| **Deploy coupling** | Coordinated releases | Independent deploys critical |
| **Tooling budget** | Can invest in build infra | Minimal tooling overhead |

### Step 2: Design Package Taxonomy

```yaml
package_taxonomy:
  layers:
    foundation:
      purpose: "Zero-dependency, pure logic"
      examples: ["@scope/types", "@scope/constants", "@scope/tokens"]
      rules: "No React, no platform imports, no side effects"

    core:
      purpose: "Shared business logic with minimal deps"
      examples: ["@scope/utils", "@scope/validation", "@scope/api-client"]
      rules: "May import foundation, no UI framework"

    ui:
      purpose: "Shared UI components"
      examples: ["@scope/ui", "@scope/icons", "@scope/charts"]
      rules: "May import foundation + core, React allowed"

    features:
      purpose: "Composed feature modules"
      examples: ["@scope/auth", "@scope/dashboard", "@scope/settings"]
      rules: "May import all layers below, no cross-feature imports"

    apps:
      purpose: "Deployable applications"
      examples: ["web", "mobile", "admin", "storybook"]
      rules: "May import any package, not importable by others"
```

### Step 3: Define Dependency Constraints

```yaml
dependency_constraints:
  matrix:
    #           foundation  core  ui  features  apps
    foundation: [self,       no,   no, no,       no]
    core:       [yes,        self, no, no,       no]
    ui:         [yes,        yes,  self, no,     no]
    features:   [yes,        yes,  yes, no,      no]  # No cross-feature!
    apps:       [yes,        yes,  yes, yes,     no]   # No cross-app!

  enforcement:
    tool: "eslint-plugin-boundaries | @nx/enforce-module-boundaries"
    ci: "Runs on every PR"
    pre_commit: "Optional for fast feedback"

  violations:
    action: "Block merge"
    exceptions: "Require ADR documenting why constraint is bypassed"
```

### Step 4: Design Build Graph

```yaml
build_graph:
  strategy: "Bottom-up (foundation → core → ui → features → apps)"
  parallelism: "Packages at same layer build in parallel"
  caching:
    strategy: "{turborepo | nx}"
    cache_key_inputs: ["src/**", "tsconfig.json", "package.json"]
    remote_cache: "{enabled | disabled}"
  affected_analysis:
    tool: "{turborepo --filter | nx affected}"
    ci_optimization: "Only build/test changed packages + dependents"
```

### Step 5: Define Versioning Strategy

```yaml
versioning:
  internal_packages:
    strategy: "workspace:*"  # Always latest in monorepo
    publishing: "Not published to npm (internal only)"

  published_packages:
    strategy: "independent"  # Each package has own version
    tool: "changesets"
    changelog: "auto-generated per package"
    release: "CI publishes on merge to main"
```

### Step 6: Produce ADR

Generate Architecture Decision Record:
- **Context:** Why monorepo (or polyrepo)
- **Decision:** Package taxonomy, constraints, tooling
- **Consequences:** Build complexity, DX impact, team workflow

## Quality Criteria

- Package taxonomy has clear layer boundaries
- Dependency constraints are enforceable by tooling
- Build graph has no cycles
- ADR documents trade-offs and alternatives considered

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Taxonomy | All packages classified into layers |
| Constraints | Dependency rules enforced by linter |
| Build | Graph has no cycles, builds bottom-up |
| ADR | Decision documented with rationale |

## Handoff

- Package structure feeds `@react-eng` for component organization
- Build config feeds `@perf-eng` for bundle analysis
- CI pipeline feeds `@devops` for GitHub Actions setup
