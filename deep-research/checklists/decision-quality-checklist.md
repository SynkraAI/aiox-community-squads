# Decision Quality Checklist

```yaml
checklist:
  id: dr-decision-quality
  version: 1.0.0
  created: 2026-03-06
  purpose: "Validate Kahneman cognitive bias audit meets decision hygiene standards"
  mode: blocking
  used_by: kahneman
  when: "After Kahneman completes decision quality audit (QG-004 - FINAL gate)"
```

---

## 12-Question Bias Checklist

```yaml
bias_checklist_checks:
  - id: KBC-001
    check: "All 12 questions evaluated"
    type: blocking
    validation: "checklist_score is set (0-12), each question answered yes/no"
    questions:
      1: "Is there reason to suspect motivated reasoning?"
      2: "Have the people making the recommendation fallen in love with it?"
      3: "Were there dissenting opinions? Were they explored?"
      4: "Could the diagnosis be overly influenced by an analogy to a memorable past case?"
      5: "Are credible alternatives included?"
      6: "If you had to make this decision again in a year, what information would you want?"
      7: "Do you know where the numbers came from? Can you get the same result with different models?"
      8: "Is the assessment overly optimistic? Can you get a pre-mortem?"
      9: "Is the base case overly cautious?"
      10: "Is the worst case bad enough?"
      11: "Is the recommending team overly attached to past decisions?"
      12: "Would the recommending team make the same recommendation in a year?"

  - id: KBC-002
    check: "Score >= 8/12 for PASS, 6-7 for CONDITIONAL, < 6 for FAIL"
    type: blocking
    validation: "threshold applied and result determined"
```

---

## Cognitive Bias Scan

```yaml
cognitive_bias_checks:
  - id: COG-001
    check: "Anchoring bias assessed"
    type: blocking
    validation: "checked if initial information disproportionately influenced conclusions"

  - id: COG-002
    check: "Availability bias assessed"
    type: blocking
    validation: "checked if vivid/recent examples overweighted vs base rates"

  - id: COG-003
    check: "Confirmation bias assessed"
    type: blocking
    validation: "checked if evidence was sought to confirm rather than falsify"

  - id: COG-004
    check: "Overconfidence assessed"
    type: blocking
    validation: "checked if confidence levels match evidence strength"

  - id: COG-005
    check: "Sunk cost fallacy assessed"
    type: recommended
    validation: "checked if past investment is influencing forward-looking recommendation"

  - id: COG-006
    check: "Each detected bias has mitigation recommendation"
    type: blocking
    validation: "bias_entry has mitigation field with actionable suggestion"

  - id: COG-007
    check: "No recommendation flagged with >= 2 cognitive biases without revision"
    type: blocking
    validation: "if bias_count >= 2 on a recommendation: revision_required = true"
```

---

## System 1/System 2 Analysis

```yaml
system_checks:
  - id: SYS-001
    check: "System 1 triggers identified (intuitive, fast, emotional)"
    type: blocking
    validation: "system1_triggers list is present (may be empty if none detected)"

  - id: SYS-002
    check: "System 2 engagement verified for high-stakes recommendations"
    type: blocking
    validation: "high-stakes recommendations have deliberate analysis, not just gut reaction"

  - id: SYS-003
    check: "Framing effects checked"
    type: blocking
    validation: "checked if different framing of same data would change the recommendation"
```

---

## Pre-Mortem

```yaml
premortem_checks:
  - id: PM-001
    check: "Pre-mortem conducted on major recommendations"
    type: blocking
    validation: "failure_scenarios list has >= 2 entries for primary recommendation"

  - id: PM-002
    check: "Each failure scenario has probability estimate"
    type: recommended
    validation: "probability in [high, medium, low] per scenario"

  - id: PM-003
    check: "Mitigation strategies proposed for top failure modes"
    type: blocking
    validation: "top 2 failure scenarios have mitigation_strategy defined"
```

---

## Decision Hygiene

```yaml
hygiene_checks:
  - id: HYG-001
    check: "Confidence calibration assessed"
    type: blocking
    validation: "calibration in [overconfident, calibrated, underconfident]"

  - id: HYG-002
    check: "Alternative framings presented"
    type: blocking
    validation: "at least 1 alternative framing of the core recommendation"

  - id: HYG-003
    check: "Noise assessment (would different analysts reach same conclusion?)"
    type: recommended
    validation: "variability_risk in [low, medium, high]"
```

---

## Final Verdict

```yaml
verdict_checks:
  - id: FV-001
    check: "Decision quality verdict issued"
    type: blocking
    validation: "verdict in [PASS, CONDITIONAL, FAIL]"

  - id: FV-002
    check: "Bias warnings attached to final report"
    type: blocking
    validation: "bias_warnings list included in handoff to dr-orchestrator"

  - id: FV-003
    check: "If FAIL: mandatory revision before synthesis"
    type: blocking
    validation: "if verdict == FAIL: revision_required = true, synthesis blocked"
```

---

## Scoring

| Score | Result | Action |
|-------|--------|--------|
| 100% Blocking (20/20) + 12-Question >= 8 | PASS | Proceed to synthesis |
| >= 85% Blocking (17+/20) + 12-Question >= 6 | CONDITIONAL | Proceed with bias warnings |
| < 85% Blocking OR 12-Question < 6 | FAIL | Mandate revision |

**Total Checks:** 20 blocking + 3 recommended = 23

---

**Version:** 1.0.0
**Standard:** Deep Research Decision Quality (QG-004)
