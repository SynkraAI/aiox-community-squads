# Run PMF Test - Sean Ellis Product-Market Fit Survey

## Purpose

Systematic Product-Market Fit (PMF) assessment using Sean Ellis's proven methodology. This task transforms the subjective question "Do we have PMF?" into a quantifiable, actionable metric based on the famous "Very Disappointed" survey question.

The Sean Ellis Test (also known as the PMF Survey) has become the gold standard for measuring product-market fit because it directly measures how essential your product has become to users. Unlike vanity metrics like signups or page views, this test measures the emotional connection users have with your product—the kind that drives retention, word-of-mouth, and sustainable growth.

## When to Use

- **PRE-LAUNCH** - Validating MVP before scaling marketing spend
- **POST-LAUNCH** - Measuring initial product-market fit
- **PIVOT DECISION** - Determining if current direction is working
- **FUNDRAISING** - Providing investors quantifiable PMF evidence
- **GROWTH PLANNING** - Knowing when to step on the gas vs. iterate
- **QUARTERLY HEALTH** - Regular PMF pulse check for established products

## Primary Agent

```yaml
primary_agent: sean-ellis
supporting_agents:
  - peter-fader  # Segment-level PMF analysis
  - nick-mehta   # Customer success correlation

sean_ellis_perspective:
  core_belief: "Product-Market Fit isn't binary. It's a spectrum, and the 40% threshold tells you where you stand."

  key_insight: |
    "When 40% or more of your users say they'd be 'very disappointed'
    without your product, you've crossed the threshold where growth
    becomes significantly easier. Below that, you're pushing a boulder
    uphill. Above it, the boulder starts rolling on its own."
```

---

## Metadata

```yaml
task:
  name: Run PMF Test
  id: run-pmf-test
  version: "1.0"
  category: product_strategy
  difficulty: beginner
  estimated_effort: 1-2 weeks (survey design, collection, analysis)

  primary_agents:
    - sean-ellis

  supporting_agents:
    - peter-fader
    - nick-mehta

  outputs:
    - pmf_survey_template
    - survey_results_analysis
    - segment_breakdown
    - action_recommendations
    - improvement_roadmap

  prerequisites:
    - active_user_base
    - email_access_to_users
    - minimum_sample_size
```

---

## Sean Ellis's PMF Philosophy

```
┌────────────────────────────────────────────────────────────────────────────┐
│               SEAN ELLIS'S PRODUCT-MARKET FIT PRINCIPLES                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. PMF IS MEASURABLE                                                       │
│     "Stop debating whether you have PMF. Measure it.                        │
│      If you can't quantify it, you can't improve it."                      │
│                                                                              │
│  2. THE 40% THRESHOLD IS REAL                                               │
│     "After analyzing hundreds of startups, 40% 'very disappointed'         │
│      is the inflection point where growth becomes sustainable."            │
│                                                                              │
│  3. ASK THE RIGHT PEOPLE                                                    │
│     "Only survey users who have truly experienced your product.            │
│      New signups and inactive users will skew your results."               │
│                                                                              │
│  4. FOCUS ON THE 'VERY DISAPPOINTED' GROUP                                 │
│     "Your best customers aren't who you think. They're the ones           │
│      who'd be very disappointed without you. Find their patterns."         │
│                                                                              │
│  5. PMF VARIES BY SEGMENT                                                   │
│     "You might have PMF with developers but not enterprise.               │
│      Segment your results to find your true believers."                    │
│                                                                              │
│  6. BELOW 40% = ITERATE, DON'T SCALE                                       │
│     "Growing without PMF is like filling a leaky bucket.                   │
│      Fix the product first, then step on the gas."                         │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 0: PRE-FLIGHT CHECK

### Eligibility Requirements

Before running the PMF test, verify you meet minimum requirements:

```yaml
eligibility_requirements:

  user_base:
    minimum_users: 40
    ideal_users: 100+
    rationale: "Statistical significance requires sufficient sample"

  user_activation:
    requirement: "Users must have experienced core value"
    examples:
      - "Completed at least 2 core actions"
      - "Used product for at least 2 weeks"
      - "Completed onboarding flow"
    why: "Non-activated users will skew to 'not disappointed'"

  recency:
    requirement: "Active within last 30 days"
    rationale: "Inactive users have already 'voted with their feet'"

  diversity:
    requirement: "Sample should represent user base"
    caution: "Don't cherry-pick happy customers"
```

### Pre-Flight Checklist

```
□ User Base Verification
  □ Have at least 40 active users
  □ Users have experienced core product value
  □ Can identify and segment user types
  □ Have email access or in-app survey capability

□ Survey Infrastructure
  □ Survey tool selected (Typeform, Google Forms, SurveyMonkey, etc.)
  □ Can segment responses by user attributes
  □ Can track response rates
  □ Results can be exported for analysis

□ Timing Considerations
  □ Not during unusual product period (outage, major release)
  □ Survey window allows sufficient response time (7-14 days)
  □ Team ready to act on results

□ Stakeholder Alignment
  □ Leadership understands PMF test methodology
  □ Clear on what results mean for strategy
  □ Commitment to act on findings
```

---

## PHASE 1: SURVEY DESIGN

### Step 1.1: The Core Question

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    THE SEAN ELLIS PMF QUESTION                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  "How would you feel if you could no longer use [PRODUCT NAME]?"           │
│                                                                              │
│  ANSWER OPTIONS (exactly as written):                                       │
│                                                                              │
│  ○ Very disappointed                                                        │
│  ○ Somewhat disappointed                                                    │
│  ○ Not disappointed (it isn't really that useful)                          │
│  ○ N/A – I no longer use [PRODUCT NAME]                                    │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  CRITICAL: Use these exact answer options.                                  │
│  The wording has been validated across thousands of surveys.               │
│  "Somewhat" disappointed is intentionally weaker than "very."              │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 1.2: Essential Follow-Up Questions

```yaml
follow_up_questions:

  question_2:
    question: "What type of people do you think would most benefit from [PRODUCT]?"
    type: "open_text"
    purpose: "Identifies ideal customer profile from user perspective"
    insight: "Users often describe themselves when answering this"

  question_3:
    question: "What is the main benefit you receive from [PRODUCT]?"
    type: "open_text"
    purpose: "Reveals actual value proposition (may differ from marketing)"
    insight: "The words users use become your messaging foundation"

  question_4:
    question: "How can we improve [PRODUCT] for you?"
    type: "open_text"
    purpose: "Identifies gaps preventing 'very disappointed' response"
    insight: "Patterns reveal what's blocking PMF"

  question_5:
    question: "What would you likely use as an alternative if [PRODUCT] were no longer available?"
    type: "open_text"
    purpose: "Reveals competitive landscape and switching costs"
    insight: "High specificity = real alternatives exist"
    alternatives_interpretation:
      - "Nothing" = Strong PMF signal
      - "Build it myself" = High value, high effort
      - "Competitor X" = Clear competitive threat
      - "Just wouldn't do it" = Nice-to-have, not must-have
```

### Step 1.3: Optional Segmentation Questions

```yaml
segmentation_questions:

  role_based:
    question: "What is your role?"
    options:
      - "Developer"
      - "Product Manager"
      - "Designer"
      - "Marketing"
      - "Executive/Founder"
      - "Other: ___"
    purpose: "Segment PMF by persona"

  company_size:
    question: "How large is your company?"
    options:
      - "Just me (solo)"
      - "2-10 employees"
      - "11-50 employees"
      - "51-200 employees"
      - "201-1000 employees"
      - "1000+ employees"
    purpose: "Segment PMF by company size"

  use_case:
    question: "What is your primary use case for [PRODUCT]?"
    options: "[Customized to your product]"
    purpose: "Identify which use cases have strongest PMF"

  usage_frequency:
    question: "How often do you use [PRODUCT]?"
    options:
      - "Daily"
      - "Several times a week"
      - "Weekly"
      - "A few times a month"
      - "Rarely"
    purpose: "Correlate usage frequency with PMF score"

  time_using:
    question: "How long have you been using [PRODUCT]?"
    options:
      - "Less than 1 month"
      - "1-3 months"
      - "3-6 months"
      - "6-12 months"
      - "More than 1 year"
    purpose: "Understand PMF evolution over customer lifecycle"
```

### Step 1.4: Complete Survey Template

```markdown
# [PRODUCT NAME] Feedback Survey

We're constantly working to improve [PRODUCT NAME] and would love your feedback.
This survey takes about 2-3 minutes.

---

**Question 1 (Required)**
How would you feel if you could no longer use [PRODUCT NAME]?

○ Very disappointed
○ Somewhat disappointed
○ Not disappointed (it isn't really that useful)
○ N/A – I no longer use [PRODUCT NAME]

---

**Question 2 (Required)**
What type of people do you think would most benefit from [PRODUCT NAME]?

[Open text field]

---

**Question 3 (Required)**
What is the main benefit you receive from [PRODUCT NAME]?

[Open text field]

---

**Question 4 (Required)**
How can we improve [PRODUCT NAME] for you?

[Open text field]

---

**Question 5 (Optional)**
What would you likely use as an alternative if [PRODUCT NAME] were no longer available?

[Open text field]

---

**Question 6 (Optional)**
What is your role?

○ Developer
○ Product Manager
○ Designer
○ Marketing
○ Executive/Founder
○ Other: ___

---

**Question 7 (Optional)**
How large is your company?

○ Just me (solo)
○ 2-10 employees
○ 11-50 employees
○ 51-200 employees
○ 201-1000 employees
○ 1000+ employees

---

**Question 8 (Optional)**
How long have you been using [PRODUCT NAME]?

○ Less than 1 month
○ 1-3 months
○ 3-6 months
○ 6-12 months
○ More than 1 year

---

Thank you for your feedback! Your responses help us build a better product.
```

---

## PHASE 2: SAMPLE SIZE & DISTRIBUTION

### Step 2.1: Sample Size Requirements

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       SAMPLE SIZE GUIDELINES                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MINIMUM VIABLE SAMPLE                                                      │
│  ─────────────────────                                                      │
│  Responses: 40                                                              │
│  Confidence: Low (directional only)                                         │
│  Use Case: Early stage validation                                           │
│                                                                              │
│  RECOMMENDED SAMPLE                                                         │
│  ─────────────────────                                                      │
│  Responses: 100-200                                                         │
│  Confidence: Medium (actionable insights)                                   │
│  Use Case: Most startups and SMBs                                          │
│                                                                              │
│  IDEAL SAMPLE                                                               │
│  ─────────────────────                                                      │
│  Responses: 300+                                                            │
│  Confidence: High (statistical significance)                                │
│  Use Case: Segment-level analysis, enterprise                              │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  MARGIN OF ERROR TABLE (95% Confidence)                                     │
│                                                                              │
│  Sample Size    Margin of Error                                             │
│  ───────────    ───────────────                                             │
│  40             ±15.5%                                                      │
│  100            ±9.8%                                                       │
│  200            ±6.9%                                                       │
│  300            ±5.7%                                                       │
│  500            ±4.4%                                                       │
│  1000           ±3.1%                                                       │
│                                                                              │
│  INTERPRETATION:                                                            │
│  If 42% say "very disappointed" with 100 responses (±9.8%),                │
│  true value is likely between 32.2% and 51.8%.                             │
│  Need larger sample for confident PMF determination.                        │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 2.2: Who to Survey

```yaml
survey_targeting:

  include:
    description: "Users who have truly experienced your product"
    criteria:
      - active_in_last_30_days: true
      - completed_core_action: true
      - used_for_minimum_period: "7+ days recommended"
      - has_email_contact: true

  exclude:
    description: "Users who haven't experienced core value"
    criteria:
      - never_logged_in_after_signup: true
      - only_used_once: true
      - inactive_for_90_plus_days: true
      - internal_team_members: true
      - test_accounts: true

  special_considerations:
    freemium_products: |
      Survey both free and paid users separately.
      PMF for free tier vs paid tier often differs significantly.

    b2b_products: |
      Survey the actual users, not just the buyer.
      Decision-maker PMF may differ from end-user PMF.

    multi_product: |
      Specify which product/feature you're asking about.
      Or run separate surveys for each.
```

### Step 2.3: Expected Response Rates

```yaml
response_rate_benchmarks:

  email_survey:
    typical_range: "10-25%"
    factors:
      - relationship_with_brand: "Engaged users respond more"
      - email_quality: "Personal > mass marketing"
      - incentive: "Can boost 5-10%"
      - timing: "Midweek > weekend"

  in_app_survey:
    typical_range: "15-30%"
    factors:
      - prominence: "Modal > banner"
      - timing: "After positive experience best"
      - friction: "Fewer questions = more responses"

  planning_calculation:
    formula: "Target Responses / Expected Response Rate = Emails Needed"
    example:
      target_responses: 100
      expected_response_rate: "15%"
      emails_needed: 667
```

---

## PHASE 3: SURVEY DISTRIBUTION

### Step 3.1: Distribution Methods

```yaml
distribution_methods:

  email_survey:
    pros:
      - "Can reach inactive users"
      - "Easy to track who responded"
      - "Can follow up non-responders"
    cons:
      - "Lower response rates"
      - "May hit spam filters"
    best_practices:
      - "Send from founder/product lead email"
      - "Personal, non-marketing tone"
      - "Short subject line mentioning feedback"
      - "Mobile-optimized survey link"

  in_app_survey:
    pros:
      - "Catches users in context"
      - "Higher response rates"
      - "Immediate feedback"
    cons:
      - "Can be intrusive"
      - "Only reaches active users"
      - "May interrupt workflows"
    best_practices:
      - "Trigger after positive experience (completed task, etc.)"
      - "Dismissible and non-blocking"
      - "Show once, then wait 30+ days"

  targeted_outreach:
    pros:
      - "Highest quality responses"
      - "Can probe deeper"
      - "Builds relationships"
    cons:
      - "Doesn't scale"
      - "Selection bias risk"
    best_practices:
      - "Use for very early stage only"
      - "Balance happy/unhappy customers"
      - "Don't lead the witness"
```

### Step 3.2: Email Template

```markdown
Subject: Quick question about [PRODUCT NAME]

Hi [FIRST NAME],

I'm [YOUR NAME], [YOUR ROLE] at [COMPANY].

I'm reaching out personally because we're working to make [PRODUCT] better, and your feedback would be incredibly valuable.

I have just one question that takes 30 seconds:

→ [SURVEY LINK]

Your honest feedback—positive or negative—helps us build something truly useful.

Thanks,
[YOUR NAME]

P.S. No need to reply to this email. The survey link above is the best way to share your thoughts.
```

### Step 3.3: Follow-Up Sequence

```yaml
follow_up_sequence:

  initial_send:
    day: 0
    message: "Initial survey invitation (email template above)"

  reminder_1:
    day: 3
    subject: "Quick reminder: 30-second feedback request"
    message: |
      Hi [FIRST NAME],

      Just a quick follow-up on my note from a few days ago.

      If you have 30 seconds, your feedback on [PRODUCT] would be hugely helpful:

      → [SURVEY LINK]

      Thanks!
      [YOUR NAME]

  reminder_2:
    day: 7
    subject: "Last chance: Quick feedback on [PRODUCT]"
    message: |
      Hi [FIRST NAME],

      This is my last note about this—I don't want to spam you!

      If you've got a minute to share your thoughts:

      → [SURVEY LINK]

      Either way, thanks for being a [PRODUCT] user.

      [YOUR NAME]

  close_survey:
    day: 10-14
    action: "Close survey and begin analysis"
```

---

## PHASE 4: ANALYSIS METHODOLOGY

### Step 4.1: The 40% Threshold

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    THE 40% PMF THRESHOLD                                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CALCULATION:                                                               │
│                                                                              │
│  PMF Score = (Very Disappointed) / (Very + Somewhat + Not) × 100           │
│                                                                              │
│  IMPORTANT: Exclude "N/A - I no longer use" from calculation               │
│  (These users have already churned)                                         │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  EXAMPLE CALCULATION:                                                       │
│                                                                              │
│  Total Responses: 150                                                       │
│  - Very disappointed: 52                                                    │
│  - Somewhat disappointed: 61                                                │
│  - Not disappointed: 28                                                     │
│  - N/A (churned): 9                                                         │
│                                                                              │
│  PMF Score = 52 / (52 + 61 + 28) × 100                                     │
│  PMF Score = 52 / 141 × 100                                                │
│  PMF Score = 36.9%                                                          │
│                                                                              │
│  INTERPRETATION: Below 40% threshold. PMF not yet achieved.                │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 4.2: PMF Score Interpretation

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    PMF SCORE INTERPRETATION GUIDE                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  0-15% "VERY DISAPPOINTED"                                                  │
│  ─────────────────────────                                                  │
│  Status: No PMF                                                             │
│  Diagnosis: Product is a "vitamin," not a "painkiller"                     │
│  Action: Major pivot or fundamental rethink needed                         │
│  Caution: Do NOT scale marketing. Fix product first.                       │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  15-25% "VERY DISAPPOINTED"                                                 │
│  ─────────────────────────                                                  │
│  Status: Weak PMF                                                           │
│  Diagnosis: Solving a real problem, but execution gaps exist               │
│  Action: Deep dive into "very disappointed" cohort patterns                │
│  Opportunity: May have PMF with specific segment                           │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  25-40% "VERY DISAPPOINTED"                                                 │
│  ─────────────────────────                                                  │
│  Status: Approaching PMF                                                    │
│  Diagnosis: Product works, but not "must-have" yet                         │
│  Action: Focus improvements on converting "somewhat" to "very"             │
│  Opportunity: Close to inflection point                                    │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  40-60% "VERY DISAPPOINTED"                                                 │
│  ─────────────────────────                                                  │
│  Status: PMF Achieved                                                       │
│  Diagnosis: Product is "must-have" for significant segment                 │
│  Action: Can begin scaling acquisition                                     │
│  Focus: Retention and expanding "very disappointed" cohort                 │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  60%+ "VERY DISAPPOINTED"                                                   │
│  ─────────────────────────                                                  │
│  Status: Strong PMF                                                         │
│  Diagnosis: Product is essential to users                                  │
│  Action: Accelerate growth, expand use cases                               │
│  Examples: Slack at launch, early Dropbox                                  │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 4.3: Response Distribution Analysis

```yaml
distribution_analysis:

  healthy_distribution:
    very_disappointed: "40%+"
    somewhat_disappointed: "30-40%"
    not_disappointed: "10-20%"
    churned: "<10%"
    interpretation: "Strong core, room to convert 'somewhat'"

  warning_distribution:
    very_disappointed: "20-30%"
    somewhat_disappointed: "40-50%"
    not_disappointed: "20-30%"
    churned: "<10%"
    interpretation: "Many lukewarm users. Product liked, not loved."

  problem_distribution:
    very_disappointed: "<20%"
    somewhat_disappointed: "30-40%"
    not_disappointed: "30-40%"
    churned: "10%+"
    interpretation: "Nice-to-have product. Fundamental value prop issue."

  analysis_questions:
    - "Is 'somewhat' group closer to 'very' or 'not'?"
    - "What patterns exist in the 'very disappointed' cohort?"
    - "Why are 'not disappointed' users still using the product?"
    - "Can 'churned' users be recovered?"
```

### Step 4.4: Segment Analysis

```
SEGMENT-LEVEL PMF ANALYSIS:

The aggregate PMF score hides important nuances.
You may have strong PMF with one segment and none with another.

SEGMENTATION ANALYSIS FRAMEWORK:

┌─────────────────────────────────────────────────────────────────────────┐
│ SEGMENT           │ RESPONSES │ VERY DIS. │ PMF SCORE │ ACTION         │
├───────────────────┼───────────┼───────────┼───────────┼────────────────┤
│ Developers        │ 45        │ 23        │ 51.1%     │ DOUBLE DOWN    │
│ Product Managers  │ 38        │ 12        │ 31.6%     │ IMPROVE        │
│ Designers         │ 22        │ 4         │ 18.2%     │ DEPRIORITIZE   │
│ Marketing         │ 36        │ 13        │ 36.1%     │ IMPROVE        │
├───────────────────┼───────────┼───────────┼───────────┼────────────────┤
│ TOTAL             │ 141       │ 52        │ 36.9%     │                │
└─────────────────────────────────────────────────────────────────────────┘

INSIGHTS FROM ABOVE EXAMPLE:
- Aggregate shows 36.9% (below threshold)
- But Developers show 51.1% (ABOVE threshold!)
- Designers at 18.2% are dragging down average
- Strategy: Double down on developers, deprioritize designers

CRITICAL INSIGHT:
"You don't need PMF with everyone. You need PMF with someone."
- Sean Ellis
```

### Step 4.5: Qualitative Analysis

```yaml
qualitative_analysis:

  analyzing_very_disappointed_responses:
    purpose: "Understand what makes product essential"
    process:
      1: "Export all open-text responses from 'very disappointed' cohort"
      2: "Identify common themes in 'main benefit' answers"
      3: "Extract exact language they use (for marketing)"
      4: "Note patterns in 'type of person' descriptions"
      5: "Document their alternatives (or lack thereof)"

    output:
      - ideal_customer_profile
      - true_value_proposition
      - messaging_language
      - competitive_moat

  analyzing_somewhat_disappointed_responses:
    purpose: "Identify what's blocking 'very disappointed'"
    process:
      1: "Export open-text responses from 'somewhat disappointed' cohort"
      2: "Focus on 'how can we improve' answers"
      3: "Categorize improvement requests"
      4: "Identify quick wins vs major changes"
      5: "Cross-reference with 'very disappointed' needs"

    output:
      - feature_gap_analysis
      - improvement_roadmap
      - quick_win_opportunities

  analyzing_not_disappointed_responses:
    purpose: "Understand why they're using but don't care"
    process:
      1: "Review why they're using despite low attachment"
      2: "Check if they're in wrong segment"
      3: "Identify if they're getting value differently"
      4: "Determine if worth trying to convert"

    insight: |
      "Not disappointed" users often reveal misaligned expectations.
      They signed up for X but product does Y.
      Either product positioning is wrong or they're not your ICP.
```

---

## PHASE 5: ACTION RECOMMENDATIONS

### Step 5.1: Action Framework by Score

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    ACTION FRAMEWORK BY PMF SCORE                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SCORE: 0-15% - "FUNDAMENTAL PROBLEM"                                       │
│  ─────────────────────────────────────                                      │
│                                                                              │
│  Diagnosis: Product isn't solving a meaningful problem                      │
│                                                                              │
│  Actions:                                                                    │
│  □ STOP all growth/marketing spend immediately                             │
│  □ Conduct deep customer interviews (not surveys)                          │
│  □ Revisit problem hypothesis                                               │
│  □ Consider pivot options                                                   │
│  □ Test radically different value propositions                             │
│                                                                              │
│  Timeline: 2-4 weeks to new hypothesis, then re-test                       │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  SCORE: 15-25% - "SEGMENT OPPORTUNITY"                                      │
│  ─────────────────────────────────────                                      │
│                                                                              │
│  Diagnosis: May have PMF with specific segment                              │
│                                                                              │
│  Actions:                                                                    │
│  □ Deep segment analysis (find your "very disappointed" tribe)             │
│  □ Interview 'very disappointed' users extensively                         │
│  □ Identify common patterns in this cohort                                 │
│  □ Narrow focus to highest PMF segment                                     │
│  □ Build features that deepen value for that segment                       │
│                                                                              │
│  Timeline: 4-6 weeks for segment focus, then re-test                       │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  SCORE: 25-40% - "CONVERSION OPPORTUNITY"                                   │
│  ─────────────────────────────────────                                      │
│                                                                              │
│  Diagnosis: Product works but isn't "must-have" yet                        │
│                                                                              │
│  Actions:                                                                    │
│  □ Focus on converting "somewhat" to "very disappointed"                   │
│  □ Analyze what "very" users do that "somewhat" don't                      │
│  □ Improve onboarding to drive deeper engagement                           │
│  □ Address top improvement requests                                        │
│  □ Test pricing/packaging changes                                          │
│                                                                              │
│  Timeline: 6-8 weeks focused iteration, then re-test                       │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  SCORE: 40-60% - "GROWTH MODE"                                             │
│  ─────────────────────────────────────                                      │
│                                                                              │
│  Diagnosis: PMF achieved, ready to scale                                    │
│                                                                              │
│  Actions:                                                                    │
│  □ Begin scaling acquisition channels                                       │
│  □ Invest in retention (don't lose your believers)                         │
│  □ Document and replicate success patterns                                 │
│  □ Build referral/viral mechanisms                                         │
│  □ Expand to adjacent segments carefully                                   │
│                                                                              │
│  Timeline: Shift from product iteration to growth                          │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────         │
│                                                                              │
│  SCORE: 60%+ - "ACCELERATE"                                                 │
│  ─────────────────────────────────────                                      │
│                                                                              │
│  Diagnosis: Strong PMF, potential category winner                          │
│                                                                              │
│  Actions:                                                                    │
│  □ Aggressively scale acquisition                                          │
│  □ Expand product surface area                                             │
│  □ Enter new markets/segments                                              │
│  □ Build moats (network effects, data, integrations)                       │
│  □ Consider raising capital for rapid expansion                            │
│                                                                              │
│  Timeline: Move fast, market window may be limited                         │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 5.2: Converting "Somewhat" to "Very" Disappointed

```yaml
conversion_strategies:

  analyze_the_gap:
    process:
      1: "Compare 'main benefit' answers between very vs somewhat"
      2: "Identify what 'very' users do that 'somewhat' don't"
      3: "Find the 'aha moment' that separates them"
      4: "Check if 'somewhat' users have discovered key features"

  common_gap_patterns:

    pattern_1_incomplete_onboarding:
      symptom: "'Somewhat' users haven't discovered core value"
      solution: "Improve onboarding, add in-app guidance"
      metric: "Completion rate of key onboarding steps"

    pattern_2_wrong_use_case:
      symptom: "'Somewhat' users using for secondary purpose"
      solution: "Better positioning, segment-specific messaging"
      metric: "Use case match rate"

    pattern_3_missing_feature:
      symptom: "'Somewhat' users cite specific feature gaps"
      solution: "Prioritize features that 'very' users love"
      metric: "Feature adoption rate"

    pattern_4_integration_gaps:
      symptom: "'Somewhat' users can't fit into workflow"
      solution: "Build key integrations, improve import/export"
      metric: "Integration usage rate"

    pattern_5_frequency_difference:
      symptom: "'Somewhat' users engage less frequently"
      solution: "Add triggers for regular engagement (notifications, reports)"
      metric: "Weekly active usage"

  tactical_improvements:
    quick_wins:
      - "Send 'very disappointed' users' tips to 'somewhat' users"
      - "Create case studies from 'very disappointed' cohort"
      - "A/B test onboarding focused on 'aha moment'"
      - "Add missing features most requested by 'somewhat'"

    medium_term:
      - "Redesign onboarding around 'very disappointed' patterns"
      - "Create segment-specific value propositions"
      - "Build community around power users"
      - "Develop certification/training programs"
```

### Step 5.3: Improvement Prioritization

```yaml
improvement_prioritization:

  framework: "Sean Ellis ICE Scoring"

  scoring:
    impact:
      question: "If this works, how much will PMF improve?"
      scale: "1-10"
      guidance:
        "1-3": "Minor improvement to edge cases"
        "4-6": "Meaningful improvement for some users"
        "7-10": "Could significantly move 'somewhat' to 'very'"

    confidence:
      question: "How confident are we this will work?"
      scale: "1-10"
      guidance:
        "1-3": "Gut feeling, no data"
        "4-6": "Some supporting evidence"
        "7-10": "Strong signal from user feedback"

    ease:
      question: "How easy is this to implement?"
      scale: "1-10"
      guidance:
        "1-3": "Multi-quarter initiative"
        "4-6": "1-2 month project"
        "7-10": "Days to weeks"

  calculation: "ICE Score = (Impact + Confidence + Ease) / 3"

  example_prioritization:
    | Improvement              | Impact | Confidence | Ease | ICE Score |
    |-------------------------|--------|------------|------|-----------|
    | Better onboarding       | 8      | 7          | 6    | 7.0       |
    | Mobile app              | 7      | 6          | 3    | 5.3       |
    | Slack integration       | 6      | 8          | 7    | 7.0       |
    | Advanced analytics      | 5      | 4          | 5    | 4.7       |
    | Team features           | 7      | 6          | 4    | 5.7       |
```

---

## PHASE 6: TRACKING & ITERATION

### Step 6.1: PMF Tracking Over Time

```yaml
tracking_cadence:

  recommended_frequency:
    early_stage: "Every 4-6 weeks"
    growth_stage: "Every quarter"
    mature_stage: "Every 6 months"

  tracking_metrics:
    primary:
      - pmf_score: "% very disappointed"
      - trend: "Change vs last measurement"
      - segment_scores: "PMF by key segments"

    supporting:
      - response_rate: "Survey participation rate"
      - sample_size: "Total responses"
      - distribution_shift: "Movement between categories"

  visualization:
    chart_type: "Line chart with segment overlay"
    x_axis: "Time (survey dates)"
    y_axis: "PMF Score (%)"
    benchmark_line: "40% threshold"
    segments: "Colored lines per segment"
```

### Step 6.2: PMF Dashboard Template

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    PRODUCT-MARKET FIT DASHBOARD                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CURRENT PMF SCORE                                                          │
│  ────────────────────────────────────────────────────────────              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │                                                               │          │
│  │                         38.7%                                 │          │
│  │                    "Very Disappointed"                        │          │
│  │                                                               │          │
│  │   ▲ +4.2% from last quarter        Status: APPROACHING PMF   │          │
│  │                                                               │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  RESPONSE DISTRIBUTION                                                      │
│  ────────────────────────────────────────────────────────────              │
│                                                                              │
│  Very Disappointed    ████████████████████████████████████░░░░  38.7%      │
│  Somewhat Disappointed████████████████████████████████████████  42.1%      │
│  Not Disappointed     ██████████████████░░░░░░░░░░░░░░░░░░░░░░  15.4%      │
│  N/A (Churned)        ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.8%      │
│                                                                              │
│  PMF BY SEGMENT                                                             │
│  ────────────────────────────────────────────────────────────              │
│                                                                              │
│  Developers        ███████████████████████████████████████████  52.3% ✓    │
│  Product Managers  █████████████████████████████████░░░░░░░░░░  38.1%      │
│  Marketing         ████████████████████████████░░░░░░░░░░░░░░░  31.2%      │
│  Designers         █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  19.7%      │
│                                                                              │
│  PMF TREND (Last 12 Months)                                                 │
│  ────────────────────────────────────────────────────────────              │
│                                                                              │
│  50% ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │          │
│  40% ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ●━━━━●         │          │
│  30% ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ●━━━━●━━━━●                     │          │
│  20% ─ ─ ─ ─ ─ ─ ●━━━━●━━━━●                                   │          │
│  10% ─ ─ ●━━━━●                                                  │          │
│      Q1    Q2    Q3    Q4    Q1    Q2    Q3    Q4               │          │
│      2025  2025  2025  2025  2026  2026  2026  2026             │          │
│                                                                              │
│  TOP IMPROVEMENT THEMES (from "How can we improve?")                        │
│  ────────────────────────────────────────────────────────────              │
│                                                                              │
│  1. Mobile app (42 mentions)                                                │
│  2. Better integrations (38 mentions)                                       │
│  3. Team collaboration features (27 mentions)                               │
│  4. Faster performance (23 mentions)                                        │
│  5. Better onboarding (19 mentions)                                         │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Step 6.3: Iteration Playbook

```yaml
iteration_playbook:

  after_each_pmf_survey:

    immediate_actions:
      - "Calculate aggregate PMF score"
      - "Segment by key dimensions"
      - "Export qualitative responses"
      - "Share results with team"

    week_1_analysis:
      - "Code open-text responses"
      - "Identify top themes"
      - "Compare with previous survey"
      - "Generate insights report"

    week_2_planning:
      - "Prioritize improvements (ICE)"
      - "Assign owners to top items"
      - "Set timeline for changes"
      - "Schedule next survey"

    execution_period:
      - "Implement prioritized changes"
      - "Track leading indicators"
      - "Gather ongoing feedback"
      - "Prepare for next survey"

  success_metrics:
    - pmf_score_improvement: "+5% per quarter target"
    - segment_coverage: "All key segments >30%"
    - response_rate: ">15% participation"
    - action_completion: ">80% of planned improvements"
```

---

## Elicitation Questions

Before running the PMF test, gather this information:

### Product Context

```yaml
elicitation:

  product_basics:
    - "What is your product name?"
    - "What problem does it solve in one sentence?"
    - "How long has the product been live?"
    - "What is your business model? (SaaS, marketplace, etc.)"

  user_base:
    - "How many active users do you have?"
    - "What defines an 'active' user for you?"
    - "How do users typically find you?"
    - "What are your main user segments/personas?"

  current_state:
    - "Have you run a PMF survey before?"
    - "What's your gut feeling on PMF? (1-10)"
    - "What do your happiest users love most?"
    - "What do churning users complain about?"

  goals:
    - "What will you do with PMF survey results?"
    - "Are you deciding whether to pivot?"
    - "Are you deciding whether to scale?"
    - "Is this for internal use or external (investors)?"
```

### Survey Logistics

```yaml
logistics_questions:

  distribution:
    - "How will you distribute the survey? (email, in-app, both)"
    - "Do you have email addresses for active users?"
    - "What survey tool do you have access to?"
    - "Can you segment users in your survey tool?"

  sample:
    - "How many users will you send the survey to?"
    - "Can you identify users who have experienced core value?"
    - "What's your expected response rate?"
    - "Do you want to incentivize responses?"

  timing:
    - "When do you want to run the survey?"
    - "How long will you keep the survey open?"
    - "Are there any product events that might affect timing?"
    - "When do you need results?"
```

---

## Output Format

### PMF Survey Report Template

```markdown
# Product-Market Fit Survey Report
## [PRODUCT NAME] - [DATE]

### Executive Summary

**PMF Score: [X]%**
**Status: [No PMF / Approaching PMF / PMF Achieved / Strong PMF]**
**Trend: [↑/↓/→ X% vs previous]**

Key Findings:
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

Recommended Actions:
1. [Action 1]
2. [Action 2]
3. [Action 3]

---

### Survey Details

| Metric | Value |
|--------|-------|
| Survey Period | [Start] - [End] |
| Emails Sent | [X] |
| Responses | [X] |
| Response Rate | [X%] |
| Valid Responses | [X] |

---

### Response Distribution

| Response | Count | Percentage |
|----------|-------|------------|
| Very Disappointed | [X] | [X%] |
| Somewhat Disappointed | [X] | [X%] |
| Not Disappointed | [X] | [X%] |
| N/A (Churned) | [X] | [X%] |

**PMF Score Calculation:**
[Very Disappointed] / ([Very] + [Somewhat] + [Not]) = [X%]

---

### Segment Analysis

| Segment | Responses | Very Disappointed | PMF Score | Status |
|---------|-----------|-------------------|-----------|--------|
| [Segment 1] | [X] | [X] | [X%] | [Status] |
| [Segment 2] | [X] | [X] | [X%] | [Status] |
| [Segment 3] | [X] | [X] | [X%] | [Status] |

---

### Qualitative Insights

#### Top Benefits Cited (from "Very Disappointed" cohort)
1. [Benefit 1] - [X mentions]
2. [Benefit 2] - [X mentions]
3. [Benefit 3] - [X mentions]

#### Top Improvement Requests
1. [Request 1] - [X mentions]
2. [Request 2] - [X mentions]
3. [Request 3] - [X mentions]

#### Competitive Alternatives Mentioned
1. [Alternative 1] - [X mentions]
2. [Alternative 2] - [X mentions]
3. "Nothing" / "Would build it" - [X mentions]

---

### Recommendations

#### Immediate Actions (This Sprint)
- [ ] [Action 1]
- [ ] [Action 2]

#### Short-Term (This Quarter)
- [ ] [Action 1]
- [ ] [Action 2]

#### Medium-Term (Next Quarter)
- [ ] [Action 1]
- [ ] [Action 2]

---

### Next Steps

- Next PMF Survey: [Date]
- Owner: [Name]
- Success Metric: [Target PMF score]
```

---

## Examples

### Example 1: Early-Stage SaaS (Low PMF)

```
CONTEXT:
- Product: Task management tool for remote teams
- Users: 180 active users
- Time in market: 6 months
- Gut feeling: "Users like us but don't love us"

SURVEY RESULTS:
- Responses: 62
- Very Disappointed: 14 (22.6%)
- Somewhat Disappointed: 29 (46.8%)
- Not Disappointed: 17 (27.4%)
- Churned: 2 (3.2%)

PMF SCORE: 23.3% (Below threshold)

SEGMENT ANALYSIS:
- Startups (<10 employees): 38.5% ← OPPORTUNITY
- SMB (10-50): 18.2%
- Mid-market (50+): 15.4%

KEY INSIGHTS:
- Startups love the simplicity
- Larger teams need more structure/permissions
- Top request: Better Slack integration

ACTIONS TAKEN:
1. Narrowed positioning to "task management for startups"
2. Deprioritized enterprise features
3. Built Slack integration
4. Simplified onboarding further

RESULT (3 months later):
PMF Score: 41.2% (Crossed threshold!)
```

### Example 2: B2B Product Approaching PMF

```
CONTEXT:
- Product: Analytics platform for e-commerce
- Users: 450 active users
- Time in market: 18 months
- Previous PMF score: 32%

SURVEY RESULTS:
- Responses: 147
- Very Disappointed: 56 (38.1%)
- Somewhat Disappointed: 58 (39.5%)
- Not Disappointed: 29 (19.7%)
- Churned: 4 (2.7%)

PMF SCORE: 39.2% (Almost there!)

SEGMENT ANALYSIS:
- Shopify stores: 47.3% ← STRONG PMF
- WooCommerce: 31.2%
- Custom platforms: 28.6%

KEY INSIGHTS:
- Shopify integration is key differentiator
- WooCommerce users want better integration
- "Somewhat" users cite missing cohort analysis

ACTIONS TAKEN:
1. Doubled down on Shopify features
2. Improved WooCommerce integration
3. Built cohort analysis feature
4. Created Shopify-specific marketing

RESULT (3 months later):
PMF Score: 46.8% (Confirmed PMF!)
```

### Example 3: Consumer App with Strong PMF

```
CONTEXT:
- Product: Meditation app
- Users: 12,000 active users
- Time in market: 2 years
- Previous PMF score: 52%

SURVEY RESULTS:
- Responses: 1,847
- Very Disappointed: 1,142 (61.8%)
- Somewhat Disappointed: 517 (28.0%)
- Not Disappointed: 166 (9.0%)
- Churned: 22 (1.2%)

PMF SCORE: 62.6% (Strong PMF!)

SEGMENT ANALYSIS:
- Daily users: 78.3% ← Core believers
- Weekly users: 45.2%
- Monthly users: 23.1%

KEY INSIGHTS:
- Daily habit = strong emotional connection
- Users who complete 7-day streak → 3x more likely "very disappointed"
- Top benefit: "Helps me sleep"
- Alternative: "Would probably just stop meditating"

ACTIONS TAKEN:
1. Focused growth on acquisition
2. Built streak/habit features
3. Created "sleep" positioning
4. Launched referral program

RESULT:
Grew from 12K to 45K users in 6 months
Maintained 60%+ PMF score
```

---

## Integration

### Related Tasks

- **calculate-clv.md** - Correlate PMF score with customer value
- **predict-churn.md** - PMF cohort churn analysis
- **define-north-star.md** - PMF informs North Star metric selection
- **run-growth-experiment.md** - Only run growth experiments after PMF

### Related Agents

- **sean-ellis** - Primary methodology owner
- **peter-fader** - Segment value analysis
- **nick-mehta** - Customer success correlation

### Related Checklists

- **customer-360-checklist.md** - User data for segmentation

### Tool Recommendations

```yaml
survey_tools:
  free:
    - google_forms: "Basic but functional"
    - typeform_free: "Better UX, limited responses"

  paid:
    - typeform_pro: "Best user experience"
    - surveymonkey: "Good analytics"
    - delighted: "Built for NPS/PMF surveys"
    - hotjar: "In-app surveys"

  in_app:
    - intercom: "Contextual surveys"
    - pendo: "In-product surveys"
    - appcues: "User onboarding + surveys"
    - chameleon: "Product tours + surveys"

analysis_tools:
  - excel_sheets: "Basic analysis"
  - amplitude: "Behavioral correlation"
  - mixpanel: "Cohort analysis"
  - tableau: "Advanced visualization"
```

---

## Sean Ellis's Final Wisdom

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    SEAN ELLIS'S PMF PRINCIPLES                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  "Product-Market Fit is the moment when your product becomes a             │
│   must-have for a specific group of people. It's not when everyone         │
│   likes you—it's when someone NEEDS you."                                  │
│                                                                              │
│  1. THE 40% RULE IS A MINIMUM, NOT A GOAL                                  │
│     "40% means you can start scaling. 60%+ means you can                   │
│      scale aggressively. Aim higher."                                      │
│                                                                              │
│  2. SEGMENT BEFORE AGGREGATING                                              │
│     "Your overall PMF might be 30%, but you might have 60%                 │
│      with one segment. Find your believers first."                         │
│                                                                              │
│  3. LISTEN TO 'VERY DISAPPOINTED' USERS                                    │
│     "They're not just your best customers—they're your                     │
│      product development team. They'll tell you what to build."            │
│                                                                              │
│  4. DON'T SCALE WITHOUT PMF                                                 │
│     "Growing without PMF is like pouring water into a                      │
│      bucket with holes. Fix the bucket first."                             │
│                                                                              │
│  5. PMF CAN BE LOST                                                         │
│     "Market changes, competitors emerge, needs evolve.                     │
│      Keep measuring. PMF isn't a one-time achievement."                    │
│                                                                              │
│  FINAL THOUGHT:                                                             │
│  "The PMF survey isn't just a measurement tool—it's a                      │
│   compass. It tells you whether to iterate, pivot, or scale.               │
│   Without it, you're navigating blind."                                    │
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
      - "Sean Ellis methodology integrated"
      - "6-phase framework established"
      - "Survey templates included"
      - "40% threshold analysis framework"
      - "Segment analysis methodology"
      - "Action recommendations by score"
      - "3 real-world examples included"
```
