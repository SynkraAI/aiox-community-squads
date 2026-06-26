---
id: i18n-date-number-formatting
version: "1.0.0"
title: "Locale-Aware Date & Number Formatting"
description: "Implement Intl-based date, time, number, currency, and relative time formatting with timezone awareness and locale-specific patterns"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - formatting-patterns-spec.md
  - formatting-utils.yaml
---

# Locale-Aware Date & Number Formatting

## When This Task Runs

- App displays dates, times, or numbers to users
- Multi-locale support needed
- Timezone-aware display required
- Currency formatting across regions
- `*apex-i18n-audit` identified formatting issues

## Execution Steps

### Step 1: Audit Current Formatting
```
SCAN project for formatting patterns:
- .toLocaleDateString() / .toLocaleString() usage
- Intl.DateTimeFormat / Intl.NumberFormat usage
- Moment.js / date-fns / dayjs usage
- Hardcoded date formats ("MM/DD/YYYY", etc.)
- Manual number formatting (toFixed, regex commas)

OUTPUT: Formatting inventory + inconsistencies
```

### Step 2: Define Formatting Standards

**elicit: true** — Confirm target locales and formats:

| Type | Example (pt-BR) | Example (en-US) | API |
|------|-----------------|-----------------|-----|
| **Short date** | 11/03/2026 | 03/11/2026 | Intl.DateTimeFormat |
| **Long date** | 11 de março de 2026 | March 11, 2026 | Intl.DateTimeFormat |
| **Time** | 14:30 | 2:30 PM | Intl.DateTimeFormat |
| **Relative** | há 5 minutos | 5 minutes ago | Intl.RelativeTimeFormat |
| **Number** | 1.234,56 | 1,234.56 | Intl.NumberFormat |
| **Currency** | R$ 1.234,56 | $1,234.56 | Intl.NumberFormat |
| **Percent** | 85,5% | 85.5% | Intl.NumberFormat |
| **Compact** | 1,2 mil | 1.2K | Intl.NumberFormat |

### Step 3: Create Formatting Utilities

```typescript
// Date formatting patterns
const dateFormats = {
  short: { day: '2-digit', month: '2-digit', year: 'numeric' },
  long: { day: 'numeric', month: 'long', year: 'numeric' },
  time: { hour: '2-digit', minute: '2-digit' },
  datetime: { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' },
}

// Number formatting patterns
const numberFormats = {
  decimal: { style: 'decimal' },
  currency: { style: 'currency', currency: 'BRL' },
  percent: { style: 'percent', maximumFractionDigits: 1 },
  compact: { notation: 'compact', compactDisplay: 'short' },
}
```

### Step 4: Handle Timezone Correctly

```yaml
timezone_strategy:
  storage: "UTC always (ISO 8601)"
  display: "User's timezone (from browser or profile)"
  api_communication: "UTC with timezone offset"
  edge_cases:
    - "DST transitions"
    - "Timezone-ambiguous dates (date-only fields)"
    - "Server-generated timestamps vs user input"
  testing: "Test with UTC+0, UTC-3 (BRT), UTC-12, UTC+14"
```

### Step 5: Relative Time Implementation

```yaml
relative_time:
  thresholds:
    - range: "< 1 min"
      display: "agora mesmo"  # "just now"
    - range: "1-59 min"
      display: "há {n} minutos"
    - range: "1-23 hours"
      display: "há {n} horas"
    - range: "1-6 days"
      display: "há {n} dias"
    - range: "7+ days"
      display: "formatted date (short)"
  auto_update: "Every 60s for items < 1 hour old"
```

### Step 6: Validate Formatting

- [ ] All dates displayed in user's locale format
- [ ] Timezone handling: stored UTC, displayed local
- [ ] Number separators correct per locale (. vs ,)
- [ ] Currency symbol and position correct per locale
- [ ] Relative time auto-updates for recent items
- [ ] No hardcoded format strings in components

## Quality Criteria

- Zero hardcoded date/number formats in component code
- All formatting uses Intl APIs (not manual string manipulation)
- Timezone-safe: UTC storage, local display
- Consistent formatting patterns across all views

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| No hardcoded | Zero manual format strings |
| Locale-aware | Formats change with locale |
| Timezone-safe | UTC storage, local display |
| Consistent | Same format pattern across similar contexts |

## Handoff

- Formatting patterns feed `@react-eng` for hook/component design
- Timezone strategy feeds `@frontend-arch` for middleware configuration
- Display patterns feed `@a11y-eng` for `datetime` attribute validation
