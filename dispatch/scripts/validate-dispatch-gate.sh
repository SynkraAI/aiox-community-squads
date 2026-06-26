#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# Dispatch Squad — Veto Condition Checker
# Law #1: CODE > LLM — Validation checks are deterministic.
# Pattern: Pedro Valério validation script pattern
#
# Usage:
#   bash squads/dispatch/scripts/validate-dispatch-gate.sh <task-prompt-file>
#   bash squads/dispatch/scripts/validate-dispatch-gate.sh <task-prompt-file> --verbose
#
# Exit codes:
#   0 = ALL VETO CONDITIONS PASSED
#   1 = DISPATCH BLOCKED (N conditions triggered)
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

ERRORS=0
WARNINGS=0
VERBOSE=0
TASK_FILE="${1:-}"

if [ -z "$TASK_FILE" ]; then
    echo "Usage: validate-dispatch-gate.sh <task-prompt-file> [--verbose]"
    exit 2
fi

if [ "${2:-}" = "--verbose" ]; then
    VERBOSE=1
fi

if [ ! -f "$TASK_FILE" ]; then
    echo "❌ File not found: $TASK_FILE"
    exit 2
fi

CONTENT=$(cat "$TASK_FILE")

# ═══════════════════════════════════════════════════════════════════════════════
# V1.1: Task has output path
# ═══════════════════════════════════════════════════════════════════════════════
if ! echo "$CONTENT" | grep -qi "output\|save to\|output_path"; then
    echo "❌ V1.1: VETO — No output path defined"
    ERRORS=$((ERRORS+1))
elif [ "$VERBOSE" -eq 1 ]; then
    echo "✅ V1.1: Output path defined"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# V1.2: No subjective acceptance criteria
# ═══════════════════════════════════════════════════════════════════════════════
if echo "$CONTENT" | grep -qiE "(good quality|well-written|appropriate tone|nice |adequate )"; then
    echo "❌ V1.2: VETO — Subjective acceptance criterion found"
    ERRORS=$((ERRORS+1))
elif [ "$VERBOSE" -eq 1 ]; then
    echo "✅ V1.2: No subjective criteria"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# V1.3: No placeholders
# ═══════════════════════════════════════════════════════════════════════════════
if echo "$CONTENT" | grep -qE "\[XXX\]|\{TODO\}|TBD|\[PLACEHOLDER\]|\[INSERT\]"; then
    echo "❌ V1.3: VETO — Placeholder text found"
    ERRORS=$((ERRORS+1))
elif [ "$VERBOSE" -eq 1 ]; then
    echo "✅ V1.3: No placeholders"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# V1.5: Template present for Haiku outputs > 50 lines
# (Check if prompt mentions template/structure for large outputs)
# ═══════════════════════════════════════════════════════════════════════════════
if echo "$CONTENT" | grep -qi "haiku"; then
    if ! echo "$CONTENT" | grep -qiE "(template|structure|format|##)"; then
        echo "⚠️  V1.5: WARNING — Haiku prompt may lack template for structured output"
        WARNINGS=$((WARNINGS+1))
    elif [ "$VERBOSE" -eq 1 ]; then
        echo "✅ V1.5: Template/structure present for Haiku"
    fi
fi

# ═══════════════════════════════════════════════════════════════════════════════
# V1.9: No vague verbs without specifics
# ═══════════════════════════════════════════════════════════════════════════════
if echo "$CONTENT" | grep -qiE "(^|\s)(improve|optimize|enhance|better|fix up)(\s|$)" | grep -qviE "(\d|specific|exactly|measure)"; then
    echo "⚠️  V1.9: WARNING — Vague verb detected (improve/optimize/enhance)"
    WARNINGS=$((WARNINGS+1))
elif [ "$VERBOSE" -eq 1 ]; then
    echo "✅ V1.9: No vague verbs"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# Check: DO NOT ask questions instruction present
# ═══════════════════════════════════════════════════════════════════════════════
if ! echo "$CONTENT" | grep -qi "DO NOT ask"; then
    echo "⚠️  HAIKU RULE: Missing 'DO NOT ask questions' instruction"
    WARNINGS=$((WARNINGS+1))
elif [ "$VERBOSE" -eq 1 ]; then
    echo "✅ HAIKU: 'DO NOT ask questions' present"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# RESULT
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "=== ALL VETO CONDITIONS PASSED ($WARNINGS warnings) ==="
    exit 0
else
    echo "=== DISPATCH BLOCKED: $ERRORS veto conditions triggered ($WARNINGS warnings) ==="
    exit 1
fi
