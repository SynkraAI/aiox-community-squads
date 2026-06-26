# Task: web-fusion-workflow

```yaml
id: web-fusion-workflow
version: "1.0.0"
title: "Design Fusion — External to Project Integration"
description: >
  Workflow for merging extracted design intelligence into the current project.
  Takes user-approved tokens/patterns from extraction results and coordinates
  the handoff to internal squad agents for integration. This is the bridge
  between external intelligence (@web-intel) and internal implementation
  (@design-sys-eng, @css-eng, @motion-eng).
elicit: true
owner: web-intel
executor: web-intel
inputs:
  - extraction_id: "Reference to previous extraction results"
  - user_decisions: "ADOPT/ADAPT selections from extraction phase"
outputs:
  - Handoff artifact for @design-sys-eng
  - Integration plan with file list
  - Before/after token comparison
veto_conditions:
  - "Fusion without user-approved selections → BLOCK"
  - "Fusion that overwrites existing tokens without confirmation → BLOCK"
  - "Fusion without @design-sys-eng involvement for token changes → BLOCK"
```

---

## Command

### `*fuse {extraction-id}`

Start fusion workflow — merge extracted tokens with project.

---

## Execution Steps

### Step 1: Load Extraction Results

Load the cached extraction results and user decisions (ADOPT/ADAPT/IGNORE).

### Step 2: Map to Project Structure

```yaml
mapping:
  identify:
    - "Where do project tokens live? (CSS vars, Tailwind config, theme file)"
    - "What naming convention does the project use?"
    - "What token categories exist vs what's being added?"
  plan:
    - "New tokens: where to add, what to name"
    - "Modified tokens: what changes, what stays"
    - "Conflicts: where external and project tokens disagree"
```

### Step 3: Present Fusion Plan

**Elicitation:**
```
## Fusion Plan

### New Tokens to Add ({N})
| Token | Value | Source | Target File |
|-------|-------|--------|-------------|
| --shadow-lg | 0 8px 32px rgba(0,0,0,0.12) | linear.app | src/index.css |
| ... | ... | ... | ... |

### Tokens to Modify ({N})
| Token | Current | New | Source |
|-------|---------|-----|--------|
| --radius-card | 12px | 8px | stripe.com |
| ... | ... | ... | ... |

### Conflicts ({N})
| Token | Ours | Theirs | Recommendation |
|-------|------|--------|----------------|
| --color-accent | #38BDF8 | #5E6AD2 | Keep ours (brand) |

Proceed with fusion? (yes / adjust / cancel)
```

### Step 4: Generate Handoff

```yaml
handoff:
  to: "@design-sys-eng (Diana)"
  format: "FUSION_READY"
  artifact:
    new_tokens: "list with names, values, target files"
    modified_tokens: "list with current vs new values"
    conflicts_resolved: "user decisions on conflicts"
    source_urls: "all [SOURCE] tags preserved"
    project_files: "files that will be modified"
  message: |
    Kilian completed design fusion from {url}.
    User approved {N} new tokens, {M} modifications.
    {C} conflicts resolved by user.
    Please integrate into the design system.
```

### Step 5: Track Integration

After handoff, web-intel tracks:
- Were all tokens integrated?
- Do integrated tokens match extraction values?
- Any drift between extraction and implementation?

Report back to user if discrepancies found.
