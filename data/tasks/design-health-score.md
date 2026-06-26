# Design Health Score - Customer Health Measurement System

## Purpose

Systematic Health Score design task based on Nick Mehta's Customer Success methodology (Gainsight DEAR framework) and Peter Fader's Customer Centricity principles. This task transforms subjective customer assessment ("I think they're doing well") into quantified, actionable health measurement ("score 73, trending down 8 points, intervention needed on support component").

Health Score is not just a metric - it's the foundation of proactive customer success. When designed correctly, it becomes an early warning system that enables intervention before customers reach the point of no return.

## Workspace Output Contract

- Preflight: `*workspace-preflight` + `*workspace-context {slug}`
- Output canônico (template-first): `workspace/businesses/{slug}/analytics/health-score-report.yaml`
- Output custom (ad-hoc): `docs/data/{slug}/health-score-design-{date}.md`
- Regra: escrita canônica só se existir template em `workspace/_templates/analytics/health-score-report.yaml`

## When to Use

- **BUILDING FROM SCRATCH** - Creating first Health Score system
- **REDESIGNING** - Current health score doesn't predict outcomes
- **SCALING CS** - Moving from gut-feel to systematic measurement
- **POST-CHURN ANALYSIS** - After unexpected churn, building prevention system
- **STRATEGIC INITIATIVE** - Executive mandate for customer health visibility

## Primary Agents

```yaml
primary_agent: nick-mehta
supporting_agents:
  - peter-fader  # CLV context for prioritization

nick_mehta_perspective:
  core_belief: "Health Score is not about predicting churn - it's about identifying opportunities for proactive intervention before it's too late."

  key_insight: |
    "A customer's health is not a single number. It's a composite of deployment,
    engagement, adoption, and ROI. Miss any dimension and you miss the full picture."

peter_fader_perspective:
  core_belief: "Not all unhealthy customers are worth saving equally. Combine health with CLV for prioritization."

  key_insight: |
    "Health Score tells you WHO needs attention. CLV tells you HOW MUCH
    attention they deserve. Without both, you're flying blind."
```

---

## Metadata

```yaml
task:
  name: Design Health Score
  id: design-health-score
  version: "1.0"
  category: customer_success
  difficulty: intermediate
  estimated_effort: 2-4 weeks initial design, ongoing refinement

  primary_agents:
    - nick-mehta

  supporting_agents:
    - peter-fader

  outputs:
    - health_score_components
    - weight_calculation_methodology
    - threshold_definitions
    - alert_trigger_system
    - dashboard_recommendations
    - implementation_guide

  prerequisites:
    - customer_data_access
    - usage_analytics
    - support_ticket_history
    - nps_csat_data
    - stakeholder_alignment

  related_tasks:
    - predict-churn.md
    - calculate-clv.md
    - segment-rfm.md

  related_checklists:
    - health-score-checklist.md
    - customer-360-checklist.md
```

---

## Nick Mehta's Health Score Philosophy

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    MEHTA'S HEALTH SCORE PRINCIPLES                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. HEALTH IS MULTI-DIMENSIONAL                                             │
│     "A customer can have great usage but terrible support experience.       │
│      Single metrics lie. Composite scores reveal truth."                    │
│                                                                              │
│  2. LEADING INDICATORS > LAGGING OUTCOMES                                   │
│     "By the time a customer asks to cancel, they've been unhealthy         │
│      for months. Health Score should catch the disease early."              │
│                                                                              │
│  3. ACTIONABLE > ACCURATE                                                   │
│     "A slightly less accurate score that drives action beats a              │
│      perfect score that sits in a dashboard."                               │
│                                                                              │
│  4. COMPONENTS SHOULD MAP TO INTERVENTIONS                                  │
│     "Every health dimension should have a playbook. If you can't           │
│      act on it, don't measure it."                                          │
│                                                                              │
│  5. CALIBRATE WITH OUTCOMES                                                 │
│     "A Health Score that doesn't correlate with retention and expansion    │
│      is just expensive reporting. Validate relentlessly."                   │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 0: PRE-FLIGHT CHECK

### Required Data Sources

Before designing Health Score, verify access to these data sources:

```yaml
data_requirements:

  product_usage_data:
    required: true
    importance: "Critical - most predictive component"
    sources:
      - application_analytics
      - feature_usage_logs
      - login_history
      - session_duration
      - api_calls
    minimum_history: 6 months
    ideal_history: 12+ months
    refresh_frequency: daily

  support_data:
    required: true
    importance: "High - leading indicator of friction"
    sources:
      - support_tickets
      - ticket_sentiment
      - resolution_times
      - escalations
      - csat_per_ticket
    minimum_history: 6 months
    refresh_frequency: real-time preferred

  engagement_data:
    required: true
    importance: "Medium - interest signals"
    sources:
      - email_opens_clicks
      - event_attendance
      - webinar_participation
      - community_activity
      - marketing_touchpoints
    minimum_history: 6 months
    refresh_frequency: weekly

  relationship_data:
    required: true
    importance: "High - satisfaction proxy"
    sources:
      - nps_scores
      - csat_surveys
      - executive_sponsor_info
      - champion_status
      - qbr_attendance
    minimum_history: 12 months
    refresh_frequency: monthly

  growth_signals:
    required: false_but_valuable
    importance: "Medium - expansion indicators"
    sources:
      - upsell_conversations
      - expansion_requests
      - referrals_given
      - case_study_willingness
      - advocacy_participation
    minimum_history: 12 months
    refresh_frequency: monthly

  financial_data:
    required: false_but_valuable
    importance: "Low-Medium - billing health"
    sources:
      - payment_history
      - contract_value
      - seat_utilization
      - discount_dependency
    minimum_history: 12 months
    refresh_frequency: monthly
```

### Pre-Flight Checklist

```
□ Objective Clarity
  □ What outcome should Health Score predict? (churn, expansion, NPS?)
  □ What is the prediction window? (30, 60, 90 days?)
  □ How will "healthy" vs "at risk" be defined?
  □ What is the current baseline churn rate?

□ Data Assessment
  □ Product usage data accessible and complete?
  □ Support ticket data available with sentiment?
  □ NPS/CSAT collected with adequate coverage?
  □ Historical churn data for validation?

□ Stakeholder Alignment
  □ CS leadership aligned on approach?
  □ Product team consulted on usage metrics?
  □ Finance aligned on churn definition?
  □ Executive sponsor identified?

□ Resource Commitment
  □ Technical resources to build/maintain?
  □ CS team capacity to act on alerts?
  □ Analytics support for ongoing refinement?
```

---

## PHASE 1: HEALTH SCORE COMPONENTS

### Step 1.1: The DEAR Framework (Gainsight Foundation)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          DEAR FRAMEWORK                                      │
│                    (Gainsight Customer Success)                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  D - DEPLOYMENT (Implementation)                                            │
│  ─────────────────────────────────────                                      │
│  Question: "Has the customer implemented the product?"                       │
│                                                                              │
│  Signals:                                                                    │
│  • Setup/onboarding completion rate                                          │
│  • Core feature activation                                                   │
│  • Integration completion                                                    │
│  • Data migration status                                                     │
│  • Go-live achieved                                                          │
│                                                                              │
│  Mehta: "If they haven't deployed, nothing else matters.                    │
│          This is the foundation of all value."                              │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  E - ENGAGEMENT (Activity)                                                  │
│  ─────────────────────────────────────                                      │
│  Question: "Is the customer actively using the product?"                     │
│                                                                              │
│  Signals:                                                                    │
│  • Login frequency (DAU, WAU, MAU)                                          │
│  • Session duration                                                          │
│  • Actions per session                                                       │
│  • User adoption % (active/total)                                           │
│  • Time in product                                                           │
│                                                                              │
│  Mehta: "Usage is the pulse. A customer who doesn't log in                  │
│          is a customer who doesn't see value."                              │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  A - ADOPTION (Depth)                                                       │
│  ─────────────────────────────────────                                      │
│  Question: "Is the customer using advanced features?"                        │
│                                                                              │
│  Signals:                                                                    │
│  • Feature adoption % (features used/available)                             │
│  • Advanced feature usage                                                    │
│  • Workflow complexity                                                       │
│  • Module expansion                                                          │
│  • API usage depth                                                           │
│                                                                              │
│  Mehta: "Breadth of usage creates stickiness.                               │
│          The more features used, the harder to leave."                      │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  R - ROI (Value Realization)                                                │
│  ─────────────────────────────────────                                      │
│  Question: "Does the customer perceive value?"                               │
│                                                                              │
│  Signals:                                                                    │
│  • NPS score                                                                 │
│  • CSAT survey results                                                       │
│  • Value statements/testimonials                                             │
│  • Reference willingness                                                     │
│  • Renewal intent (if asked)                                                 │
│                                                                              │
│  Mehta: "Perception is reality. If they don't FEEL value,                   │
│          all the usage metrics in the world won't save them."               │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 1.2: Extended Component Categories

Beyond DEAR, include these additional dimensions:

```yaml
extended_components:

  support_health:
    category: "Support Experience"
    importance: "High - friction indicator"
    signals:
      - ticket_volume:
          metric: "Tickets per month"
          healthy: "<2"
          warning: "2-5"
          critical: ">5"
          scoring: "Lower is better"

      - ticket_sentiment:
          metric: "Sentiment score (1-10)"
          healthy: ">7"
          warning: "5-7"
          critical: "<5"
          scoring: "Higher is better"

      - open_tickets:
          metric: "Currently open tickets"
          healthy: "0-1"
          warning: "2-3"
          critical: ">3"
          scoring: "Lower is better"

      - critical_tickets:
          metric: "Critical/urgent tickets open"
          healthy: "0"
          warning: "1"
          critical: ">1"
          scoring: "Lower is better"

      - resolution_time:
          metric: "Avg days to resolution"
          healthy: "<2"
          warning: "2-5"
          critical: ">5"
          scoring: "Lower is better"

      - escalations:
          metric: "Escalations in 90 days"
          healthy: "0"
          warning: "1"
          critical: ">1"
          scoring: "Lower is better"

  relationship_health:
    category: "Relationship Strength"
    importance: "High - human element"
    signals:
      - nps_score:
          metric: "NPS score"
          healthy: ">8 (Promoter)"
          warning: "7-8 (Passive)"
          critical: "<7 (Detractor)"
          scoring: "Higher is better"

      - executive_access:
          metric: "Exec engagement in 90 days"
          healthy: "Yes"
          warning: "Attempted"
          critical: "No access"
          scoring: "Binary with levels"

      - champion_strength:
          metric: "Champion engaged?"
          healthy: "Active champion"
          warning: "Lukewarm"
          critical: "No champion or left"
          scoring: "Categorical"

      - stakeholder_depth:
          metric: "Number of engaged contacts"
          healthy: ">3"
          warning: "2-3"
          critical: "1"
          scoring: "Higher is better"

      - qbr_attendance:
          metric: "Attended last QBR?"
          healthy: "Yes, participated"
          warning: "Attended passively"
          critical: "No-show or declined"
          scoring: "Categorical"

      - responsiveness:
          metric: "Response to outreach"
          healthy: "Within 48 hrs"
          warning: "Within 1 week"
          critical: "No response"
          scoring: "Categorical"

  growth_signals:
    category: "Expansion Indicators"
    importance: "Medium - positive health"
    signals:
      - expansion_interest:
          metric: "Expressed interest in upsell?"
          healthy: "Active discussion"
          warning: "Receptive"
          critical: "No interest or downgrade"
          scoring: "Categorical"

      - referral_activity:
          metric: "Made referrals?"
          healthy: ">1 referral"
          warning: "Willing but none"
          critical: "Declined"
          scoring: "Categorical"

      - advocacy_participation:
          metric: "Case study, review, reference?"
          healthy: "Participated"
          warning: "Willing"
          critical: "Declined"
          scoring: "Categorical"

      - contract_trajectory:
          metric: "Contract value trend"
          healthy: "Growing"
          warning: "Flat"
          critical: "Declining"
          scoring: "Categorical"

  financial_health:
    category: "Billing & Contract"
    importance: "Low-Medium"
    signals:
      - payment_status:
          metric: "Payment timeliness"
          healthy: "Always on time"
          warning: "1 late payment"
          critical: "2+ late or failed"
          scoring: "Categorical"

      - seat_utilization:
          metric: "Active users / paid seats"
          healthy: ">75%"
          warning: "50-75%"
          critical: "<50%"
          scoring: "Higher is better"

      - discount_dependency:
          metric: "Renewal with discount?"
          healthy: "No discount needed"
          warning: "Minor discount"
          critical: "Heavy discount or threat"
          scoring: "Categorical"
```

### Step 1.3: Component Selection Framework

```
COMPONENT SELECTION DECISION TREE:

For each potential component, ask:

1. DATA AVAILABILITY
   "Can we measure this reliably?"
   □ Yes → Continue
   □ No → Exclude (data first)

2. VARIANCE
   "Does this metric vary across customers?"
   □ Yes → Continue
   □ No → Exclude (constant = useless)

3. BUSINESS RATIONALE
   "Do stakeholders agree this matters?"
   □ Yes → Continue
   □ No → Validate or exclude

4. ACTIONABILITY
   "Can CS team act if this component is low?"
   □ Yes → Include
   □ No → Consider excluding (can't fix = why measure?)

5. CORRELATION (if historical data exists)
   "Does this correlate with churn/expansion?"
   □ Yes, significantly → Definitely include
   □ Weak correlation → Include with caution
   □ No correlation → Exclude

MINIMUM VIABLE HEALTH SCORE:
- At least 1 component from EACH DEAR category
- Support health (leading indicator)
- Total: 5-8 components minimum
```

### Step 1.4: Component Documentation Template

```yaml
component_documentation_template:

  component_name: "[Name]"
  category: "[DEAR letter or Extended category]"

  definition:
    description: "[What this measures]"
    business_rationale: "[Why it matters for health]"

  data:
    source_system: "[Where data comes from]"
    metric_formula: "[Exact calculation]"
    refresh_frequency: "[Real-time | Daily | Weekly | Monthly]"
    data_quality_score: "[1-10, with notes]"
    missing_data_handling: "[How to handle gaps]"

  scoring:
    scale: "[0-100 | 0-10 | Categorical]"
    healthy_threshold: "[Value or range]"
    warning_threshold: "[Value or range]"
    critical_threshold: "[Value or range]"
    scoring_direction: "[Higher is better | Lower is better]"

  action:
    when_low: "[What intervention?]"
    owner: "[Who acts?]"
    playbook_link: "[Reference to playbook]"

  validation:
    correlation_with_churn: "[r value if known]"
    lead_time: "[Days before outcome]"
    false_positive_rate: "[If known]"
```

---

## PHASE 2: WEIGHT CALCULATION METHODOLOGY

### Step 2.1: Weighting Approaches

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      WEIGHT CALCULATION APPROACHES                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  APPROACH 1: EXPERT-BASED (Quick Start)                                     │
│  ────────────────────────────────────────                                   │
│  Best for: First implementation, limited historical data                    │
│                                                                              │
│  Process:                                                                    │
│  1. Gather 3-5 stakeholders (CS, Product, Exec)                            │
│  2. Each ranks components by importance (1-10)                              │
│  3. Calculate average rankings                                              │
│  4. Convert to weights summing to 100%                                      │
│  5. Document rationale for each weight                                      │
│                                                                              │
│  Pros: Fast, incorporates domain expertise                                  │
│  Cons: May not match actual outcome correlation                            │
│                                                                              │
│  ────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  APPROACH 2: DATA-DRIVEN (Accurate)                                        │
│  ────────────────────────────────────────                                   │
│  Best for: 100+ churn events, data science capability                       │
│                                                                              │
│  Process:                                                                    │
│  1. Collect historical component values for churned customers               │
│  2. Run logistic regression: Churn ~ Component1 + Component2 + ...          │
│  3. Extract feature importance / coefficients                               │
│  4. Normalize to weights summing to 100%                                    │
│  5. Validate on holdout set                                                 │
│                                                                              │
│  Pros: Objectively reflects outcome correlation                            │
│  Cons: Requires historical data, data science skills                        │
│                                                                              │
│  ────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  APPROACH 3: HYBRID (Recommended)                                           │
│  ────────────────────────────────────────                                   │
│  Best for: Most organizations                                               │
│                                                                              │
│  Process:                                                                    │
│  1. Start with expert-based weights                                         │
│  2. Calculate correlation for each component                                │
│  3. Adjust expert weights based on correlation                              │
│  4. Repeat quarterly as more data accumulates                               │
│                                                                              │
│  Pros: Starts fast, improves with data                                     │
│  Cons: More complex to maintain                                             │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 2.2: Expert-Based Weight Collection

```yaml
expert_weighting_process:

  step_1_preparation:
    participants:
      - role: "CS Leader"
        perspective: "Day-to-day customer interaction"
      - role: "Product Leader"
        perspective: "Usage and adoption patterns"
      - role: "Executive"
        perspective: "Strategic customer value"
      - role: "Data/Analytics"
        perspective: "What data shows"

    materials_needed:
      - "List of proposed components with definitions"
      - "Current churn data (if available)"
      - "Customer examples (healthy, churned)"

  step_2_individual_ranking:
    instruction: |
      "Rank each component from 1-10 based on how strongly you believe
       it predicts customer health and future retention."

    ranking_scale:
      10: "Critical - single most important factor"
      7-9: "Very important - major health indicator"
      4-6: "Moderately important - contributes to picture"
      1-3: "Minor importance - nice to have"

  step_3_consolidation:
    process:
      - "Calculate average ranking per component"
      - "Discuss outliers (>2 point spread)"
      - "Reach consensus or document dissent"
      - "Convert to percentages (normalize to 100%)"

  step_4_documentation:
    template: |
      Component: [Name]
      Expert Rankings: [List]
      Average: [X.X]
      Consensus Weight: [X%]
      Rationale: [Why this weight]
```

### Step 2.3: Data-Driven Weight Calculation

```python
# Logistic Regression for Weight Calculation
# (Pseudocode for data science team)

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

def calculate_data_driven_weights(customer_data):
    """
    Calculate component weights based on churn correlation.

    customer_data: DataFrame with columns:
      - churned: 0/1 target variable
      - component_1, component_2, ... : normalized component scores
    """

    # Separate features and target
    X = customer_data[['deployment_score', 'engagement_score',
                       'adoption_score', 'roi_score',
                       'support_score', 'relationship_score']]
    y = customer_data['churned']

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit logistic regression
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y)

    # Extract feature importance (absolute coefficients)
    importance = np.abs(model.coef_[0])

    # Normalize to weights summing to 100%
    weights = (importance / importance.sum()) * 100

    # Create weight dictionary
    weight_dict = dict(zip(X.columns, weights))

    return weight_dict

# Example output:
# {
#   'deployment_score': 12.5,
#   'engagement_score': 28.3,
#   'adoption_score': 18.7,
#   'roi_score': 15.2,
#   'support_score': 15.8,
#   'relationship_score': 9.5
# }
```

### Step 2.4: Weight Guidelines (Benchmarks)

```yaml
typical_weight_ranges:

  deployment:
    range: "5-15%"
    rationale: "Important early, less so after go-live"
    adjust_higher_if: "High implementation complexity"
    adjust_lower_if: "Simple onboarding"

  engagement:
    range: "25-35%"
    rationale: "Most directly observable health signal"
    adjust_higher_if: "Product is daily-use"
    adjust_lower_if: "Product is periodic-use (monthly billing)"

  adoption:
    range: "15-25%"
    rationale: "Depth creates stickiness"
    adjust_higher_if: "Multi-feature platform"
    adjust_lower_if: "Single-purpose tool"

  roi:
    range: "10-20%"
    rationale: "Perception matters, but harder to measure"
    adjust_higher_if: "Strong NPS program"
    adjust_lower_if: "Limited survey data"

  support:
    range: "15-25%"
    rationale: "Leading indicator of friction"
    adjust_higher_if: "Complex product, high support dependency"
    adjust_lower_if: "Self-serve product"

  relationship:
    range: "10-20%"
    rationale: "Human element matters for enterprise"
    adjust_higher_if: "Enterprise / high-touch model"
    adjust_lower_if: "SMB / tech-touch model"

  growth_signals:
    range: "5-10%"
    rationale: "Positive indicator but not core health"
    adjust_higher_if: "Land-and-expand model"
    adjust_lower_if: "Fixed-scope contracts"

  financial:
    range: "5-10%"
    rationale: "Hygiene factor"
    adjust_higher_if: "High payment failure rate"
    adjust_lower_if: "Stable billing"
```

### Step 2.5: Weight Validation Checklist

```
WEIGHT VALIDATION CHECKLIST:

□ Mathematical Checks
  □ All weights sum to exactly 100%?
  □ No single component > 40%? (avoid over-dependence)
  □ All included components >= 5%? (if included, should matter)

□ Business Logic Checks
  □ Highest-weighted components align with business priorities?
  □ Weights make intuitive sense to CS team?
  □ No component weight conflicts with known customer patterns?

□ Data Validation (if available)
  □ Higher-weighted components have higher correlation with churn?
  □ Back-tested on historical churns?
  □ Sensitivity analysis performed?

□ Documentation
  □ Rationale documented for each weight?
  □ Dissenting opinions recorded?
  □ Review schedule established?
```

---

## PHASE 3: THRESHOLD DEFINITIONS

### Step 3.1: Health Categories

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      HEALTH SCORE CATEGORIES                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HEALTHY (Green) - Score 70-100                                             │
│  ─────────────────────────────────────                                      │
│  Meaning: Customer is thriving                                              │
│  Signals: High usage, good support, positive sentiment                      │
│  Risk Level: Low churn risk                                                 │
│  Action: Maintain relationship, pursue upsell/advocacy                      │
│  Typical Distribution: 50-65% of customers                                  │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  AT RISK (Yellow/Orange) - Score 40-69                                      │
│  ─────────────────────────────────────                                      │
│  Meaning: Customer showing warning signs                                    │
│  Signals: Declining usage, support issues, lukewarm sentiment               │
│  Risk Level: Moderate churn risk                                            │
│  Action: Proactive intervention required                                    │
│  Typical Distribution: 25-35% of customers                                  │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  CRITICAL (Red) - Score 0-39                                                │
│  ─────────────────────────────────────                                      │
│  Meaning: Customer in danger                                                │
│  Signals: No usage, unresolved issues, negative sentiment                   │
│  Risk Level: High churn risk                                                │
│  Action: Immediate rescue intervention                                      │
│  Typical Distribution: 10-20% of customers                                  │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 3.2: Threshold Setting Process

```yaml
threshold_setting:

  initial_thresholds:
    healthy: "70-100"
    at_risk: "40-69"
    critical: "0-39"
    note: "Standard starting point, adjust based on distribution"

  validation_process:

    step_1_calculate_distribution:
      action: "Apply thresholds to current customer base"
      check: "Is distribution reasonable?"
      expected:
        healthy: "50-65%"
        at_risk: "25-35%"
        critical: "10-20%"
      if_too_many_critical: "Raise critical threshold"
      if_too_few_critical: "Lower critical threshold"

    step_2_check_differentiation:
      action: "Calculate outcome rate per category"
      check: "Do categories have different outcomes?"
      example:
        healthy_churn_rate: "5%"
        at_risk_churn_rate: "15%"
        critical_churn_rate: "40%"
      if_similar_rates: "Thresholds not differentiating, adjust"

    step_3_check_actionability:
      action: "Calculate counts per category"
      check: "Can CS team handle volume?"
      example:
        critical_count: 50
        cs_capacity_weekly: 20
        weeks_to_address: 2.5
      if_overwhelming: "Raise threshold or prioritize by CLV"

    step_4_add_hysteresis:
      purpose: "Prevent flip-flop between categories"
      band_size: "5 points"
      example:
        healthy_to_at_risk: "Score must drop to 65 (70-5)"
        at_risk_to_healthy: "Score must rise to 75 (70+5)"
```

### Step 3.3: Sub-Thresholds (Advanced)

```yaml
sub_thresholds:

  healthy:
    advocacy_ready:
      range: "85-100"
      description: "Best customers, candidates for case study, referral"
      action: "Pursue advocacy programs"
    healthy_standard:
      range: "70-84"
      description: "Good customers, standard engagement"
      action: "Maintain relationship, identify upsell"

  at_risk:
    moderate_risk:
      range: "55-69"
      description: "Early warning signs, proactive intervention"
      action: "CSM outreach, value reinforcement"
    elevated_risk:
      range: "40-54"
      description: "Multiple concerning signals"
      action: "Manager involvement, rescue plan"

  critical:
    critical_standard:
      range: "25-39"
      description: "High risk, needs immediate attention"
      action: "Executive escalation, save offer"
    critical_severe:
      range: "0-24"
      description: "Very high risk, likely churning"
      action: "All-hands rescue, prepare for exit"
```

### Step 3.4: Threshold Documentation

```yaml
threshold_documentation_template:

  version: "[X.X]"
  effective_date: "[YYYY-MM-DD]"

  thresholds:
    healthy:
      range: "[X-100]"
      distribution_target: "[X-Y%]"
      expected_churn_rate: "[X%]"
      action: "[Standard engagement]"

    at_risk:
      range: "[X-Y]"
      distribution_target: "[X-Y%]"
      expected_churn_rate: "[X%]"
      action: "[Proactive intervention]"

    critical:
      range: "[0-X]"
      distribution_target: "[X-Y%]"
      expected_churn_rate: "[X%]"
      action: "[Immediate rescue]"

  hysteresis:
    enabled: "[Yes/No]"
    band_size: "[X points]"

  validation:
    last_validated: "[Date]"
    churn_correlation: "[r value]"
    differentiation_test: "[p-value]"

  review_schedule: "Quarterly"
  owner: "[Name/Role]"
```

---

## PHASE 4: ALERT TRIGGERS

### Step 4.1: Alert Types

```yaml
alert_types:

  threshold_breach:
    trigger: "Score crosses category threshold"
    examples:
      - "Customer drops from Healthy (72) to At Risk (68)"
      - "Customer rises from At Risk (65) to Healthy (75)"
    urgency: "Medium (downward), Low (upward)"
    notification: "CSM email, dashboard flag"

  rapid_decline:
    trigger: "Score drops >X points in Y days"
    configuration:
      decline_threshold: 10  # points
      time_window: 14  # days
    examples:
      - "Score dropped from 75 to 62 in 10 days"
    urgency: "High"
    notification: "CSM + Manager email, Slack"

  component_spike:
    trigger: "Individual component hits critical level"
    configuration:
      components_to_watch:
        - "support_health"
        - "nps_score"
        - "champion_status"
    examples:
      - "Support health dropped to Critical (3+ open tickets)"
      - "NPS went from Promoter to Detractor"
    urgency: "High"
    notification: "Immediate CSM alert"

  trend_alert:
    trigger: "Consistent decline over multiple periods"
    configuration:
      decline_periods: 4  # consecutive weeks
      decline_threshold: 2  # points per week
    examples:
      - "Score declined 4 weeks in a row: 78→75→72→69"
    urgency: "Medium"
    notification: "Weekly digest flag"

  renewal_proximity:
    trigger: "Critical/At Risk + renewal within X days"
    configuration:
      at_risk_renewal_window: 90  # days
      critical_renewal_window: 120  # days
    examples:
      - "Critical customer with renewal in 45 days"
    urgency: "High"
    notification: "CSM + Manager + Exec"

  champion_loss:
    trigger: "Champion leaves company or goes silent"
    examples:
      - "Primary champion no longer at company (LinkedIn update)"
      - "Champion hasn't responded in 30+ days"
    urgency: "High"
    notification: "CSM + AE immediately"
```

### Step 4.2: Alert Configuration Template

```yaml
alert_configuration:

  alert_name: "[Name]"
  alert_type: "[threshold_breach | rapid_decline | component_spike | trend | renewal | champion]"

  trigger:
    condition: "[Exact trigger condition]"
    threshold_value: "[Value or formula]"
    lookback_period: "[Time window if applicable]"

  notification:
    channels:
      - email: "[recipients]"
      - slack: "[channel]"
      - in_app: "[true/false]"
      - sms: "[for critical only]"
    frequency: "[Immediate | Daily digest | Weekly]"

  response:
    sla: "[Time to first response]"
    owner: "[Role responsible]"
    escalation:
      if_no_response: "[Next escalation level]"
      escalation_window: "[Hours/days]"

  metadata:
    created_date: "[Date]"
    last_modified: "[Date]"
    enabled: "[true/false]"
```

### Step 4.3: Alert Volume Management

```
ALERT VOLUME GUIDELINES:

Mehta's Rule: "More than 5 critical alerts per CSM per day = alert fatigue.
              Quality of response matters more than quantity of alerts."

VOLUME TARGETS:
┌─────────────────┬────────────────┬─────────────────────────────┐
│ Alert Priority  │ Target Volume  │ If Exceeded                 │
├─────────────────┼────────────────┼─────────────────────────────┤
│ Critical        │ <5/day per CSM │ Raise threshold or filter   │
│ High            │ <10/day per CSM│ Consolidate similar alerts  │
│ Medium          │ <20/day per CSM│ Move to digest              │
│ Low             │ Unlimited      │ Dashboard only              │
└─────────────────┴────────────────┴─────────────────────────────┘

VOLUME REDUCTION TACTICS:
- Prioritize by CLV (high-value first)
- Consolidate related alerts
- Increase time windows for trend alerts
- Filter noise (one-time blips)
- Digest low-priority into weekly summary
```

### Step 4.4: Alert Templates

```yaml
alert_templates:

  threshold_breach_down:
    subject: "[HEALTH ALERT] {customer_name} moved to {new_category}"
    body: |
      Customer: {customer_name}
      Previous Health: {old_score} ({old_category})
      Current Health: {new_score} ({new_category})

      Key Factors:
      - {component_1}: {component_1_status}
      - {component_2}: {component_2_status}
      - {component_3}: {component_3_status}

      Contract: {contract_value} ARR, renews {renewal_date}

      Recommended Action: {recommended_action}

      [View Customer] [Start Intervention]

  rapid_decline:
    subject: "[URGENT] {customer_name} health declined {points} points"
    body: |
      ⚠️ RAPID DECLINE DETECTED

      Customer: {customer_name}
      Health Score: {current_score} (was {previous_score})
      Decline: -{points} points in {days} days

      What Changed:
      {change_summary}

      Contract: {contract_value} ARR
      Renewal: {days_to_renewal} days

      Immediate Action Required: {action}

      [View Details] [Contact Customer]

  component_critical:
    subject: "[ALERT] {customer_name}: {component_name} is Critical"
    body: |
      Critical Component Alert

      Customer: {customer_name}
      Component: {component_name}
      Status: CRITICAL
      Value: {component_value}

      What This Means: {component_explanation}

      Recommended Action: {action}

      Overall Health: {health_score} ({category})

      [View Customer] [Open Ticket] [Schedule Call]
```

---

## PHASE 5: DASHBOARD RECOMMENDATIONS

### Step 5.1: Executive Dashboard

```yaml
executive_dashboard:

  purpose: "High-level health visibility for leadership"
  refresh: "Real-time or daily"

  sections:

    health_distribution:
      visualization: "Pie or donut chart"
      metrics:
        - healthy_count
        - healthy_percentage
        - at_risk_count
        - at_risk_percentage
        - critical_count
        - critical_percentage
      comparison: "vs last month"

    arr_at_risk:
      visualization: "Single number with trend"
      metric: "Sum of ARR for At Risk + Critical customers"
      comparison: "vs last month"
      drill_down: "Click to see customer list"

    health_trend:
      visualization: "Line chart"
      metrics:
        - average_health_score
        - critical_percentage
      time_period: "6 months trailing"

    top_critical_accounts:
      visualization: "Table"
      columns:
        - customer_name
        - arr
        - health_score
        - days_to_renewal
        - primary_risk_factor
      limit: 10
      sort_by: "ARR descending"

    interventions_summary:
      visualization: "Progress bars"
      metrics:
        - active_interventions
        - completed_this_month
        - save_rate
```

### Step 5.2: CS Manager Dashboard

```yaml
cs_manager_dashboard:

  purpose: "Team performance and account oversight"
  refresh: "Real-time"

  sections:

    team_book_health:
      visualization: "Stacked bar by CSM"
      metrics:
        - accounts_per_csm
        - healthy_per_csm
        - at_risk_per_csm
        - critical_per_csm

    critical_accounts:
      visualization: "Table with actions"
      columns:
        - customer_name
        - csm_owner
        - health_score
        - primary_risk_factor
        - arr
        - days_to_renewal
        - intervention_status
      filters:
        - by_csm
        - by_risk_level
        - by_renewal_date

    alerts_queue:
      visualization: "List with priority"
      content:
        - unacknowledged_alerts
        - alerts_past_sla
      actions:
        - assign
        - acknowledge
        - escalate

    intervention_pipeline:
      visualization: "Funnel or pipeline"
      stages:
        - identified
        - in_progress
        - resolved
        - saved
        - churned

    score_changes:
      visualization: "List with sparklines"
      content: "Biggest score changes this week"
      direction: "Both up and down"
```

### Step 5.3: CSM Individual Dashboard

```yaml
csm_dashboard:

  purpose: "Day-to-day account management"
  refresh: "Real-time"

  sections:

    my_book_summary:
      visualization: "Cards"
      metrics:
        - total_accounts
        - healthy_accounts
        - at_risk_accounts
        - critical_accounts
        - avg_health_score

    today_priorities:
      visualization: "List"
      content:
        - critical_accounts
        - alerts_to_address
        - interventions_due
        - renewals_this_week
      sort_by: "Priority (CLV × Risk)"

    account_list:
      visualization: "Table"
      columns:
        - customer_name
        - health_score
        - health_trend
        - days_to_renewal
        - last_contact
        - next_action
      filters:
        - by_health_category
        - by_renewal_proximity
      sort_options:
        - health_score_asc
        - health_score_desc
        - renewal_date

    my_metrics:
      visualization: "KPIs"
      metrics:
        - retention_rate
        - save_rate
        - avg_health_score
        - response_time_to_alerts
```

### Step 5.4: Account Detail View

```yaml
account_detail:

  purpose: "Deep dive into individual customer"

  sections:

    health_summary:
      content:
        - overall_score
        - category
        - trend_arrow
        - score_history_sparkline

    component_breakdown:
      visualization: "Radar chart or bars"
      content:
        - each_component_score
        - each_component_trend
        - contribution_to_overall
      click_action: "Drill into component"

    score_history:
      visualization: "Line chart"
      time_period: "12 months"
      annotations: "Key events (support escalation, QBR, etc.)"

    risk_factors:
      visualization: "List with severity"
      content:
        - current_risk_factors
        - recent_changes

    intervention_history:
      visualization: "Timeline"
      content:
        - past_interventions
        - outcomes

    relationship_map:
      visualization: "Org chart or network"
      content:
        - key_contacts
        - engagement_level
        - champion_status

    contract_info:
      content:
        - arr
        - contract_start
        - renewal_date
        - products_owned
        - expansion_opportunity
```

---

## PHASE 6: IMPLEMENTATION GUIDE

### Step 6.1: Implementation Phases

```yaml
implementation_phases:

  phase_1_foundation:
    duration: "2-3 weeks"
    activities:
      - "Finalize component selection"
      - "Document component definitions"
      - "Validate data availability"
      - "Build data pipelines"
      - "Create initial scoring model"
    deliverables:
      - "Component specification document"
      - "Data pipeline architecture"
      - "Initial score calculation"
    gate: "Scores calculated for all customers"

  phase_2_calibration:
    duration: "2-3 weeks"
    activities:
      - "Set initial weights"
      - "Calibrate thresholds"
      - "Validate against historical churn"
      - "Adjust based on validation"
      - "Define alert rules"
    deliverables:
      - "Weight justification document"
      - "Threshold specification"
      - "Alert configuration"
    gate: "Score correlates with churn (r > 0.5)"

  phase_3_dashboard:
    duration: "1-2 weeks"
    activities:
      - "Build executive dashboard"
      - "Build CS team dashboards"
      - "Build account detail views"
      - "Configure alerts"
      - "Test notification delivery"
    deliverables:
      - "Live dashboards"
      - "Working alerts"
    gate: "Dashboards reviewed by stakeholders"

  phase_4_rollout:
    duration: "2-4 weeks"
    activities:
      - "Train CS team"
      - "Create intervention playbooks"
      - "Soft launch to pilot CSMs"
      - "Gather feedback"
      - "Iterate based on feedback"
      - "Full rollout"
    deliverables:
      - "Training materials"
      - "Playbook documentation"
      - "Feedback summary"
    gate: "CS team actively using score"

  phase_5_optimization:
    duration: "Ongoing"
    activities:
      - "Monitor correlation with outcomes"
      - "Track intervention effectiveness"
      - "Refine weights quarterly"
      - "Add/remove components as needed"
      - "Expand automation"
    deliverables:
      - "Monthly health score report"
      - "Quarterly calibration updates"
```

### Step 6.2: Rollout Checklist

```
PRE-LAUNCH CHECKLIST:

□ Technical Readiness
  □ Data pipelines running reliably?
  □ Scores calculating correctly?
  □ Dashboards loading quickly?
  □ Alerts delivering as configured?
  □ Historical data populated?

□ Business Readiness
  □ Thresholds approved by leadership?
  □ Weights documented and justified?
  □ Intervention playbooks created?
  □ CS team trained?
  □ Escalation paths defined?

□ Process Readiness
  □ Alert response SLAs defined?
  □ Feedback mechanism established?
  □ Recalibration schedule set?
  □ Owner/maintainer assigned?

□ Communication
  □ Executive briefing complete?
  □ CS team announcement ready?
  □ Documentation accessible?
  □ FAQ prepared?

LAUNCH SEQUENCE:
1. Final stakeholder review
2. Soft launch to pilot group (1 week)
3. Incorporate feedback
4. Full CS team rollout
5. Cross-functional announcement
6. Begin monitoring
```

### Step 6.3: Training Guide

```yaml
training_curriculum:

  module_1_what_is_health_score:
    duration: "30 minutes"
    content:
      - "Purpose and philosophy"
      - "How score is calculated"
      - "What each component measures"
      - "How to interpret the score"
    hands_on: "Review 3 customer examples"

  module_2_using_dashboards:
    duration: "45 minutes"
    content:
      - "Dashboard navigation"
      - "Filtering and sorting"
      - "Understanding visualizations"
      - "Exporting data"
    hands_on: "Find your critical accounts, filter by renewal"

  module_3_responding_to_alerts:
    duration: "30 minutes"
    content:
      - "Alert types and urgency"
      - "Response expectations"
      - "Escalation procedures"
      - "Documenting actions"
    hands_on: "Process sample alerts"

  module_4_intervention_playbooks:
    duration: "1 hour"
    content:
      - "Playbook for each health category"
      - "Component-specific interventions"
      - "Save offer guidelines"
      - "Documentation requirements"
    hands_on: "Role-play intervention scenario"

  module_5_providing_feedback:
    duration: "15 minutes"
    content:
      - "When to flag false positives"
      - "How to request weight changes"
      - "Continuous improvement process"
```

---

## Elicitation Questions

Before beginning Health Score design, gather this information:

### Business Context

```yaml
elicitation:

  objective:
    - "What is the primary purpose of Health Score?"
    - "What outcome should it predict? (churn, expansion, NPS?)"
    - "What is your current churn rate?"
    - "What is the typical time from 'at risk' to 'churn'?"

  customer_model:
    - "How many customers do you have?"
    - "What is your engagement model? (high-touch, tech-touch, pooled)"
    - "How are customers segmented today?"
    - "Do different segments need different health models?"

  current_state:
    - "Do you have any health scoring today?"
    - "How do CSMs currently identify at-risk customers?"
    - "What data do you currently track?"
    - "What tools do you use? (CS platform, CRM, analytics)"

  historical_data:
    - "Can you identify customers who churned in last 12 months?"
    - "Do you have data from before they churned?"
    - "Have you done exit interviews or post-churn analysis?"
```

### Data Availability

```yaml
data_questions:

  usage_data:
    - "What usage data do you have? (logins, actions, features)"
    - "At what granularity? (daily, weekly)"
    - "How far back does data go?"

  support_data:
    - "Where are tickets tracked?"
    - "Can you measure ticket sentiment?"
    - "Is ticket data linked to customer records?"

  engagement_data:
    - "Do you track email engagement?"
    - "Is event/webinar attendance logged?"
    - "Is community participation tracked?"

  relationship_data:
    - "How often is NPS collected?"
    - "Do you track executive engagement?"
    - "Is champion information maintained?"
```

### Team Readiness

```yaml
team_questions:

  cs_team:
    - "How large is your CS team?"
    - "How many accounts per CSM?"
    - "What is current capacity for proactive outreach?"

  processes:
    - "Do you have intervention playbooks today?"
    - "What is the escalation path for at-risk accounts?"
    - "How are save decisions made?"

  tools:
    - "What CS platform do you use?"
    - "Where should health score live?"
    - "What dashboarding tool do you have?"
```

---

## Output Format

### Health Score Design Deliverable

```yaml
deliverable_structure:

  1_component_specification:
    contents:
      - "Component definitions"
      - "Data sources"
      - "Scoring methodology per component"
    format: "YAML or structured document"

  2_weight_calculation:
    contents:
      - "Weight per component"
      - "Methodology used"
      - "Justification for each weight"
    format: "Table with rationale"

  3_threshold_definitions:
    contents:
      - "Category thresholds"
      - "Distribution expectations"
      - "Hysteresis bands"
    format: "Specification document"

  4_alert_configuration:
    contents:
      - "Alert types"
      - "Trigger conditions"
      - "Notification rules"
    format: "Configuration table"

  5_dashboard_specifications:
    contents:
      - "Executive dashboard design"
      - "CS team dashboard design"
      - "Account detail view"
    format: "Wireframes or specifications"

  6_implementation_plan:
    contents:
      - "Phase timeline"
      - "Resource requirements"
      - "Rollout checklist"
    format: "Project plan"
```

### Sample Output Summary

```
HEALTH SCORE DESIGN SUMMARY
═══════════════════════════════════

Components (6 total):
┌────────────────────────────────────────────────────────────────┐
│ Component        │ Weight │ Data Source          │ Refresh    │
├────────────────────────────────────────────────────────────────┤
│ Engagement       │ 30%    │ Product analytics    │ Daily      │
│ Adoption         │ 20%    │ Feature usage logs   │ Weekly     │
│ Support Health   │ 20%    │ Zendesk              │ Real-time  │
│ ROI (NPS)        │ 15%    │ Survey tool          │ Monthly    │
│ Relationship     │ 10%    │ CRM                  │ Weekly     │
│ Growth Signals   │ 5%     │ CRM                  │ Monthly    │
└────────────────────────────────────────────────────────────────┘

Thresholds:
- Healthy: 70-100 (target 55% of customers)
- At Risk: 40-69 (target 30% of customers)
- Critical: 0-39 (target 15% of customers)

Alerts Configured:
- Threshold breach (up and down)
- Rapid decline (>10 points in 14 days)
- Critical component (support, NPS)
- Renewal proximity (90 days + at risk)

Dashboards:
- Executive: Health distribution, ARR at risk, trends
- Manager: Team book, critical accounts, intervention pipeline
- CSM: My book, priorities, account details

Validation Results:
- Correlation with churn: r = 0.62 (p < 0.01)
- Healthy churn rate: 4%
- At Risk churn rate: 18%
- Critical churn rate: 42%
- Lift vs baseline: 3.2x

Implementation Timeline:
- Phase 1 (Foundation): 3 weeks
- Phase 2 (Calibration): 2 weeks
- Phase 3 (Dashboards): 2 weeks
- Phase 4 (Rollout): 3 weeks
- Total: 10 weeks to full deployment
```

---

## Examples

### Example 1: B2B SaaS Health Score

```
CONTEXT:
- B2B SaaS, 500 customers
- High-touch CS model (50-80 accounts per CSM)
- ARR range: $20K - $500K
- Current churn: 12% annual

COMPONENT DESIGN:

┌──────────────────────────────────────────────────────────────────────────┐
│ Component          │ Weight │ Metric                     │ Thresholds   │
├──────────────────────────────────────────────────────────────────────────┤
│ DEPLOYMENT         │ 10%    │ Onboarding completion %    │ >90% healthy │
│ ENGAGEMENT (WAU)   │ 25%    │ Weekly active users %      │ >60% healthy │
│ ADOPTION           │ 20%    │ Feature adoption %         │ >40% healthy │
│ SUPPORT HEALTH     │ 20%    │ Composite (tickets, CSAT)  │ Score >70    │
│ NPS                │ 15%    │ NPS score                  │ >8 healthy   │
│ RELATIONSHIP       │ 10%    │ Exec engagement + champion │ Score >70    │
└──────────────────────────────────────────────────────────────────────────┘

THRESHOLDS:
- Healthy: 70-100 → 52% of customers
- At Risk: 45-69 → 33% of customers
- Critical: 0-44 → 15% of customers

VALIDATION:
- Churn rate in Critical: 38%
- Churn rate in At Risk: 14%
- Churn rate in Healthy: 3%
- Correlation (r): 0.58

ALERT CONFIGURATION:
- Critical threshold breach: Immediate notification
- At Risk + renewal <90 days: Manager + CSM alert
- Rapid decline (>15 pts/month): Escalation alert
```

### Example 2: Tech-Touch / Pooled CS Model

```
CONTEXT:
- SMB segment, 3,000 customers
- Pooled CS model (500+ accounts per CSM)
- ARR range: $1K - $10K
- High volume = automation required

COMPONENT DESIGN:

┌──────────────────────────────────────────────────────────────────────────┐
│ Component          │ Weight │ Metric                     │ Automation   │
├──────────────────────────────────────────────────────────────────────────┤
│ ENGAGEMENT (DAU)   │ 35%    │ Daily active users %       │ Auto-calc    │
│ ADOPTION           │ 25%    │ Key feature adoption       │ Auto-calc    │
│ SUPPORT HEALTH     │ 25%    │ Ticket volume + sentiment  │ Auto-calc    │
│ PAYMENT HEALTH     │ 15%    │ Payment success rate       │ Auto-calc    │
└──────────────────────────────────────────────────────────────────────────┘

Note: No manual relationship component (too many customers)

THRESHOLDS:
- Healthy: 65-100 → 60% of customers
- At Risk: 35-64 → 28% of customers
- Critical: 0-34 → 12% of customers

AUTOMATION:
- Critical customers: Auto-email + in-app message
- At Risk: Automated nurture sequence
- Healthy: Self-serve resources

HUMAN ESCALATION:
- Critical >$5K ARR: Human outreach
- Critical + 3 support tickets: Human escalation
```

### Example 3: Enterprise Account Health

```
CONTEXT:
- Enterprise segment, 75 customers
- Strategic CS model (10-15 accounts per CSM)
- ARR range: $200K - $5M
- Cannot afford to lose any account

COMPONENT DESIGN:

┌──────────────────────────────────────────────────────────────────────────┐
│ Component            │ Weight │ Metric                   │ Owner        │
├──────────────────────────────────────────────────────────────────────────┤
│ EXECUTIVE ENGAGEMENT │ 20%    │ Exec meeting frequency   │ CSM + Exec   │
│ VALUE REALIZATION    │ 20%    │ ROI documented + NPS     │ CSM          │
│ ENGAGEMENT           │ 15%    │ WAU + session depth      │ Auto         │
│ ADOPTION             │ 15%    │ Module + user expansion  │ Auto         │
│ RELATIONSHIP DEPTH   │ 15%    │ Multi-threading score    │ CSM          │
│ STRATEGIC ALIGNMENT  │ 10%    │ Roadmap alignment        │ CSM + Product│
│ SUPPORT HEALTH       │ 5%     │ Escalation count         │ Support      │
└──────────────────────────────────────────────────────────────────────────┘

THRESHOLDS:
- Healthy: 75-100 → 50% of customers
- At Risk: 50-74 → 35% of customers
- Critical: 0-49 → 15% of customers

Note: Higher healthy threshold for enterprise

SPECIAL RULES:
- ANY executive loss: Auto-critical flag
- Missing QBR: -10 points
- No exec contact 6 months: -15 points
```

---

## Integration

### Related Tasks

- **predict-churn.md** - Use health score as input to churn prediction
- **calculate-clv.md** - Prioritize health interventions by CLV
- **segment-rfm.md** - Behavioral segmentation complements health

### Related Agents

- **nick-mehta** - Primary methodology owner for Health Score
- **peter-fader** - CLV-based prioritization for interventions

### Related Checklists

- **health-score-checklist.md** - Comprehensive validation checklist
- **customer-360-checklist.md** - Data foundation for health score

### Tool Integrations

```yaml
tool_integrations:

  cs_platforms:
    - gainsight: "Native health score support"
    - churnzero: "Real-time health scoring"
    - totango: "Health score modules"
    - vitally: "Automated health calculation"

  crm:
    - salesforce: "Custom object for health data"
    - hubspot: "Health score properties"

  analytics:
    - amplitude: "Usage data for engagement/adoption"
    - mixpanel: "Feature usage tracking"
    - heap: "Behavioral analytics"

  support:
    - zendesk: "Ticket data integration"
    - intercom: "Support + engagement data"
    - freshdesk: "Ticket health component"

  dashboarding:
    - looker: "Health score dashboards"
    - tableau: "Executive reporting"
    - metabase: "Team dashboards"
```

---

## Nick Mehta's Parting Wisdom

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    NICK MEHTA'S HEALTH SCORE PRINCIPLES                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  "Health Score is not a destination. It's a journey.                        │
│   The first version will be wrong. The tenth version will be better.       │
│   The key is to start measuring and keep improving."                        │
│                                                                              │
│  1. START SIMPLE                                                             │
│     "A 3-component health score that drives action beats a                  │
│      15-component score that sits in a dashboard."                          │
│                                                                              │
│  2. COMPONENT = ACTION                                                       │
│     "Every component should have an intervention. If you can't              │
│      act on it when it's low, don't measure it."                            │
│                                                                              │
│  3. VALIDATE RELENTLESSLY                                                    │
│     "A health score that doesn't correlate with outcomes is                 │
│      expensive noise. Test it against churn every quarter."                 │
│                                                                              │
│  4. HUMAN + MACHINE                                                          │
│     "The score tells you WHO needs attention. The CSM figures               │
│      out HOW to help. Don't automate judgment."                             │
│                                                                              │
│  5. CONTINUOUS IMPROVEMENT                                                   │
│     "Components change. Weights shift. Thresholds evolve.                   │
│      Schedule quarterly reviews and actually do them."                      │
│                                                                              │
│  FINAL THOUGHT:                                                              │
│  "Health Score is about creating time. Time to intervene,                   │
│   time to save, time to grow. A customer in red today can                   │
│   be green in 90 days if you act now."                                      │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Changelog

```yaml
changelog:
  - version: "1.0"
    date: "2026-01-23"
    author: "Data Intelligence Pack"
    changes:
      - "Initial task creation"
      - "Nick Mehta DEAR framework integrated"
      - "Weight calculation methodology (3 approaches)"
      - "Threshold definitions with validation"
      - "Alert trigger system"
      - "Dashboard recommendations (3 levels)"
      - "Implementation guide (5 phases)"
      - "3 examples (B2B SaaS, Tech-Touch, Enterprise)"
```

## Acceptance Criteria

- [ ] As fontes de dados obrigatórias e opcionais foram validadas antes do desenho do score.
- [ ] Cada componente do Health Score possui peso, racional e owner operacional explícitos.
- [ ] Thresholds e alertas foram definidos com playbooks compatíveis com cada faixa de risco.
- [ ] O output final deixa claro como validar o score contra churn, retenção ou expansão.
