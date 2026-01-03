# Equipment Failure Prediction

## Use Case

Analyze equipment data to predict potential failures:
- Interpreting sensor data patterns for failure indicators
- Assessing remaining useful life from degradation trends
- Prioritizing maintenance interventions
- Explaining predictions for maintenance planning

Use to support predictive maintenance programs with actionable failure risk assessments.

## Input Format

**Required:**
- `equipment_data`: Current sensor readings, operating parameters, or condition data
- `equipment_info`: Equipment type, age, specifications

**Optional:**
- `historical_data`: Trend data over time (readings, maintenance history)
- `failure_patterns`: Known failure modes and signatures for this equipment type
- `maintenance_history`: Recent maintenance activities
- `operating_context`: Current duty cycle, environment, load

## Output Format

```json
{
  "prediction_summary": {
    "equipment_id": "EQ-12345",
    "analysis_timestamp": "2024-01-15T10:00:00Z",
    "overall_health_score": 72,
    "failure_risk_level": "medium",
    "failure_probability_30_day": 0.15,
    "recommended_action": "schedule_maintenance"
  },
  "component_analysis": [
    {
      "component": "main_bearing",
      "health_score": 55,
      "failure_probability": 0.25,
      "failure_mode": "wear",
      "remaining_useful_life": {
        "estimate": 45,
        "unit": "days",
        "confidence": 0.7
      },
      "indicators": [
        {
          "indicator": "vibration_amplitude",
          "current_value": 4.2,
          "threshold": 5.0,
          "trend": "increasing",
          "concern_level": "medium"
        }
      ]
    }
  ],
  "risk_factors": [
    {
      "factor": "Approaching recommended replacement interval",
      "impact": "medium",
      "evidence": "Bearing at 85% of expected life"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "action": "Schedule bearing replacement within 30 days",
      "rationale": "Vibration trending toward limit",
      "cost_of_inaction": "Unplanned downtime $15,000"
    }
  ],
  "monitoring_plan": {
    "parameters": ["vibration", "temperature"],
    "frequency": "daily",
    "alert_thresholds": {...}
  }
}
```

## The Prompt

```
You are a reliability engineer analyzing equipment condition data to predict potential failures. Assess the equipment health and provide maintenance recommendations.

EQUIPMENT INFORMATION:
{{equipment_info}}

CURRENT EQUIPMENT DATA:
{{equipment_data}}

{{#if historical_data}}
HISTORICAL DATA:
{{historical_data}}
{{/if}}

{{#if failure_patterns}}
KNOWN FAILURE PATTERNS:
{{failure_patterns}}
{{/if}}

{{#if maintenance_history}}
MAINTENANCE HISTORY:
{{maintenance_history}}
{{/if}}

{{#if operating_context}}
OPERATING CONTEXT:
{{operating_context}}
{{/if}}

FAILURE PREDICTION FRAMEWORK:

1. HEALTH SCORING (0-100)
   Score components and overall equipment:
   - 90-100: Excellent condition, no concerns
   - 75-89: Good condition, monitor
   - 60-74: Fair condition, plan maintenance
   - 40-59: Poor condition, schedule maintenance soon
   - Below 40: Critical, immediate action needed

2. FAILURE PROBABILITY ASSESSMENT
   Estimate probability of failure within:
   - 7 days (P7)
   - 30 days (P30)
   - 90 days (P90)

   Consider:
   - Current condition vs thresholds
   - Trend direction and rate
   - Time since last maintenance
   - Operating stress level

3. COMMON FAILURE INDICATORS

   Vibration analysis:
   - Amplitude: Overall level increasing
   - Frequency: New peaks appearing
   - Harmonics: Bearing defect frequencies

   Temperature:
   - Absolute: Above normal operating range
   - Differential: Hot spots developing
   - Trend: Increasing over time

   Electrical:
   - Current draw: Increasing (mechanical stress)
   - Power factor: Changing (electrical issues)
   - Insulation: Resistance declining

   Performance:
   - Efficiency: Declining
   - Output: Below specification
   - Cycle time: Increasing

4. REMAINING USEFUL LIFE (RUL)
   Estimate RUL with confidence interval:
   - Based on degradation rate
   - Compared to failure threshold
   - Accounting for uncertainty

   Confidence factors:
   - Data quality
   - Historical failure data availability
   - Operating condition variability

5. FAILURE MODES TO CONSIDER

   Rotating equipment:
   - Bearing failure (wear, fatigue, contamination)
   - Shaft misalignment
   - Imbalance
   - Looseness

   Electrical systems:
   - Insulation breakdown
   - Connection degradation
   - Overheating

   Mechanical systems:
   - Wear (abrasion, erosion)
   - Fatigue (cyclic loading)
   - Corrosion
   - Seal failure

6. RISK FACTORS
   Identify factors increasing failure risk:
   - Age relative to design life
   - Operating conditions (overload, environment)
   - Maintenance history (gaps, quality)
   - Historical failure pattern

7. RECOMMENDATIONS
   Prioritized by risk:
   - Critical: Immediate action to prevent failure
   - High: Schedule within days
   - Medium: Plan for next maintenance window
   - Low: Monitor, address at convenience

   Include:
   - Specific action
   - Timeframe
   - Rationale
   - Cost of inaction

8. MONITORING PLAN
   Define ongoing surveillance:
   - Parameters to watch
   - Monitoring frequency
   - Alert thresholds
   - Escalation criteria

OUTPUT REQUIREMENTS:
- Overall health assessment with score
- Component-level analysis
- Failure probability estimates with confidence
- Prioritized recommendations
- Monitoring plan

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{equipment_info}}` | string | Yes | Equipment type, age, specifications |
| `{{equipment_data}}` | string | Yes | Current sensor/condition readings |
| `{{historical_data}}` | string | No | Trend data over time |
| `{{failure_patterns}}` | string | No | Known failure signatures |
| `{{maintenance_history}}` | string | No | Recent maintenance records |
| `{{operating_context}}` | string | No | Current operating conditions |

## Examples

### Example 1: Rotating Equipment with Developing Issue

**Input:**
```
equipment_info: |
  Equipment: Centrifugal Pump P-101
  Service: Cooling water circulation
  Manufacturer: Goulds
  Model: 3196
  Size: 4x6-13
  Speed: 1750 RPM
  Age: 6 years
  Design life: 10 years
  Last overhaul: 3 years ago

equipment_data: |
  CURRENT READINGS (01/15/2024):

  Vibration (in/sec peak):
  - Bearing DE (drive end): 0.28 (baseline: 0.12)
  - Bearing NDE (non-drive end): 0.15 (baseline: 0.10)
  - Vertical: 0.22 (baseline: 0.11)

  Vibration spectrum shows developing peak at 3.5x RPM on DE bearing

  Temperature (°F):
  - Bearing DE: 165 (baseline: 135)
  - Bearing NDE: 142 (baseline: 135)
  - Motor: 185 (baseline: 180)

  Performance:
  - Flow: 485 GPM (design: 500 GPM)
  - Discharge pressure: 78 PSI (design: 80 PSI)
  - Motor current: 28A (normal: 26A)

historical_data: |
  VIBRATION TREND (DE Bearing, in/sec peak):
  - 6 months ago: 0.12 (baseline)
  - 3 months ago: 0.18
  - 1 month ago: 0.22
  - 2 weeks ago: 0.25
  - Current: 0.28

  TEMPERATURE TREND (DE Bearing, °F):
  - 6 months ago: 135 (baseline)
  - 3 months ago: 142
  - 1 month ago: 155
  - Current: 165

  Alert threshold: 0.35 in/sec, 180°F

failure_patterns: |
  Common failure modes for 3196 pumps:
  - Bearing failure: 40% of failures
    Signature: Increasing vibration, temperature; 3.5x and 7x RPM peaks
  - Seal failure: 25% of failures
    Signature: Leakage, bearing contamination
  - Impeller wear: 20% of failures
    Signature: Reduced flow, efficiency drop
  - Coupling issues: 15% of failures
    Signature: 1x and 2x peaks, axial vibration

maintenance_history: |
  - 3 years ago: Full overhaul (bearings, seals, wear rings)
  - 1 year ago: Coupling alignment check - OK
  - 6 months ago: Baseline vibration survey
  - 3 months ago: Grease added to bearings
  - Current: No outstanding work orders
```

**Output:**
```json
{
  "prediction_summary": {
    "equipment_id": "P-101",
    "equipment_name": "Centrifugal Pump P-101",
    "service": "Cooling water circulation",
    "analysis_timestamp": "2024-01-15T10:00:00Z",
    "overall_health_score": 58,
    "health_status": "poor",
    "failure_risk_level": "high",
    "failure_probability": {
      "7_day": 0.05,
      "30_day": 0.25,
      "90_day": 0.65
    },
    "recommended_action": "schedule_maintenance_urgent",
    "primary_concern": "Drive end bearing degradation"
  },
  "component_analysis": [
    {
      "component": "drive_end_bearing",
      "health_score": 42,
      "status": "poor",
      "failure_probability_30_day": 0.30,
      "failure_mode": "bearing_wear_fatigue",
      "remaining_useful_life": {
        "estimate": 35,
        "unit": "days",
        "confidence": 0.65,
        "range": {"low": 20, "high": 60}
      },
      "indicators": [
        {
          "indicator": "vibration_amplitude",
          "current_value": 0.28,
          "unit": "in/sec peak",
          "baseline": 0.12,
          "threshold": 0.35,
          "percent_of_threshold": 80,
          "trend": "increasing",
          "trend_rate": "accelerating",
          "concern_level": "high"
        },
        {
          "indicator": "temperature",
          "current_value": 165,
          "unit": "°F",
          "baseline": 135,
          "threshold": 180,
          "percent_of_threshold": 92,
          "trend": "increasing",
          "concern_level": "high"
        },
        {
          "indicator": "spectral_signature",
          "finding": "3.5x RPM peak developing",
          "significance": "Outer race defect signature",
          "concern_level": "high"
        }
      ],
      "analysis_notes": "Vibration has more than doubled from baseline in 6 months with accelerating trend. Temperature rise of 30°F indicates friction increase. 3.5x RPM spectral peak is characteristic of outer race bearing defect. Pattern strongly suggests bearing wear progressing toward failure."
    },
    {
      "component": "non_drive_end_bearing",
      "health_score": 78,
      "status": "good",
      "failure_probability_30_day": 0.05,
      "indicators": [
        {
          "indicator": "vibration_amplitude",
          "current_value": 0.15,
          "baseline": 0.10,
          "threshold": 0.35,
          "percent_of_threshold": 43,
          "trend": "stable",
          "concern_level": "low"
        },
        {
          "indicator": "temperature",
          "current_value": 142,
          "baseline": 135,
          "threshold": 180,
          "concern_level": "low"
        }
      ],
      "analysis_notes": "Slight increase from baseline but within acceptable range. No immediate concern but should be inspected during DE bearing replacement."
    },
    {
      "component": "motor",
      "health_score": 82,
      "status": "good",
      "failure_probability_30_day": 0.03,
      "indicators": [
        {
          "indicator": "temperature",
          "current_value": 185,
          "baseline": 180,
          "threshold": 220,
          "concern_level": "low"
        },
        {
          "indicator": "current_draw",
          "current_value": 28,
          "baseline": 26,
          "trend": "slightly_elevated",
          "concern_level": "low",
          "notes": "Elevated current likely due to increased bearing friction"
        }
      ]
    },
    {
      "component": "hydraulic_performance",
      "health_score": 88,
      "status": "good",
      "indicators": [
        {
          "indicator": "flow",
          "current_value": 485,
          "design": 500,
          "percent_of_design": 97,
          "concern_level": "low"
        },
        {
          "indicator": "discharge_pressure",
          "current_value": 78,
          "design": 80,
          "concern_level": "low"
        }
      ],
      "analysis_notes": "Hydraulic performance near design. Minor reduction may be due to bearing friction or normal wear ring clearance increase."
    }
  ],
  "risk_factors": [
    {
      "factor": "Accelerating degradation trend",
      "impact": "high",
      "evidence": "Vibration increased from 0.22 to 0.28 in/sec in just 2 weeks (27% increase)"
    },
    {
      "factor": "Approaching alert threshold",
      "impact": "high",
      "evidence": "Currently at 80% of vibration alert threshold (0.28 vs 0.35)"
    },
    {
      "factor": "Bearing defect signature in spectrum",
      "impact": "high",
      "evidence": "3.5x RPM peak characteristic of outer race defect"
    },
    {
      "factor": "Time since overhaul",
      "impact": "medium",
      "evidence": "3 years since bearing replacement; typical life 3-5 years for this duty"
    },
    {
      "factor": "Correlated temperature increase",
      "impact": "medium",
      "evidence": "Temperature and vibration rising together confirms mechanical issue"
    }
  ],
  "failure_scenario": {
    "most_likely_failure_mode": "Drive end bearing seizure",
    "failure_progression": [
      "Current: Outer race defect developing",
      "Next stage: Defect propagation, increased metal-to-metal contact",
      "Warning signs: Vibration exceeds 0.35, temperature exceeds 180°F",
      "Failure: Bearing seizure, potential shaft damage, unplanned shutdown"
    ],
    "estimated_time_to_failure": {
      "conservative": "20-30 days",
      "best_estimate": "35-45 days",
      "optimistic": "50-60 days"
    },
    "failure_consequence": {
      "downtime": "24-72 hours for emergency repair",
      "collateral_damage_risk": "Shaft damage if bearing seizes",
      "cost_unplanned": 15000,
      "cost_planned": 4500,
      "currency": "USD"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "action": "Schedule bearing replacement within 21 days",
      "component": "drive_end_bearing",
      "rationale": "Avoid unplanned failure and potential shaft damage",
      "estimated_duration": "4-6 hours",
      "estimated_cost": 4500,
      "cost_of_inaction": "$15,000+ for emergency repair plus production loss"
    },
    {
      "priority": "medium",
      "action": "Inspect NDE bearing during repair",
      "component": "non_drive_end_bearing",
      "rationale": "3 years old, economical to replace while pump is open",
      "estimated_additional_cost": 800
    },
    {
      "priority": "medium",
      "action": "Check coupling alignment after reassembly",
      "component": "coupling",
      "rationale": "Misalignment can accelerate bearing wear; verify as part of repair"
    },
    {
      "priority": "low",
      "action": "Inspect wear rings during repair",
      "component": "wear_rings",
      "rationale": "Minor flow reduction may indicate wear ring clearance; check while accessible"
    }
  ],
  "monitoring_plan": {
    "enhanced_monitoring_period": "Until repair completed",
    "parameters": [
      {
        "parameter": "DE_bearing_vibration",
        "current_frequency": "weekly",
        "recommended_frequency": "daily",
        "alert_threshold": 0.35,
        "shutdown_threshold": 0.50
      },
      {
        "parameter": "DE_bearing_temperature",
        "current_frequency": "continuous",
        "alert_threshold": 180,
        "shutdown_threshold": 200
      }
    ],
    "escalation_criteria": [
      "Vibration exceeds 0.35 in/sec: Expedite repair to within 7 days",
      "Temperature exceeds 180°F: Expedite repair to within 7 days",
      "Vibration exceeds 0.45 in/sec OR temperature exceeds 190°F: Consider shutdown for repair"
    ]
  },
  "confidence_assessment": {
    "data_quality": "good",
    "trend_reliability": "high",
    "prediction_confidence": 0.75,
    "limiting_factors": [
      "Exact remaining life depends on operating conditions",
      "Sudden load changes could accelerate degradation"
    ]
  }
}
```

### Example 2: Electrical System with Early Warning Signs

**Input:**
```
equipment_info: |
  Equipment: Motor Control Center MCC-A
  Voltage: 480V
  Installed: 2015
  Circuits: 24 motor starters
  Last thermal scan: 6 months ago

equipment_data: |
  THERMAL SCAN RESULTS (01/15/2024):

  Hot spots identified:
  - Starter 12 (Conveyor C-101): 142°F (normal <120°F)
    Connection at line side showing elevated temp
  - Starter 18 (Pump P-205): 128°F (normal <120°F)
    Load side connection slightly elevated

  Normal readings:
  - All other starters: 95-115°F
  - Main breaker connections: 108°F
  - Bus bars: 102°F

  Power quality data:
  - Voltage: 477V (nominal 480V) - normal
  - Current imbalance: 3% - normal
  - Power factor: 0.92 - normal
```

**Output:**
```json
{
  "prediction_summary": {
    "equipment_id": "MCC-A",
    "equipment_name": "Motor Control Center MCC-A",
    "analysis_timestamp": "2024-01-15T10:00:00Z",
    "overall_health_score": 78,
    "health_status": "good_with_concerns",
    "failure_risk_level": "medium",
    "failure_probability": {
      "7_day": 0.02,
      "30_day": 0.08,
      "90_day": 0.20
    },
    "recommended_action": "schedule_maintenance_normal",
    "primary_concern": "Starter 12 connection overheating"
  },
  "component_analysis": [
    {
      "component": "Starter 12 (Conveyor C-101)",
      "health_score": 55,
      "status": "fair",
      "failure_probability_30_day": 0.15,
      "failure_mode": "high_resistance_connection",
      "remaining_useful_life": {
        "estimate": 60,
        "unit": "days",
        "confidence": 0.5,
        "notes": "Connection degradation is unpredictable; could fail sooner under high load"
      },
      "indicators": [
        {
          "indicator": "connection_temperature",
          "location": "line_side",
          "current_value": 142,
          "unit": "°F",
          "threshold": 120,
          "delta_above_ambient": 52,
          "severity": "serious",
          "concern_level": "high"
        }
      ],
      "analysis_notes": "22°F above threshold indicates high-resistance connection. This is typically caused by loose connection, corrosion, or conductor damage. Will progressively worsen under load. Fire risk if not addressed."
    },
    {
      "component": "Starter 18 (Pump P-205)",
      "health_score": 75,
      "status": "fair",
      "failure_probability_30_day": 0.05,
      "indicators": [
        {
          "indicator": "connection_temperature",
          "location": "load_side",
          "current_value": 128,
          "unit": "°F",
          "threshold": 120,
          "delta_above_normal": 8,
          "severity": "minor",
          "concern_level": "medium"
        }
      ],
      "analysis_notes": "Slightly elevated but not critical. Monitor and address during next scheduled maintenance or when repairing Starter 12."
    },
    {
      "component": "Main breaker and bus",
      "health_score": 95,
      "status": "good",
      "failure_probability_30_day": 0.01,
      "indicators": [
        {
          "indicator": "temperature",
          "current_value": "102-108",
          "unit": "°F",
          "status": "normal",
          "concern_level": "none"
        }
      ]
    }
  ],
  "risk_factors": [
    {
      "factor": "High-resistance connection developing",
      "impact": "high",
      "evidence": "Starter 12 line connection 22°F above threshold"
    },
    {
      "factor": "Fire risk",
      "impact": "high",
      "evidence": "Overheating electrical connections are common ignition sources"
    },
    {
      "factor": "Progressive failure mode",
      "impact": "medium",
      "evidence": "High resistance creates heat, heat creates oxidation, oxidation increases resistance - self-accelerating"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "action": "De-energize and repair Starter 12 connection within 14 days",
      "component": "Starter 12",
      "rationale": "142°F is serious concern. Clean/tighten or replace connection before failure.",
      "estimated_duration": "2 hours",
      "estimated_cost": 500,
      "cost_of_inaction": "Potential fire, equipment damage, production loss"
    },
    {
      "priority": "medium",
      "action": "Inspect and tighten Starter 18 connection",
      "component": "Starter 18",
      "rationale": "Address while addressing Starter 12; prevent escalation",
      "estimated_additional_cost": 200
    },
    {
      "priority": "low",
      "action": "Increase thermal scan frequency to quarterly",
      "rationale": "9-year-old MCC may have other developing connection issues"
    }
  ],
  "monitoring_plan": {
    "parameters": [
      {
        "parameter": "Starter 12 temperature",
        "method": "thermal_scan",
        "frequency": "weekly until repaired",
        "alert_threshold": 160,
        "shutdown_threshold": 180
      }
    ],
    "escalation_criteria": [
      "If temperature exceeds 160°F: Expedite repair to within 48 hours",
      "If temperature exceeds 180°F: De-energize immediately"
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Threshold blindness**: Value just below threshold is still concerning if trending up.
2. **Single point prediction**: Always provide ranges/confidence for RUL estimates.
3. **Ignoring context**: Same vibration level means different things under different loads.
4. **Over-precision**: "42 days remaining life" implies false precision.

### Edge Cases to Handle
- **Insufficient data**: State uncertainty clearly
- **Conflicting indicators**: One parameter improving while another degrades
- **Intermittent issues**: May not appear in point-in-time readings
- **New equipment**: No baseline or historical pattern

### When NOT to Use This Prompt
- **Real-time alerting**: Needs different architecture
- **ML model training**: Different data format needed
- **Warranty claims**: Need specific documentation format
- **Safety-critical predictions**: Require certified methods

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-parameter analysis | Best at synthesizing multiple indicators |
| **Acceptable:** Claude Sonnet 4 | Standard predictions | Good balance |
| **Acceptable:** GPT-4o | Technical explanations | Strong on technical detail |
| **Caution:** Smaller models | - | May miss critical correlations |
