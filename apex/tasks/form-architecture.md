---
id: form-architecture
version: "1.0.0"
title: "Form Architecture & Handling"
description: "Design form architecture with React Hook Form, server actions, validation strategies, progressive enhancement, and accessible form patterns"
elicit: true
owner: react-eng
executor: react-eng
outputs:
  - form-architecture-spec.md
  - validation-schema.yaml
---

# Form Architecture & Handling

## When This Task Runs

- Building new forms or form-heavy features
- Migrating to React Hook Form or server actions
- Form validation needs standardization
- Multi-step form design needed
- `*form` command invoked

## Execution Steps

### Step 1: Audit Current Forms
```
SCAN project for form patterns:
- Form elements (<form>, <input>, <select>, <textarea>)
- Form state management (useState, controlled inputs)
- Validation approaches (inline, onSubmit, schema)
- Error display patterns
- Loading/submission states
- Form libraries (React Hook Form, Formik, etc.)

OUTPUT: Form inventory + pattern consistency report
```

### Step 2: Select Form Strategy

**elicit: true** — Confirm form architecture:

| Pattern | Best For | Progressive Enhancement |
|---------|----------|------------------------|
| **React Hook Form + Zod** | Complex forms, client validation | Partial |
| **Server Actions + useFormState** | RSC apps, simple forms | Full |
| **RHF + Server Action** | Best of both worlds | Full |
| **Uncontrolled + FormData** | Simple forms, max perf | Full |

### Step 3: Design Validation Architecture

```yaml
validation:
  schema_library: "Zod (shared between client and server)"

  layers:
    client_side:
      when: "Instant feedback during typing"
      library: "React Hook Form + Zod resolver"
      mode: "onBlur + onChange after first error"

    server_side:
      when: "After submission (always, even if client validates)"
      approach: "Parse FormData with Zod schema"
      reason: "Client validation can be bypassed"

  shared_schema: |
    // schemas/contact-form.ts
    import { z } from 'zod'

    export const contactFormSchema = z.object({
      name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
      email: z.string().email('Email inválido'),
      phone: z.string().regex(/^\(\d{2}\) \d{4,5}-\d{4}$/, 'Telefone inválido'),
      message: z.string().min(10, 'Mensagem muito curta').max(500),
    })

    export type ContactFormData = z.infer<typeof contactFormSchema>

  error_display:
    inline: "Below each field, appears on validation failure"
    summary: "Top of form for server-side errors"
    toast: "For submission success/failure feedback"
```

### Step 4: Design Form Patterns

```yaml
patterns:
  simple_form:
    approach: "Server Action + useFormState"
    progressive_enhancement: true
    code: |
      // Works without JavaScript
      <form action={submitAction}>
        <input name="email" required />
        <SubmitButton />
      </form>

  complex_form:
    approach: "React Hook Form + Zod + Server Action"
    progressive_enhancement: true
    code: |
      // Enhanced with JS, works without
      const form = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: 'onBlur',
      })

  multi_step:
    approach: "React Hook Form + step state"
    state_persistence: "Form values preserved across steps"
    validation: "Per-step schema validation"
    navigation: "Back/forward without losing data"

  dynamic_fields:
    approach: "useFieldArray from React Hook Form"
    add_remove: "Dynamic field rows"
    validation: "Array schema with per-item validation"
```

### Step 5: Design Submission Handling

```yaml
submission:
  states:
    idle: "Form ready for input"
    submitting: "Button disabled, spinner shown"
    success: "Success message, redirect or reset"
    error: "Error displayed, form still editable"

  optimistic_ui:
    approach: "useOptimistic for instant feedback"
    rollback: "Revert on server error"

  double_submit_prevention:
    client: "Disable button on submit"
    server: "Idempotency key in FormData"

  error_handling:
    field_errors: "Map to specific fields"
    form_errors: "Display at top of form"
    network_errors: "Toast with retry option"
    rate_limiting: "Show countdown timer"
```

### Step 6: Validate Form Architecture

- [ ] All forms have both client and server validation
- [ ] Forms work without JavaScript (progressive enhancement)
- [ ] Error messages are user-friendly (not technical)
- [ ] Loading/submission states prevent double submit
- [ ] Keyboard navigation works (Tab order, Enter submit)
- [ ] Screen readers announce errors (aria-invalid, aria-describedby)

## Quality Criteria

- Shared Zod schemas between client and server
- Progressive enhancement (forms work without JS)
- No double-submit possible
- Accessible error announcements

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Validation | Client + server, shared schema |
| Progressive | Works without JavaScript |
| Double submit | Prevented on client and server |
| A11y | Errors announced to screen readers |

## Handoff

- Form specs feed `@a11y-eng` for keyboard and screen reader testing
- Validation schemas feed `@frontend-arch` for shared package design
- Submission patterns feed `@interaction-dsgn` for loading state design
