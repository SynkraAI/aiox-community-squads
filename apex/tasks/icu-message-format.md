---
id: icu-message-format
version: "1.0.0"
title: "ICU Message Format Implementation"
description: "Design and implement ICU MessageFormat patterns for pluralization, gender selection, ordinals, and nested selects for robust internationalization"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - i18n-message-catalog.md
  - message-format-patterns.yaml
---

# ICU Message Format Implementation

## When This Task Runs

- App needs multi-language support
- Pluralization rules are hardcoded or English-only
- Gender-aware messaging needed
- Complex message patterns with nested variables
- `*apex-i18n-audit` identified missing ICU patterns

## Execution Steps

### Step 1: Audit Current String Handling
```
SCAN project for i18n patterns:
- Hardcoded user-facing strings
- Template literals with embedded values
- Existing i18n library usage (react-intl, i18next, etc.)
- Pluralization attempts (ternary operators for singular/plural)
- Date/number formatting (toLocaleDateString, Intl.*)

OUTPUT: String inventory + i18n readiness assessment
```

### Step 2: Select i18n Stack

**elicit: true** — Confirm i18n library choice:

| Library | ICU Support | Bundle Size | React Integration |
|---------|-------------|-------------|-------------------|
| **react-intl** (FormatJS) | Full ICU | ~15KB | `<FormattedMessage>`, hooks |
| **i18next** + react-i18next | Via plugin | ~10KB | `useTranslation` hook |
| **next-intl** | Full ICU | ~12KB | RSC-native, App Router |
| **Intl (native)** | Basic | 0KB | Manual, no React bindings |

### Step 3: Design Message Patterns

For each message type:

```yaml
# Simple message
simple:
  id: "greeting"
  defaultMessage: "Hello, {name}!"
  description: "Greeting on dashboard"

# Plural
plural:
  id: "item_count"
  defaultMessage: "{count, plural, =0 {No items} one {# item} other {# items}}"
  description: "Item count display"

# Gender select
gender:
  id: "profile_update"
  defaultMessage: "{gender, select, male {He updated his profile} female {She updated her profile} other {They updated their profile}}"

# Ordinal
ordinal:
  id: "ranking"
  defaultMessage: "{rank, selectordinal, one {#st} two {#nd} few {#rd} other {#th}} place"

# Nested (plural + gender)
nested:
  id: "activity"
  defaultMessage: "{gender, select, male {{count, plural, one {He wrote # comment} other {He wrote # comments}}} female {{count, plural, one {She wrote # comment} other {She wrote # comments}}} other {{count, plural, one {They wrote # comment} other {They wrote # comments}}}}"
```

### Step 4: Extract and Catalog Strings

```yaml
extraction_strategy:
  tool: "formatjs extract"  # or i18next-parser
  source_patterns: ["src/**/*.{ts,tsx}"]
  output: "locales/{locale}.json"
  id_generation: "literal"  # or hash-based
  default_locale: "pt-BR"
  fallback_chain: ["pt-BR", "pt", "en"]
```

### Step 5: Define Translation Workflow

```
1. Developer writes message with defaultMessage
2. Extract tool generates message catalog
3. Translator receives catalog (JSON/XLIFF)
4. Translated catalog placed in locales/{locale}.json
5. Runtime loads based on user locale
6. Missing translations fallback to default locale
```

### Step 6: Validate ICU Patterns

- [ ] All user-facing strings extracted to message catalog
- [ ] Plural rules cover target locales (not just English one/other)
- [ ] Gender-aware messages use select, not hardcoded
- [ ] Nested patterns parse correctly in target i18n library
- [ ] Fallback chain configured (locale → language → default)
- [ ] Message IDs are stable (no hash changes on typo fix)

## Quality Criteria

- Zero hardcoded user-facing strings in component code
- ICU plural rules match CLDR for all target locales
- Gender patterns use inclusive "other" as default
- Translation workflow documented and repeatable

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Extraction | All strings extracted to catalog |
| Plurals | Correct CLDR plural rules per locale |
| Fallback | Missing translation falls back gracefully |
| No hardcoded | Zero user-facing strings inline |

## Handoff

- Message catalog structure feeds `@react-eng` for component integration
- Locale detection feeds `@frontend-arch` for routing/middleware design
- RTL requirements feed `rtl-layout-patterns` task
