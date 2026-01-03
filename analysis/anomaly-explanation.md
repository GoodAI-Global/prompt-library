# Anomaly Explanation

## Use Case

Explain detected anomalies in data or metrics to stakeholders:
- Data science anomaly alerts interpretation
- Business metric deviation explanation
- System monitoring alert context
- Financial transaction irregularity analysis

Use when you need to translate technical anomaly detections into business-understandable explanations.

## Input Format

**Required:**
- `anomaly_details`: Description of the detected anomaly
- `context`: Normal patterns and baseline information

**Optional:**
- `detection_method`: How the anomaly was detected
- `historical_data`: Relevant historical patterns
- `related_factors`: Potentially related variables or events
- `audience`: Technical level of intended recipients

## Output Format

```json
{
  "anomaly_summary": {
    "anomaly_id": "ANM-2024-001",
    "detection_time": "2024-01-15T10:30:00Z",
    "metric": "daily_active_users",
    "severity": "medium",
    "confidence": 0.92
  },
  "explanation": {
    "what_happened": "Clear description of the deviation",
    "magnitude": "How significant is this deviation",
    "comparison": "This is X standard deviations from normal",
    "temporal_context": "When did this start, is it ongoing"
  },
  "likely_causes": [
    {
      "cause": "Hypothesis description",
      "probability": 0.7,
      "supporting_evidence": ["Evidence 1", "Evidence 2"],
      "contradicting_evidence": []
    }
  ],
  "impact_assessment": {
    "business_impact": "What this means for the business",
    "risk_level": "low/medium/high",
    "affected_areas": ["Area 1", "Area 2"]
  },
  "recommendations": [
    {
      "action": "What to do",
      "urgency": "immediate/short_term/monitoring",
      "rationale": "Why this action"
    }
  ],
  "stakeholder_messages": {
    "executive": "One sentence for executives",
    "technical": "Detailed technical explanation"
  }
}
```

## The Prompt

```
You are a data analyst explaining anomaly detections. Translate technical findings into clear, actionable explanations.

ANOMALY DETAILS:
{{anomaly_details}}

CONTEXT:
{{context}}

{{#if detection_method}}
DETECTION METHOD:
{{detection_method}}
{{/if}}

{{#if historical_data}}
HISTORICAL DATA:
{{historical_data}}
{{/if}}

{{#if related_factors}}
RELATED FACTORS:
{{related_factors}}
{{/if}}

AUDIENCE: {{audience | default: "business"}}

EXPLANATION FRAMEWORK:

1. WHAT HAPPENED (Clear Description)
   - Describe the anomaly in plain language
   - Quantify the deviation (%, absolute, relative)
   - Establish the timeframe
   - Compare to normal patterns

2. MAGNITUDE ASSESSMENT
   - How unusual is this? (standard deviations, percentiles)
   - Historical comparison (has this happened before?)
   - Relative importance (minor blip vs significant shift)

3. CAUSE ANALYSIS
   For each hypothesis:
   - State the potential cause
   - Estimate probability
   - List supporting evidence
   - List contradicting evidence
   - Note what would confirm/refute

   Common cause categories:
   - Technical: System issues, data problems
   - Operational: Process changes, staffing
   - External: Market events, seasonality
   - Behavioral: User/customer changes

4. IMPACT ASSESSMENT
   - Business impact (revenue, cost, risk)
   - Operational impact (processes affected)
   - Customer impact (experience, satisfaction)
   - Reputational impact (if applicable)

5. RECOMMENDATIONS
   Categorize by urgency:
   - Immediate: Action within hours
   - Short-term: Action within days
   - Monitoring: Watch and reassess

6. COMMUNICATION TAILORING
   Adjust explanation for audience:
   - Executive: Impact and action, minimal technical detail
   - Technical: Full detail, methodology, data
   - Operations: What to do, when, why
   - External: Carefully worded, appropriate disclosure

EXPLANATION QUALITY:
- Lead with the bottom line
- Use analogies for technical concepts
- Quantify where possible
- Acknowledge uncertainty
- Separate facts from hypotheses

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{anomaly_details}}` | string | Yes | Description of the detected anomaly |
| `{{context}}` | string | Yes | Normal patterns and baselines |
| `{{detection_method}}` | string | No | How anomaly was detected |
| `{{historical_data}}` | string | No | Relevant historical patterns |
| `{{related_factors}}` | string | No | Potentially related events |
| `{{audience}}` | string | No | Intended audience level |

## Examples

### Example 1: Revenue Anomaly

**Input:**
```
anomaly_details: |
  Metric: Daily Revenue
  Date: January 15, 2024
  Expected: $125,000 (based on 30-day average)
  Actual: $78,000
  Deviation: -37.6%
  Z-score: -3.2

context: |
  - E-commerce platform, B2C
  - Normal daily range: $110,000 - $140,000
  - Weekday pattern typically stable
  - January historically slower than December but stable
  - No known system issues reported

detection_method: |
  Prophet model with 95% confidence interval
  Seasonal decomposition: day-of-week, monthly
  Alert triggered when actual falls outside interval

related_factors: |
  - Payment processor status: Normal
  - Website traffic: Down 15% from average
  - Cart abandonment rate: Up from 65% to 78%
  - Email campaign sent yesterday (Tuesday)
  - Competitor launched sale Monday

audience: executive
```

**Output:**
```json
{
  "anomaly_summary": {
    "anomaly_id": "REV-2024-0115",
    "detection_time": "2024-01-15T23:59:00Z",
    "metric": "daily_revenue",
    "severity": "high",
    "confidence": 0.95,
    "headline": "Revenue 38% below expected, driven by elevated cart abandonment"
  },
  "explanation": {
    "what_happened": "Daily revenue on January 15 was $78,000, falling 38% short of the expected $125,000. This is the largest single-day revenue shortfall in the past 90 days.",
    "magnitude": "This deviation is 3.2 standard deviations below our 30-day average—an event we'd expect to see less than once per year under normal conditions. Revenue fell $47,000 below forecast.",
    "comparison": "For context, our normal daily range is $110,000-$140,000. The last time we saw revenue this low on a Wednesday was over 8 months ago.",
    "temporal_context": "The decline appears to have started Tuesday evening and continued through Wednesday. Traffic dropped 15% while cart abandonment spiked to 78% (normally 65%)."
  },
  "likely_causes": [
    {
      "cause": "Price sensitivity due to competitor sale",
      "probability": 0.65,
      "supporting_evidence": [
        "Major competitor launched sale on Monday",
        "Cart abandonment up 13 percentage points (customers may be comparison shopping)",
        "Traffic only down 15% but conversion hit much harder"
      ],
      "contradicting_evidence": [
        "No direct customer feedback yet confirming this"
      ],
      "confirmation_approach": "Check competitor's sale end date; monitor if our metrics recover when their sale ends"
    },
    {
      "cause": "Email campaign may have backfired",
      "probability": 0.25,
      "supporting_evidence": [
        "Email campaign sent Tuesday (day before drop)",
        "If campaign drove traffic but had poor offer, could increase abandonment"
      ],
      "contradicting_evidence": [
        "Traffic is down, not up (would expect up if email drove visits)",
        "Campaign typically performs well"
      ],
      "confirmation_approach": "Analyze email campaign click-through and conversion rates"
    },
    {
      "cause": "Technical issue affecting checkout",
      "probability": 0.10,
      "supporting_evidence": [
        "High cart abandonment could indicate checkout problems"
      ],
      "contradicting_evidence": [
        "No error alerts from payment processor or monitoring",
        "$78K still processed, so checkout was functional"
      ],
      "confirmation_approach": "Review checkout funnel for drop-off anomalies"
    }
  ],
  "impact_assessment": {
    "business_impact": "$47,000 revenue shortfall for January 15. If trend continues, weekly impact could exceed $200,000.",
    "risk_level": "high",
    "affected_areas": ["Revenue", "Conversion rate", "Customer acquisition"],
    "projection": "If caused by competitor sale (ending Sunday), we should see recovery by Monday. If structural issue, ongoing impact."
  },
  "recommendations": [
    {
      "action": "Monitor competitor sale end date and our metrics correlation",
      "urgency": "immediate",
      "rationale": "If recovery follows competitor sale end, confirms hypothesis and no action needed"
    },
    {
      "action": "Consider promotional response if competitor sale continues",
      "urgency": "short_term",
      "rationale": "May need to match or counter competitor pricing to protect market share"
    },
    {
      "action": "Deep dive on checkout funnel to rule out technical issues",
      "urgency": "immediate",
      "rationale": "Quick check to eliminate technical cause—if found, fix immediately"
    },
    {
      "action": "Analyze email campaign performance",
      "urgency": "short_term",
      "rationale": "Understand if campaign contributed to issue or if it's unrelated"
    }
  ],
  "stakeholder_messages": {
    "executive": "Revenue fell 38% ($47K) below forecast on Wednesday. Most likely cause is a competitor's ongoing sale increasing customer comparison shopping—our cart abandonment spiked to 78%. We're monitoring and will consider promotional response if the trend continues.",
    "technical": "Prophet model flagged $78K revenue vs $125K forecast (z=-3.2). Traffic down 15%, cart abandonment up 13pp to 78%. Temporal correlation with competitor sale launch (Monday). Checkout funnel and payment processor nominal. Recommend: checkout drop-off analysis to rule out technical; cohort analysis on email campaign recipients; monitor for recovery when competitor sale ends.",
    "board_summary": "We experienced a significant one-day revenue drop that appears driven by competitive dynamics. We're monitoring the situation and have contingency plans ready."
  },
  "follow_up": {
    "next_check": "2024-01-16T09:00:00Z",
    "success_criteria": "Revenue returns to $100K+ and cart abandonment below 70%",
    "escalation_trigger": "If trend continues for 3+ days, escalate for promotional response decision"
  }
}
```

## Gotchas

### Common Failure Modes
1. **False causation**: Correlation doesn't prove cause. Be careful with "caused by."
2. **Single explanation bias**: Multiple factors often contribute.
3. **Overconfidence**: Acknowledge uncertainty appropriately.
4. **Technical jargon**: Match explanation to audience level.

### Edge Cases to Handle
- **Multiple simultaneous anomalies**: May be related or independent
- **Gradual drift vs sudden spike**: Different explanation approaches
- **Anomaly on anomaly**: Secondary issue during ongoing problem
- **False positive alerts**: Sometimes data is just variable

### When NOT to Use This Prompt
- **Automated alerting**: Need different format for automated systems
- **Regulatory reporting**: Specific formats required
- **Root cause analysis**: Need formal RCA methodology
- **Real-time dashboards**: Different presentation needed

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-factor | Best synthesis |
| **Acceptable:** Claude Sonnet 4 | Standard anomalies | Good balance |
| **Acceptable:** GPT-4o | Stakeholder comm | Strong language |
| **Caution:** Smaller models | - | May oversimplify |
