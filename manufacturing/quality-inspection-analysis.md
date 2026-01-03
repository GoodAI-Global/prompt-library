# Quality Inspection Analysis

## Use Case

Analyze quality inspection reports and data to determine pass/fail status:
- Visual inspection report analysis
- Dimensional measurement evaluation
- Defect classification and severity assessment
- Quality trend identification
- Corrective action recommendations

Use for automated quality gate decisions and quality data analysis in manufacturing.

## Input Format

**Required:**
- `inspection_data`: Inspection report, measurements, or observations
- `product_type`: Type of product being inspected

**Optional:**
- `specifications`: Product specifications and tolerances
- `inspection_type`: incoming, in_process, final, audit
- `quality_standards`: Applicable quality standards (ISO, industry-specific)
- `defect_catalog`: Known defect types and classifications
- `historical_data`: Prior inspection results for context

## Output Format

```json
{
  "inspection_result": {
    "inspection_id": "INS-2024-00123",
    "timestamp": "2024-01-15T10:30:00Z",
    "product_type": "machined_component",
    "overall_status": "conditional_pass",
    "confidence": 0.88
  },
  "measurements": [
    {
      "dimension": "outer_diameter",
      "specification": {"nominal": 25.00, "tolerance": 0.05, "unit": "mm"},
      "measured": 25.02,
      "deviation": 0.02,
      "status": "pass",
      "cpk": 1.33
    }
  ],
  "defects_found": [
    {
      "defect_type": "surface_scratch",
      "location": "top_face",
      "severity": "minor",
      "classification": "cosmetic",
      "disposition": "accept",
      "image_reference": "IMG-001"
    }
  ],
  "quality_scores": {
    "dimensional": 95,
    "visual": 85,
    "functional": 100,
    "overall": 92
  },
  "disposition": {
    "decision": "accept_with_deviation",
    "conditions": ["document minor cosmetic defect"],
    "requires_approval": false
  },
  "recommendations": [
    {
      "priority": "medium",
      "recommendation": "Review tooling for surface finish",
      "category": "process_improvement",
      "rationale": "Minor scratches may indicate tool wear"
    }
  ],
  "quality_metrics": {
    "this_batch": {"pass_rate": 0.95, "defect_rate": 0.05},
    "vs_historical": {"trend": "stable", "deviation": "+0.02"}
  }
}
```

## The Prompt

```
You are a quality inspection analyst for manufacturing operations. Analyze the inspection data and provide structured quality assessment.

PRODUCT TYPE: {{product_type}}
INSPECTION TYPE: {{inspection_type | default: "standard"}}

INSPECTION DATA:
{{inspection_data}}

{{#if specifications}}
PRODUCT SPECIFICATIONS:
{{specifications}}
{{/if}}

{{#if quality_standards}}
APPLICABLE STANDARDS:
{{quality_standards}}
{{/if}}

{{#if defect_catalog}}
DEFECT CATALOG:
{{defect_catalog}}
{{/if}}

{{#if historical_data}}
HISTORICAL DATA:
{{historical_data}}
{{/if}}

QUALITY ANALYSIS FRAMEWORK:

1. DIMENSIONAL ANALYSIS
   For each measured dimension:
   - Compare to specification (nominal ± tolerance)
   - Calculate deviation from nominal
   - Determine pass/fail status
   - Calculate process capability (Cpk) if sample data available

   Cpk interpretation:
   - ≥1.33: Capable process
   - 1.00-1.33: Marginal capability
   - <1.00: Process improvement needed

2. DEFECT CLASSIFICATION
   Severity levels:
   - critical: Safety issue or complete non-function
   - major: Significant functionality impact
   - minor: Slight functionality impact
   - cosmetic: Appearance only, no function impact

   Classifications:
   - dimensional: Out of tolerance
   - visual: Surface defects, discoloration
   - functional: Performance issues
   - material: Material defects
   - contamination: Foreign material

3. DISPOSITION DECISIONS
   Options:
   - accept: Meets all specifications
   - accept_with_deviation: Minor non-conformance, documented acceptance
   - rework: Can be corrected
   - scrap: Cannot be corrected
   - hold: Requires further evaluation
   - return_to_vendor: Incoming inspection failure

4. QUALITY SCORING
   Calculate scores (0-100) for:
   - dimensional: Based on deviation from nominal
   - visual: Based on surface quality
   - functional: Based on performance tests
   - overall: Weighted average

5. PASS/FAIL CRITERIA
   Overall status:
   - pass: All specs met, no defects
   - conditional_pass: Minor deviations, acceptable with documentation
   - fail_rework: Can be corrected
   - fail_scrap: Cannot be corrected
   - hold: Needs additional evaluation

6. CONFIDENCE SCORING
   - 1.0: Clear measurement, definitive result
   - 0.8-0.9: Clear with minor interpretation
   - 0.6-0.8: Some ambiguity in data
   - <0.6: Significant uncertainty, recommend re-inspection

7. RECOMMENDATIONS
   Categories:
   - immediate_action: Required now
   - process_improvement: Long-term optimization
   - investigation: Root cause analysis needed
   - documentation: Recording requirements

OUTPUT REQUIREMENTS:
- Clear pass/fail determination with confidence
- All measurements compared to specs
- Defects classified by severity
- Disposition decision with rationale
- Actionable recommendations
- Quality metrics for trending

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{product_type}}` | string | Yes | Type of product being inspected |
| `{{inspection_data}}` | string | Yes | Inspection measurements and observations |
| `{{specifications}}` | string | No | Product specifications and tolerances |
| `{{inspection_type}}` | string | No | Type of inspection being performed |
| `{{quality_standards}}` | string | No | Applicable quality standards |
| `{{defect_catalog}}` | string | No | Known defect classifications |
| `{{historical_data}}` | string | No | Prior inspection data for comparison |

## Examples

### Example 1: Machined Component - Pass

**Input:**
```
product_type: CNC machined aluminum housing
inspection_type: final
inspection_data: |
  PART NUMBER: HSG-2024-A
  LOT: L20240115-001
  QUANTITY: 50 pieces
  SAMPLE SIZE: 5 pieces (AQL inspection)

  DIMENSIONAL MEASUREMENTS (all in mm):

  | Dimension      | Spec      | Piece 1 | Piece 2 | Piece 3 | Piece 4 | Piece 5 |
  |----------------|-----------|---------|---------|---------|---------|---------|
  | Length         | 100±0.1   | 100.02  | 99.98   | 100.01  | 99.99   | 100.03  |
  | Width          | 50±0.05   | 50.01   | 49.99   | 50.02   | 50.00   | 49.98   |
  | Height         | 25±0.05   | 25.00   | 24.98   | 25.01   | 25.02   | 24.99   |
  | Bore Diameter  | 12+0/-0.02| 11.99   | 11.98   | 11.99   | 11.98   | 11.99   |
  | Thread Depth   | 10 min    | 10.5    | 10.3    | 10.4    | 10.2    | 10.5    |

  VISUAL INSPECTION:
  - Surface finish: Ra 1.6 (spec: Ra 3.2 max) - PASS
  - Anodize coating: Uniform, no bare spots - PASS
  - Edges: Deburred, no sharp edges - PASS
  - Marking: Part number legible - PASS

  FUNCTIONAL TESTS:
  - Thread gauge: GO/NO-GO passed all samples
  - Bore gauge: All within tolerance

  NOTES:
  - No defects observed on any sample
  - Excellent surface finish throughout lot

specifications: |
  Drawing: HSG-2024-A Rev C
  Material: 6061-T6 Aluminum
  Surface treatment: Type II anodize, clear
  Critical dimensions: Bore diameter (affects assembly)
```

**Output:**
```json
{
  "inspection_result": {
    "inspection_id": "INS-2024-00789",
    "timestamp": "2024-01-15T14:30:00Z",
    "product_type": "CNC machined aluminum housing",
    "part_number": "HSG-2024-A",
    "lot_number": "L20240115-001",
    "sample_size": 5,
    "lot_quantity": 50,
    "overall_status": "pass",
    "confidence": 0.98
  },
  "measurements": [
    {
      "dimension": "Length",
      "specification": {"nominal": 100.00, "tolerance_plus": 0.1, "tolerance_minus": 0.1, "unit": "mm"},
      "measured_values": [100.02, 99.98, 100.01, 99.99, 100.03],
      "mean": 100.006,
      "range": 0.05,
      "std_dev": 0.02,
      "min_deviation": -0.02,
      "max_deviation": 0.03,
      "status": "pass",
      "cpk": 1.67
    },
    {
      "dimension": "Width",
      "specification": {"nominal": 50.00, "tolerance_plus": 0.05, "tolerance_minus": 0.05, "unit": "mm"},
      "measured_values": [50.01, 49.99, 50.02, 50.00, 49.98],
      "mean": 50.00,
      "range": 0.04,
      "std_dev": 0.016,
      "min_deviation": -0.02,
      "max_deviation": 0.02,
      "status": "pass",
      "cpk": 1.04
    },
    {
      "dimension": "Height",
      "specification": {"nominal": 25.00, "tolerance_plus": 0.05, "tolerance_minus": 0.05, "unit": "mm"},
      "measured_values": [25.00, 24.98, 25.01, 25.02, 24.99],
      "mean": 25.00,
      "range": 0.04,
      "std_dev": 0.015,
      "min_deviation": -0.02,
      "max_deviation": 0.02,
      "status": "pass",
      "cpk": 1.11
    },
    {
      "dimension": "Bore Diameter",
      "specification": {"nominal": 12.00, "tolerance_plus": 0.00, "tolerance_minus": 0.02, "unit": "mm"},
      "measured_values": [11.99, 11.98, 11.99, 11.98, 11.99],
      "mean": 11.986,
      "range": 0.01,
      "std_dev": 0.005,
      "min_deviation": -0.02,
      "max_deviation": -0.01,
      "status": "pass",
      "cpk": 1.33,
      "notes": "Critical dimension - all within tolerance"
    },
    {
      "dimension": "Thread Depth",
      "specification": {"minimum": 10.0, "unit": "mm"},
      "measured_values": [10.5, 10.3, 10.4, 10.2, 10.5],
      "mean": 10.38,
      "min_value": 10.2,
      "status": "pass",
      "notes": "All samples exceed minimum requirement"
    }
  ],
  "visual_inspection": {
    "surface_finish": {
      "specification": "Ra 3.2 max",
      "measured": "Ra 1.6",
      "status": "pass",
      "notes": "Exceeds specification - excellent finish"
    },
    "anodize_coating": {
      "requirement": "Uniform Type II clear",
      "result": "Uniform, no bare spots",
      "status": "pass"
    },
    "edges": {
      "requirement": "Deburred, no sharp edges",
      "result": "Deburred, no sharp edges",
      "status": "pass"
    },
    "marking": {
      "requirement": "Part number legible",
      "result": "Part number legible",
      "status": "pass"
    }
  },
  "functional_tests": {
    "thread_gauge": {"test": "GO/NO-GO", "result": "pass", "samples_passed": 5, "samples_tested": 5},
    "bore_gauge": {"test": "Diameter check", "result": "pass", "samples_passed": 5, "samples_tested": 5}
  },
  "defects_found": [],
  "quality_scores": {
    "dimensional": 98,
    "visual": 100,
    "functional": 100,
    "overall": 99
  },
  "disposition": {
    "decision": "accept",
    "conditions": [],
    "requires_approval": false,
    "released_quantity": 50
  },
  "recommendations": [
    {
      "priority": "low",
      "recommendation": "Monitor Width dimension Cpk",
      "category": "process_improvement",
      "rationale": "Cpk of 1.04 is marginal. While passing, process could be optimized for more margin."
    }
  ],
  "quality_metrics": {
    "this_lot": {
      "pass_rate": 1.0,
      "defect_rate": 0,
      "average_cpk": 1.29
    },
    "capability_summary": {
      "dimensions_capable": 4,
      "dimensions_marginal": 1,
      "dimensions_incapable": 0
    }
  },
  "inspector_notes": "Excellent lot quality. No defects observed. Surface finish significantly better than requirement."
}
```

### Example 2: Visual Inspection - Conditional Pass

**Input:**
```
product_type: injection molded plastic enclosure
inspection_type: final
inspection_data: |
  PART: ENC-500 Front Cover
  LOT: M20240115
  QUANTITY: 200 pieces
  INSPECTION: 100% visual (cosmetic part)

  DEFECTS FOUND:
  - 3 pieces with minor sink marks near ribbing (barely visible)
  - 1 piece with small flow line on inside surface
  - 2 pieces with slight gate vestige (within spec but at limit)

  DIMENSIONAL SPOT CHECK (10 pieces):
  - All critical dimensions within spec
  - No warpage detected

  COLOR CHECK:
  - Color matches master sample
  - Gloss level consistent

  OVERALL:
  - 194 pieces: No visible defects
  - 6 pieces: Minor cosmetic issues as noted above

specifications: |
  Surface: Class A exterior finish required
  Critical areas: Front face must be defect-free
  Acceptable: Minor defects on interior surfaces only
  Gate vestige: 0.3mm max
```

**Output:**
```json
{
  "inspection_result": {
    "inspection_id": "INS-2024-00456",
    "timestamp": "2024-01-15T16:45:00Z",
    "product_type": "injection molded plastic enclosure",
    "part_number": "ENC-500",
    "lot_number": "M20240115",
    "inspection_method": "100% visual",
    "lot_quantity": 200,
    "overall_status": "conditional_pass",
    "confidence": 0.92
  },
  "defects_found": [
    {
      "defect_type": "sink_marks",
      "quantity": 3,
      "location": "near ribbing",
      "severity": "minor",
      "classification": "cosmetic",
      "visibility": "barely visible",
      "disposition": "hold_for_review",
      "notes": "Near internal ribs - may not be visible in assembly"
    },
    {
      "defect_type": "flow_lines",
      "quantity": 1,
      "location": "inside_surface",
      "severity": "minor",
      "classification": "cosmetic",
      "disposition": "accept",
      "notes": "Interior surface only - not visible in final product"
    },
    {
      "defect_type": "gate_vestige",
      "quantity": 2,
      "location": "gate_area",
      "severity": "minor",
      "classification": "cosmetic",
      "disposition": "accept_with_note",
      "notes": "At specification limit (0.3mm) but within tolerance"
    }
  ],
  "defect_summary": {
    "total_defective_pieces": 6,
    "defect_rate": 0.03,
    "defects_by_type": {
      "sink_marks": 3,
      "flow_lines": 1,
      "gate_vestige": 2
    },
    "defects_by_severity": {
      "critical": 0,
      "major": 0,
      "minor": 6,
      "cosmetic": 6
    }
  },
  "dimensional_results": {
    "sample_size": 10,
    "status": "pass",
    "critical_dimensions": "all within spec",
    "warpage": "none detected"
  },
  "color_results": {
    "color_match": "pass",
    "gloss_consistency": "pass"
  },
  "quality_scores": {
    "dimensional": 100,
    "visual": 85,
    "color_match": 100,
    "overall": 92
  },
  "disposition": {
    "decision": "accept_with_deviation",
    "breakdown": {
      "accept": 195,
      "hold_for_review": 3,
      "rework": 0,
      "scrap": 0
    },
    "conditions": [
      "3 pieces with sink marks require engineering review for acceptability",
      "Document minor cosmetic variations for lot traceability",
      "Monitor gate vestige trend - at specification limit"
    ],
    "requires_approval": true,
    "approval_level": "quality_engineer"
  },
  "recommendations": [
    {
      "priority": "medium",
      "recommendation": "Review packing pressure profile for sink mark reduction",
      "category": "process_improvement",
      "rationale": "Sink marks near ribs suggest potential packing optimization"
    },
    {
      "priority": "low",
      "recommendation": "Inspect gate trim tool for wear",
      "category": "investigation",
      "rationale": "Gate vestige at limit may indicate tool wear"
    },
    {
      "priority": "low",
      "recommendation": "Evaluate ribbing design for future tooling",
      "category": "design_feedback",
      "rationale": "Sink marks near ribs may be design-related"
    }
  ],
  "quality_metrics": {
    "this_lot": {
      "pass_rate": 0.97,
      "first_pass_yield": 0.97,
      "defect_rate": 0.03
    },
    "defect_pareto": [
      {"defect": "sink_marks", "count": 3, "percent": 50},
      {"defect": "gate_vestige", "count": 2, "percent": 33},
      {"defect": "flow_lines", "count": 1, "percent": 17}
    ]
  }
}
```

### Example 3: Critical Failure - Scrap Decision

**Input:**
```
product_type: safety-critical brake component
inspection_type: final
inspection_data: |
  PART: BRK-001 Brake Caliper Mount
  LOT: L-SAFETY-0115
  QUANTITY: 25 pieces
  SAMPLE: 100% inspection (safety critical)

  DIMENSIONAL INSPECTION:

  CRITICAL DIMENSION - MOUNTING HOLE DIAMETER:
  Specification: 12.00 +0.02/-0.00 mm (critical safety tolerance)

  Results:
  | Piece | Measurement | Status    |
  |-------|-------------|-----------|
  | 1-10  | 12.01       | PASS      |
  | 11-15 | 12.00       | PASS      |
  | 16    | 12.05       | FAIL      |
  | 17    | 12.04       | FAIL      |
  | 18    | 12.03       | FAIL      |
  | 19-22 | 12.02       | PASS      |
  | 23-25 | 12.01       | PASS      |

  3 pieces FAILED critical dimension - mounting holes oversized

  OTHER DIMENSIONS:
  - All other dimensions pass on all 25 pieces
  - Surface finish: All pass
  - Visual: No defects

  MATERIAL CERT:
  - Material certification matches specification

specifications: |
  SAFETY CRITICAL COMPONENT - ZERO DEFECTS ALLOWED ON CRITICAL DIMENSIONS
  Mounting hole: Must not exceed 12.02mm for proper bolt engagement
  Quality Level: PPAP Level 3, Cpk minimum 1.67
  Disposition: Any critical dimension failure = SCRAP
```

**Output:**
```json
{
  "inspection_result": {
    "inspection_id": "INS-2024-00890",
    "timestamp": "2024-01-15T11:20:00Z",
    "product_type": "safety-critical brake component",
    "part_number": "BRK-001",
    "lot_number": "L-SAFETY-0115",
    "inspection_method": "100% inspection",
    "lot_quantity": 25,
    "overall_status": "fail_partial_scrap",
    "confidence": 1.0
  },
  "measurements": [
    {
      "dimension": "Mounting Hole Diameter",
      "specification": {"nominal": 12.00, "tolerance_plus": 0.02, "tolerance_minus": 0.00, "unit": "mm"},
      "classification": "critical_safety",
      "results_summary": {
        "pass": 22,
        "fail": 3,
        "pass_rate": 0.88
      },
      "failed_pieces": [
        {"piece": 16, "measured": 12.05, "deviation": 0.03, "status": "fail_oversize"},
        {"piece": 17, "measured": 12.04, "deviation": 0.02, "status": "fail_oversize"},
        {"piece": 18, "measured": 12.03, "deviation": 0.01, "status": "fail_oversize"}
      ],
      "status": "fail",
      "cpk": 0.67,
      "notes": "CRITICAL FAILURE - 3 pieces exceed maximum tolerance"
    }
  ],
  "defects_found": [
    {
      "defect_type": "oversized_critical_dimension",
      "quantity": 3,
      "location": "mounting_hole",
      "severity": "critical",
      "classification": "dimensional",
      "piece_numbers": [16, 17, 18],
      "disposition": "scrap",
      "notes": "Safety critical dimension - no rework permitted"
    }
  ],
  "defect_summary": {
    "total_defective_pieces": 3,
    "defect_rate": 0.12,
    "critical_defects": 3,
    "major_defects": 0,
    "minor_defects": 0
  },
  "quality_scores": {
    "dimensional": 0,
    "visual": 100,
    "material": 100,
    "overall": 0
  },
  "disposition": {
    "decision": "fail_partial_scrap",
    "breakdown": {
      "accept": 22,
      "scrap": 3,
      "hold": 0,
      "rework": 0
    },
    "scrap_pieces": [16, 17, 18],
    "scrap_rationale": "Critical safety dimension exceeded - no deviation permitted per quality requirements",
    "requires_approval": true,
    "approval_level": "quality_manager",
    "notification_required": [
      "production_supervisor",
      "quality_manager",
      "engineering"
    ]
  },
  "containment_actions": [
    {
      "action": "Segregate failed pieces immediately",
      "priority": "immediate",
      "status": "required"
    },
    {
      "action": "Verify no prior lots affected - check last 5 production runs",
      "priority": "immediate",
      "status": "required"
    },
    {
      "action": "Hold current WIP for 100% inspection",
      "priority": "immediate",
      "status": "required"
    }
  ],
  "root_cause_investigation": {
    "required": true,
    "initial_observations": [
      "Failed pieces are sequential (16, 17, 18) suggesting process drift",
      "Failures occurred mid-lot, not at start or end",
      "Possible tool wear or machine adjustment issue"
    ],
    "investigation_points": [
      "Review tool change/adjustment log around piece 16",
      "Check reamer/boring bar for wear",
      "Review spindle condition and thermal drift",
      "Verify measurement equipment calibration"
    ]
  },
  "recommendations": [
    {
      "priority": "critical",
      "recommendation": "Initiate 8D investigation for critical dimension failure",
      "category": "immediate_action",
      "rationale": "Safety critical failure requires formal root cause analysis"
    },
    {
      "priority": "critical",
      "recommendation": "Review and contain any downstream inventory from this lot",
      "category": "containment",
      "rationale": "Ensure no non-conforming parts in assembly or shipment"
    },
    {
      "priority": "high",
      "recommendation": "Implement in-process gaging for this dimension",
      "category": "process_improvement",
      "rationale": "100% final inspection is reactive - in-process check would catch earlier"
    },
    {
      "priority": "high",
      "recommendation": "Verify Cpk capability after corrective action",
      "category": "process_improvement",
      "rationale": "Current Cpk of 0.67 indicates incapable process for safety-critical dimension"
    }
  ],
  "quality_metrics": {
    "this_lot": {
      "pass_rate": 0.88,
      "first_pass_yield": 0.88,
      "critical_defect_rate": 0.12,
      "cpk_critical_dimension": 0.67
    },
    "trend_alert": {
      "level": "critical",
      "message": "Cpk below 1.67 minimum for safety-critical dimension"
    }
  },
  "escalation": {
    "level": "quality_incident",
    "notifications": ["quality_manager", "plant_manager", "customer_quality"],
    "documentation_required": ["8D report", "containment record", "scrap authorization"]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Spec interpretation**: Unilateral vs bilateral tolerance. +0.02/-0.00 is NOT ±0.02.
2. **Sample size math**: Cpk requires minimum sample size for statistical validity.
3. **Critical vs major**: Don't downgrade critical safety issues to major.
4. **Visual subjectivity**: "Minor scratch" needs consistent definition.

### Edge Cases to Handle
- **Measurement uncertainty**: CMM accuracy affects pass/fail on tight tolerances
- **Environmental effects**: Temperature affects dimensional measurements
- **Lot segregation**: Mixed conforming/non-conforming requires tracking
- **Rework verification**: Re-inspection required after any rework

### When NOT to Use This Prompt
- **Statistical process control**: Different analysis for SPC charting
- **First article inspection**: Needs enhanced documentation
- **Customer returns**: Different disposition logic
- **Regulatory audits**: Specific format requirements

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-dimensional inspection | Best judgment on edge cases |
| **Acceptable:** Claude Sonnet 4 | Standard inspections | Good balance |
| **Acceptable:** GPT-4o | Visual inspection analysis | Strong with descriptions |
| **Caution:** Smaller models | - | May miss critical issues |

## Integration Notes

### Decision Logic
```python
def disposition_decision(inspection_result):
    """Determine lot disposition based on inspection results"""
    critical_failures = [
        d for d in inspection_result['defects_found']
        if d['severity'] == 'critical'
    ]

    if critical_failures:
        return {
            'decision': 'fail',
            'reason': 'critical_defects',
            'requires_8d': True
        }

    major_failures = [
        d for d in inspection_result['defects_found']
        if d['severity'] == 'major'
    ]

    if major_failures:
        defect_rate = len(major_failures) / inspection_result['lot_quantity']
        if defect_rate > 0.02:  # AQL threshold
            return {'decision': 'fail', 'reason': 'aql_exceeded'}
        return {'decision': 'conditional_pass', 'requires_mrb': True}

    return {'decision': 'pass'}
```

### Traceability
```python
def create_inspection_record(result):
    """Create traceable inspection record"""
    return {
        "inspection_id": result['inspection_result']['inspection_id'],
        "lot_number": result['inspection_result']['lot_number'],
        "part_number": result['inspection_result']['part_number'],
        "quantity_inspected": result['inspection_result']['lot_quantity'],
        "quantity_passed": result['disposition']['breakdown']['accept'],
        "quantity_failed": sum([
            result['disposition']['breakdown'].get('scrap', 0),
            result['disposition']['breakdown'].get('rework', 0)
        ]),
        "disposition": result['disposition']['decision'],
        "timestamp": result['inspection_result']['timestamp'],
        "inspector_id": get_current_inspector(),
        "equipment_used": get_inspection_equipment(),
        "attachments": result.get('image_references', [])
    }
```
