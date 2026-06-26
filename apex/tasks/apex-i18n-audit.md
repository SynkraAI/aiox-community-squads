# Task: apex-i18n-audit

```yaml
id: apex-i18n-audit
version: "1.0.0"
title: "Apex i18n Audit"
description: >
  Audits the project for internationalization readiness. Detects hardcoded strings,
  missing locale support, RTL issues, text overflow risks, and pluralization gaps.
  Does NOT require the project to already use i18n — it assesses readiness.
elicit: false
owner: apex-lead
executor: css-eng, react-eng
dependencies:
  - tasks/apex-scan.md
outputs:
  - i18n readiness report
  - Hardcoded string inventory
  - RTL readiness assessment
  - i18n health score
```

---

## Command

### `*apex-i18n-audit`

Audits the project for internationalization readiness.

---

## How It Works

### Step 1: Detect Current i18n State

```yaml
detection:
  libraries:
    - react-intl: ["<FormattedMessage", "useIntl", "intl.formatMessage"]
    - next-intl: ["useTranslations", "getTranslations", "NextIntlClientProvider"]
    - react-i18next: ["useTranslation", "Trans", "i18n.t"]
    - lingui: ["<Trans>", "useLingui", "msg"]
    - none: "No i18n library detected"

  result:
    library: "{detected or none}"
    locale_files: "{paths to locale JSON/YAML}"
    default_locale: "{detected or unknown}"
    supported_locales: "[{list}]"
```

### Step 2: Scan for Hardcoded Strings

```yaml
hardcoded_strings:
  scan_targets:
    - "JSX text content (between tags)"
    - "aria-label values"
    - "placeholder text"
    - "title attributes"
    - "alt text (unless empty)"
    - "Error messages in catch blocks"
    - "Toast/notification messages"

  exclude:
    - "CSS class names"
    - "HTML tag names"
    - "URLs and paths"
    - "Console.log messages"
    - "Test files"
    - "Single characters (icons, separators)"

  output_per_file:
    file: "{path}"
    hardcoded_count: N
    strings: ["{line}: \"{text}\""]
```

### Step 3: RTL Readiness Assessment

```yaml
rtl_assessment:
  checks:
    logical_properties:
      description: "Uses CSS logical properties (margin-inline, padding-block) vs physical (margin-left, padding-top)"
      scan: "Count logical vs physical property usage"
      scoring:
        - ">80% logical": "RTL-ready"
        - "50-80% logical": "Partially ready"
        - "<50% logical": "Not RTL-ready"

    text_alignment:
      description: "Uses text-align: start/end vs left/right"
      scan: "Count start/end vs left/right in text-align"

    flex_direction:
      description: "Hardcoded flex-direction that would break in RTL"
      scan: "Check for row/row-reverse without RTL consideration"

    icons_with_direction:
      description: "Arrows and directional icons that need mirroring"
      scan: "Detect arrow/chevron icons without RTL flip"

    layout_mirroring:
      description: "Layouts that assume LTR reading order"
      scan: "Detect fixed left/right positioning of nav, sidebar, icons"
```

### Step 4: Text Overflow Risk Detection

```yaml
text_overflow:
  description: "Strings that will break layout when translated (German/Finnish +30% longer)"
  checks:
    - fixed_width_containers: "Containers with fixed width containing text"
    - truncation_without_tooltip: "text-overflow: ellipsis without title/tooltip"
    - single_line_constraints: "white-space: nowrap on user-facing text"
    - button_text_overflow: "Buttons with fixed width and text content"

  expansion_factor:
    note: "German text is ~30% longer, Finnish ~40%, Chinese ~50% shorter"
    test: "Would the UI break if all strings were 40% longer?"
```

### Step 5: Pluralization & Formatting Gaps

```yaml
formatting_gaps:
  checks:
    - hardcoded_plurals: "Strings with 's' appended for plural (e.g., `{n} items`)"
    - hardcoded_currency: "Currency symbols hardcoded ($, R$, €)"
    - hardcoded_date_format: "Date formatting without locale (MM/DD/YYYY vs DD/MM/YYYY)"
    - hardcoded_number_format: "Number formatting without locale (1,000 vs 1.000)"
    - concatenated_strings: "String concatenation for sentences (word order changes per locale)"
```

### Step 6: Calculate i18n Health Score

```yaml
health_score:
  formula: "100 - (penalties)"
  penalties:
    hardcoded_string: -1 each (max -40)
    physical_css_property: -0.5 each (max -15)
    text_align_left_right: -1 each (max -10)
    fixed_width_text_container: -2 each (max -10)
    hardcoded_plural: -2 each (max -10)
    hardcoded_currency: -3 each (max -9)
    concatenated_sentence: -3 each (max -9)
    no_i18n_library: -10

  classification:
    90-100: "i18n-ready — minimal work to add locales"
    70-89: "partially-ready — some hardcoded strings and CSS to fix"
    50-69: "needs-work — significant refactoring required"
    0-49: "not-ready — i18n architecture not in place"
```

### Step 7: Output

```yaml
output_format: |
  ## i18n Audit

  **i18n Library:** {library or "none detected"}
  **Supported Locales:** {list or "none"}
  **i18n Health Score:** {score}/100 ({classification})

  ### Hardcoded Strings
  | File | Count | Examples |
  |------|-------|---------|
  | src/components/Header.tsx | 5 | "Agendar Consulta", "Serviços" |

  **Total:** {total} hardcoded strings across {file_count} files

  ### RTL Readiness
  | Check | Status | Details |
  |-------|--------|---------|
  | Logical properties | {%} | {n} logical vs {m} physical |
  | Text alignment | {status} | {n} start/end vs {m} left/right |
  | Directional icons | {status} | {n} icons need RTL flip |

  ### Text Overflow Risks
  - {n} fixed-width containers with text
  - {n} truncations without tooltip

  ### Options
  1. Setup i18n library ({recommended})
  2. Convert physical → logical CSS properties
  3. Fix hardcoded strings (top {n} files)
  4. Just the report
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-I18N-001
    condition: "Concatenated strings used to build sentences"
    action: "WARN — Sentence structure changes per locale. Use template strings with placeholders."
    available_check: "manual"
    on_unavailable: MANUAL_CHECK
```

---

## Cache

```yaml
cache:
  location: ".aios/apex-context/i18n-cache.yaml"
  ttl: "Until src/ files change"
  invalidate_on:
    - "Any .tsx/.jsx file modified"
    - "Locale files modified"
    - "User runs *apex-i18n-audit explicitly"
```

---

*Apex Squad — i18n Audit Task v1.0.0*
