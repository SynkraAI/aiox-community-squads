# Task: Structured Interview for Process Extraction

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `structured-interview` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `sop-extractor` |
| **Execution Type** | `Agent` |

## Metadata
```yaml
id: structured-interview
name: "Structured Interview for Process Extraction"
category: extraction
agent: sop-extractor
elicit: true
autonomous: false
description: "Conduct a 5-phase structured interview with a process performer to extract SOP-ready process knowledge. Based on Taiichi Ohno's Gemba methodology and ethnographic research techniques."
```

## Purpose

Extract complete process knowledge through a systematic interview with the person who actually performs the work. Unlike free-form description extraction (`extract-sop.md`), this task follows a rigid 5-phase protocol designed to capture the full process including tribal knowledge, edge cases, and undocumented workarounds.

This is the highest-fidelity extraction method when direct observation is not possible. Output confidence is typically 0.8 (`[REP]`) for practitioner-reported steps, with lower-confidence items flagged for follow-up according to `confidence-levels.yaml`.

## Prerequisites

- [ ] Process performer (subject matter expert) is available for interview
- [ ] Process name and general domain identified
- [ ] Interview will take 30-60 minutes of uninterrupted time
- [ ] `confidence-levels.yaml` accessible for scoring reference
- [ ] `extraction-output-template.md` accessible for output formatting

## Inputs

```yaml
inputs:
  process_name:
    type: string
    required: true
    description: "Name of the process to extract"

  interviewee_role:
    type: string
    required: true
    description: "Role/title of the person being interviewed"

  interview_context:
    type: string
    required: false
    description: "Any background context about the process or organization"
```

## Workflow / Steps

### Phase 1: Overview (5 minutes)

```
GOAL: Establish scope and context of the process

ASK (in order):
  1. "What is this process called? What does it accomplish?"
  2. "How often is it performed? Who performs it?"
  3. "What triggers this process to start?"
  4. "What does 'done' look like? How do you know it is complete?"

CAPTURE:
  - Process name, purpose, frequency, criticality
  - Trigger event or condition
  - Completion criteria
  - Initial actor inventory

CONFIDENCE: All answers = 0.8 (Reported by Practitioner)
```

### Phase 2: Step-by-Step Walkthrough (15-25 minutes)

```
GOAL: Capture the complete step sequence with tools and decisions

ASK (in order):
  1. "Walk me through the process step by step, starting from the trigger."
  2. "What tools or systems do you use at each step?"
  3. "Where do you make decisions? What determines which path you take?"
  4. "How long does each step typically take?"

TECHNIQUE:
  - Let the interviewee narrate without interruption first
  - Then go back step-by-step and ask for:
    * Exact actions performed
    * Tools/systems used
    * Inputs consumed and outputs produced
    * Expected result at each step
  - Number each step as captured

CAPTURE:
  - Numbered step sequence with actor, tool, and expected result
  - Decision points with conditions and branches
  - Duration estimates per step
  - Tool/system inventory

CONFIDENCE: Detailed steps with demonstration = 0.8, vague steps = 0.5

VETO: If interviewee cannot describe steps sequentially, STOP and
recommend direct observation (gemba walk) instead.
```

### Phase 3: Exception Hunting (10-15 minutes)

```
GOAL: Surface failure modes, edge cases, and tribal knowledge workarounds

ASK (in order):
  1. "What goes wrong most often? How do you handle it?"
  2. "What is the worst-case scenario? Has it ever happened?"
  3. "Are there steps that vary depending on the situation?"
  4. "What do you do when the system is down?"

TECHNIQUE:
  - Push for specifics: "Can you give me a recent example?"
  - For each exception: capture symptom, cause, workaround, frequency
  - Probe for undocumented workarounds: "Is there a trick that everyone knows?"

CAPTURE:
  - Exception catalog: trigger, frequency, workaround, severity
  - Edge cases and conditional branches
  - System failure workarounds
  - "Tribal tricks" not in any documentation

CONFIDENCE:
  - Specific examples with dates = 0.8
  - General statements without examples = 0.5
  - "I think this happens sometimes" = 0.3
```

### Phase 4: Tribal Knowledge Deep Dive (5-10 minutes)

```
GOAL: Capture knowledge that exists only in people's heads

ASK (in order):
  1. "What do new team members struggle with most?"
  2. "What is not written down anywhere but everyone knows?"
  3. "If you were out sick, what would your backup need to know?"
  4. "What has changed recently that old documentation does not reflect?"

TECHNIQUE:
  - These questions surface implicit knowledge
  - For each answer: ask "How would someone learn this without you?"
  - Mark all items as high-priority for documentation

CAPTURE:
  - Onboarding pain points (often = missing SOP content)
  - Unwritten rules and conventions
  - Backup/handoff gaps
  - Recently changed but undocumented steps

CONFIDENCE: Corroborated by multiple people = 0.8, single source = 0.5
```

### Phase 5: Validation Read-Back (5 minutes)

```
GOAL: Verify accuracy and completeness of captured information

ASK (in order):
  1. "Let me read back what I have -- does this match your experience?"
  2. "Is anything missing or incorrect?"
  3. "Who else should I talk to for a different perspective?"

TECHNIQUE:
  - Read back step sequence in order
  - Pause after each step for confirmation or correction
  - Note any corrections and update confidence accordingly

CAPTURE:
  - Corrections to any previously captured information
  - Additional sources recommended for cross-reference
  - Confirmation signature (verbal or written)

CONFIDENCE:
  - Confirmed steps = maintain or upgrade confidence
  - Corrected steps = maintain 0.8 (now more accurate)
  - "I'm not sure about that one" = downgrade to 0.5
```

### Phase 6: Output Generation

```
ACTION: Compile interview results into extraction output format

STEPS:
  1. Load extraction-output-template.md
  2. Fill all 10 sections from interview data
  3. Assign confidence scores per confidence-levels.yaml rules
  4. Flag all items below threshold (0.8) in Gaps section
  5. Document all sources in Provenance section
  6. Run extraction-completeness-checklist.md
  7. Determine handoff readiness

OUTPUT: Completed extraction package ready for handoff
```

## Output

```yaml
outputs:
  primary:
    format: "Extraction output following extraction-output-template.md"
    description: "Complete 10-section extraction package with confidence scores"

  secondary:
    - format: "Interview transcript summary"
      description: "Chronological record of questions asked and answers received"
```

## Acceptance Criteria

- [ ] All 5 interview phases executed in order
- [ ] Step sequence captured with at least 3 steps
- [ ] Each step has actor, tool, and expected result
- [ ] Confidence score assigned to every extracted element
- [ ] Exception/edge cases section populated (even if "none identified")
- [ ] Tribal knowledge section populated (even if "none identified")
- [ ] Read-back validation completed with interviewee
- [ ] Output formatted per extraction-output-template.md
- [ ] extraction-completeness-checklist.md executed

## Veto Conditions

- STOP if interviewee cannot describe the process sequentially (recommend observation)
- STOP if interviewee has never personally performed the process (find actual performer)
- STOP if process has more than 50 steps (split into sub-processes first)
- STOP if interviewee contradicts themselves on critical steps without resolution

## Handoff

- **On success:** Extraction package → @sop-creator (human SOP) or @sop-ml-architect (ML SOP)
- **On incomplete:** Flag gaps → recommend additional interview or observation pass
