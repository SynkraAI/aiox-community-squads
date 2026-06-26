# Pre-Execution Gate — Quality Veto Conditions (V1.*)

> **Phase:** 4.5 (Pre-Execution Quality Gate)
> **Agent:** quality-gate (Deming)
> **Type:** Automatic (hard block, latency < 60s)
> **Behavior:** BLOCK execution, return to wave-planner for fix (max 2 iterations)
> **Source:** PRD Section 3.3 Phase 4.5 + veto-conditions.yaml V1.*
> **Script:** `scripts/validate-dispatch-gate.sh --phase pre-execution`

---

## Purpose

Validates that EVERY task is sufficiently defined and unambiguous BEFORE any dispatch happens. Prevents defective prompts from reaching subagents, which would waste tokens and produce garbage.

**Deming Principle:** "Quality is built in at the source, not inspected in at the end."

**Pedro Valério Principle:** "Se o executor CONSEGUE fazer errado, VAI fazer errado."

---

## Veto Conditions

### V1.1: Task Has Output Path

| Field | Value |
|-------|-------|
| **ID** | V1.1 |
| **Condition** | Task has no output path |
| **Check** | `task.output_path is None or task.output_path == ""` |
| **Severity** | Hard block |
| **Action** | VETO — Define output path before dispatch |
| **Rationale** | No output path = nowhere to verify = V2.1 will always fail |

### V1.2: Acceptance Criterion Is Measurable

| Field | Value |
|-------|-------|
| **ID** | V1.2 |
| **Condition** | Acceptance criterion is subjective |
| **Check** | `regex match: (good\|appropriate\|adequate\|well-written\|nice\|quality\|proper)` |
| **Severity** | Hard block |
| **Action** | VETO — Rewrite with measurable criteria |
| **Rationale** | Subjective criteria = subjective quality = rework |

**Examples:**

| Bad (subjective) | Good (operational) |
|-------------------|--------------------|
| "good quality" | "< 500 words" |
| "well-written" | "contains CTA" |
| "appropriate tone" | "3+ sections" |
| "nice layout" | "file exists at path X" |
| "proper formatting" | "YAML valid (parseable)" |

### V1.3: No Placeholder Text

| Field | Value |
|-------|-------|
| **ID** | V1.3 |
| **Condition** | Prompt has placeholders |
| **Check** | `regex match: (\[XXX\]\|\{TODO\}\|TBD\|\[PLACEHOLDER\]\|\[INSERT\])` |
| **Severity** | Hard block |
| **Action** | VETO — Resolve all placeholders |
| **Rationale** | Placeholders = deferred decisions = ambiguity for executor |

### V1.4: No Circular Dependencies

| Field | Value |
|-------|-------|
| **ID** | V1.4 |
| **Condition** | Circular dependency in DAG |
| **Check** | `python scripts/wave-optimizer.py tasks.json --check-cycles` returns non-zero |
| **Severity** | Hard block |
| **Action** | VETO — Fix dependency graph (remove circular reference) |
| **Rationale** | Circular deps = execution deadlock |

### V1.5: Haiku Output > 50 Lines Has Template

| Field | Value |
|-------|-------|
| **ID** | V1.5 |
| **Condition** | Haiku prompt without template for output > 50 lines |
| **Check** | `task.model == "haiku" AND task.expected_lines > 50 AND no template in prompt` |
| **Severity** | Hard block |
| **Action** | VETO — Add output template (Haiku ALWAYS rule) |
| **Rationale** | Haiku without template for long output = unpredictable structure |

### V1.6: No Code-Switching in Prompt

| Field | Value |
|-------|-------|
| **ID** | V1.6 |
| **Condition** | Haiku prompt with code-switching (EN+PT mixed) |
| **Check** | `detect_language_mixing(prompt) == True` |
| **Severity** | Hard block |
| **Action** | VETO — Instructions in EN, output language specified separately |
| **Rationale** | Mixed-language instructions confuse Haiku, reduce output quality |

### V1.7: Single Deliverable Per Task

| Field | Value |
|-------|-------|
| **ID** | V1.7 |
| **Condition** | Task has multiple deliverables |
| **Check** | `count_deliverables(task) > 1` |
| **Severity** | Hard block |
| **Action** | VETO — Split into 1 task = 1 deliverable |
| **Rationale** | Multi-deliverable = ambiguous scope = partial completion |

### V1.8: Timeout Defined

| Field | Value |
|-------|-------|
| **ID** | V1.8 |
| **Condition** | Task has no timeout defined |
| **Check** | `task.timeout is None` |
| **Severity** | Hard block |
| **Action** | VETO — Assign timeout from timeout-rules.yaml |
| **Rationale** | "O que não tem data pode ser feito qualquer hora. Qualquer hora = nunca." (PV002) |

### V1.9: No Vague Verbs

| Field | Value |
|-------|-------|
| **ID** | V1.9 |
| **Condition** | Vague verbs in task description |
| **Check** | `regex match: (improve\|optimize\|enhance\|better\|fix up) without specifics` |
| **Severity** | Hard block |
| **Action** | VETO — Replace with specific actions |
| **Rationale** | Vague verbs = infinite scope = executor decides what to do |

### V1.10: Model Assigned

| Field | Value |
|-------|-------|
| **ID** | V1.10 |
| **Condition** | No model assigned to task |
| **Check** | `task.model is None or task.model == ""` |
| **Severity** | Hard block |
| **Action** | VETO — Run task-router to assign model |
| **Rationale** | No model = unpredictable cost |

### V1.11: Agent Assigned

| Field | Value |
|-------|-------|
| **ID** | V1.11 |
| **Condition** | No agent/command assigned to task |
| **Check** | `task.agent is None AND task.executor_type != "worker"` |
| **Severity** | Hard block |
| **Action** | VETO — Run task-router to assign agent |
| **Rationale** | No agent = wrong execution context |

---

## Execution Flow

```
For EACH task in execution plan:
│
├── V1.1: output_path defined?     → FAIL: "Define output_path"
├── V1.2: criteria measurable?     → FAIL: "Rewrite subjective criteria"
├── V1.3: no placeholders?         → FAIL: "Resolve [XXX], {TODO}, TBD"
├── V1.7: single deliverable?      → FAIL: "Split into 1 task = 1 deliverable"
├── V1.8: timeout defined?         → FAIL: "Assign from timeout-rules.yaml"
├── V1.9: no vague verbs?          → FAIL: "Replace improve/optimize/enhance"
├── V1.10: model assigned?         → FAIL: "Run task-router"
├── V1.11: agent assigned?         → FAIL: "Run task-router"
│
├── IF model == "haiku":
│   ├── V1.5: template for >50 lines?  → FAIL: "Add output template"
│   └── V1.6: no code-switching?        → FAIL: "English only"
│
├── V1.4: DAG no cycles?           → FAIL: "Fix circular dependency"
│
└── ALL PASS → ✅ CLEARED FOR EXECUTION
    ANY FAIL → ❌ BLOCK — return to wave-planner (max 2 fix iterations)
```

---

## Failure Handling

| Failure Count | Action |
|---------------|--------|
| 1st failure | Return to wave-planner with specific fix instructions |
| 2nd failure | Return again with more detailed instructions |
| 3rd failure | ESCALATE to user — gate cannot be auto-fixed |

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Let "good quality" pass as criterion | VETO V1.2 — demand measurable |
| Accept task with 3 deliverables | VETO V1.7 — split into 3 tasks |
| Skip gate to save time | Gate catches errors that cost 10x more to fix after |
| Haiku prompt in PT-BR | VETO V1.6 — instructions always in EN |
