# Define North Star Metric - Sean Ellis Framework

## Purpose

Systematic process for defining, validating, and operationalizing your North Star Metric (NSM). The North Star Metric is the single measurement that best captures the core value your product delivers to customers. When properly defined, it aligns every team, clarifies priorities, and predicts long-term sustainable growth.

Sean Ellis coined the term to solve a common problem: companies drowning in metrics but lacking a unified focus. The North Star Metric cuts through the noise by identifying the ONE number that, when improved, drives everything else that matters.

## When to Use

- **PRODUCT STRATEGY** - Defining or refining product direction
- **COMPANY ALIGNMENT** - Getting all teams focused on the same goal
- **GROWTH PLANNING** - Knowing what to optimize before scaling
- **INVESTOR COMMUNICATION** - Single metric that demonstrates value creation
- **NEW PRODUCT LAUNCH** - Establishing success criteria from day one
- **PIVOT DECISION** - Determining if current direction is working
- **TEAM ONBOARDING** - Helping new hires understand what matters most

## Primary Agent

```yaml
primary_agent: sean-ellis
supporting_agents:
  - peter-fader  # Customer value correlation
  - avinash-kaushik  # Metrics hierarchy and DMMM

sean_ellis_perspective:
  core_belief: "Every product needs ONE metric that captures the value you deliver to customers. Everything else is either an input to that metric or a result of it."

  key_insight: |
    "The North Star Metric isn't your revenue number. Revenue is a lagging
    indicator of value delivered. The NSM captures the moment when your
    customer gets value - and if you get that right, revenue follows."
```

---

## Metadata

```yaml
task:
  name: Define North Star Metric
  id: define-north-star
  version: "1.0"
  category: product_strategy
  difficulty: intermediate
  estimated_effort: 1-2 weeks (workshop, validation, operationalization)

  primary_agents:
    - sean-ellis

  supporting_agents:
    - peter-fader
    - avinash-kaushik

  outputs:
    - north_star_definition
    - input_metrics_tree
    - validation_results
    - dashboard_specifications
    - team_alignment_doc

  prerequisites:
    - product_understanding
    - user_behavior_data
    - business_model_clarity
    - stakeholder_availability
```

---

## Sean Ellis's North Star Philosophy

```
+---------------------------------------------------------------------------+
|                   SEAN ELLIS'S NORTH STAR PRINCIPLES                       |
+---------------------------------------------------------------------------+
|                                                                             |
|  1. ONE METRIC TO RULE THEM ALL                                            |
|     "If you can only look at one number to know if your business is        |
|      healthy, what would it be? That's your North Star."                   |
|                                                                             |
|  2. VALUE, NOT REVENUE                                                     |
|     "Revenue is the result of delivering value. Your NSM should            |
|      capture the VALUE moment, not the payment moment."                    |
|                                                                             |
|  3. LEADING, NOT LAGGING                                                   |
|     "A good North Star predicts future success. It moves before            |
|      revenue moves. That's how you know you're on the right track."        |
|                                                                             |
|  4. ACTIONABLE BY TEAMS                                                    |
|     "If your teams can't directly influence the metric, it's not           |
|      a good North Star. It needs to be something they can move."           |
|                                                                             |
|  5. SIMPLE TO UNDERSTAND                                                   |
|     "Everyone from the CEO to the newest engineer should be able           |
|      to explain the NSM and why it matters in under 30 seconds."           |
|                                                                             |
|  6. CONNECTED TO BUSINESS OUTCOMES                                         |
|     "The NSM must correlate with business success. If it goes up           |
|      and revenue doesn't follow, you've picked the wrong metric."          |
|                                                                             |
+---------------------------------------------------------------------------+
```

---

## PHASE 0: PRE-WORKSHOP PREPARATION

### Step 0.1: Stakeholder Alignment

Before running a North Star workshop, ensure key stakeholders understand the concept and are committed to the process.

```yaml
stakeholder_checklist:

  executive_buy_in:
    required: true
    who:
      - CEO or GM
      - Head of Product
      - Head of Growth/Marketing
    what_they_need_to_understand:
      - "NSM is not replacing all metrics, it's prioritizing one"
      - "Teams will use this to make daily decisions"
      - "NSM may differ from what we've been measuring"
      - "Commitment to track and report on NSM regularly"

  cross_functional_participation:
    required: true
    who:
      - Product lead
      - Engineering lead
      - Marketing/Growth lead
      - Customer Success lead
      - Data/Analytics lead
    why_all_teams:
      - "NSM affects everyone's priorities"
      - "Need buy-in for adoption"
      - "Different perspectives improve quality"

  pre_work_for_participants:
    - "Review current key metrics and their limitations"
    - "List what they believe drives customer value"
    - "Identify their team's current success metrics"
    - "Bring data on user behavior and outcomes"
```

### Step 0.2: Data Preparation

```yaml
data_requirements:

  user_behavior_data:
    essential:
      - "User activation events"
      - "Core feature usage frequency"
      - "Retention/churn patterns"
      - "Engagement metrics over time"
    nice_to_have:
      - "Cohort analysis"
      - "User journey maps"
      - "Feature adoption rates"

  business_data:
    essential:
      - "Revenue by customer segment"
      - "Customer acquisition cost"
      - "Lifetime value estimates"
      - "Conversion funnel metrics"
    nice_to_have:
      - "NPS or satisfaction scores"
      - "Referral/viral metrics"
      - "Support ticket patterns"

  qualitative_insights:
    essential:
      - "Why customers say they use the product"
      - "What makes power users different"
      - "Common churn reasons"
    nice_to_have:
      - "PMF survey results"
      - "Customer interview summaries"
      - "Competitive positioning"
```

### Step 0.3: Pre-Workshop Questions

```yaml
pre_workshop_questions:

  for_leadership:
    - "What is the single most important thing our product does for customers?"
    - "If you could only track one metric, what would it be?"
    - "What behavior indicates a customer is getting real value?"
    - "What's the 'aha moment' when customers realize our value?"

  for_product:
    - "What action do our best customers take that others don't?"
    - "What feature usage correlates most with retention?"
    - "At what point do customers become 'sticky'?"
    - "What defines an 'activated' user?"

  for_growth:
    - "What metric do you use to define a 'successful' user?"
    - "What leading indicator best predicts conversion?"
    - "What behavior precedes referrals?"
    - "What engagement level predicts long-term retention?"

  for_customer_success:
    - "What do healthy accounts do differently?"
    - "What's the first sign a customer might churn?"
    - "What makes customers recommend us?"
    - "What value do customers mention most in reviews?"
```

---

## PHASE 1: NORTH STAR CRITERIA

### Step 1.1: The Three Requirements

Every North Star Metric must meet three requirements:

```
+---------------------------------------------------------------------------+
|                    NORTH STAR METRIC REQUIREMENTS                          |
+---------------------------------------------------------------------------+
|                                                                             |
|  REQUIREMENT 1: REFLECTS CUSTOMER VALUE                                    |
|  +-----------------------------------------------------------------+      |
|  |                                                                   |      |
|  |  The metric captures the moment when customers receive VALUE      |      |
|  |  from your product. Not when they sign up, not when they pay,     |      |
|  |  but when they actually GET what they came for.                   |      |
|  |                                                                   |      |
|  |  TEST: "Does improving this metric mean customers are getting     |      |
|  |         more value from our product?"                             |      |
|  |                                                                   |      |
|  |  EXAMPLES:                                                        |      |
|  |  - Airbnb: Nights booked (guest got accommodation)               |      |
|  |  - Slack: Messages sent (team communicated)                      |      |
|  |  - Spotify: Time spent listening (user enjoyed music)            |      |
|  |                                                                   |      |
|  +-----------------------------------------------------------------+      |
|                                                                             |
|  REQUIREMENT 2: IS A LEADING INDICATOR                                     |
|  +-----------------------------------------------------------------+      |
|  |                                                                   |      |
|  |  The metric moves BEFORE revenue moves. It predicts future        |      |
|  |  business success rather than measuring past performance.         |      |
|  |                                                                   |      |
|  |  TEST: "If this metric improves today, will revenue improve       |      |
|  |         in the coming weeks/months?"                              |      |
|  |                                                                   |      |
|  |  LEADING vs LAGGING:                                             |      |
|  |  - Leading: Active users, engagement, completions               |      |
|  |  - Lagging: Revenue, profit, market share                       |      |
|  |                                                                   |      |
|  +-----------------------------------------------------------------+      |
|                                                                             |
|  REQUIREMENT 3: IS ACTIONABLE BY TEAMS                                     |
|  +-----------------------------------------------------------------+      |
|  |                                                                   |      |
|  |  Teams can directly influence the metric through their work.      |      |
|  |  If teams can't move it, it's not useful for alignment.           |      |
|  |                                                                   |      |
|  |  TEST: "Can our product, engineering, and growth teams run        |      |
|  |         experiments that directly impact this metric?"            |      |
|  |                                                                   |      |
|  |  ACTIONABLE:                                                     |      |
|  |  - Weekly active users (can improve onboarding, features)        |      |
|  |  - Documents created (can improve UX, templates)                 |      |
|  |                                                                   |      |
|  |  NOT ACTIONABLE:                                                 |      |
|  |  - Market conditions (external factors)                          |      |
|  |  - Competitor behavior (can't control)                           |      |
|  |                                                                   |      |
|  +-----------------------------------------------------------------+      |
|                                                                             |
+---------------------------------------------------------------------------+
```

### Step 1.2: Good vs Bad North Star Metrics

```yaml
good_north_star_characteristics:

  captures_value_exchange:
    description: "Measures the moment value is delivered"
    good_examples:
      - "Rides completed (Uber)"
      - "Messages sent (Slack)"
      - "Courses completed (education)"
    bad_examples:
      - "App downloads (no value yet)"
      - "Accounts created (no value yet)"
      - "Page views (passive, not value)"

  is_compound_metric:
    description: "Combines breadth and depth"
    good_examples:
      - "Weekly active users x sessions per user"
      - "Paying customers x average order value"
      - "Active courses x completion rate"
    bad_examples:
      - "Total users (vanity, no engagement)"
      - "Revenue only (lagging)"
      - "Features shipped (output, not outcome)"

  has_natural_frequency:
    description: "Can be measured at meaningful intervals"
    good_examples:
      - "Daily: Messages sent"
      - "Weekly: Active users"
      - "Monthly: Transactions completed"
    bad_examples:
      - "Yearly revenue (too slow to act on)"
      - "Lifetime value (can't measure in real-time)"
      - "NPS (too infrequent)"

  is_understandable:
    description: "Anyone can explain it in 30 seconds"
    good_examples:
      - "Nights booked"
      - "Songs played"
      - "Orders delivered"
    bad_examples:
      - "Engagement score (what's that?)"
      - "Health index (too abstract)"
      - "Weighted activity units (too complex)"

bad_north_star_patterns:

  vanity_metrics:
    description: "Numbers that look good but don't predict success"
    examples:
      - "Total registered users (includes inactive)"
      - "Total app downloads (includes churned)"
      - "Social media followers (not product value)"
    why_bad: "Can grow while business declines"

  revenue_as_nsm:
    description: "Using revenue or ARR as North Star"
    examples:
      - "Monthly Recurring Revenue"
      - "Gross Merchandise Value"
      - "Annual Contract Value"
    why_bad: "Lagging indicator - moves after value delivered"
    exception: "Marketplaces sometimes use GMV as proxy for value exchange"

  ratio_only_metrics:
    description: "Percentages without volume context"
    examples:
      - "Conversion rate (could be 100% of 1 user)"
      - "Retention rate (could be high but tiny base)"
      - "NPS score (doesn't show scale)"
    why_bad: "Can be gamed, doesn't show absolute progress"

  composite_scores:
    description: "Weighted combinations that obscure truth"
    examples:
      - "Customer Health Score"
      - "Engagement Index"
      - "Product Quality Score"
    why_bad: "Hard to understand, easy to manipulate weights"
```

---

## PHASE 2: DISCOVERY WORKSHOP

### Step 2.1: Workshop Structure

```yaml
workshop_format:

  duration: "Half-day (4 hours) or full-day for complex products"

  participants: "6-12 people from cross-functional teams"

  facilitator: "Product lead or external facilitator"

  materials_needed:
    - "Whiteboard or virtual board (Miro, Figjam)"
    - "Sticky notes (physical or digital)"
    - "Pre-workshop data package"
    - "Timer for timeboxed exercises"

  agenda:
    1_context_setting:
      duration: "30 min"
      activities:
        - "Review what North Star Metric means"
        - "Share pre-workshop findings"
        - "Align on workshop goals"

    2_value_exploration:
      duration: "60 min"
      activities:
        - "Exercise: Customer Value Canvas"
        - "Exercise: Aha Moment Mapping"
        - "Exercise: Power User Analysis"

    3_metric_brainstorm:
      duration: "45 min"
      activities:
        - "Generate candidate metrics (divergent)"
        - "Group similar metrics"
        - "Initial filtering against criteria"

    4_metric_evaluation:
      duration: "60 min"
      activities:
        - "Deep evaluation of top 3-5 candidates"
        - "Input metrics tree for each"
        - "Scoring against criteria"

    5_selection_decision:
      duration: "30 min"
      activities:
        - "Present top candidates with pros/cons"
        - "Discussion and debate"
        - "Commitment to one metric"

    6_operationalization:
      duration: "30 min"
      activities:
        - "Define measurement methodology"
        - "Identify data requirements"
        - "Assign ownership and next steps"
```

### Step 2.2: Exercise 1 - Customer Value Canvas

```
+---------------------------------------------------------------------------+
|                       CUSTOMER VALUE CANVAS                                |
+---------------------------------------------------------------------------+
|                                                                             |
|  Instructions: Fill each quadrant with your team's perspective             |
|                                                                             |
|  +--------------------------------+--------------------------------+       |
|  |                                |                                |       |
|  |  WHAT PROBLEM DO WE SOLVE?     |  HOW DO CUSTOMERS DESCRIBE     |       |
|  |                                |  THE VALUE THEY GET?           |       |
|  |  - Primary pain point          |                                |       |
|  |  - Secondary pain points       |  - In their own words          |       |
|  |  - Jobs to be done             |  - From reviews/testimonials   |       |
|  |                                |  - From sales conversations    |       |
|  |  ____________________________  |  ____________________________  |       |
|  |  ____________________________  |  ____________________________  |       |
|  |  ____________________________  |  ____________________________  |       |
|  |                                |                                |       |
|  +--------------------------------+--------------------------------+       |
|  |                                |                                |       |
|  |  WHAT ACTION INDICATES         |  WHAT HAPPENS WHEN CUSTOMERS   |       |
|  |  VALUE WAS RECEIVED?           |  GET MAXIMUM VALUE?            |       |
|  |                                |                                |       |
|  |  - Specific user behavior      |  - Power user behaviors        |       |
|  |  - Measurable action           |  - Ideal customer journey      |       |
|  |  - Completion/success event    |  - Expansion indicators        |       |
|  |                                |                                |       |
|  |  ____________________________  |  ____________________________  |       |
|  |  ____________________________  |  ____________________________  |       |
|  |  ____________________________  |  ____________________________  |       |
|  |                                |                                |       |
|  +--------------------------------+--------------------------------+       |
|                                                                             |
+---------------------------------------------------------------------------+
```

### Step 2.3: Exercise 2 - Aha Moment Mapping

```yaml
aha_moment_exercise:

  purpose: "Identify the moment when customers realize product value"

  process:
    step_1:
      instruction: "List behaviors that differentiate retained vs churned users"
      examples:
        - "Invited a team member"
        - "Completed first project"
        - "Connected integration"
        - "Used feature X more than 3 times"

    step_2:
      instruction: "For each behavior, note the timeframe it typically happens"
      examples:
        - "Invited team member: Day 1-3"
        - "Completed first project: Day 3-7"
        - "Connected integration: Day 7-14"

    step_3:
      instruction: "Identify which behavior best predicts long-term retention"
      question: "Which single action, if completed, most strongly predicts the user will stay?"

    step_4:
      instruction: "Define the 'Aha Moment' in a sentence"
      template: "Users experience the Aha Moment when they [ACTION] within [TIMEFRAME]"
      examples:
        - "Slack: Send 2,000 team messages within 30 days"
        - "Dropbox: Put at least one file in one folder on one device"
        - "Facebook: Add 7 friends in 10 days"

  output:
    aha_moment_definition: "____________________________________"
    correlation_with_retention: "___% more likely to retain"
    current_achievement_rate: "___% of users reach Aha Moment"
```

### Step 2.4: Exercise 3 - Metric Brainstorm

```yaml
brainstorm_exercise:

  phase_1_divergent:
    duration: "15 minutes"
    instruction: |
      Everyone writes potential North Star Metrics on sticky notes.
      One metric per note. No filtering yet - quantity over quality.
      Think about: What captures customer value? What predicts retention?

    prompt_questions:
      - "What action shows a customer got value?"
      - "What do power users do that others don't?"
      - "What would we celebrate if it doubled?"
      - "What metric would hurt most if it dropped 50%?"

  phase_2_grouping:
    duration: "10 minutes"
    instruction: |
      Group similar metrics together.
      Name each group.
      Look for patterns and themes.

  phase_3_initial_filter:
    duration: "15 minutes"
    instruction: |
      For each group, quickly evaluate against the three criteria:
      1. Does it reflect customer value? (Yes/No/Maybe)
      2. Is it a leading indicator? (Yes/No/Maybe)
      3. Is it actionable? (Yes/No/Maybe)

      Keep only metrics with at least 2 "Yes" answers for deep evaluation.

  output:
    total_metrics_generated: "___"
    groups_identified: "___"
    metrics_advancing: "___"
```

---

## PHASE 3: COMMON NORTH STARS BY BUSINESS MODEL

### Step 3.1: Business Model Categories

```
+---------------------------------------------------------------------------+
|                   NORTH STAR METRICS BY BUSINESS MODEL                     |
+---------------------------------------------------------------------------+
|                                                                             |
|  ATTENTION/MEDIA MODEL                                                     |
|  Value = Time spent engaging with content                                  |
|  +------------------------------------------------------------------+     |
|  | Business Type    | Common North Star Metrics                      |     |
|  |------------------+-----------------------------------------------|     |
|  | Social Media     | Daily Active Users (DAU)                      |     |
|  | Streaming        | Time spent watching/listening                 |     |
|  | News/Content     | Time spent reading                            |     |
|  | Gaming           | Time played per session                       |     |
|  +------------------------------------------------------------------+     |
|  | Examples:                                                         |     |
|  | - Facebook: Daily Active Users                                   |     |
|  | - Netflix: Hours streamed                                        |     |
|  | - Spotify: Time spent listening                                  |     |
|  | - Medium: Total time reading                                     |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
+---------------------------------------------------------------------------+
|                                                                             |
|  TRANSACTION MODEL                                                         |
|  Value = Successful purchases/exchanges                                    |
|  +------------------------------------------------------------------+     |
|  | Business Type    | Common North Star Metrics                      |     |
|  |------------------+-----------------------------------------------|     |
|  | E-commerce       | Purchases completed                           |     |
|  | Marketplace      | Transactions/GMV                              |     |
|  | On-demand        | Orders/rides completed                         |     |
|  | Fintech          | Transactions processed                         |     |
|  +------------------------------------------------------------------+     |
|  | Examples:                                                         |     |
|  | - Amazon: Purchases per customer                                 |     |
|  | - Airbnb: Nights booked                                          |     |
|  | - Uber: Rides completed                                          |     |
|  | - Stripe: Transactions processed                                 |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
+---------------------------------------------------------------------------+
|                                                                             |
|  PRODUCTIVITY/SaaS MODEL                                                   |
|  Value = Tasks accomplished / Problems solved                              |
|  +------------------------------------------------------------------+     |
|  | Business Type    | Common North Star Metrics                      |     |
|  |------------------+-----------------------------------------------|     |
|  | Collaboration    | Messages sent / Documents created              |     |
|  | Project Mgmt     | Tasks completed                                |     |
|  | Dev Tools        | Builds/deploys completed                       |     |
|  | Analytics        | Reports/insights generated                     |     |
|  +------------------------------------------------------------------+     |
|  | Examples:                                                         |     |
|  | - Slack: Messages sent                                           |     |
|  | - Notion: Blocks created                                         |     |
|  | - GitHub: Pull requests merged                                   |     |
|  | - Figma: Designs created                                         |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
+---------------------------------------------------------------------------+
|                                                                             |
|  SUBSCRIPTION/RETENTION MODEL                                              |
|  Value = Ongoing engagement that justifies subscription                    |
|  +------------------------------------------------------------------+     |
|  | Business Type    | Common North Star Metrics                      |     |
|  |------------------+-----------------------------------------------|     |
|  | B2B SaaS         | Weekly Active Users / Active accounts          |     |
|  | Consumer Sub     | Sessions per week                              |     |
|  | Membership       | Member visits/uses                             |     |
|  | Education        | Lessons/courses completed                      |     |
|  +------------------------------------------------------------------+     |
|  | Examples:                                                         |     |
|  | - Salesforce: Weekly Active Users                                |     |
|  | - Peloton: Workouts completed                                    |     |
|  | - Duolingo: Lessons completed                                    |     |
|  | - Headspace: Meditations completed                               |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
+---------------------------------------------------------------------------+
|                                                                             |
|  CUSTOMER SUCCESS MODEL                                                    |
|  Value = Customer achieving their goals                                    |
|  +------------------------------------------------------------------+     |
|  | Business Type    | Common North Star Metrics                      |     |
|  |------------------+-----------------------------------------------|     |
|  | Enterprise SaaS  | Customer outcomes achieved                     |     |
|  | Professional Svc | Projects/engagements completed                 |     |
|  | Consulting       | Client goals achieved                          |     |
|  | Training         | Certifications earned                          |     |
|  +------------------------------------------------------------------+     |
|  | Examples:                                                         |     |
|  | - HubSpot: Customers generating leads                            |     |
|  | - Amplitude: Insights actioned                                   |     |
|  | - Gainsight: Accounts with healthy scores                        |     |
|  | - Coursera: Courses completed                                    |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
+---------------------------------------------------------------------------+
```

### Step 3.2: Detailed Examples by Industry

```yaml
detailed_examples:

  # SaaS / B2B
  saas_examples:

    slack:
      north_star: "Messages sent in teams"
      why_it_works:
        - "Captures team communication value"
        - "Leading indicator of stickiness"
        - "Actionable (improve onboarding, integrations)"
      input_metrics:
        - "Teams created"
        - "Users invited"
        - "Channels created"
        - "Integrations connected"

    hubspot:
      north_star: "Weekly Active Teams"
      why_it_works:
        - "Shows teams getting ongoing value"
        - "Combines breadth and engagement"
        - "Predicts retention"
      input_metrics:
        - "Contacts added"
        - "Emails sent"
        - "Deals created"
        - "Automations active"

    zoom:
      north_star: "Weekly meeting participants"
      why_it_works:
        - "Captures core value: meetings held"
        - "Scales with team adoption"
        - "Leading indicator of expansion"
      input_metrics:
        - "Meetings scheduled"
        - "Meeting duration"
        - "Participants per meeting"
        - "Recording usage"

    notion:
      north_star: "Weekly Active Users creating content"
      why_it_works:
        - "Captures value creation, not just viewing"
        - "Indicates product stickiness"
        - "Differentiates active vs passive users"
      input_metrics:
        - "Pages created"
        - "Blocks added"
        - "Team members invited"
        - "Templates used"

  # Marketplaces
  marketplace_examples:

    airbnb:
      north_star: "Nights booked"
      why_it_works:
        - "Core value exchange: accommodation provided"
        - "Captures both sides (host + guest)"
        - "Revenue directly correlates"
      input_metrics:
        - "Listings created"
        - "Searches performed"
        - "Booking requests"
        - "Reviews submitted"

    uber:
      north_star: "Rides completed"
      why_it_works:
        - "Core value: transportation provided"
        - "Two-sided marketplace success"
        - "Actionable by product and ops"
      input_metrics:
        - "Driver availability"
        - "Ride requests"
        - "Estimated wait time"
        - "Driver ratings"

    etsy:
      north_star: "Gross Merchandise Sales"
      why_it_works:
        - "Captures seller success"
        - "Indicates buyer value found"
        - "Marketplace health indicator"
      input_metrics:
        - "Active sellers"
        - "Listings created"
        - "Search-to-purchase rate"
        - "Repeat purchase rate"

  # Consumer / Media
  consumer_examples:

    spotify:
      north_star: "Time spent listening"
      why_it_works:
        - "Direct measure of entertainment value"
        - "Correlates with subscription retention"
        - "Actionable (recommendations, discovery)"
      input_metrics:
        - "Songs played"
        - "Playlists created"
        - "Artists followed"
        - "Podcast episodes completed"

    duolingo:
      north_star: "Daily Active Learners"
      why_it_works:
        - "Learning requires daily practice"
        - "Captures habit formation"
        - "Predicts long-term retention"
      input_metrics:
        - "Lessons completed"
        - "Streak days"
        - "XP earned"
        - "Courses started"

    medium:
      north_star: "Total Time Reading"
      why_it_works:
        - "Core value: reading quality content"
        - "Indicates content resonance"
        - "Publisher value creation"
      input_metrics:
        - "Articles read"
        - "Claps given"
        - "Following relationships"
        - "Newsletter subscriptions"

  # E-commerce / DTC
  ecommerce_examples:

    amazon:
      north_star: "Purchases per active customer"
      why_it_works:
        - "Measures repeat value delivery"
        - "Indicates customer satisfaction"
        - "Combines acquisition and retention"
      input_metrics:
        - "Products viewed"
        - "Cart additions"
        - "Conversion rate"
        - "Prime membership rate"

    stitch_fix:
      north_star: "Items kept per fix"
      why_it_works:
        - "Direct measure of styling success"
        - "Customer got clothes they love"
        - "Predicts repeat orders"
      input_metrics:
        - "Style profile completeness"
        - "Feedback submitted"
        - "Items tried"
        - "Fix frequency"
```

---

## PHASE 4: INPUT METRICS TREE

### Step 4.1: The North Star Framework

```
+---------------------------------------------------------------------------+
|                      THE NORTH STAR FRAMEWORK                              |
+---------------------------------------------------------------------------+
|                                                                             |
|                         +-------------------+                               |
|                         |   NORTH STAR      |                               |
|                         |     METRIC        |                               |
|                         +-------------------+                               |
|                                  |                                          |
|                                  |                                          |
|            +---------------------+---------------------+                    |
|            |                     |                     |                    |
|     +------v------+       +------v------+       +------v------+            |
|     |   INPUT     |       |   INPUT     |       |   INPUT     |            |
|     |  METRIC 1   |       |  METRIC 2   |       |  METRIC 3   |            |
|     | (Breadth)   |       | (Depth)     |       | (Frequency) |            |
|     +-------------+       +-------------+       +-------------+            |
|            |                     |                     |                    |
|    +-------+-------+     +-------+-------+     +-------+-------+           |
|    |       |       |     |       |       |     |       |       |           |
|   Sub     Sub     Sub   Sub     Sub     Sub   Sub     Sub     Sub          |
|  Input   Input   Input Input   Input   Input Input   Input   Input         |
|                                                                             |
+---------------------------------------------------------------------------+
|                                                                             |
|  INPUT METRIC CATEGORIES:                                                  |
|                                                                             |
|  1. BREADTH - How many users/customers?                                    |
|     - Total active users                                                   |
|     - New users acquired                                                   |
|     - Retained users                                                       |
|                                                                             |
|  2. DEPTH - How much value per user?                                       |
|     - Actions per user                                                     |
|     - Features used per user                                               |
|     - Value received per user                                              |
|                                                                             |
|  3. FREQUENCY - How often do users engage?                                 |
|     - Sessions per week                                                    |
|     - Return rate                                                          |
|     - Time between sessions                                                |
|                                                                             |
|  4. EFFICIENCY - How well do we convert?                                   |
|     - Conversion rates                                                     |
|     - Time to value                                                        |
|     - Success rates                                                        |
|                                                                             |
+---------------------------------------------------------------------------+
```

### Step 4.2: Building Your Input Metrics Tree

```yaml
input_metrics_template:

  north_star_metric: "____________________"

  definition:
    what_it_measures: "____________________"
    how_calculated: "____________________"
    measurement_frequency: "daily / weekly / monthly"

  input_metrics:

    breadth:
      name: "____________________"
      description: "How many users are in the system?"
      sub_inputs:
        - sub_input_1: "____________________"
        - sub_input_2: "____________________"
        - sub_input_3: "____________________"
      team_owner: "____________________"

    depth:
      name: "____________________"
      description: "How much value does each user get?"
      sub_inputs:
        - sub_input_1: "____________________"
        - sub_input_2: "____________________"
        - sub_input_3: "____________________"
      team_owner: "____________________"

    frequency:
      name: "____________________"
      description: "How often do users engage?"
      sub_inputs:
        - sub_input_1: "____________________"
        - sub_input_2: "____________________"
        - sub_input_3: "____________________"
      team_owner: "____________________"

    efficiency:
      name: "____________________"
      description: "How well do we convert interest to action?"
      sub_inputs:
        - sub_input_1: "____________________"
        - sub_input_2: "____________________"
        - sub_input_3: "____________________"
      team_owner: "____________________"
```

### Step 4.3: Example Input Metrics Trees

```yaml
example_tree_slack:

  north_star: "Messages sent in Slack"

  input_metrics:

    breadth:
      name: "Weekly Active Teams"
      sub_inputs:
        - "New teams created"
        - "Teams onboarded (>10 users)"
        - "Retained teams (active 4+ weeks)"
      team_owner: "Growth"

    depth:
      name: "Messages per active user"
      sub_inputs:
        - "Users sending 10+ messages/week"
        - "Channels per team"
        - "Integrations per team"
      team_owner: "Product"

    frequency:
      name: "Daily engagement rate"
      sub_inputs:
        - "DAU/WAU ratio"
        - "Days active per week"
        - "Sessions per day"
      team_owner: "Product"

    efficiency:
      name: "Activation rate"
      sub_inputs:
        - "% reaching 2,000 team messages"
        - "Time to first 100 messages"
        - "% inviting teammates"
      team_owner: "Growth"

example_tree_education_platform:

  north_star: "Courses completed"

  input_metrics:

    breadth:
      name: "Active learners"
      sub_inputs:
        - "New enrollments"
        - "Returning learners"
        - "Retained learners (30-day)"
      team_owner: "Growth"

    depth:
      name: "Progress per learner"
      sub_inputs:
        - "Lessons completed per course"
        - "Assessment scores"
        - "Projects submitted"
      team_owner: "Learning Design"

    frequency:
      name: "Learning sessions per week"
      sub_inputs:
        - "Sessions per learner"
        - "Streak maintenance rate"
        - "Weekly active rate"
      team_owner: "Product"

    efficiency:
      name: "Completion rate"
      sub_inputs:
        - "Module completion rate"
        - "Course dropout points"
        - "Time to completion"
      team_owner: "Learning Design"

example_tree_saas_analytics:

  north_star: "Insights actioned"

  input_metrics:

    breadth:
      name: "Active accounts using analytics"
      sub_inputs:
        - "Accounts with data connected"
        - "Accounts with active dashboards"
        - "Users viewing reports weekly"
      team_owner: "Customer Success"

    depth:
      name: "Reports created per account"
      sub_inputs:
        - "Custom dashboards created"
        - "Queries run"
        - "Segments defined"
      team_owner: "Product"

    frequency:
      name: "Weekly analysis sessions"
      sub_inputs:
        - "Logins per user"
        - "Time in product"
        - "Reports exported/shared"
      team_owner: "Product"

    efficiency:
      name: "Insight-to-action rate"
      sub_inputs:
        - "Alerts configured"
        - "Integrations triggered"
        - "Recommendations implemented"
      team_owner: "Product"
```

---

## PHASE 5: VALIDATION CHECKLIST

### Step 5.1: Pre-Adoption Validation

Before committing to a North Star Metric, validate it against these criteria:

```
+---------------------------------------------------------------------------+
|                    NORTH STAR VALIDATION CHECKLIST                         |
+---------------------------------------------------------------------------+
|                                                                             |
|  FUNDAMENTAL CRITERIA                                                      |
|  +------------------------------------------------------------------+     |
|  |                                                                    |     |
|  | [ ] Reflects Customer Value                                       |     |
|  |     Does improving this metric mean customers get more value?     |     |
|  |                                                                    |     |
|  | [ ] Is Leading Indicator                                          |     |
|  |     Does it move before revenue moves?                            |     |
|  |                                                                    |     |
|  | [ ] Is Actionable                                                 |     |
|  |     Can teams directly influence it through their work?           |     |
|  |                                                                    |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
|  PRACTICAL CRITERIA                                                        |
|  +------------------------------------------------------------------+     |
|  |                                                                    |     |
|  | [ ] Measurable Today                                              |     |
|  |     Can we track this metric with current data infrastructure?    |     |
|  |                                                                    |     |
|  | [ ] Not Gameable                                                  |     |
|  |     Is it hard to artificially inflate without real value?        |     |
|  |                                                                    |     |
|  | [ ] Simple to Explain                                             |     |
|  |     Can anyone explain it in under 30 seconds?                    |     |
|  |                                                                    |     |
|  | [ ] Has Right Frequency                                           |     |
|  |     Does it move fast enough to inform decisions?                 |     |
|  |                                                                    |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
|  CORRELATION CRITERIA                                                      |
|  +------------------------------------------------------------------+     |
|  |                                                                    |     |
|  | [ ] Correlates with Retention                                     |     |
|  |     Users who achieve higher NSM retain better                    |     |
|  |                                                                    |     |
|  | [ ] Correlates with Revenue                                       |     |
|  |     NSM improvements lead to revenue improvements                 |     |
|  |                                                                    |     |
|  | [ ] Correlates with Referral                                      |     |
|  |     High-NSM users refer more                                     |     |
|  |                                                                    |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
|  ALIGNMENT CRITERIA                                                        |
|  +------------------------------------------------------------------+     |
|  |                                                                    |     |
|  | [ ] All Teams Can Contribute                                      |     |
|  |     Every team can see how their work impacts the NSM             |     |
|  |                                                                    |     |
|  | [ ] Leadership Buy-In                                             |     |
|  |     Executives committed to using this as primary metric          |     |
|  |                                                                    |     |
|  | [ ] No Conflicting Goals                                          |     |
|  |     Other metrics don't work against the NSM                      |     |
|  |                                                                    |     |
|  +------------------------------------------------------------------+     |
|                                                                             |
|  SCORE: ___/12 criteria passed                                             |
|                                                                             |
|  RECOMMENDATION:                                                           |
|  - 12/12: Strong NSM candidate, proceed with confidence                   |
|  - 9-11: Good candidate, minor refinements may be needed                  |
|  - 6-8:  Needs more work, address gaps before adopting                    |
|  - <6:   Not ready, continue exploring alternatives                       |
|                                                                             |
+---------------------------------------------------------------------------+
```

### Step 5.2: Correlation Analysis

```yaml
correlation_validation:

  purpose: "Verify NSM correlates with business outcomes"

  retention_correlation:
    analysis:
      - "Segment users by NSM achievement level"
      - "Compare retention rates across segments"
      - "Look for statistically significant differences"
    expected_pattern:
      - "High-NSM users retain 2-5x better"
      - "Clear threshold effect (e.g., 10+ actions = stickiness)"
    red_flags:
      - "No correlation between NSM and retention"
      - "High-NSM users churn as much as low-NSM"

  revenue_correlation:
    analysis:
      - "Track NSM changes over time"
      - "Compare with revenue changes (with lag)"
      - "Look for leading indicator relationship"
    expected_pattern:
      - "NSM increases precede revenue increases by 2-4 weeks"
      - "NSM dips predict revenue dips"
    red_flags:
      - "NSM and revenue move independently"
      - "Revenue moves first (NSM is lagging)"

  referral_correlation:
    analysis:
      - "Identify users who referred others"
      - "Compare their NSM levels vs non-referrers"
      - "Look for threshold that predicts referral"
    expected_pattern:
      - "Referrers have 2-3x higher NSM"
      - "Clear NSM level that triggers referral behavior"
    red_flags:
      - "No relationship between NSM and referrals"
      - "Referral happens before NSM achievement"
```

### Step 5.3: Stress Testing

```yaml
stress_tests:

  gaming_test:
    question: "Could we artificially inflate this metric without delivering real value?"
    examples_of_gameable:
      - "Page views (can add auto-refresh)"
      - "Signups (can incentivize low-quality)"
      - "Sessions (can force logouts)"
    examples_of_not_gameable:
      - "Messages sent by others to you"
      - "Items purchased"
      - "Courses completed with assessment"
    action_if_gameable: "Add quality filter or change metric"

  ceiling_test:
    question: "Is there a natural ceiling that limits growth?"
    examples_of_ceiling:
      - "DAU can't exceed registered users"
      - "Purchases per customer has limits"
    mitigation: "Consider compound metrics or growth rate"

  sensitivity_test:
    question: "Is the metric sensitive enough to show progress?"
    examples_of_insensitive:
      - "Annual metrics (move too slow)"
      - "Large aggregate numbers (small changes invisible)"
    mitigation: "Break into segments or shorter time periods"

  conflict_test:
    question: "Could optimizing this metric hurt other important outcomes?"
    examples_of_conflict:
      - "Maximizing engagement might hurt well-being"
      - "Maximizing messages might reduce quality"
    mitigation: "Add guardrail metrics"
```

---

## PHASE 6: OPERATIONALIZATION

### Step 6.1: Measurement Setup

```yaml
measurement_setup:

  data_requirements:
    events_to_track:
      - event_name: "____________________"
        description: "____________________"
        properties: ["property1", "property2"]
      - event_name: "____________________"
        description: "____________________"
        properties: ["property1", "property2"]

    calculation_logic:
      formula: "____________________"
      aggregation: "daily / weekly / monthly"
      segments: ["segment1", "segment2"]

    data_source: "____________________"
    update_frequency: "____________________"
    historical_data_available: "yes / no / partial"

  dashboard_requirements:
    primary_visualization:
      type: "line chart / bar chart / gauge"
      timeframe: "last 30 days / last 12 weeks / custom"
      comparison: "vs previous period / vs target"

    drill_down_views:
      - "By segment"
      - "By cohort"
      - "By input metric"

    alerts:
      - condition: "NSM drops >10% week over week"
        notification: "email to leadership"
      - condition: "NSM below target for 2+ weeks"
        notification: "slack to product team"
```

### Step 6.2: Team Alignment Document

```yaml
alignment_document_template:

  north_star_definition:
    metric_name: "____________________"
    definition: "____________________"
    calculation: "____________________"
    why_this_metric: "____________________"

  current_state:
    baseline_value: "____________________"
    trend: "improving / stable / declining"
    segments_breakdown:
      - segment: "____________________"
        value: "____________________"

  targets:
    quarterly_target: "____________________"
    annual_target: "____________________"
    rationale: "____________________"

  input_metrics:
    - input: "____________________"
      owner: "____________________"
      target: "____________________"
    - input: "____________________"
      owner: "____________________"
      target: "____________________"

  guardrail_metrics:
    - metric: "____________________"
      threshold: "____________________"
      why: "____________________"

  review_cadence:
    frequency: "weekly / bi-weekly / monthly"
    attendees: "____________________"
    agenda: "Review NSM, input metrics, blockers, experiments"
```

### Step 6.3: Communication Plan

```yaml
communication_plan:

  launch_announcement:
    audience: "All company"
    channel: "All-hands / email / wiki"
    content:
      - "What is our North Star Metric"
      - "Why we chose it"
      - "How each team connects to it"
      - "Where to track it"

  ongoing_communication:
    weekly:
      - "NSM update in team standup"
      - "Dashboard link in weekly digest"
    monthly:
      - "NSM deep dive in all-hands"
      - "Progress vs target"
      - "Top wins and learnings"
    quarterly:
      - "NSM review in board meeting"
      - "Trend analysis"
      - "Input metric correlation review"

  reinforcement:
    meeting_mentions: "Start key meetings with NSM update"
    decision_framing: "How does this decision impact NSM?"
    experiment_focus: "Experiments should connect to NSM or inputs"
```

---

## Elicitation Questions

Before defining your North Star Metric, gather this information:

### Business Context

```yaml
elicitation:

  business_basics:
    - "What does your product do in one sentence?"
    - "What is your business model? (SaaS, marketplace, e-commerce, etc.)"
    - "Who is your primary customer segment?"
    - "What is your current stage? (pre-PMF, scaling, mature)"

  value_proposition:
    - "What problem do you solve for customers?"
    - "What do customers say they love most about your product?"
    - "What would customers miss most if your product disappeared?"
    - "What's the 'aha moment' when customers realize your value?"

  current_metrics:
    - "What metrics do you currently track most closely?"
    - "What metric would hurt most if it dropped 50%?"
    - "What metric would you celebrate most if it doubled?"
    - "Do different teams focus on different metrics?"

  data_availability:
    - "What user behavior data do you have access to?"
    - "Can you segment users by behavior and outcomes?"
    - "Do you have cohort analysis capabilities?"
    - "What's your current analytics stack?"
```

### Workshop Logistics

```yaml
logistics_questions:

  participation:
    - "Who needs to be in the workshop?"
    - "Who has decision-making authority on metrics?"
    - "Who will own the NSM after it's defined?"
    - "What's the best time for a half-day session?"

  preparation:
    - "What data can you pull before the workshop?"
    - "Have you done any customer research recently?"
    - "Is there existing documentation on product strategy?"
    - "Any previous attempts at defining key metrics?"

  constraints:
    - "Are there any metrics leadership is attached to?"
    - "Any political considerations around metrics?"
    - "What's the timeline for implementing the NSM?"
    - "What resources are available for measurement setup?"
```

---

## Output Format

### North Star Metric Definition Document

```markdown
# North Star Metric Definition
## [PRODUCT NAME] - [DATE]

### Executive Summary

**North Star Metric:** [METRIC NAME]

**Definition:** [One sentence explanation]

**Current Value:** [X]
**Target (Quarterly):** [X]
**Target (Annual):** [X]

### Why This Metric?

[2-3 sentences explaining why this captures customer value and predicts success]

---

### Metric Details

| Attribute | Value |
|-----------|-------|
| Metric Name | [Name] |
| Calculation | [Formula] |
| Measurement Frequency | [Daily/Weekly/Monthly] |
| Data Source | [System] |
| Owner | [Team/Person] |

---

### Input Metrics Tree

```
                    [NORTH STAR METRIC]
                           |
         +-----------------+-----------------+
         |                 |                 |
    [INPUT 1]         [INPUT 2]         [INPUT 3]
    (Breadth)          (Depth)         (Frequency)
         |                 |                 |
    +----|----+       +----|----+       +----|----+
    |    |    |       |    |    |       |    |    |
   Sub  Sub  Sub     Sub  Sub  Sub     Sub  Sub  Sub
```

**Input Metrics:**

| Input | Owner | Current | Target |
|-------|-------|---------|--------|
| [Input 1] | [Team] | [X] | [Y] |
| [Input 2] | [Team] | [X] | [Y] |
| [Input 3] | [Team] | [X] | [Y] |

---

### Guardrail Metrics

| Metric | Threshold | Action if Breached |
|--------|-----------|-------------------|
| [Metric 1] | [Threshold] | [Action] |
| [Metric 2] | [Threshold] | [Action] |

---

### Validation Results

- [x] Reflects Customer Value
- [x] Is Leading Indicator
- [x] Is Actionable
- [x] Correlates with Retention
- [x] Correlates with Revenue
- [x] Not Gameable
- [x] Simple to Explain

**Validation Score:** [X]/12

---

### Review Schedule

| Cadence | Forum | Owner |
|---------|-------|-------|
| Weekly | Team Standup | [Name] |
| Monthly | All-Hands | [Name] |
| Quarterly | Board Review | [Name] |

---

### Next Steps

1. [ ] Set up tracking in [analytics tool]
2. [ ] Build dashboard with input metrics
3. [ ] Communicate to all teams
4. [ ] Schedule first review meeting
```

---

## Examples

### Example 1: B2B SaaS Project Management Tool

```
CONTEXT:
- Product: Project management tool for agencies
- Business model: Per-seat SaaS subscription
- Stage: Post-PMF, scaling
- Current metrics: MRR, DAU, Projects created

WORKSHOP OUTCOME:

North Star Metric: "Projects completed"

WHY:
- Captures core value: helping teams finish work
- Leading indicator: completed projects drive renewals
- Actionable: product can improve completion tools

INPUT METRICS TREE:
                    Projects Completed
                           |
         +-----------------+-----------------+
         |                 |                 |
    Active Teams       Tasks/Project     Completion Rate
         |                 |                 |
    +----+----+       +----+----+       +----+----+
    |    |    |       |    |    |       |    |    |
   New  Ret  Exp     Tasks Assign  Collab  Time   Blocks

VALIDATION:
- Teams with 5+ completed projects retain 3.2x better
- Completion rate correlates 0.78 with NPS
- Not gameable (requires real work)
- All teams can influence (Product: UX, Growth: onboarding, CS: adoption)

TARGETS:
- Current: 12,000 projects/month
- Q1 Target: 15,000 (+25%)
- Annual Target: 25,000 (+108%)
```

### Example 2: Consumer Education App

```
CONTEXT:
- Product: Language learning app
- Business model: Freemium + subscription
- Stage: Growth stage
- Current metrics: Downloads, DAU, Lessons started

WORKSHOP OUTCOME:

North Star Metric: "Weekly Active Learners completing lessons"

WHY:
- Captures value: learning requires completion, not just starting
- Leading indicator: lesson completion predicts subscription
- Actionable: can improve content, gamification, reminders

INPUT METRICS TREE:
                Weekly Active Learners Completing
                              |
         +--------------------+--------------------+
         |                    |                    |
    Active Learners     Lessons/Learner     Completion Rate
         |                    |                    |
    +----+----+          +----+----+          +----+----+
    |    |    |          |    |    |          |    |    |
   New  Ret  React      Daily  Streak       Finish  Engage

VALIDATION:
- Users completing 7+ lessons/week convert to paid 4.1x
- 30-day retention 2.8x higher for high-completers
- Gamification increases completion without gaming metric
- Product, Growth, and Content teams can all impact

TARGETS:
- Current: 450,000 WAL completing
- Q1 Target: 550,000 (+22%)
- Annual Target: 900,000 (+100%)
```

### Example 3: B2B Marketplace

```
CONTEXT:
- Product: Freelancer marketplace for creative services
- Business model: Transaction fee (15%)
- Stage: Approaching PMF
- Current metrics: GMV, Active buyers, Active freelancers

WORKSHOP OUTCOME:

North Star Metric: "Successful projects delivered"

WHY:
- Captures two-sided value: client got deliverable, freelancer got paid
- Leading indicator: successful delivery drives repeat usage
- Better than GMV: quality matters, not just volume

INPUT METRICS TREE:
              Successful Projects Delivered
                          |
         +----------------+----------------+
         |                |                |
    Active Clients   Projects/Client   Success Rate
         |                |                |
    +----+----+      +----+----+      +----+----+
    |    |    |      |    |    |      |    |    |
   New  Ret  Exp    Jobs  Hire  Rehire  Qual  Time

VALIDATION:
- Clients with 3+ successful projects retain 5.2x
- Freelancers with 5+ successful projects earn 3x
- Success rate correlates 0.82 with referral rate
- Not gameable (requires genuine completion)

TARGETS:
- Current: 2,800 projects/month
- Q1 Target: 3,500 (+25%)
- Annual Target: 6,000 (+114%)
```

---

## Integration

### Related Tasks

- **run-pmf-test.md** - PMF test helps identify what drives value
- **calculate-clv.md** - CLV should correlate with NSM achievement
- **design-health-score.md** - Health score inputs often overlap with NSM inputs
- **create-dashboard.md** - Dashboard should feature NSM prominently
- **run-growth-experiment.md** - Experiments should target NSM or inputs

### Related Agents

- **sean-ellis** - Primary methodology owner
- **peter-fader** - Customer value perspective
- **avinash-kaushik** - Metrics hierarchy and dashboard design

### Related Checklists

- **customer-360-checklist.md** - Data infrastructure for NSM tracking

---

## Common Pitfalls

### Pitfall 1: Choosing Revenue as NSM

```yaml
mistake:
  description: "Using MRR, ARR, or GMV as North Star"
  why_tempting: "Revenue is what business ultimately cares about"
  why_wrong:
    - "Revenue is lagging - moves after value delivered"
    - "Can't distinguish healthy growth from unsustainable growth"
    - "Teams can't directly influence revenue (except sales)"
  solution: "Find the metric that PREDICTS revenue"
```

### Pitfall 2: Choosing Vanity Metrics

```yaml
mistake:
  description: "Using total users, downloads, or registrations"
  why_tempting: "Numbers are big and always going up"
  why_wrong:
    - "Includes inactive and churned users"
    - "Doesn't indicate value delivery"
    - "Can grow while business declines"
  solution: "Add engagement qualifier (active, completed, etc.)"
```

### Pitfall 3: Too Many North Stars

```yaml
mistake:
  description: "Having 2-3 'North Star' metrics"
  why_tempting: "Hard to choose just one, multiple feel safer"
  why_wrong:
    - "Defeats the purpose of alignment"
    - "Teams optimize for different metrics"
    - "Conflicts between metrics cause confusion"
  solution: "One NSM, multiple input metrics"
```

### Pitfall 4: Not Validating Correlation

```yaml
mistake:
  description: "Assuming NSM correlates with outcomes"
  why_tempting: "Logic suggests it should correlate"
  why_wrong:
    - "Gut feeling often wrong"
    - "May optimize for wrong thing"
    - "Waste resources on false signal"
  solution: "Run correlation analysis before committing"
```

### Pitfall 5: Set and Forget

```yaml
mistake:
  description: "Defining NSM and never revisiting"
  why_tempting: "Stability feels good, change is hard"
  why_wrong:
    - "Business evolves, NSM should too"
    - "May hit ceiling on current NSM"
    - "Correlation may weaken over time"
  solution: "Review NSM quarterly, change if needed"
```

---

## Sean Ellis's Final Wisdom

```
+---------------------------------------------------------------------------+
|                    SEAN ELLIS'S NORTH STAR PRINCIPLES                      |
+---------------------------------------------------------------------------+
|                                                                             |
|  "The North Star Metric isn't just a number to track. It's a way of        |
|   thinking. Every decision, every feature, every experiment should         |
|   ultimately connect back to this one metric."                             |
|                                                                             |
|  1. START WITH VALUE                                                       |
|     "Don't start with 'what can we measure?' Start with 'what value        |
|      do we deliver?' The metric follows the value, not the other way."     |
|                                                                             |
|  2. INPUT METRICS ARE YOUR LEVERS                                          |
|     "The North Star tells you where you're going. The input metrics        |
|      are what you actually work on. Every team should own an input."       |
|                                                                             |
|  3. EXPECT IT TO CHANGE                                                    |
|     "Your North Star at seed stage won't be your North Star at Series C.   |
|      As your product and market evolve, so should your metric."            |
|                                                                             |
|  4. ALIGNMENT > PRECISION                                                  |
|     "A slightly imperfect metric that everyone understands and aligns to   |
|      is better than a perfect metric that nobody uses."                    |
|                                                                             |
|  5. CELEBRATE PUBLICLY                                                     |
|     "When the North Star moves up, celebrate. When it moves down,          |
|      investigate. Make it the heartbeat of your company."                  |
|                                                                             |
|  FINAL THOUGHT:                                                            |
|  "The companies that win aren't the ones with the most metrics.            |
|   They're the ones with the clearest focus. One metric, understood         |
|   by everyone, driving every decision. That's the North Star."             |
|                                                                             |
+---------------------------------------------------------------------------+
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
      - "North Star criteria documented"
      - "Workshop format included"
      - "Common NSMs by business model"
      - "Input metrics tree framework"
      - "Comprehensive validation checklist"
      - "3 real-world examples"
      - "Common pitfalls documented"
```
