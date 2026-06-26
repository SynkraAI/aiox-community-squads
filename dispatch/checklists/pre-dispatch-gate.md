# Pre-Dispatch Gate — Sufficiency Veto Conditions (V0.*)

> **Phase:** 0 (Sufficiency Gate)
> **Agent:** dispatch-chief
> **Type:** Human-in-Loop (soft block, latency < 30s)
> **Behavior:** Redirect with recommendation — does NOT block silently
> **Source:** PRD Section 3.3 Phase 0 + veto-conditions.yaml V0.*

---

## Purpose

Validates that input is SUFFICIENT for dispatch. If not, redirects user to the correct agent to prepare better input. This gate prevents dispatch from wasting resources on vague or incomplete requests.

**Principle:** "Dispatch is an EXECUTION engine, not a THINKING engine. If the input needs thinking, route to the right thinker first."

---

## Veto Conditions

### V0.1: Story Has Acceptance Criteria

| Field | Value |
|-------|-------|
| **ID** | V0.1 |
| **Condition** | Story has no acceptance criteria |
| **Check** | `grep -c 'acceptance\|criteria\|[ ]' {story_file} == 0` |
| **Severity** | Soft block |
| **Action** | VETO — Redirect to `/po` for acceptance criteria |
| **Rationale** | No acceptance criteria = no way to verify output = rework guaranteed |

### V0.2: Input Meets Minimum Detail

| Field | Value |
|-------|-------|
| **ID** | V0.2 |
| **Condition** | Input < 10 words with no deliverables |
| **Check** | `word_count < 10 AND no quantities detected` |
| **Severity** | Soft block |
| **Action** | VETO — Redirect to `/pm` or `/copy:agents:copy-chief` |
| **Rationale** | Vague input = guesswork = wrong output |

### V0.3: Specific Deliverables Mentioned

| Field | Value |
|-------|-------|
| **ID** | V0.3 |
| **Condition** | No specific deliverables mentioned |
| **Check** | `no file types, no quantities, no output paths` |
| **Severity** | Soft block |
| **Action** | VETO — Ask for quantities and deliverables |
| **Rationale** | Without concrete deliverables, can't decompose into atomic tasks |

---

## Execution Flow

```
INPUT arrives
│
├── Is it a story file? (.md with story structure)
│   ├── YES → Check V0.1 (acceptance criteria present?)
│   │   ├── PASS → SUFFICIENT → Phase 1
│   │   └── FAIL → REDIRECT: "Story needs acceptance criteria. Use /po to add them."
│   └── NO → Continue
│
├── Is it a PRD file?
│   ├── YES → SUFFICIENT (PRDs have requirements by definition) → Phase 1
│   └── NO → Continue
│
├── Is it a task list with clear deliverables?
│   ├── YES → Check V0.3 (specific deliverables?)
│   │   ├── PASS → SUFFICIENT → Phase 1
│   │   └── FAIL → REDIRECT: "Need specific deliverables (e.g., '5 emails', 'config.yaml')"
│   └── NO → Continue
│
├── Is it free text?
│   ├── Check V0.2 (>= 10 words or has quantities?)
│   │   ├── PASS → CONVERT via convert-input.md → Phase 1
│   │   └── FAIL → REDIRECT with recommendation:
│   │       ├── "Precisa de estratégia?" → /pm
│   │       ├── "Precisa de stories?" → /po
│   │       ├── "Precisa de briefing?" → /copy:agents:copy-chief
│   │       └── "Não sei o que preciso" → /lens
│   └── Continue
│
└── Unknown input → REDIRECT: "Input format not recognized. Options: story, PRD, task list, or detailed text."
```

---

## Redirect Recommendations

| User Need | Redirect To | What They Get |
|-----------|-------------|---------------|
| Strategy/planning | `/pm` | PRD with requirements |
| User stories | `/po` | Stories with acceptance criteria |
| Copy briefing | `/copy:agents:copy-chief` | Structured briefing |
| Creative copy | `/copy:agents:copy-chief` | Copy with style/tone defined |
| Multi-perspective analysis | `/lens` | Analysis before deciding |
| Don't know what I need | `/lens` | Structured analysis of options |

---

## Validation Script

```bash
# Executed by: scripts/validate-dispatch-gate.sh --phase sufficiency
# Exit 0 = PASS, Exit 1 = BLOCKED

ERRORS=0

# V0.1: Acceptance criteria
if [ "$INPUT_TYPE" = "story" ]; then
  if ! grep -qiE 'acceptance|criteria|\[ \]' "$INPUT_FILE"; then
    echo "❌ V0.1: VETO — Story has no acceptance criteria"
    ERRORS=$((ERRORS+1))
  fi
fi

# V0.2: Minimum detail
WORD_COUNT=$(wc -w < "$INPUT_FILE")
if [ "$WORD_COUNT" -lt 10 ]; then
  if ! grep -qE '[0-9]+\s+(emails?|newsletters?|tasks?|agents?)' "$INPUT_FILE"; then
    echo "❌ V0.2: VETO — Input too vague (< 10 words, no deliverables)"
    ERRORS=$((ERRORS+1))
  fi
fi

# V0.3: Specific deliverables
if ! grep -qE '[0-9]+|\.md|\.yaml|\.json|\.py|output/' "$INPUT_FILE"; then
  echo "❌ V0.3: VETO — No specific deliverables mentioned"
  ERRORS=$((ERRORS+1))
fi

if [ "$ERRORS" -eq 0 ]; then
  echo "=== SUFFICIENCY GATE PASSED ==="
  exit 0
else
  echo "=== DISPATCH BLOCKED: $ERRORS sufficiency conditions failed ==="
  exit 1
fi
```

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Accept "make it better" and guess | REDIRECT to `/pm` for requirements |
| Accept 3-word input and decompose | REDIRECT — need specific deliverables |
| Block silently without recommendation | REDIRECT with specific agent suggestion |
| Ask 5 clarifying questions | REDIRECT to agent that asks the right questions |
