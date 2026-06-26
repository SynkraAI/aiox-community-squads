# Task: Diagnose CFA Level

## Metadata
```yaml
task_id: HZ-AUTO-DIAGNOSE_CFA_LEVEL
agent: hormozi-models
type: execution
complexity: medium
estimated_time: 30-45min
source: remediation-generated
```

## SINKRA Contract

Domain: Strategic
atomic_layer: Atom
Input:
- business_context
- offer_context
Output:
- diagnose_cfa_level_artifact
pre_condition:
- contexto de negócio e objetivo da tarefa definidos
post_condition:
- artefato principal pronto para handoff e revisão
performance:
- entregar artefato estruturado com trilha explícita de decisão
Completion Criteria:
- artefato principal gerado
- cálculo, framework ou recomendação explicitados
- pronto para handoff do próximo executor


## Purpose

Identify which of the 3 CFA levels the business is currently at.

## Source

$100M Money Models - Module 6: CFA (Client Finance Acquisition)

---

## The 3 Levels (from training)

### Level 1: Basic Profitability

```
Lifetime Gross Profit > CAC
```

- **Minimum:** 3:1 LTGP:CAC ratio
- **Result:** You have a business that can make money and grow (minimum requirement)

### Level 2: Self-Funding Growth

```
30-Day Gross Profit > CAC
```

- **Result:** You never spend your own money to grow
- **Why 30 days:** Every business can borrow money at **zero interest** for 30 days via credit cards or credit lines. The financial system gives you 30 days interest-free.

The process:
1. Use credit card to acquire customers
2. Make back more than CAC in gross profit within 30 days
3. Pay off credit card
4. Recycle the cash → get another customer
5. Never carry debt while growing

**Limitation:** You're still capped by your credit limit.

### Level 3: Unlimited Scale (The Goal)

```
30-Day Gross Profit > 2x CAC
```

- **Result:** Never being limited by money at all
- **Mechanism:** Exponential doubling — by customer, not by month

How it works:
1. Spend $X to get 1 customer
2. Customer generates $2X+ in gross profit within 30 days
3. $X pays back original spend, other $X buys another customer
4. That customer also generates $2X → pays back + buys another
5. Exponential growth

---

## Diagnostic Questions

Ask the business owner:

1. **What is your CAC?** (fully loaded — ads, payroll, software, commissions)
2. **What is your 30-day gross profit per customer?** (revenue minus COGS in first 30 days)
3. **What is your LTGP per customer?** (total gross profit over customer lifetime)

---

## Output Calculations

### Step 1: Calculate LTGP:CAC Ratio

```
LTGP:CAC Ratio = Lifetime Gross Profit / CAC
```

- If ratio < 3:1 → **NOT at Level 1** (business fundamentally broken)
- If ratio >= 3:1 → **At Level 1** (basic profitability achieved)

### Step 2: Determine Level 2 Status

```
Compare: 30-Day GP vs CAC
```

- If 30-Day GP < CAC → **NOT at Level 2** (still spending own money to grow)
- If 30-Day GP >= CAC → **At Level 2** (self-funding growth)

### Step 3: Determine Level 3 Status

```
Compare: 30-Day GP vs 2x CAC
```

- If 30-Day GP < 2x CAC → **NOT at Level 3**
- If 30-Day GP >= 2x CAC → **At Level 3** (unlimited scale potential)

---

## Compounding Table (from MM_6)

If at Level 3 and reinvesting all 30-day advertising profits:

| Month | New Customers | Total Customers |
|-------|---------------|-----------------|
| 1     | 1             | 1               |
| 2     | 2             | 3               |
| 3     | 4             | 7               |
| 4     | 8             | 15              |
| 5     | 16            | 31              |
| 6     | 32            | 63              |
| 7     | 64            | 127             |
| 8     | 128           | 255             |
| 9     | 256           | 511             |
| 10    | 512           | 1,023           |
| 11    | 1,024         | 2,047           |
| 12    | 2,048         | 4,095           |

> "Within a year of reinvesting your advertising profits, advertising is obviously no longer a bottleneck."

---

## Key Insight

> "Somebody who has fewer skills needs more money. Somebody who has more skills needs less money."

The goal of all money models is achieving Level 2 (minimum) or Level 3 (ideal).

---

## Diagnosis Report Template

```markdown
## CFA Level Diagnosis

**Business:** [Name]
**Date:** [Date]

### Inputs
- CAC: $[X]
- 30-Day GP: $[Y]
- LTGP: $[Z]

### Calculations
- LTGP:CAC Ratio: [Z/X]:1
- 30-Day GP vs CAC: [Y] vs [X] → [Y >= X ? "PASS" : "FAIL"]
- 30-Day GP vs 2x CAC: [Y] vs [2X] → [Y >= 2X ? "PASS" : "FAIL"]

### Current Level: [1/2/3]

### Bottleneck
- [If Level 1: "Need to improve offer or reduce CAC"]
- [If Level 2: "Credit limit and operational capacity"]
- [If Level 3: "Only operational constraints — scale unlocked"]

### Next Action
[Specific recommendation to reach next level]
```

---

## Related

- `calculate-ppd.md` - Calculate Payback Period
- Case Library: CASE-014 (Gym Launch Metrics — 12:1 30-day, 96:1 12-month)
- Mental Model: MM_009 (CFA Levels)
