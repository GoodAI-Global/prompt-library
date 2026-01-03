# Maintenance Log Interpretation

## Use Case

Analyze maintenance logs and work orders to extract insights:
- Work order summarization
- Maintenance pattern identification
- Equipment health trending
- Technician note interpretation
- Compliance documentation extraction

Use for maintenance analytics, reliability engineering, and CMMS data quality improvement.

## Input Format

**Required:**
- `maintenance_logs`: Raw maintenance log entries, work orders, or technician notes
- `equipment_id`: Equipment identifier or asset tag

**Optional:**
- `equipment_info`: Equipment type, manufacturer, model, age
- `maintenance_history`: Prior maintenance records for context
- `failure_codes`: Standard failure code definitions
- `time_range`: Period covered by logs

## Output Format

```json
{
  "log_analysis": {
    "equipment_id": "EQ-12345",
    "time_range": {"start": "2024-01-01", "end": "2024-01-15"},
    "entries_analyzed": 12,
    "analysis_timestamp": "2024-01-15T10:00:00Z"
  },
  "work_summary": [
    {
      "work_order": "WO-2024-001",
      "date": "2024-01-05",
      "work_type": "corrective",
      "category": "mechanical",
      "description": "Replaced worn bearing on main drive",
      "components": ["drive_bearing"],
      "duration_hours": 2.5,
      "technician_observations": ["Bearing showed excessive wear", "Checked adjacent bearings - OK"]
    }
  ],
  "patterns_identified": [
    {
      "pattern": "recurring_failure",
      "description": "Belt replacement every 3 months",
      "frequency": "quarterly",
      "recommendation": "Evaluate belt specification or tension"
    }
  ],
  "health_indicators": {
    "overall_status": "attention_needed",
    "failure_trend": "increasing",
    "mtbf_current": 720,
    "mtbf_trend": "declining",
    "risk_level": "medium"
  },
  "action_items": [
    {
      "priority": "high",
      "action": "Schedule vibration analysis",
      "rationale": "Multiple bearing mentions suggest developing issue",
      "due_date": "2024-01-30"
    }
  ],
  "compliance_notes": {
    "pm_adherence": "85%",
    "overdue_tasks": ["Annual inspection - due 2024-01-10"],
    "documentation_gaps": ["Missing calibration record"]
  }
}
```

## The Prompt

```
You are a maintenance analyst specializing in interpreting maintenance logs and work orders. Analyze the provided logs and extract structured insights.

EQUIPMENT ID: {{equipment_id}}

MAINTENANCE LOGS:
{{maintenance_logs}}

{{#if equipment_info}}
EQUIPMENT INFORMATION:
{{equipment_info}}
{{/if}}

{{#if maintenance_history}}
MAINTENANCE HISTORY:
{{maintenance_history}}
{{/if}}

{{#if failure_codes}}
FAILURE CODE DEFINITIONS:
{{failure_codes}}
{{/if}}

{{#if time_range}}
TIME RANGE: {{time_range}}
{{/if}}

LOG ANALYSIS FRAMEWORK:

1. WORK ORDER CLASSIFICATION
   Work Types:
   - preventive: Scheduled maintenance (PM)
   - predictive: Condition-based maintenance (PdM)
   - corrective: Unplanned repair after failure
   - emergency: Urgent repair affecting production
   - improvement: Upgrades or modifications

   Categories:
   - mechanical: Bearings, gears, belts, motors
   - electrical: Wiring, controls, sensors, drives
   - hydraulic: Pumps, valves, cylinders, hoses
   - pneumatic: Compressors, actuators, valves
   - lubrication: Oil, grease, fluid changes
   - safety: Guards, interlocks, emergency stops
   - calibration: Sensor adjustments, alignment

2. TECHNICIAN NOTES INTERPRETATION
   Extract from free-text notes:
   - Symptoms observed
   - Root cause findings
   - Parts replaced/repaired
   - Condition observations
   - Recommendations for future
   - Safety concerns noted

   Common abbreviations:
   - PM: Preventive Maintenance
   - CM: Corrective Maintenance
   - WO: Work Order
   - OOS: Out of Service
   - NFF: No Fault Found
   - R&R: Remove and Replace

3. PATTERN IDENTIFICATION
   Look for:
   - Recurring failures (same component, similar symptoms)
   - Seasonal patterns (temperature, humidity related)
   - Degradation trends (increasing frequency)
   - Related failures (failure cascade patterns)
   - PM effectiveness (failures between PMs)

4. HEALTH INDICATORS
   Calculate/estimate:
   - MTBF (Mean Time Between Failures)
   - MTTR (Mean Time To Repair)
   - Availability (uptime percentage)
   - PM completion rate
   - Corrective/Preventive ratio

   Status levels:
   - healthy: No concerns, stable operation
   - attention_needed: Minor issues or developing trends
   - degraded: Significant issues requiring action
   - critical: Immediate intervention required

5. COMPLIANCE TRACKING
   Identify:
   - Overdue PM tasks
   - Missing documentation
   - Calibration status
   - Safety inspection gaps
   - Regulatory requirements

6. ROOT CAUSE INDICATORS
   Flag entries suggesting:
   - Design issues (repeated same failure)
   - Operating issues (operator error, overload)
   - Maintenance issues (improper repair, PM gap)
   - Age/wear-out (expected end of life)

OUTPUT REQUIREMENTS:
- Structured summary of all work orders
- Pattern analysis with recommendations
- Health status with supporting metrics
- Prioritized action items
- Compliance gaps identified

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{equipment_id}}` | string | Yes | Equipment identifier |
| `{{maintenance_logs}}` | string | Yes | Raw maintenance logs/work orders |
| `{{equipment_info}}` | string | No | Equipment details |
| `{{maintenance_history}}` | string | No | Historical maintenance data |
| `{{failure_codes}}` | string | No | Failure code definitions |
| `{{time_range}}` | string | No | Analysis time period |

## Examples

### Example 1: CNC Machine Analysis

**Input:**
```
equipment_id: CNC-LATHE-005
equipment_info: |
  Type: CNC Turning Center
  Make: Haas
  Model: ST-30
  Year: 2018
  Hours: 24,500

maintenance_logs: |
  WO-2024-0112 | 01/15/2024 | PM | Completed
  Technician: Mike S.
  Performed 500-hour PM checklist. Checked spindle bearings - slight roughness
  noted but within spec. Replaced way lube filter. Topped off hydraulic oil.
  Greased all fittings. Coolant concentration 8% - adjusted to 10%.
  Notes: Recommend monitoring spindle bearings - schedule vibration analysis.
  Time: 3 hours

  WO-2024-0098 | 01/10/2024 | CM | Completed
  Technician: Dave R.
  Machine stopped mid-cycle with alarm "Spindle Drive Fault".
  Found loose connection at spindle drive. Reseated connector, tested OK.
  Production resumed after 45 min downtime.
  Time: 1 hour

  WO-2024-0085 | 01/05/2024 | CM | Completed
  Technician: Mike S.
  Operator reported unusual vibration during heavy cuts.
  Checked spindle balance - OK. Checked toolholder - found runout 0.002".
  Replaced toolholder, vibration eliminated.
  Notes: Toolholder wear - need to rotate stock more frequently.
  Time: 1.5 hours

  WO-2024-0071 | 01/02/2024 | PM | Completed
  Technician: Carlos M.
  Quarterly PM - Full inspection per manufacturer spec.
  All systems checked OK. Replaced coolant filter. Calibrated tool probe.
  No issues found.
  Time: 4 hours

  WO-2023-1245 | 12/15/2023 | CM | Completed
  Technician: Dave R.
  Spindle orientation error on tool change. Reset parameters, cleared alarm.
  Suspect low battery on encoder - recommend replacing at next PM.
  Time: 0.5 hours

  WO-2023-1180 | 11/28/2023 | CM | Completed
  Technician: Mike S.
  Coolant pump failed - no flow. Replaced pump motor. Flushed coolant system.
  Root cause: Pump motor bearing failure due to coolant ingress.
  Added recommendation to check motor seals at PMs.
  Time: 4 hours
```

**Output:**
```json
{
  "log_analysis": {
    "equipment_id": "CNC-LATHE-005",
    "equipment_type": "CNC Turning Center",
    "make_model": "Haas ST-30",
    "age_years": 6,
    "operating_hours": 24500,
    "time_range": {"start": "2023-11-28", "end": "2024-01-15"},
    "entries_analyzed": 6,
    "analysis_timestamp": "2024-01-15T10:00:00Z"
  },
  "work_summary": [
    {
      "work_order": "WO-2024-0112",
      "date": "2024-01-15",
      "work_type": "preventive",
      "category": "multi_system",
      "description": "500-hour PM checklist completion",
      "components": ["spindle_bearings", "way_lube_filter", "hydraulic_system", "lubrication_points", "coolant_system"],
      "duration_hours": 3.0,
      "technician": "Mike S.",
      "technician_observations": [
        "Spindle bearings showing slight roughness - within spec but noted for monitoring",
        "Coolant concentration was low (8%) - adjusted to 10%"
      ],
      "recommendations": ["Schedule vibration analysis for spindle bearings"]
    },
    {
      "work_order": "WO-2024-0098",
      "date": "2024-01-10",
      "work_type": "corrective",
      "category": "electrical",
      "description": "Spindle drive fault - loose connection",
      "components": ["spindle_drive", "electrical_connections"],
      "duration_hours": 1.0,
      "downtime_production": 0.75,
      "technician": "Dave R.",
      "technician_observations": ["Loose connector at spindle drive caused fault alarm"],
      "root_cause": "loose_connection"
    },
    {
      "work_order": "WO-2024-0085",
      "date": "2024-01-05",
      "work_type": "corrective",
      "category": "mechanical",
      "description": "Vibration during cutting - worn toolholder",
      "components": ["toolholder"],
      "duration_hours": 1.5,
      "technician": "Mike S.",
      "technician_observations": [
        "Toolholder runout at 0.002 inch",
        "Spindle balance checked - OK"
      ],
      "recommendations": ["Rotate toolholder stock more frequently"]
    },
    {
      "work_order": "WO-2024-0071",
      "date": "2024-01-02",
      "work_type": "preventive",
      "category": "multi_system",
      "description": "Quarterly PM - full inspection",
      "components": ["coolant_filter", "tool_probe"],
      "duration_hours": 4.0,
      "technician": "Carlos M.",
      "technician_observations": ["All systems checked OK"]
    },
    {
      "work_order": "WO-2023-1245",
      "date": "2023-12-15",
      "work_type": "corrective",
      "category": "electrical",
      "description": "Spindle orientation error on tool change",
      "components": ["encoder", "spindle_orientation"],
      "duration_hours": 0.5,
      "technician": "Dave R.",
      "technician_observations": ["Possible low encoder battery"],
      "recommendations": ["Replace encoder battery at next PM"]
    },
    {
      "work_order": "WO-2023-1180",
      "date": "2023-11-28",
      "work_type": "corrective",
      "category": "mechanical",
      "description": "Coolant pump failure - motor replaced",
      "components": ["coolant_pump", "pump_motor"],
      "duration_hours": 4.0,
      "technician": "Mike S.",
      "technician_observations": ["Motor bearing failure due to coolant ingress"],
      "recommendations": ["Add motor seal check to PM checklist"]
    }
  ],
  "patterns_identified": [
    {
      "pattern": "spindle_attention",
      "description": "Multiple spindle-related entries in short period",
      "entries": ["WO-2024-0112", "WO-2024-0098", "WO-2023-1245"],
      "frequency": "3 entries in 2 months",
      "concern_level": "medium",
      "recommendation": "Schedule comprehensive spindle inspection including vibration analysis. Pattern suggests developing spindle issue."
    },
    {
      "pattern": "electrical_intermittent",
      "description": "Two electrical issues with loose connections/intermittent faults",
      "entries": ["WO-2024-0098", "WO-2023-1245"],
      "frequency": "2 in 1 month",
      "concern_level": "low",
      "recommendation": "Review electrical connections during next PM. Consider thermal cycling effects."
    }
  ],
  "health_indicators": {
    "overall_status": "attention_needed",
    "primary_concern": "spindle_system",
    "concern_details": "Spindle bearing roughness noted, spindle drive fault, and orientation error within 2 months suggest developing spindle issues",
    "failure_trend": "stable_but_watch",
    "mtbf_estimate": {
      "value": 360,
      "unit": "hours",
      "calculation": "4 corrective WOs over ~500 operating hours",
      "trend": "needs_monitoring"
    },
    "mttr_average": {
      "value": 1.75,
      "unit": "hours"
    },
    "pm_adherence": "100%",
    "corrective_to_preventive_ratio": "2:1",
    "risk_level": "medium"
  },
  "action_items": [
    {
      "priority": "high",
      "action": "Schedule spindle vibration analysis",
      "rationale": "Technician noted spindle bearing roughness and recommended analysis. Combined with drive fault suggests proactive investigation needed.",
      "due_date": "2024-01-30",
      "assigned_to": "reliability_engineering"
    },
    {
      "priority": "medium",
      "action": "Replace encoder battery",
      "rationale": "Technician suspects low battery caused orientation error. Prevent repeat failure.",
      "due_date": "next_PM",
      "assigned_to": "maintenance"
    },
    {
      "priority": "medium",
      "action": "Add motor seal inspection to PM checklist",
      "rationale": "Coolant pump failure was caused by seal deterioration. Prevent similar failures.",
      "due_date": "2024-01-31",
      "assigned_to": "maintenance_planner"
    },
    {
      "priority": "low",
      "action": "Implement toolholder rotation program",
      "rationale": "Worn toolholder caused quality issue. Regular rotation extends life and maintains quality.",
      "due_date": "2024-02-15",
      "assigned_to": "production_supervisor"
    }
  ],
  "compliance_notes": {
    "pm_adherence": "100%",
    "pm_schedule": "On track - next 500hr PM due at 25,000 hours",
    "overdue_tasks": [],
    "documentation_quality": "Good - technicians providing detailed observations",
    "recommendations_follow_up": {
      "pending": [
        "Vibration analysis (WO-2024-0112)",
        "Encoder battery replacement (WO-2023-1245)",
        "Motor seal check addition to PM (WO-2023-1180)"
      ]
    }
  },
  "technician_insights": {
    "quality_observations": "Technicians are providing valuable predictive observations",
    "notable_catches": [
      "Mike S. identified spindle bearing roughness before failure",
      "Dave R. identified low battery as potential root cause",
      "Mike S. identified coolant ingress as pump failure cause"
    ],
    "knowledge_sharing": "Consider sharing spindle observations across shifts"
  }
}
```

### Example 2: HVAC System with Recurring Issues

**Input:**
```
equipment_id: HVAC-RTU-03
equipment_info: |
  Type: Rooftop Unit
  Make: Carrier
  Capacity: 20 tons
  Age: 12 years

maintenance_logs: |
  01/12/24 - EMERGENCY - Unit not cooling
  Found compressor #1 tripped on high pressure. Checked condenser - extremely dirty.
  Cleaned condenser coils. Reset compressor. Unit running but compressor #2 struggling.
  Recommend replacing compressor #2 soon.

  12/15/23 - PM - Quarterly
  Checked refrigerant - low on R-410A, added 3 lbs. Replaced filters.
  Condenser coils need cleaning but skipped due to weather (too cold).

  09/18/23 - EMERGENCY - No cooling
  Compressor #2 locked rotor. Replaced contactor, unit running on comp #1 only.
  Temporary fix - comp #2 may need replacement.

  06/22/23 - PM - Summer prep
  Low on refrigerant again - added 2 lbs. Possible leak but couldn't locate.
  Cleaned condenser. Replaced filters. Checked belts.

  03/14/23 - PM - Spring startup
  Added 4 lbs refrigerant (significantly low). Belts cracking - replaced.
  Unit old - recommend planning for replacement next budget cycle.
```

**Output:**
```json
{
  "log_analysis": {
    "equipment_id": "HVAC-RTU-03",
    "equipment_type": "Rooftop Unit",
    "make": "Carrier",
    "capacity": "20 tons",
    "age_years": 12,
    "time_range": {"start": "2023-03-14", "end": "2024-01-12"},
    "entries_analyzed": 5,
    "analysis_timestamp": "2024-01-15T10:00:00Z"
  },
  "work_summary": [
    {
      "work_order": "01/12/24",
      "date": "2024-01-12",
      "work_type": "emergency",
      "category": "mechanical",
      "description": "Unit not cooling - compressor tripped, dirty condenser",
      "components": ["compressor_1", "compressor_2", "condenser_coils"],
      "technician_observations": [
        "Compressor #1 tripped on high pressure",
        "Condenser extremely dirty",
        "Compressor #2 struggling"
      ],
      "recommendations": ["Replace compressor #2 soon"]
    },
    {
      "work_order": "12/15/23",
      "date": "2023-12-15",
      "work_type": "preventive",
      "category": "multi_system",
      "description": "Quarterly PM - added refrigerant, replaced filters",
      "components": ["refrigerant_system", "filters", "condenser_coils"],
      "technician_observations": [
        "Low on R-410A - added 3 lbs",
        "Condenser cleaning skipped due to weather"
      ],
      "issues_deferred": ["Condenser coil cleaning"]
    },
    {
      "work_order": "09/18/23",
      "date": "2023-09-18",
      "work_type": "emergency",
      "category": "electrical",
      "description": "No cooling - compressor #2 locked rotor",
      "components": ["compressor_2", "contactor"],
      "technician_observations": [
        "Compressor #2 locked rotor",
        "Replaced contactor as temporary fix",
        "Unit running on compressor #1 only"
      ],
      "recommendations": ["Compressor #2 may need replacement"]
    },
    {
      "work_order": "06/22/23",
      "date": "2023-06-22",
      "work_type": "preventive",
      "category": "multi_system",
      "description": "Summer prep PM",
      "components": ["refrigerant_system", "condenser_coils", "filters", "belts"],
      "technician_observations": [
        "Low on refrigerant again - added 2 lbs",
        "Possible leak but couldn't locate"
      ],
      "recommendations": ["Investigate refrigerant leak"]
    },
    {
      "work_order": "03/14/23",
      "date": "2023-03-14",
      "work_type": "preventive",
      "category": "multi_system",
      "description": "Spring startup PM",
      "components": ["refrigerant_system", "belts"],
      "technician_observations": [
        "Significantly low on refrigerant - added 4 lbs",
        "Belts cracking - replaced"
      ],
      "recommendations": ["Plan for unit replacement next budget cycle"]
    }
  ],
  "patterns_identified": [
    {
      "pattern": "chronic_refrigerant_leak",
      "description": "Repeated refrigerant additions over 10 months",
      "entries": ["03/14/23", "06/22/23", "12/15/23"],
      "frequency": "Every PM requires refrigerant",
      "total_refrigerant_added": "9 lbs in 10 months",
      "concern_level": "high",
      "recommendation": "Perform leak detection. 9 lbs lost in 10 months is significant. Environmental and cost impact."
    },
    {
      "pattern": "compressor_2_degradation",
      "description": "Compressor #2 showing progressive failure",
      "entries": ["09/18/23", "01/12/24"],
      "timeline": [
        "09/18: Locked rotor - contactor replaced as temporary fix",
        "01/12: Still struggling after comp #1 returned to service"
      ],
      "concern_level": "critical",
      "recommendation": "Compressor #2 failure imminent. Plan replacement or unit replacement."
    },
    {
      "pattern": "deferred_maintenance",
      "description": "Condenser cleaning deferred then caused emergency",
      "entries": ["12/15/23", "01/12/24"],
      "timeline": [
        "12/15: Cleaning skipped due to weather",
        "01/12: Dirty condenser caused high pressure trip"
      ],
      "concern_level": "medium",
      "recommendation": "Do not defer condenser cleaning. Schedule for suitable weather conditions."
    }
  ],
  "health_indicators": {
    "overall_status": "critical",
    "primary_concern": "end_of_life",
    "concern_details": "12-year-old unit with chronic refrigerant leak, failing compressor, and multiple emergency calls indicates unit approaching end of useful life",
    "failure_trend": "increasing",
    "mtbf_estimate": {
      "value": 1800,
      "unit": "hours",
      "calculation": "2 emergencies in ~3600 operating hours",
      "trend": "declining"
    },
    "availability_estimate": "Degraded - operating on 1 of 2 compressors",
    "pm_adherence": "100%",
    "pm_effectiveness": "Low - PMs not preventing failures",
    "corrective_to_preventive_ratio": "2:3",
    "risk_level": "high",
    "failure_probability_30_day": "high"
  },
  "action_items": [
    {
      "priority": "critical",
      "action": "Capital planning for unit replacement",
      "rationale": "12-year-old unit with multiple systemic issues. Repair costs approaching replacement value. Technician recommended replacement in March 2023.",
      "budget_estimate": "$25,000-$40,000 for 20-ton RTU",
      "timeline": "Plan for next budget cycle; interim repairs may be needed"
    },
    {
      "priority": "high",
      "action": "Perform comprehensive leak detection",
      "rationale": "9 lbs refrigerant lost in 10 months. R-410A cost and environmental regulations require repair or documentation.",
      "due_date": "2024-01-31",
      "estimated_cost": "$500-$800 for detection; repair unknown"
    },
    {
      "priority": "high",
      "action": "Assess compressor #2 for replacement vs unit replacement",
      "rationale": "Compressor struggling and previously failed. Determine if repair extends useful life or if funds better spent on replacement.",
      "due_date": "2024-01-25",
      "decision_needed": "Repair compressor ($3,000-5,000) vs replace unit"
    },
    {
      "priority": "medium",
      "action": "Clean condenser coils",
      "rationale": "Dirty condenser caused most recent emergency. Clean regardless of weather using appropriate methods.",
      "due_date": "2024-01-20"
    }
  ],
  "compliance_notes": {
    "pm_adherence": "100%",
    "refrigerant_tracking": {
      "concern": "high",
      "details": "9 lbs R-410A added in 10 months without leak repair",
      "regulation": "EPA Section 608 requires repair if leak rate exceeds threshold",
      "action_needed": "Document leak rate; perform leak detection; repair or document exemption"
    },
    "documentation_gaps": [
      "Leak detection not performed despite multiple refrigerant additions"
    ]
  },
  "cost_analysis": {
    "maintenance_cost_10_months": {
      "refrigerant": "$450 (9 lbs @ ~$50/lb)",
      "emergency_repairs": "$800 (estimated)",
      "pm_labor": "$600",
      "total": "$1,850"
    },
    "projected_repair_cost": {
      "compressor_replacement": "$3,000-$5,000",
      "leak_repair": "$500-$2,000"
    },
    "replacement_cost": "$25,000-$40,000",
    "recommendation": "At current failure rate and repair costs, replacement ROI likely within 2-3 years"
  }
}
```

## Gotchas

### Common Failure Modes
1. **Abbreviation misinterpretation**: Industry-specific abbreviations vary. "LB" could be pounds or locked rotor blocked.
2. **Time zone confusion**: Log timestamps may be local, UTC, or server time.
3. **Technician subjectivity**: "Running rough" means different things to different people.
4. **Missing context**: "Fixed the issue" without details loses valuable information.

### Edge Cases to Handle
- **Handwritten logs**: OCR quality varies
- **Multiple technicians**: Different terminology and documentation styles
- **Incomplete entries**: Missing dates, times, or details
- **Foreign equipment**: Non-English documentation

### When NOT to Use This Prompt
- **Real-time monitoring**: Different analysis for live sensor data
- **Predictive maintenance models**: Different input format
- **CMMS data migration**: Needs specific field mapping
- **Regulatory compliance reports**: Specific format requirements

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex logs, pattern detection | Best judgment on ambiguous entries |
| **Acceptable:** Claude Sonnet 4 | Standard log analysis | Good balance |
| **Acceptable:** GPT-4o | Mixed format logs | Strong at interpreting varied formats |
| **Caution:** Smaller models | - | May miss patterns |
