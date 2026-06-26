# Task: Design Custom Hooks

**Task ID:** CCM-PI-006
**Version:** 1.1.0
**Command:** `*hook-designer`
**Owner:** Conduit (project-integrator)
**Purpose:** Design custom Claude Code hooks for a project by identifying automation needs, choosing appropriate hook types and events, designing hook logic, and producing implementation-ready specifications aligned to the current runtime behavior.

## Contrato SINKRA

task: hook-designer
atomic_layer: Atom
executor: hooks-architect
Domain: Operational
accountability_token: TK-CCM-ACC-001
Input:
- hook_purpose
- trigger_event
- project_path
Output:
- hook-design-spec
- hook-implementation
output_schema: hook-implementation
Pre-Conditions:
- Contexto do projeto disponível e legível
- Artefatos de referência acessíveis ao executor
- Critério de sucesso entendido antes da execução
Post-Conditions:
- Output publicado em formato auditável
- Próximo passo explícito ou handoff emitido
- Decisões relevantes registradas no artefato final
Performance:
- Execução em uma sessão sem falha silenciosa
- Thresholds e veto conditions respeitados
- Resultado acionável para o próximo executor
Completion Criteria:
- Executor único definido
- Inputs e outputs explícitos
- Critério final verificável no artefato entregue

---


## Overview

```
  Automation Needs
       |
       v
  +---------------------+
  | 1. Identify Hook     |
  |    Needs             |
  +---------------------+
       |
       v
  +---------------------+
  | 2. Choose Hook Type  |
  |    & Category        |
  +---------------------+
       |
       v
  +---------------------+
  | 3. Select Events     |
  +---------------------+
       |
       v
  +---------------------+
  | 4. Design Hook Logic |
  +---------------------+
       |
       v
  +---------------------+
  | 5. Implement & Test  |
  +---------------------+
       |
       v
  +---------------------+
  | 6. Integration       |
  |    Verification      |
  +---------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| hook_purpose | string | User | Yes | Description of what the hook should automate |
| trigger_event | string | User | No | Specific event if known (e.g., "PreToolUse", "Stop") |
| project_path | string | User or cwd | Yes | Project directory for context |

---

## Preconditions

- Claude Code installed and functional
- Understanding of the project's workflow and pain points
- `.claude/` directory exists (or will be created)

---

## Execution Phases

### Phase 1: Identify Hook Needs

Analyze the requested automation against hook capabilities:

1. **Categorize the need**:
   - Security: blocking dangerous commands, validating inputs
   - Automation: auto-formatting, auto-logging, state management
   - Quality: linting on save, test on commit, review on complete
   - Observability: timing, token tracking, cost monitoring
   - Context management: compaction, memory updates, state persistence

2. **Validate hook-suitability**: some needs are better served by:
   - Skills/commands (user-triggered, not event-triggered)
   - Rules (static instructions, not runtime logic)
   - CI/CD (post-merge, not during session)

If the need is not hook-suitable, recommend the appropriate alternative.

### Phase 2: Choose Hook Type and Category

Claude Code hooks operate in four handler types:

| Type | Language | Best For | Constraint |
|------|----------|----------|------------|
| command | Any (bash, node, python) | Validation, file operations, API calls, complex logic | Must exit within timeout |
| prompt | N/A (returns text) | Injecting guidance into conversation | Output is added to assistant context |
| http | Remote service/webhook | Observability, external policy engines, AIOX Monitor | Network dependency; keep failures non-blocking unless critical |
| agent | Claude sub-agent | Multi-turn review, richer contextual judgment | Highest latency/cost; reserve for high-value reasoning |

**Hook categories by event:**

| Event | When Fires | Common Uses |
|-------|-----------|-------------|
| PreToolUse | Before any tool call | Block dangerous commands, validate inputs, stop foreground `sleep`/poll loops |
| PostToolUse | After tool completes | Log results, capture metrics, trigger follow-ups |
| Stop | Session ends normally | Save state, generate summary, update memory |
| SubagentStop | Subagent completes | Collect results, merge outputs |
| PreCompact | Before context compaction | Preserve critical state |
| Notification | User receives notification | Custom notification routing |
| UserPromptSubmit | User sends message | Input preprocessing, routing |
| PermissionRequest | When a permission dialog would appear | Auto-allow or auto-deny promptable operations |
| ConfigChange | When settings surfaces mutate during session | Audit config drift, block unauthorized settings rewrites |

Select the appropriate event based on when the automation should trigger.

### Phase 3: Select Appropriate Events

For the identified need, determine:

1. **Primary event**: the main trigger for the hook
2. **Guard conditions**: when the hook should fire vs skip
   - Tool name filter (for PreToolUse/PostToolUse)
   - Session state checks
   - File pattern matching
   - Runtime caveats by event:
     - `PermissionRequest` does not fire in headless mode and is bypassed by `dontAsk`
     - `ConfigChange` covers settings surfaces, not `.mcp.json`/`managed-mcp.json`
3. **Timeout**: maximum execution time (default 10s for command hooks)
4. **Error behavior**: what happens if the hook fails
   - `continue`: session proceeds (recommended for non-critical hooks)
   - `stop`: session halts (use only for security-critical hooks)

### Phase 4: Design Hook Logic

Design the hook implementation:

1. **Input contract**: what data the hook receives from Claude Code
   ```json
   {
     "tool_name": "Bash",
     "tool_input": { "command": "rm -rf /tmp/test" },
     "session_id": "abc123"
   }
   ```

2. **Processing logic**: what the hook does with the input
   - Parse input data
   - Apply business logic (validation, transformation, logging)
   - Produce output (block/allow, log entry, context injection)

3. **Output contract**: what the hook returns
   - For PreToolUse: `{ "decision": "allow" }` or `{ "decision": "block", "reason": "..." }`
   - For PermissionRequest: allow/deny resolution only; this event cannot introduce a third "block" state
   - For prompt hooks: plain text to inject into conversation
   - For command hooks: exit code 0 (success) or non-zero (failure)

4. **Performance requirements**:
   - Hook must complete within timeout
   - No blocking I/O without timeouts
   - Graceful degradation on failure

5. **State management** (if needed):
   - Where to store state (file, environment variable)
   - State format (JSON, YAML)
   - Concurrency considerations

### Phase 5: Implement and Test

Create the hook implementation:

1. **Write the hook script** following the designed logic
   - Use the language best suited to the task (Node.js for JSON, Bash for simple commands)
   - Include error handling and timeout protection
   - Add inline comments explaining the logic

2. **Register the hook** in settings.json:
   ```json
   {
     "hooks": {
       "{EventName}": [
         {
            "type": "command",
            "command": "node .claude/hooks/{hook-name}.js",
            "timeout": 10000
          }
        ]
      }
    }
   ```

   Use `http` or `agent` handlers when the design actually benefits from remote dispatch or multi-turn reasoning; do not default to them for simple shell checks.

3. **Test the hook**:
   - Manual trigger with sample input
   - Edge cases: missing fields, malformed input, timeout simulation
   - Verify exit code and output format

### Phase 6: Integration Verification

Verify the hook works within the full Claude Code session:

1. Start a Claude Code session
2. Trigger the event that fires the hook
3. Verify the hook executed (check logs, output, or behavior)
4. Confirm no interference with other hooks or normal workflow
5. Check performance: hook completes well within timeout

---

## Output Format

```markdown
## Hook Design Specification

**Purpose:** {hook_purpose}
**Event:** {event_name}
**Type:** {command|prompt}
**Language:** {node|bash|python}

### Design

**Trigger:** {when the hook fires}
**Guard:** {conditions to skip execution}
**Timeout:** {N}ms

### Input/Output Contract

**Input:**
```json
{input_schema}
```

**Output:**
```json
{output_schema}
```

### Implementation

**File:** `.claude/hooks/{hook-name}.js`
**Registration:**
```json
{settings_json_snippet}
```

### Test Plan

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Normal case | {input} | {output} |
| Edge case | {input} | {output} |
| Error case | {input} | {output} |

### Performance

- Expected execution time: {N}ms
- Timeout configured: {N}ms
- Failure mode: {continue|stop}
```

---

## Veto Conditions

- **NEVER** design hooks that block all tool use without escape hatch
- **NEVER** design hooks that send data to external services without user consent
- **NEVER** set hook timeout above 30 seconds (causes session lag)
- **NEVER** use `stop` error behavior for non-security hooks
- **NEVER** design hooks that modify source code -- hooks observe and gate, they do not author

---

## Completion Criteria

- [ ] Hook need identified and validated as hook-suitable
- [ ] Hook type and event selected with rationale
- [ ] Input/output contract defined
- [ ] Hook logic designed with error handling
- [ ] Implementation created and registered in settings.json
- [ ] Test plan documented with at least 3 scenarios
- [ ] Integration verified in a real session
