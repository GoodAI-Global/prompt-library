# Trend Interpretation

## Use Case

Interpret data trends and translate them into actionable business insights:
- Time series pattern explanation
- Business metric trending analysis
- Performance trajectory assessment
- Forecasting context for decision-makers

Use when presenting trend data to stakeholders who need to understand implications and make decisions.

## Input Format

**Required:**
- `trend_data`: Time series or trend data with values over time
- `metric_context`: What the metric represents and why it matters

**Optional:**
- `comparison_data`: Benchmarks, targets, or comparison periods
- `external_context`: Market conditions, events, or factors
- `business_goals`: Relevant targets or objectives
- `audience`: Technical level of recipients

## Output Format

```json
{
  "trend_summary": {
    "metric": "monthly_recurring_revenue",
    "period": "Q4 2023",
    "direction": "increasing",
    "rate": "+8.5% quarter-over-quarter",
    "significance": "above_target"
  },
  "pattern_analysis": {
    "overall_direction": "upward",
    "velocity": "accelerating",
    "volatility": "low",
    "seasonality": "detected",
    "inflection_points": [...]
  },
  "interpretation": {
    "what_the_data_shows": "Plain language description",
    "what_it_means": "Business implications",
    "key_drivers": ["Driver 1", "Driver 2"],
    "risks_and_opportunities": [...]
  },
  "projections": {
    "if_trend_continues": "Expected outcome",
    "confidence": 0.75,
    "scenarios": {...}
  },
  "recommendations": [...],
  "stakeholder_narrative": {
    "headline": "One line summary",
    "executive_summary": "2-3 sentences",
    "detailed_analysis": "Full explanation"
  }
}
```

## The Prompt

```
You are a business analyst interpreting data trends. Translate patterns into clear, actionable insights for decision-makers.

TREND DATA:
{{trend_data}}

METRIC CONTEXT:
{{metric_context}}

{{#if comparison_data}}
COMPARISON DATA:
{{comparison_data}}
{{/if}}

{{#if external_context}}
EXTERNAL CONTEXT:
{{external_context}}
{{/if}}

{{#if business_goals}}
BUSINESS GOALS:
{{business_goals}}
{{/if}}

AUDIENCE: {{audience | default: "business"}}

TREND INTERPRETATION FRAMEWORK:

1. PATTERN IDENTIFICATION
   Direction:
   - Increasing / Decreasing / Flat
   - Consistent / Volatile
   - Seasonal / Cyclical / Random

   Velocity:
   - Accelerating: Rate of change increasing
   - Decelerating: Rate of change decreasing
   - Linear: Constant rate of change

   Key points:
   - Inflection points (where direction changed)
   - Peaks and troughs
   - Breakouts from historical range

2. CONTEXTUALIZATION
   Compare to:
   - Historical performance (YoY, QoQ)
   - Targets/budgets
   - Industry benchmarks
   - Competitors if available
   - Related metrics

3. DRIVER ANALYSIS
   Identify what's driving the trend:
   - Internal factors (actions taken)
   - External factors (market conditions)
   - Structural changes
   - Temporary effects

4. IMPLICATIONS
   What does this mean for:
   - Business performance
   - Strategic objectives
   - Resource allocation
   - Risk exposure
   - Opportunities

5. PROJECTION
   If the trend continues:
   - Where will we be in 3/6/12 months?
   - What's the confidence level?
   - What could accelerate or reverse the trend?

   Scenarios:
   - Optimistic: Trend accelerates
   - Base case: Trend continues
   - Pessimistic: Trend reverses

6. ACTIONABILITY
   Recommendations:
   - Capitalize on positive trends
   - Address negative trends
   - Investigate unclear patterns
   - Monitor for changes

COMMUNICATION GUIDELINES:
- Lead with the insight, not the data
- Use comparisons for context
- Quantify implications where possible
- Distinguish correlation from causation
- Acknowledge uncertainty
- Make recommendations specific

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{trend_data}}` | string | Yes | Time series or trend data |
| `{{metric_context}}` | string | Yes | What the metric represents |
| `{{comparison_data}}` | string | No | Benchmarks or comparisons |
| `{{external_context}}` | string | No | External factors |
| `{{business_goals}}` | string | No | Targets or objectives |
| `{{audience}}` | string | No | Audience technical level |

## Examples

### Example 1: SaaS Growth Metrics

**Input:**
```
trend_data: |
  Monthly Recurring Revenue (MRR):
  Jul 2023: $850,000
  Aug 2023: $878,000
  Sep 2023: $912,000
  Oct 2023: $965,000
  Nov 2023: $1,020,000
  Dec 2023: $1,085,000
  Jan 2024: $1,142,000

  Net Revenue Retention (NRR):
  Jul 2023: 108%
  Aug 2023: 110%
  Sep 2023: 112%
  Oct 2023: 115%
  Nov 2023: 116%
  Dec 2023: 118%
  Jan 2024: 119%

  Customer Acquisition:
  Jul 2023: 42 new customers
  Aug 2023: 45 new customers
  Sep 2023: 38 new customers
  Oct 2023: 52 new customers
  Nov 2023: 48 new customers
  Dec 2023: 35 new customers
  Jan 2024: 55 new customers

metric_context: |
  B2B SaaS company, enterprise segment
  MRR is primary revenue metric
  NRR measures expansion revenue health
  Industry benchmark NRR: 110%
  Target: $1.5M MRR by end of 2024

comparison_data: |
  Same period last year:
  Jul 2022: $520,000 MRR
  Jan 2023: $680,000 MRR
  YoY growth: 68%

  Industry peers (similar stage):
  Average MRR growth: 45% YoY
  Average NRR: 110%

business_goals: |
  2024 Goals:
  - Reach $1.5M MRR
  - Maintain NRR above 115%
  - Expand to 500 total customers (currently at 380)
```

**Output:**
```json
{
  "trend_summary": {
    "metric": "Monthly Recurring Revenue (MRR)",
    "period": "July 2023 - January 2024",
    "direction": "strong_increase",
    "rate": {
      "six_month_growth": "+34.4% ($850K → $1,142K)",
      "average_monthly_growth": "+5.0%",
      "yoy_growth": "+68%"
    },
    "significance": "exceeding_industry_benchmarks"
  },
  "pattern_analysis": {
    "overall_direction": "upward",
    "velocity": "accelerating",
    "trajectory": "MRR added $50K+ monthly since October, up from $28-34K earlier",
    "volatility": "low",
    "seasonality": {
      "detected": true,
      "pattern": "December acquisition dip typical for enterprise (holiday slowdown)"
    },
    "inflection_points": [
      {
        "month": "October 2023",
        "event": "Growth acceleration",
        "detail": "Monthly MRR gain jumped from ~$34K to $53K"
      }
    ]
  },
  "interpretation": {
    "what_the_data_shows": "MRR has grown 34% in 6 months, accelerating in Q4. NRR improved steadily from 108% to 119%, indicating healthy expansion within existing customers. New customer acquisition is volatile but trending upward with strong January.",
    "what_it_means": "The business is executing well on both growth vectors: acquiring new customers and expanding existing ones. At current trajectory, $1.5M MRR goal is achievable by Q3 2024, ahead of year-end target.",
    "key_drivers": [
      "Exceptional NRR (119% vs 110% industry) - customers are expanding significantly",
      "New customer acquisition picking up (55 in January vs 42 average)",
      "October inflection suggests product/sales improvements taking effect"
    ],
    "performance_vs_peers": "Growing 68% YoY vs industry average 45% - significantly outperforming peers"
  },
  "supporting_metrics": [
    {
      "metric": "Net Revenue Retention",
      "trend": "steadily_increasing",
      "current": "119%",
      "interpretation": "Every $100 of ARR from 12 months ago is now worth $119. This is exceptional and indicates strong product value and expansion motion.",
      "implication": "High NRR means the customer base is becoming more valuable over time, reducing pressure on new acquisition."
    },
    {
      "metric": "Customer Acquisition",
      "trend": "volatile_upward",
      "interpretation": "Month-to-month variation is normal for enterprise sales. December dip (35) is typical holiday pattern. January rebound (55) is encouraging.",
      "concern": "Watch for sustained acquisition >45/month to hit 500 customer goal"
    }
  ],
  "projections": {
    "if_trend_continues": {
      "projection": "$1.5M MRR by August-September 2024",
      "method": "Linear extrapolation at 5% monthly growth",
      "confidence": 0.75
    },
    "scenarios": {
      "optimistic": {
        "outcome": "$1.65M MRR by Dec 2024",
        "assumption": "Growth accelerates to 6% monthly, NRR stays 118%+",
        "probability": 0.25
      },
      "base_case": {
        "outcome": "$1.5M MRR by Sep 2024",
        "assumption": "Current 5% monthly growth continues",
        "probability": 0.50
      },
      "pessimistic": {
        "outcome": "$1.35M MRR by Dec 2024",
        "assumption": "Growth decelerates to 3% monthly, some churn increase",
        "probability": 0.25
      }
    },
    "goal_assessment": {
      "goal": "$1.5M MRR by Dec 2024",
      "status": "on_track_to_exceed",
      "expected_achievement": "3-4 months early"
    }
  },
  "risks_and_opportunities": {
    "risks": [
      {
        "risk": "NRR sustainability",
        "detail": "119% is exceptional but may be hard to maintain as base grows",
        "mitigation": "Monitor cohort NRR, ensure expansion playbook is documented"
      },
      {
        "risk": "Acquisition volatility",
        "detail": "Month-to-month swings could create lumpy quarters",
        "mitigation": "Pipeline visibility and sales capacity planning"
      }
    ],
    "opportunities": [
      {
        "opportunity": "Accelerate investment given strong NRR",
        "detail": "With 119% NRR, each customer acquired is worth more over time",
        "action": "Consider increasing acquisition spend for faster growth"
      },
      {
        "opportunity": "Early goal achievement",
        "detail": "Likely to hit $1.5M by Q3, creating room for stretch goal",
        "action": "Consider setting $1.65M-$1.75M as new target"
      }
    ]
  },
  "recommendations": [
    {
      "priority": "high",
      "action": "Document and scale the expansion playbook",
      "rationale": "119% NRR is exceptional - ensure this is repeatable as team grows"
    },
    {
      "priority": "high",
      "action": "Review and potentially increase acquisition investment",
      "rationale": "Strong NRR makes customer acquisition more valuable than average"
    },
    {
      "priority": "medium",
      "action": "Investigate October inflection point",
      "rationale": "Understanding what changed can help maintain momentum"
    },
    {
      "priority": "medium",
      "action": "Set stretch goal for $1.65M+ given trajectory",
      "rationale": "Base goal now looks conservative"
    }
  ],
  "stakeholder_narrative": {
    "headline": "MRR growth accelerating, on track to exceed 2024 goal by Q3",
    "executive_summary": "We grew MRR 34% in the past 6 months to $1.14M, with growth accelerating since October. Our 119% NRR significantly exceeds the 110% industry benchmark, meaning existing customers are expanding rapidly. At current trajectory, we'll hit our $1.5M goal 3-4 months early—recommend setting a stretch target.",
    "detailed_analysis": "Three factors are driving outperformance: (1) Exceptional NRR at 119% indicates strong product-market fit and successful expansion motion—every cohort is worth more over time. (2) New customer acquisition trending upward with January's 55 new customers being a strong start to the year. (3) An inflection point in October accelerated monthly MRR growth from ~$30K to $55K+. We're growing 68% YoY vs 45% industry average. Key risk is NRR sustainability at this level; key opportunity is investing more in acquisition given the strong unit economics."
  }
}
```

## Gotchas

### Common Failure Modes
1. **Extrapolation overconfidence**: Trends don't continue forever.
2. **Ignoring context**: External factors may be driving the trend.
3. **Cherry-picking timeframes**: Different windows show different stories.
4. **Causation claims**: Correlation requires careful interpretation.

### Edge Cases to Handle
- **Flat trends**: May be stable or stuck—context matters
- **High volatility**: Trend line may not be meaningful
- **Short timeframes**: May be noise rather than signal
- **Regime changes**: Historical patterns may not apply

### When NOT to Use This Prompt
- **Real-time monitoring**: Need different format
- **Statistical analysis**: Use proper statistical methods
- **Regulatory reporting**: Specific formats required
- **Automated dashboards**: Different presentation needed

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Multi-metric analysis | Best synthesis |
| **Acceptable:** Claude Sonnet 4 | Standard trending | Good balance |
| **Acceptable:** GPT-4o | Narrative quality | Strong communication |
| **Caution:** Smaller models | - | May miss nuances |
