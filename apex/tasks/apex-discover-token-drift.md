# Task: apex-discover-token-drift

```yaml
id: apex-discover-token-drift
version: "1.0.0"
title: "Token Drift Discovery"
description: >
  Compares current project design tokens against previously extracted external
  tokens (from @web-intel extractions). Detects drift: adopted tokens that were
  later modified, external updates not reflected in project, and fusion artifacts
  that became stale. Answers "are my adopted design decisions still in sync
  with where they came from?"
elicit: false
owner: apex-lead
executor: web-intel
dependencies:
  - tasks/apex-scan.md
  - tasks/apex-discover-design.md
  - tasks/web-extract-tokens.md
  - tasks/web-compare-systems.md
  - templates/token-comparison-tmpl.md
outputs:
  - Token drift inventory (adopted vs current state)
  - Stale fusion report (extractions older than threshold)
  - Divergence map (which tokens drifted and by how much)
  - Re-extraction recommendations
  - Token drift score (0-100)
```

---

## Command

### `*discover-token-drift`

Compares project tokens against external extraction history. Runs as part of `*apex-audit` or independently.

**Prerequisite:** At least one prior `*scrape` or `*extract-tokens` extraction must exist (cached in `.aios/apex-context/extractions/`).

---

## Discovery Phases

### Phase 1: Load Extraction History

```yaml
extraction_history:
  cache_location: ".aios/apex-context/extractions/"
  scan:
    - "*.extraction.yaml"
    - "*.extraction.json"
    - "*.fusion-ready.yaml"

  per_extraction:
    id: "{extraction_id}"
    source_url: "{url}"
    extracted_at: "{date}"
    age_days: N
    categories: ["colors", "typography", "spacing", "shadows", "radius", "motion"]
    token_count: N
    adoption_status: "adopted | partial | ignored"

  staleness_thresholds:
    fresh: "< 30 days"
    aging: "30-90 days"
    stale: "> 90 days"
    ancient: "> 180 days"

  no_history_behavior:
    message: "No extraction history found. Run *scrape {url} or *extract-tokens {url} first."
    exit: true
```

### Phase 2: Load Current Project Tokens

```yaml
project_tokens:
  sources:
    css_variables:
      scan: ["src/**/*.css", "app/**/*.css", "styles/**/*.css"]
      extract: ":root { --var: value } declarations"

    tailwind_config:
      scan: ["tailwind.config.*"]
      extract: "theme.extend.* values"

    token_files:
      scan: ["src/**/tokens.*", "src/**/theme.*", "src/**/design-tokens.*"]
      extract: "Exported token objects"

  normalize:
    colors: "Convert all to HSL for comparison"
    spacing: "Convert all to px"
    typography: "Normalize to {size}/{weight}/{family}"
    shadows: "Parse to {x} {y} {blur} {spread} {color}"
    radius: "Convert to px"
```

### Phase 3: Compare & Detect Drift

```yaml
drift_detection:
  per_token:
    token_name: "{name}"
    category: "color | typography | spacing | shadow | radius | motion"
    source_extraction: "{extraction_id}"
    source_url: "{url}"
    extracted_value: "{original value}"
    current_value: "{project value}"
    drift_type: "none | modified | removed | added"
    drift_magnitude: "{percentage or delta}"

  drift_types:
    none:
      description: "Token matches extraction — no drift"
      severity: null

    modified:
      description: "Token was adopted but later changed"
      detection: "Value differs from extraction by > threshold"
      thresholds:
        color: "HSL distance > 5%"
        spacing: "Difference > 2px"
        typography_size: "Difference > 1px"
        shadow: "Any component changed"
        radius: "Difference > 2px"
      severity: LOW  # Intentional modifications are expected
      question: "Was this intentional customization or accidental drift?"

    removed:
      description: "Token was adopted but no longer exists in project"
      detection: "Token in extraction.adopted but not in project tokens"
      severity: MEDIUM
      question: "Was this token intentionally removed?"

    added_without_source:
      description: "New token similar to extraction but not formally adopted"
      detection: "Project token within threshold of extracted token, no adoption record"
      severity: LOW
      question: "Should this be formally linked to the extraction?"

  comparison_matrix:
    format: "token-comparison-tmpl.md"
    columns:
      - "Token"
      - "Category"
      - "Source URL"
      - "Extracted Value"
      - "Current Value"
      - "Drift"
      - "Age"
```

### Phase 4: Analyze Fusion Health

```yaml
fusion_health:
  per_extraction:
    extraction_id: "{id}"
    source_url: "{url}"
    extracted_at: "{date}"
    tokens_adopted: N
    tokens_drifted: N
    tokens_removed: N
    drift_percentage: "N%"
    staleness: "fresh | aging | stale | ancient"
    recommendation: "re-extract | review-drift | healthy"

  checks:
    stale_extractions:
      description: "Extractions older than 90 days"
      severity: MEDIUM
      action: "Re-run *scrape {url} to check for upstream changes"

    high_drift:
      description: "More than 30% of adopted tokens have drifted"
      severity: MEDIUM
      action: "Review if drift is intentional customization or accidental"

    abandoned_extractions:
      description: "Extraction exists but 0 tokens adopted"
      severity: LOW
      action: "Delete extraction cache or revisit adoption decisions"

    source_site_changed:
      description: "Source site likely redesigned (requires re-extraction to confirm)"
      detection: "Extraction > 180 days old"
      severity: MEDIUM
      action: "Re-extract and compare — site may have new design system"
```

### Phase 5: Generate Recommendations

```yaml
recommendations:
  priority_order:
    1: "Re-extract stale sources (> 90 days)"
    2: "Review high-drift tokens (> 30% drifted)"
    3: "Clean abandoned extraction caches"
    4: "Formally adopt similar-but-unlinked tokens"

  per_recommendation:
    action: "{description}"
    command: "{apex command to execute}"
    impact: "high | medium | low"
    effort: "minimal | moderate | significant"
```

---

## Scoring

```yaml
drift_score:
  formula: "100 - (stale_extractions * 10) - (high_drift_extractions * 15) - (removed_tokens * 5) - (abandoned * 3)"
  max_deductions:
    stale: 40       # max 4 stale extractions = -40
    high_drift: 30  # max 2 high-drift extractions = -30
    removed: 20     # max 4 removed tokens = -20
    abandoned: 10   # max 3 abandoned = -9

  classification:
    90-100: "In sync — tokens well-maintained, extractions fresh"
    70-89: "Minor drift — some extractions aging, review recommended"
    50-69: "Significant drift — re-extraction needed for key sources"
    0-49: "Out of sync — fusion artifacts stale, major review needed"
```

---

## Output Format

```yaml
output:
  schema: "discovery-output-schema.yaml"
  sections:
    - summary: "N extractions tracked, M tokens adopted, X drifted, drift score Y/100"
    - extraction_inventory: "Table of all extractions with age and drift status"
    - drift_map: "Token-by-token comparison (extracted vs current)"
    - stale_report: "Extractions that need re-running"
    - recommendations: "Prioritized action list"
```

---

## Intent Chaining

```yaml
after_discovery:
  suggestions:
    - label: "Re-extract stale sources"
      command: "*scrape {oldest_stale_url}"
      condition: "stale_extractions > 0"
    - label: "Compare drifted tokens with current external state"
      command: "*compare {highest_drift_url}"
      condition: "high_drift_extractions > 0"
    - label: "Run design system discovery"
      command: "*discover-design"
      condition: "always"
    - label: "Done"
      command: null
      condition: "always"
```
