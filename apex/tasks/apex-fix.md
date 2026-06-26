# Task: apex-fix

```yaml
id: apex-fix
version: "2.0.0"
title: "Apex Quick Fix — Scope-Locked & Snapshot-Enabled"
description: >
  Lightweight single-agent command for targeted fixes with SCOPE LOCK,
  SNAPSHOT rollback, and REQUEST ADHERENCE validation. Routes to the best
  specialist, locks scope, snapshots files, executes, validates adherence, done.
elicit: true
owner: apex-lead
executor: apex-lead
dependencies:
  - tasks/apex-route-request.md
  - data/veto-conditions.yaml
outputs:
  - Fixed code committed locally (not pushed)
  - Typecheck + lint passing
  - Scope-verified changes only
```

---

## Command

### `*apex-fix {description}`

Single-agent fix for targeted, scoped changes. Bypasses the full pipeline when the fix is clearly within one agent's domain.

---

## When to Use

- CSS bug fix (layout broken, spacing wrong, responsive issue)
- Component state bug (loading not showing, wrong conditional)
- Animation tweak (spring too bouncy, entrance too slow)
- Accessibility fix (missing aria-label, contrast issue)
- Performance fix (unnecessary re-render, missing lazy load)
- Single-file or 2-3 file changes within one domain

## When NOT to Use (redirect to pipeline)

- New component from scratch → `*apex-go` or `*apex-quick`
- Cross-domain change (CSS + React + animation) → `*apex-quick`
- New feature with multiple user flows → `*apex-go`
- Changes touching shared packages → `*apex-go`

---

## Execution Steps

### Step 1: Route

```
apex-lead analyzes the request using apex-route-request.md routing table.

IF scope == "single-agent":
  Proceed with *apex-fix
ELIF scope == "multi-agent" AND agents.count <= 2:
  Proceed with *apex-fix, chain agents sequentially
ELSE:
  Suggest *apex-quick or *apex-go instead
  Ask user: "This looks bigger than a quick fix. Want to use *apex-quick instead?"
```

**Output:** Target agent identified, scope confirmed.

**HANDOFF:** Follow `apex-handoff-protocol.md` — Emil announces delegation:
```
Emil: Isso e {domain} — delegando para {icon} {name} (@{id}).
      {one-line reason}
```

### Step 1.6: Intent Clarification (NEW — Non-Technical User Support)

**CRITICAL: Before scope lock, translate the user's request into visual language and CONFIRM.**

This step bridges the gap between how users describe things ("mantenha o header fixo") and technical implementation ("position: sticky"). The user should NEVER need to know CSS, React, or any framework terminology.

**Process:**
1. Scan `data/vocabulary-bridge.yaml` for matching patterns in the user's request
2. If match found: translate to `visual_description`
3. If no match: ask user to describe what they SEE or WANT (not how to code it)
4. Present translation in user language and CONFIRM before proceeding

**Format:**
```
Entendi que voce quer:
→ {visual_description_1 — in user language, NOT code}
→ {visual_description_2 — if multiple intents detected}

Correto? (sim / ajustar)
```

**Examples:**
```
User: "tire a parte do background do header deixe quase transparente mas mantenha os icones e logo, e mantenha o header fixo"

Emil:
Entendi que voce quer:
→ O fundo do header fica transparente (sem cor solida, da pra ver o que tem atras)
→ Os icones, logo e botoes continuam no lugar, sem mudar
→ O header fica SEMPRE visivel, mesmo quando rolar a pagina pra baixo

Correto? (sim / ajustar)
```

```
User: "quero que o card flutue e brilhe quando passar o mouse"

Emil:
Entendi que voce quer:
→ O card sobe levemente quando voce passa o mouse (efeito de elevacao)
→ O card ganha um brilho suave ao redor (efeito glow)

Correto? (sim / ajustar)
```

**Rules:**
- NEVER use technical terms in the confirmation (no "position: sticky", no "box-shadow", no "opacity")
- Describe what the user will SEE, not what the code will DO
- If user says "ajustar", ask WHAT specifically to adjust — loop until confirmed
- Only proceed to Scope Lock (Step 1.5) after user confirms "sim"
- If vocabulary-bridge has no match AND user can't describe clearly, ask for a reference ("Tem algum site que faz algo parecido?")

**Veto:** `VC-INTENT-001` — Cannot proceed to scope lock without user confirming intent translation.

---

### Step 1.5: Scope Lock (NEW — P0)

**CRITICAL: Before ANY file read or modification, declare and lock scope.**

```
Emil declares scope lock:

**🔒 Scope Lock:**
- Request: "{verbatim user request — copy exactly as typed}"
- Target: {file(s) that will be modified}
- Change: {specific change — what will be different}
- Out of scope: everything else in these files

{IF user provided screenshot/print:}
- Visual reference: {attached — compare result against this}
```

**Rules:**
- Copy user request VERBATIM — no interpretation, no paraphrasing
- If request is ambiguous, ASK before locking scope
- Scope lock is IMMUTABLE during execution — cannot expand without user approval
- If agent discovers other issues during fix → REPORT as suggestions AFTER, never fix inline

**Veto:** `VC-FIX-SCOPE-001` — Any modification outside declared scope is BLOCKED.

### Step 1.8: Snapshot (NEW — P0)

**CRITICAL: Before ANY file modification, snapshot the files in scope.**

```bash
# Snapshot files that will be modified
git stash push -m "apex-snapshot-$(date +%s)" -- {files_in_scope}

# If git stash fails (e.g., untracked files):
git diff -- {files_in_scope} > .aios/apex-snapshots/fix-{timestamp}.patch
```

**Veto:** `VC-SNAPSHOT-001` — Cannot start fix without snapshot.

**On failure:** If snapshot cannot be created (not a git repo, permission error):
1. WARN user: "Snapshot nao criado — rollback manual sera necessario"
2. Proceed only with user confirmation

### Step 2: Execute

```
Specialist introduces themselves (1 line) then executes:

{icon} {name} aqui. {one-line assessment}
[reads files, understands code, applies fix]
```

Agent follows existing patterns in the codebase.
No design spec, no architecture docs — just fix the code.

**Rules:**
- Follow existing code patterns (don't refactor surrounding code)
- Don't add features beyond what was requested
- Don't create new files unless absolutely necessary
- Keep the change minimal and focused
- **SCOPE LOCK: Modify ONLY files and lines declared in Step 1.5**
- **If you see other improvements → note them for Step 4, do NOT apply them**

### Step 3: Verify

Run minimal quality checks:

```bash
# Always run (profile-independent):
npm run typecheck 2>/dev/null || npx tsc --noEmit 2>/dev/null
npm run lint 2>/dev/null || true

# If test script exists:
npm test 2>/dev/null || true
```

**Gate: QG-AX-FIX-001 (Technical)**
- Zero new TypeScript errors (pre-existing errors are OK)
- Zero new lint errors (pre-existing errors are OK)
- No test regressions

**Gate: QG-AX-FIX-002 (Request Adherence) — NEW**
- Changes correspond EXACTLY to the original user request
- No out-of-scope modifications detected
- If user provided visual reference, result matches

**Adherence check format:**
```
**🎯 Adherence Check:**
- Pedido: "{original request verbatim}"
- Modificado: {files + summary of actual changes}
- Fora do escopo: {none | list of out-of-scope changes detected}
- Correspondencia: ✅ MATCH | ⚠️ PARTIAL | ❌ MISMATCH
```

**If MISMATCH or PARTIAL:**
1. Show diff to user highlighting scope deviations
2. Ask: "Essas mudanças correspondem ao que pediu?"
3. If user says no → rollback via snapshot (Step 1.8) and re-execute

If verification fails:
1. Agent fixes the issues (max 2 attempts)
2. If still failing after 2 attempts, present the issue to the user

### Step 4: Report

```
*apex-fix complete.

Agent: @{agent-id} ({agent-name})
Fix: {one-line summary}
Files modified:
  - {file1} (lines X-Y)
  - {file2} (lines X-Y)
Scope: 🔒 {scope description from Step 1.5}
Checks: typecheck {PASS|FAIL} | lint {PASS|FAIL} | tests {PASS|FAIL}
Adherence: {MATCH|PARTIAL|MISMATCH}

{IF other issues found during execution:}
💡 **Suggestions (out of scope, not applied):**
  1. {issue found but not fixed — describe briefly}
  2. {issue found but not fixed — describe briefly}
  Aplicar? (use *apex-fix para cada, ou *apex-quick para batch)

Ready to commit? (describe any additional changes if needed)

{IF user rejects:}
Reverter? Snapshot disponível — 1 comando restaura o original.
```

**IMPORTANT:** Do NOT commit automatically. Always ask the user first.

---

## Rollback Protocol

If user says "volta", "revert", "desfaz", "nao gostei":

```bash
# Restore from snapshot
git stash pop

# OR if patch was used:
git apply --reverse .aios/apex-snapshots/fix-{timestamp}.patch
```

Show: "⏪ Revertido. Arquivos restaurados ao estado anterior ao fix."

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-FIX-001
    condition: "Fix scope exceeds 5 files"
    action: "WARN — suggest *apex-quick instead"
    blocking: false  # Warning only, user can override

  - id: VC-FIX-002
    condition: "Fix creates a new user-facing component"
    action: "BLOCK — new components require *apex-quick or *apex-go"
    blocking: true

  - id: VC-FIX-003
    condition: "Fix modifies shared packages (packages/*)"
    action: "BLOCK — shared package changes require full pipeline"
    blocking: true

  # NEW — Intent Clarification
  - id: VC-INTENT-001
    condition: "Fix proceeds without user confirming intent translation"
    action: "VETO — Must translate request to visual language and get user 'sim' before scope lock"
    blocking: true

  # NEW — P0 veto conditions
  - id: VC-FIX-SCOPE-001
    condition: "Files modified outside declared scope lock"
    action: "VETO — Revert out-of-scope changes immediately"
    blocking: true

  - id: VC-FIX-SCOPE-002
    condition: "Lines changed > 3x minimum necessary for the fix"
    action: "REVIEW — Present diff to user before applying"
    blocking: false  # Warning, user decides

  - id: VC-SNAPSHOT-001
    condition: "Fix started without file snapshot (git stash or patch)"
    action: "VETO — Create snapshot before any modification"
    blocking: true

  - id: VC-FIX-ADHERENCE-001
    condition: "Fix completed without request adherence check (QG-AX-FIX-002)"
    action: "VETO — Run adherence check before finalizing"
    blocking: true
```

---

## Examples

**Example 1 — CSS fix (scope-locked):**
```
User: *apex-fix "o padding do header tá 32px no mobile, deveria ser 16px"

Emil: Routing to @css-eng (Josh) — CSS responsive issue, single-agent scope.

**🔒 Scope Lock:**
- Request: "o padding do header tá 32px no mobile, deveria ser 16px"
- Target: src/components/Header.tsx
- Change: padding 32px → 16px on mobile breakpoint
- Out of scope: everything else in Header.tsx

📸 Snapshot criado.

Josh: [reads Header.tsx, changes ONLY the padding value at mobile breakpoint]

**🎯 Adherence Check:**
- Pedido: "o padding do header tá 32px no mobile, deveria ser 16px"
- Modificado: Header.tsx (line 47: p-8 → p-4 at sm breakpoint)
- Fora do escopo: none
- Correspondencia: ✅ MATCH

Emil: Fix complete. 1 file, 1 line. typecheck PASS. Ready to commit?
```

**Example 2 — Fix with out-of-scope suggestion:**
```
User: *apex-fix "the modal close button is too small"

Emil: Routing to @a11y-eng (Sara) — touch target issue.

**🔒 Scope Lock:**
- Request: "the modal close button is too small"
- Target: src/components/ServiceDetailModal.tsx
- Change: close button size → minimum 44x44px
- Out of scope: everything else

Sara: [fixes close button to 44x44px]
      [NOTICES: modal also missing aria-labelledby — but this is OUT OF SCOPE]

**🎯 Adherence Check:**
- Correspondencia: ✅ MATCH

Fix complete. 1 file. typecheck PASS.

💡 **Suggestions (out of scope, not applied):**
  1. Modal missing aria-labelledby (a11y issue)
  Aplicar? (use *apex-fix "add aria-labelledby to modal")

Ready to commit?
```

**Example 3 — User rejects fix:**
```
User: *apex-fix "ajusta o hero layout"

Emil: [executes fix]

User: "nao gostei, volta como estava"

Emil: ⏪ Revertido. Arquivos restaurados ao estado anterior.
      O que gostaria de ajustar no pedido?
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | User (fix applied locally) |
| Next action | User decides to commit, or requests additional changes, or rollback |

---

*Apex Squad — Quick Fix Task v2.0.0 (scope-locked, snapshot-enabled, adherence-gated)*
