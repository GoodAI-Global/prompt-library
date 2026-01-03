# Production Anomaly Explanation

## Use Case

Explain production anomalies and deviations to stakeholders:
- Interpreting why production metrics deviated
- Contextualizing operational data for non-technical audiences
- Identifying likely causes from production data
- Generating incident explanations for reports

Use when you need to communicate production issues to management, customers, or cross-functional teams.

## Input Format

**Required:**
- `anomaly_data`: Description of the anomaly with supporting metrics
- `production_context`: Normal operating parameters and expectations

**Optional:**
- `timeline`: Event timeline leading to anomaly
- `equipment_data`: Equipment status and sensor readings
- `operator_notes`: Operator observations or shift notes
- `historical_data`: Prior similar events for pattern matching

## Output Format

```json
{
  "anomaly_summary": {
    "event_id": "ANM-2024-001",
    "timestamp": "2024-01-15T10:30:00Z",
    "severity": "moderate",
    "category": "quality_deviation",
    "headline": "Brief description for executive view"
  },
  "explanation": {
    "what_happened": "Clear description of the anomaly",
    "why_it_matters": "Business impact explanation",
    "likely_causes": [
      {
        "cause": "Primary suspected cause",
        "confidence": 0.8,
        "evidence": ["Supporting data point 1", "Supporting data point 2"]
      }
    ],
    "contributing_factors": ["Factor 1", "Factor 2"]
  },
  "impact_assessment": {
    "production_impact": {"units_affected": 150, "downtime_minutes": 45},
    "quality_impact": {"defect_rate_change": "+2.5%", "rework_required": true},
    "financial_impact": {"estimated_cost": 5000, "currency": "USD"},
    "customer_impact": {"shipments_delayed": 2}
  },
  "root_cause_hypothesis": {
    "primary_hypothesis": "Description of most likely root cause",
    "confidence": 0.75,
    "investigation_needed": true
  },
  "recommendations": [
    {
      "timeframe": "immediate",
      "action": "Specific action to take",
      "rationale": "Why this action helps"
    }
  ],
  "stakeholder_summary": {
    "executive": "2-sentence summary for executives",
    "operations": "Detailed summary for operations team",
    "quality": "Quality-focused summary"
  }
}
```

## The Prompt

```
You are a production analyst explaining operational anomalies to stakeholders. Analyze the anomaly and provide clear, actionable explanations.

ANOMALY DATA:
{{anomaly_data}}

PRODUCTION CONTEXT:
{{production_context}}

{{#if timeline}}
EVENT TIMELINE:
{{timeline}}
{{/if}}

{{#if equipment_data}}
EQUIPMENT DATA:
{{equipment_data}}
{{/if}}

{{#if operator_notes}}
OPERATOR NOTES:
{{operator_notes}}
{{/if}}

{{#if historical_data}}
HISTORICAL DATA:
{{historical_data}}
{{/if}}

ANALYSIS FRAMEWORK:

1. ANOMALY CLASSIFICATION
   Categories:
   - quality_deviation: Out-of-spec production
   - throughput_variation: Production rate changes
   - equipment_malfunction: Machine-related issues
   - process_upset: Process parameter deviations
   - material_issue: Raw material problems
   - human_factor: Operator-related issues
   - external_factor: Environmental, utility, or supply issues

   Severity levels:
   - critical: Production stopped, safety concern, or major quality escape
   - major: Significant impact requiring immediate attention
   - moderate: Notable deviation requiring investigation
   - minor: Small deviation, monitoring recommended

2. EXPLANATION DEVELOPMENT
   What happened:
   - Describe the anomaly in clear, non-technical language
   - Quantify the deviation (how much, how long)
   - Compare to normal operating range

   Why it matters:
   - Production impact (units, time)
   - Quality implications
   - Cost implications
   - Customer/delivery impact
   - Safety implications if any

   Likely causes:
   - Identify most probable causes based on evidence
   - Assign confidence levels
   - Note what evidence supports each cause
   - Consider timeline correlation

3. IMPACT ASSESSMENT
   Quantify where possible:
   - Units affected (produced, scrapped, reworked)
   - Time impact (downtime, delay)
   - Cost (direct, indirect, opportunity)
   - Customer impact (orders, shipments)

4. ROOT CAUSE HYPOTHESIS
   Based on available data:
   - Primary hypothesis with confidence
   - Alternative hypotheses
   - What investigation would confirm/refute

5. RECOMMENDATIONS
   Organize by timeframe:
   - Immediate: Within hours
   - Short-term: Within days
   - Long-term: Process improvements

6. STAKEHOLDER COMMUNICATION
   Tailor message to audience:
   - Executive: Impact and actions, minimal technical detail
   - Operations: What to do, when, and why
   - Quality: Specification impact, containment needs
   - Customer-facing: What it means for delivery

COMMUNICATION GUIDELINES:
- Lead with the business impact
- Use clear, jargon-free language for executives
- Provide technical detail for operations teams
- Be honest about uncertainty
- Focus on actions, not blame
- Include confidence levels for hypotheses

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{anomaly_data}}` | string | Yes | Description of the anomaly |
| `{{production_context}}` | string | Yes | Normal operating parameters |
| `{{timeline}}` | string | No | Event sequence |
| `{{equipment_data}}` | string | No | Equipment readings |
| `{{operator_notes}}` | string | No | Operator observations |
| `{{historical_data}}` | string | No | Prior similar events |

## Examples

### Example 1: Quality Deviation

**Input:**
```
anomaly_data: |
  Anomaly detected: 01/15/2024 at 2:30 PM
  Line: Assembly Line 3
  Product: Widget Model X

  METRICS:
  - Defect rate spiked to 8.5% (normal: 1.5%)
  - Primary defect: Misaligned component (95% of defects)
  - Duration: 45 minutes before detection
  - Units produced during period: 180
  - Units affected: approximately 15 defective

production_context: |
  Product: Widget Model X
  Normal production rate: 240 units/hour
  Normal defect rate: 1.5% (3-4 units/hour)
  Acceptable defect rate: <3%
  Line 3 typical performance: 1.2% defect rate (best performer)

  Assembly process:
  - Component A inserted by robot arm
  - Component B snapped into place
  - Visual inspection by camera system
  - Manual spot check every 30 minutes

timeline: |
  1:45 PM - Shift change completed
  2:00 PM - New material lot loaded (Lot M2024-115)
  2:15 PM - Operator noted robot arm "sounded different"
  2:30 PM - Camera inspection system flagged high defect rate
  2:35 PM - Line stopped for investigation
  2:50 PM - Robot arm recalibrated
  3:00 PM - Production resumed at normal defect rate

equipment_data: |
  Robot Arm Status:
  - Calibration last performed: 01/10/2024 (5 days ago)
  - Cycle time during anomaly: 14.2 sec (normal: 14.0 sec)
  - Position accuracy during anomaly: 0.8mm drift noted (spec: ±0.3mm)

  Camera System:
  - Operating normally
  - Detection rate: 100% (caught all defects)

operator_notes: |
  "Robot arm started sounding different around 2:15. Thought it might be
  the new material lot since the parts felt slightly different. Didn't
  report immediately since production seemed OK. Camera caught the problem
  at 2:30."
```

**Output:**
```json
{
  "anomaly_summary": {
    "event_id": "ANM-2024-0115-A",
    "timestamp": "2024-01-15T14:30:00Z",
    "severity": "moderate",
    "category": "quality_deviation",
    "headline": "Component misalignment defects on Line 3 due to robot arm drift"
  },
  "explanation": {
    "what_happened": "Assembly Line 3 experienced a 45-minute period of elevated defects, with the defect rate spiking from normal 1.5% to 8.5%. The primary issue was misaligned Component A, causing approximately 15 defective units out of 180 produced. The camera inspection system detected the issue, and the line was stopped for investigation.",
    "why_it_matters": "While the camera system successfully caught the defects before shipment, this represents a 5x increase in defect rate and approximately $750-1,500 in rework costs. More importantly, it indicates a potential reliability issue with the robot arm calibration that could recur.",
    "likely_causes": [
      {
        "cause": "Robot arm position drift exceeding tolerance",
        "confidence": 0.9,
        "evidence": [
          "Position accuracy measured at 0.8mm drift (spec: ±0.3mm)",
          "Cycle time slightly elevated (14.2 vs 14.0 sec)",
          "Operator noted arm 'sounded different'",
          "Recalibration resolved the issue"
        ]
      },
      {
        "cause": "New material lot dimensional variation",
        "confidence": 0.3,
        "evidence": [
          "New material lot loaded at 2:00 PM",
          "Operator noted parts 'felt slightly different'",
          "Timeline correlates with material change"
        ],
        "notes": "Less likely as primary cause since recalibration fixed issue without material change"
      }
    ],
    "contributing_factors": [
      "5 days since last calibration (may be too long for this robot)",
      "Operator delay in reporting observation (15 minutes)",
      "Camera catch rate 100% prevented quality escape but 45-min detection lag"
    ]
  },
  "impact_assessment": {
    "production_impact": {
      "units_produced_during_anomaly": 180,
      "downtime_minutes": 25,
      "production_loss_units": 100
    },
    "quality_impact": {
      "units_affected": 15,
      "defect_type": "misaligned_component",
      "rework_required": true,
      "scrap_required": false,
      "quality_escape": false
    },
    "financial_impact": {
      "rework_cost": 750,
      "downtime_cost": 500,
      "total_estimated": 1250,
      "currency": "USD"
    },
    "customer_impact": {
      "shipments_delayed": 0,
      "orders_affected": 0,
      "notes": "Contained before shipment"
    }
  },
  "root_cause_hypothesis": {
    "primary_hypothesis": "Robot arm calibration drifted beyond tolerance over 5 days of operation. The 0.8mm position error caused Component A to be placed outside the alignment zone required for proper assembly.",
    "confidence": 0.85,
    "supporting_evidence": [
      "Measured drift of 0.8mm exceeds ±0.3mm specification",
      "Recalibration immediately resolved the issue",
      "Audible change noted by operator suggests mechanical drift"
    ],
    "investigation_needed": true,
    "investigation_questions": [
      "What is the typical calibration drift rate for this robot?",
      "Is 5-day calibration interval appropriate?",
      "Are there environmental factors (temperature) affecting drift?",
      "Should material lot variations be considered in tolerances?"
    ]
  },
  "recommendations": [
    {
      "timeframe": "immediate",
      "action": "Verify current calibration is holding after recalibration",
      "rationale": "Confirm fix is stable before full production continues"
    },
    {
      "timeframe": "immediate",
      "action": "Rework the 15 affected units",
      "rationale": "Clear quality hold before next shipment"
    },
    {
      "timeframe": "short_term",
      "action": "Reduce calibration interval to 3 days for this robot",
      "rationale": "5-day interval allowed drift to exceed tolerance; shorter interval provides margin"
    },
    {
      "timeframe": "short_term",
      "action": "Implement calibration drift monitoring",
      "rationale": "Track drift over time to set data-driven calibration interval"
    },
    {
      "timeframe": "short_term",
      "action": "Train operators to report equipment observations immediately",
      "rationale": "15-minute delay between operator observation and issue detection; faster reporting could reduce impact"
    },
    {
      "timeframe": "long_term",
      "action": "Evaluate in-process position monitoring for robot arm",
      "rationale": "Real-time drift detection would catch issues before they affect quality"
    }
  ],
  "stakeholder_summary": {
    "executive": "Line 3 had a 45-minute quality issue today causing $1,250 in rework and downtime costs. The robot arm needed recalibration. We're shortening the calibration schedule to prevent recurrence. No customer impact—our camera system caught all defects before shipment.",
    "operations": "Robot arm on Line 3 drifted out of calibration causing misaligned components. Recalibration fixed it. Please reduce calibration interval to every 3 days until we establish optimal frequency. Also, please report any unusual equipment sounds/behaviors immediately—the operator noticed something 15 minutes before the camera caught the problem.",
    "quality": "15 units from Line 3 (2:30-3:15 PM) require rework for component misalignment. Camera inspection caught 100% of defects—no quality escape. Root cause is robot arm calibration drift. Verify rework effectiveness and update containment log."
  },
  "lessons_learned": [
    "Operator observations are valuable early warning—encourage immediate reporting",
    "Camera inspection system performed well as final catch",
    "Calibration intervals should be based on measured drift data"
  ]
}
```

### Example 2: Throughput Variation

**Input:**
```
anomaly_data: |
  Anomaly: Production throughput dropped 40%
  Line: Packaging Line 1
  Period: 01/15/2024, 8:00 AM - 10:30 AM (2.5 hours)

  METRICS:
  - Normal output: 1,200 units/hour
  - Observed output: 720 units/hour (40% reduction)
  - Total shortfall: 1,200 units below target

production_context: |
  Line 1 packages finished products into retail boxes
  - Normally operates at 1,200 units/hour
  - Three stations: box forming, product insertion, sealing
  - 8 operators total per shift
  - Daily target: 9,600 units

operator_notes: |
  "Machine kept jamming. We had to clear jams every few minutes.
  Box material seems thinner than usual. Changed to new carton lot this morning."
```

**Output:**
```json
{
  "anomaly_summary": {
    "event_id": "ANM-2024-0115-B",
    "timestamp": "2024-01-15T08:00:00Z",
    "severity": "major",
    "category": "throughput_variation",
    "headline": "40% throughput loss on Packaging Line 1 due to material jamming"
  },
  "explanation": {
    "what_happened": "Packaging Line 1 ran at only 60% of normal capacity for 2.5 hours this morning, producing 720 units/hour instead of the normal 1,200. The line experienced repeated jams that required operator intervention to clear, resulting in a 1,200-unit shortfall against daily targets.",
    "why_it_matters": "This represents 12.5% of the daily production target missed in a single morning. If not recovered, this could impact order fulfillment. The pattern suggests a material-related issue that could continue if not addressed.",
    "likely_causes": [
      {
        "cause": "Carton material specification issue",
        "confidence": 0.85,
        "evidence": [
          "Operator noted box material 'seems thinner than usual'",
          "New carton lot started this morning (timing correlation)",
          "Jamming pattern consistent with material handling issues"
        ]
      }
    ],
    "contributing_factors": [
      "No incoming material inspection caught thickness variation",
      "Machine parameters not adjusted for material change"
    ]
  },
  "impact_assessment": {
    "production_impact": {
      "throughput_reduction": "40%",
      "duration_hours": 2.5,
      "units_shortfall": 1200,
      "daily_target_impact": "-12.5%"
    },
    "quality_impact": {
      "quality_issues": false,
      "notes": "Output quality unaffected—just slower"
    },
    "financial_impact": {
      "lost_production_value": 3600,
      "overtime_recovery_cost": 800,
      "total_estimated": 4400,
      "currency": "USD"
    },
    "customer_impact": {
      "orders_at_risk": 1,
      "recovery_possible": true,
      "notes": "Can recover with overtime if issue resolved"
    }
  },
  "root_cause_hypothesis": {
    "primary_hypothesis": "New carton lot has thinner material than specification, causing handling issues in the box forming station. Thinner material may be more prone to buckling or mis-feeding.",
    "confidence": 0.8,
    "investigation_needed": true,
    "investigation_questions": [
      "What is the measured thickness of new carton lot vs specification?",
      "Has this supplier lot shown variation before?",
      "Can machine parameters be adjusted to handle variation?"
    ]
  },
  "recommendations": [
    {
      "timeframe": "immediate",
      "action": "Measure carton thickness vs specification",
      "rationale": "Confirm material is cause before further action"
    },
    {
      "timeframe": "immediate",
      "action": "Contact supplier about material specification",
      "rationale": "Determine if this is in-spec variation or defect"
    },
    {
      "timeframe": "immediate",
      "action": "Adjust machine parameters if possible to accommodate thinner material",
      "rationale": "Recover throughput while investigating root cause"
    },
    {
      "timeframe": "short_term",
      "action": "Schedule overtime to recover lost production",
      "rationale": "Meet daily commitments while issue is resolved"
    },
    {
      "timeframe": "long_term",
      "action": "Implement incoming material thickness verification",
      "rationale": "Catch material variations before they reach the line"
    }
  ],
  "stakeholder_summary": {
    "executive": "Packaging ran at 60% capacity this morning due to material jamming—likely caused by a thinner-than-usual carton lot. We're 1,200 units behind target. We can recover with overtime if we resolve the material issue. Investigating with supplier.",
    "operations": "Line 1 throughput issue is material-related. Please measure carton thickness and adjust machine if possible. Schedule 2-hour overtime to recover shortfall. Priority is getting back to full speed.",
    "quality": "No quality impact—just throughput. Please verify carton lot M2024-115 meets thickness specification and document for supplier discussion."
  }
}
```

## Gotchas

### Common Failure Modes
1. **Correlation vs causation**: Timeline correlation doesn't prove cause. Be clear about confidence.
2. **Missing baseline**: "40% drop" requires knowing what normal is.
3. **Blame focus**: Explain what happened, not who's fault it is.
4. **Over-precision**: Don't present estimates as exact figures.

### Edge Cases to Handle
- **Multiple contributing causes**: Rarely is there just one cause
- **Insufficient data**: Be honest about what you don't know
- **Conflicting information**: Note inconsistencies
- **Recurring anomalies**: Reference historical patterns

### When NOT to Use This Prompt
- **Safety incidents**: Need specific safety investigation format
- **Root cause analysis**: Different, more structured methodology
- **Customer-facing reports**: May need different tone/content
- **Regulatory reporting**: Specific format requirements

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-factor anomalies | Best synthesis and explanation |
| **Acceptable:** Claude Sonnet 4 | Standard explanations | Good balance |
| **Acceptable:** GPT-4o | Stakeholder communication | Strong natural language |
| **Caution:** Smaller models | - | May miss nuance |
