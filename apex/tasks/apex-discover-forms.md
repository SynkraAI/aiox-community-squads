# Task: apex-discover-forms

```yaml
id: apex-discover-forms
version: "1.0.0"
title: "Forms Discovery"
description: >
  Scans all form implementations across the project. Detects validation
  gaps, accessibility issues in forms, uncontrolled inputs, missing
  error states, and submission handling patterns. Forms are the most
  complex UI pattern — this discovery ensures they are solid.
  Transforms "are our forms OK?" into "I already audited every form —
  here's what needs fixing."
elicit: false
owner: apex-lead
executor: react-eng
dependencies:
  - tasks/apex-scan.md
outputs:
  - Form library inventory and classification
  - Complete form inventory with field maps
  - Validation coverage analysis
  - Error display audit
  - Submission handling patterns
  - Accessibility compliance per form
  - Form health score (0-100)
```

---

## Command

### `*discover-forms`

Scans the project and audits all form implementations. Runs as part of `*apex-audit` or independently.

---

## Discovery Phases

### Phase 1: Detect Form Libraries

```yaml
library_detection:
  scan:
    - "package.json"
    - "src/**/*.tsx"
    - "src/**/*.ts"
    - "app/**/*.tsx"

  classify:
    library_managed:
      react_hook_form:
        detect: "react-hook-form, useForm, Controller, register"
        version: "from package.json"
      formik:
        detect: "formik, useFormik, Formik, Field"
        version: "from package.json"

    schema_validation:
      zod:
        detect: "zod, z.object, z.string, zodResolver"
      yup:
        detect: "yup, yup.object, yup.string, yupResolver"
      valibot:
        detect: "valibot, v.object, v.string, valibotResolver"

    manual:
      detect: "plain <form onSubmit>, no form library imports"
      note: "Higher risk — validation, error handling likely manual"

  extract:
    - primary_lib: "most-used form library"
    - validation_lib: "schema validation library"
    - form_count: "total forms detected"
    - manual_form_count: "forms without library"
```

### Phase 2: Inventory Forms

```yaml
form_inventory:
  scan:
    - "src/**/*.tsx"
    - "src/**/*.jsx"
    - "app/**/*.tsx"
    - "components/**/*.tsx"

  detect_forms:
    explicit: "<form> element with onSubmit"
    implicit: "Component with multiple inputs and submit handler (no <form> tag)"
    server_action: "form with action={serverAction} (Next.js)"

  for_each_form:
    identity:
      - name: "form purpose (from component name or context)"
      - file: "file path"
      - component: "parent component name"

    fields:
      - name: "field name/id"
      - type: "text | email | password | number | select | checkbox | radio | textarea | custom"
      - required: "true/false (HTML required or validation schema)"
      - validation: "rules applied (min, max, pattern, email, etc)"
      - label: "associated label text"
      - error_display: "inline | toast | none"

    submission:
      - handler: "function name or inline"
      - api_call: "endpoint or action called"
      - method: "POST | PUT | PATCH | mutation"
      - loading_state: "disabled button | spinner | skeleton | none"
      - success_feedback: "toast | redirect | inline message | modal | none"
      - error_handling: "try/catch | .catch | onError | none"
      - reset_behavior: "reset() | clear fields | redirect | none"

    protection:
      - double_submit: "button disabled during submit | request dedup | none"
      - csrf: "CSRF token present | not applicable | missing"
      - rate_limit: "client-side throttle | none"
```

### Phase 3: Detect Issues

```yaml
issue_detection:
  - id: no_validation
    condition: "Form submits without any validation (no schema, no HTML required, no manual check)"
    severity: HIGH
    impact: "Invalid data reaches API, causes errors or data corruption"
    suggestion: "Add zod/yup schema validation with react-hook-form"

  - id: client_only_validation
    condition: "Validation only on client side, no server-side validation"
    severity: MEDIUM
    impact: "Validation can be bypassed, API accepts invalid data"
    suggestion: "Add server-side validation (same zod schema reusable)"

  - id: missing_error_display
    condition: "Validation runs but errors not shown to user"
    severity: HIGH
    impact: "User doesn't know why form won't submit — frustrating UX"
    suggestion: "Add inline error messages below each field"

  - id: no_loading_state
    condition: "No disabled/loading indicator during submission"
    severity: MEDIUM
    impact: "User clicks multiple times, doesn't know if action is processing"
    suggestion: "Disable button and show spinner during submit"

  - id: no_success_feedback
    condition: "Form submits successfully but no confirmation shown"
    severity: MEDIUM
    impact: "User unsure if action completed — may resubmit"
    suggestion: "Show toast, redirect, or inline success message"

  - id: uncontrolled_to_controlled
    condition: "Input switches between controlled and uncontrolled (defaultValue + value)"
    severity: HIGH
    impact: "React warning, unpredictable behavior, potential data loss"
    suggestion: "Use controlled (value + onChange) or uncontrolled (defaultValue + ref) consistently"

  - id: missing_form_a11y
    condition: "Form without proper labels, aria-describedby on errors, role=alert on error messages"
    severity: HIGH
    impact: "Screen readers can't navigate form or announce errors"
    feeds_gate: "QG-AX-005"
    suggestion: "Add htmlFor/id on labels, aria-describedby linking errors, role=alert"

  - id: no_keyboard_submit
    condition: "Form can't be submitted with Enter key (missing <form> or type=submit)"
    severity: MEDIUM
    impact: "Keyboard-only users can't submit — accessibility violation"
    suggestion: "Wrap in <form> with <button type=submit>"

  - id: double_submit
    condition: "No protection against double submission (button not disabled during submit)"
    severity: HIGH
    impact: "Duplicate API calls, duplicate records, race conditions"
    suggestion: "Disable button during submit, or debounce submission handler"
```

### Phase 4: Health Score

```yaml
health_score:
  formula: >
    100 - (no_validation_count * 10) - (missing_error_display_count * 8)
    - (double_submit_count * 8) - (uncontrolled_switch_count * 5)
    - (missing_form_a11y_count * 5) - (no_loading_state_count * 3)
    - (no_success_feedback_count * 3) - (no_keyboard_submit_count * 3)
    - (client_only_validation_count * 2)
  max: 100
  min: 0
  thresholds:
    solid: ">= 90 — forms are well implemented and accessible"
    good: "70-89 — minor gaps, mostly solid"
    fragile: "50-69 — significant validation or UX gaps"
    broken: "< 50 — forms need serious attention"
```

---

## Output Format

```
FORMS DISCOVERY
================
Project: {name}
Form Library: {react-hook-form | formik | manual | mixed}
Validation: {zod | yup | valibot | manual | none}
Forms Found: {count}
Health Score: {score}/100 ({solid | good | fragile | broken})

FORM INVENTORY
---------------
 #  | Form               | File                    | Fields | Validation | Loading | A11y   | Status
----|--------------------|-------------------------|--------|------------|---------|--------|--------
 1  | ScheduleForm       | ScheduleForm.tsx        | 5      | zod        | Yes     | WARN   | GOOD
 2  | ContactForm        | ContactForm.tsx         | 3      | manual     | No      | FAIL   | WARN
 3  | LoginForm          | LoginForm.tsx           | 2      | yup        | Yes     | OK     | OK
 4  | SearchFilter       | FilterBar.tsx           | 4      | none       | n/a     | WARN   | WARN

FORM DETAILS
--------------
 ScheduleForm (ScheduleForm.tsx)
   Fields: name (text, required), email (email, required), phone (tel),
           date (date, required), time (select, required)
   Validation: zod schema (zodResolver)
   Submit: POST /webhook/example-booking
   Loading: Button disabled + spinner
   Success: Confirmation screen
   A11y: WARN — 2 fields missing aria-describedby on error

 ContactForm (ContactForm.tsx)
   Fields: name (text), email (email), message (textarea)
   Validation: manual (if checks in handler)
   Submit: POST /api/contact
   Loading: NONE — button stays clickable during submit
   Success: NONE — no feedback after submit
   A11y: FAIL — no labels (placeholder-only), no error announcements

ISSUES ({count})
-----------------
 HIGH   ContactForm — no loading state, double submit possible
 HIGH   ContactForm — missing form labels (placeholder-only) — a11y violation
 HIGH   ContactForm — errors not displayed to user
 MEDIUM SearchFilter — no validation on filter inputs
 MEDIUM ScheduleForm — 2 fields missing aria-describedby
 MEDIUM ContactForm — no success feedback after submission

A11Y FORM AUDIT
-----------------
 Form             | Labels | Error Announce | Keyboard Submit | Focus Mgmt
------------------|--------|----------------|-----------------|----------
 ScheduleForm     | OK     | PARTIAL        | OK              | OK
 ContactForm      | FAIL   | FAIL           | OK              | WARN
 LoginForm        | OK     | OK             | OK              | OK
 SearchFilter     | WARN   | n/a            | WARN            | OK

================
Next steps:
  1. Fix ContactForm — add labels, loading state, error display (3 issues)
  2. Add aria-describedby to ScheduleForm error messages
  3. Add validation to SearchFilter inputs

What do you want to do?
```

---

## Integration with Other Tasks

```yaml
feeds_into:
  apex-suggest:
    what: "Form issues become proactive suggestions"
    how: "Missing validation, a11y gaps, double submit risks flagged automatically"

  apex-audit:
    what: "Form health score feeds audit report"
    how: "Health score becomes part of project readiness assessment"

  react-eng:
    what: "Kent receives full form architecture map"
    how: "Knows which forms need improvements before modifying them"

  a11y-eng:
    what: "Sara receives form accessibility data"
    how: "Missing labels, error announcements, keyboard submit gaps pre-loaded"

  interaction-dsgn:
    what: "Ahmad receives form UX pattern analysis"
    how: "Loading states, success feedback, error display patterns mapped"
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-DISC-FORMS-001
    condition: "No forms found in project"
    action: SKIP_WITH_WARNING
    severity: LOW
    blocking: false
    feeds_gate: null
    available_check: "manual"
    on_unavailable: SKIP_WITH_WARNING

  - id: VC-DISC-FORMS-002
    condition: "Form without any validation"
    action: WARN
    severity: HIGH
    blocking: false
    feeds_gate: null
    available_check: "manual"
    on_unavailable: MANUAL_CHECK
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | apex-lead (routing enrichment), react-eng (form improvements), a11y-eng (form a11y fixes) |
| Next action | User fixes form issues by severity, adds validation, or continues to other commands |

---

## Cache

```yaml
cache:
  location: ".aios/apex-context/forms-cache.yaml"
  ttl: "Until form-related files change"
  invalidate_on:
    - "Any .tsx/.jsx file containing <form> or onSubmit modified"
    - "Validation schema files modified"
    - "User runs *discover-forms explicitly"
```

---

## Edge Cases

```yaml
edge_cases:
  - condition: "No forms in project (static site)"
    action: "REPORT — score 100, no forms to audit"
  - condition: "Forms use Next.js server actions"
    action: "ADAPT — check server-side validation in action files, not just client"
  - condition: "Headless form libraries (React Aria, Radix Form)"
    action: "ADAPT — trust library patterns for a11y, focus on validation and UX"
  - condition: "Multi-step wizard form"
    action: "ADAPT — treat each step as sub-form, validate step transitions"
  - condition: "Forms with file upload"
    action: "ADAPT — check file type validation, size limits, progress indicator"
```

---

`schema_ref: data/discovery-output-schema.yaml`

---

*Apex Squad — Forms Discovery Task v1.0.0*
