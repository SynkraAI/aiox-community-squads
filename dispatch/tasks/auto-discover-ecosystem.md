# auto-discover-ecosystem

> **Version:** 1.0.0
> **Created:** 2026-02-10
> **Type:** WORKER (scripts only, zero LLM)
> **Executor:** Worker (scripts/build-command-registry.py + scripts/build-domain-registry.py)

## Purpose

Scans the entire project ecosystem and rebuilds both registries (command-registry.yaml and domain-registry.yaml) from scratch. This is the single source of truth for what the dispatch system knows about available agents, tasks, and domains.

**This task is WORKER-ONLY:** No LLM reasoning needed. Scripts do deterministic file scanning.

---

## When to Run

| Trigger | Action |
|---------|--------|
| New squad added to `squads/` | Run full discovery |
| New agent/task added to any squad | Run full discovery |
| `.aios-core/` agents changed | Run full discovery |
| First time activating dispatch | Auto-run on `*discover` |
| Before any dispatch with stale registries | Auto-run |
| After `*sync` or `install-commands` | Run full discovery |

---

## Pre-Actions

```yaml
pre_actions:
  - action: verify_scripts_exist
    check:
      - "squads/dispatch/scripts/build-command-registry.py EXISTS"
      - "squads/dispatch/scripts/build-domain-registry.py EXISTS"
    on_fail: "BLOCK — scripts missing, cannot discover"

  - action: verify_output_dir
    check:
      - "squads/dispatch/data/ directory EXISTS"
    on_fail: "CREATE directory"
```

---

## Checklist

### Phase 1: Scan Ecosystem

- [ ] **1.1** Run command registry builder:
  ```bash
  python squads/dispatch/scripts/build-command-registry.py --output squads/dispatch/data/command-registry.yaml
  ```
  - Expected: command-registry.yaml generated with all squads, agents, tasks
  - Verify: File exists and is non-empty

- [ ] **1.2** Run domain registry builder:
  ```bash
  python squads/dispatch/scripts/build-domain-registry.py --output squads/dispatch/data/domain-registry.yaml
  ```
  - Expected: domain-registry.yaml generated with all domains from squads + .aios-core
  - Verify: File exists and is non-empty

### Phase 2: Validate

- [ ] **2.1** Check all paths in command-registry.yaml point to real files:
  ```bash
  python -c "
  import yaml, pathlib, sys
  with open('squads/dispatch/data/command-registry.yaml') as f:
      data = yaml.safe_load(f)
  broken = []
  for squad, info in data.get('commands', {}).items():
      for item in info.get('agents', []) + info.get('tasks', []):
          if not pathlib.Path(item['file']).exists():
              broken.append(item['file'])
  if broken:
      print(f'BROKEN PATHS ({len(broken)}):')
      for b in broken: print(f'  - {b}')
      sys.exit(1)
  else:
      print(f'All paths valid.')
  "
  ```

- [ ] **2.2** Check domain-registry.yaml kb_files point to real files:
  ```bash
  python -c "
  import yaml, pathlib, sys
  with open('squads/dispatch/data/domain-registry.yaml') as f:
      data = yaml.safe_load(f)
  broken = []
  for domain, info in data.get('domains', {}).items():
      for kb in info.get('kb_files', []):
          if not pathlib.Path(kb).exists():
              broken.append(f'{domain}: {kb}')
  if broken:
      print(f'BROKEN KB PATHS ({len(broken)}):')
      for b in broken: print(f'  - {b}')
  else:
      print(f'All KB paths valid.')
  "
  ```

### Phase 3: Report

- [ ] **3.1** Generate discovery summary:

  **Command Registry:**
  - Total squads: {count}
  - Total agents: {count}
  - Total tasks: {count}
  - Sources scanned: squads/, .claude/commands/, .aios-core/

  **Domain Registry:**
  - Total domains: {count}
  - From squads: {count}
  - From .aios-core: {count}
  - Built-in: {count}
  - Manual overrides applied: {count}

  **Validation:**
  - Broken command paths: {count}
  - Broken KB paths: {count}

- [ ] **3.2** If previous registries existed, show diff:
  - New entries (not in previous)
  - Removed entries (in previous, not in current)
  - Changed entries (different values)

---

## Post-Actions

```yaml
post_actions:
  - action: verify_output
    check:
      - "squads/dispatch/data/command-registry.yaml EXISTS and non-empty"
      - "squads/dispatch/data/domain-registry.yaml EXISTS and non-empty"
    on_fail: "HALT — registry generation failed"

  - action: report
    format: |
      Discovery complete.

      Command Registry: {agents} agents, {tasks} tasks across {squads} squads
      Domain Registry: {domains} domains
      Broken paths: {broken_count}

      Files updated:
      - squads/dispatch/data/command-registry.yaml
      - squads/dispatch/data/domain-registry.yaml
```

---

## Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | command-registry.yaml contains ALL squads from squads/ | Count matches `ls squads/` directories with config.yaml |
| 2 | command-registry.yaml contains .aios-core agents (if .aios-core exists) | AIOS section present with agents |
| 3 | domain-registry.yaml contains domains for each squad (except dispatch itself) | Domain count >= squad count - 1 |
| 4 | domain-registry.yaml contains .aios-core domains (if .aios-core exists) | @dev, @qa, @architect etc. present |
| 5 | All file paths in both registries point to real files | Zero broken paths in validation |
| 6 | Manual overrides preserved | manual-overrides.yaml entries appear in output |
| 7 | Works without .aios-core | Run with --project-root on dir without .aios-core, no errors |
| 8 | Works without squads/ | Run with --project-root on dir without squads/, no errors |

---

## Dependencies

| Dependency | Type | Path |
|------------|------|------|
| build-command-registry.py | script | squads/dispatch/scripts/build-command-registry.py |
| build-domain-registry.py | script | squads/dispatch/scripts/build-domain-registry.py |
| manual-overrides.yaml | data | squads/dispatch/data/manual-overrides.yaml |

---

## Metadata

```yaml
metadata:
  task_name: auto-discover-ecosystem
  status: active
  responsible_executor: Worker
  execution_type: script
  estimated_time: "< 10 seconds"
  timeout: 30
```
