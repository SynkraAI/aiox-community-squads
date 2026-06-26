# Task: Calculate Payback Period (PPD)

## Metadata
```yaml
task_id: HZ-AUTO-CALCULATE_PPD
agent: hormozi-models
type: execution
complexity: medium
estimated_time: 30-45min
source: remediation-generated
```

## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- business_context
- offer_context
Output:
- calculate_ppd_artifact
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

Calculate how long until gross profit exceeds CAC.

## Source

$100M Money Models - Module 5: Payback Period

---

## Definition (from training)

> **"Payback Period (PPD): How long it takes until gross profit is greater than CAC."**

In other words, how long to break even. Also known as "cash conversion cycle."

The shorter the payback period, the easier it is to scale advertising.

---

## Why It Matters

### Problem 1: Businesses take too long to break even

They have to manage cashflow by creating a "marketing budget" — which is a constraint that limits growth.

### Problem 2: Businesses feel guilty making multiple offers

They think they're bothering people. They are wrong.

> "The people who feel this way are poorer than they should be."

---

## The Hyper Buying Cycle

Buyers have **short windows of hyper buying** followed by dormancy. If you don't capitalize on the hyper buying cycle, someone else will.

**The Bike Story:** A friend decides to lose weight, remembers she likes riding bikes, buys a bike online. Within 24-48 hours she also buys:
- Helmet, shoes, pants, gloves, water bottles
- Signs up for a race

If the bike shop owner doesn't offer these items ("I don't want to seem pushy"), she buys them elsewhere. The money is spent either way.

> "There's a very big difference between hard selling and letting a customer know the offers you have available."

---

## Calculation Example (from MM_5)

**Inputs:**
- CAC: $160
- Monthly Revenue: $100
- Monthly COGS: $20
- Monthly GP: $80

| Month | Revenue | COGS | GP | Cumulative GP - CAC |
|-------|---------|------|----|---------------------|
| 1     | $100    | $20  | $80| $80 - $160 = **-$80** |
| 2     | $100    | $20  | $80| $160 - $160 = **$0** |

**Payback Period = 2 months**

---

## CRITICAL: Calculate Off GROSS PROFIT, Not Revenue

- **WRONG:** $160 CAC / $100 revenue = 1.6 months
- **RIGHT:** $160 CAC / $80 GP = 2 months

This is a common mistake that makes PPD look better than it actually is.

---

## The First-and-Last Trick (from MM_5)

To immediately shorten PPD: **charge first AND last month upfront.**

**Example revisited:**
- CAC: $160
- First + Last month = $200 revenue, $40 COGS = $160 GP on Day 1
- **Payback period drops from 2 months to Day 1**

The "last month" fee is all gross profit. Every 2 customers now funds a 3rd customer before recurring payments even hit.

### Other Fee Names That Accomplish the Same Thing

- Initiation fee
- Onboarding fee
- Enrollment fee
- Activation fee

---

## The 5 Upsell Timing Windows (from MM_5)

| # | When | Why It Works |
|---|------|--------------|
| 1 | **Immediately** (same conversation) | Works when solving problem A naturally creates problem B |
| 2 | **Next Step** (24-72 hours) | Works when you need to guide awareness to a new problem |
| 3 | **First Big Win** (milestone) | Fully solved problem opens a fully formed new problem |
| 4 | **Halfway Point** | Historically just works (no scientific explanation, but consistently effective) |
| 5 | **Last Chance** (exit interview) | Your final shot — if you're only upselling here, you've already lost |

**Key insight:** 4 out of 5 windows are **BEFORE the halfway point.**

> "I don't want to reopen something. I want to ride the buying cycle I'm already on."

---

## The Supplement Timing Story (from MM_5)

- Selling supplements immediately after gym membership sign-up **FAILED** — customer just scratched their weight loss itch
- Selling supplements at a "nutrition orientation" 48 hours later **WORKED** — walked through their food, created a NEW problem (nutritional gaps), then solved it with supplements

> "If I just had a big steak dinner and you say 'do you want another steak?' — my steak stomach is full. But I might have a dessert stomach that's open."

---

## Sell at the Point of Greatest Deprivation

> "You sell at the point of greatest deprivation, not at the point of greatest satisfaction."

---

## PPD Calculation Template

```markdown
## PPD Calculation

**Business:** [Name]
**Date:** [Date]

### Inputs
- CAC (fully loaded): $[X]
- Monthly Revenue per Customer: $[R]
- Monthly COGS per Customer: $[C]
- Monthly GP per Customer: $[R - C] = $[GP]

### Basic PPD
PPD = CAC / Monthly GP = $[X] / $[GP] = [N] months

### With First-and-Last Trick
- First + Last Revenue: $[2R]
- First + Last COGS: $[2C]
- Day 1 GP: $[2R - 2C]
- New PPD: [Day 1 GP >= CAC ? "Day 1" : "Calculate remaining"]

### Improvement Opportunity
- Current PPD: [N] months
- Target PPD: [30 days or less for CFA Level 2]
- Gap: [N - 1] months

### Recommended Actions
1. [Add first-and-last fee]
2. [Add upsell at timing window #[X]]
3. [Review 5 timing windows for opportunities]
```

---

## Related

- `diagnose-cfa-level.md` - Diagnose CFA Level
- Case Library: CASE-014 (Gym Launch Metrics)
- Mental Model: MM_009 (CFA Levels)
- Voice DNA: "Hyper Buying Cycle", "First-and-Last Trick", "Payback Period (PPD)"
