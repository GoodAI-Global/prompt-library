# Underwriting Risk Assessment

## Use Case

Analyze insurance applications and supporting data to assess risk:
- New business submission review
- Renewal risk assessment
- Coverage modification analysis
- Risk classification recommendations
- Premium adequacy evaluation

Use to support underwriting decisions with structured risk analysis.

## Input Format

**Required:**
- `application_data`: Application details and submitted information
- `line_of_business`: commercial_property, general_liability, auto, workers_comp, professional_liability, cyber

**Optional:**
- `loss_history`: Prior claims and loss runs
- `inspection_data`: Physical inspection reports
- `financial_data`: Financial statements, credit information
- `industry_data`: Industry benchmarks and class data
- `underwriting_guidelines`: Carrier-specific guidelines to apply

## Output Format

```json
{
  "assessment_summary": {
    "risk_id": "UW-2024-00123",
    "assessment_date": "2024-01-15",
    "line_of_business": "commercial_property",
    "overall_risk_grade": "B+",
    "recommendation": "accept_with_conditions",
    "confidence": 0.85
  },
  "risk_factors": [
    {
      "factor": "Building construction",
      "current_value": "Frame",
      "impact": "negative",
      "severity": "medium",
      "weight": 15,
      "notes": "Higher fire risk than masonry"
    }
  ],
  "positive_factors": [...],
  "negative_factors": [...],
  "risk_scoring": {
    "property_score": 72,
    "liability_score": 85,
    "management_score": 80,
    "financial_score": 78,
    "overall_score": 79
  },
  "loss_analysis": {
    "frequency": "average",
    "severity": "below_average",
    "trend": "improving",
    "loss_ratio": 45,
    "expected_losses": 12500
  },
  "pricing_considerations": {
    "base_rate_adequacy": "adequate",
    "suggested_modifications": [
      {
        "factor": "schedule_credit",
        "value": -5,
        "rationale": "Sprinkler system upgrade"
      }
    ],
    "minimum_premium": 8500,
    "target_premium": 10200
  },
  "conditions": [
    {
      "condition": "Install monitored burglar alarm",
      "type": "pre-bind",
      "mandatory": true,
      "rationale": "Crime score indicates elevated theft risk"
    }
  ],
  "recommendations": [...],
  "referral_triggers": []
}
```

## The Prompt

```
You are an insurance underwriting analyst. Assess the risk presented in the application and provide structured analysis.

LINE OF BUSINESS: {{line_of_business}}

APPLICATION DATA:
{{application_data}}

{{#if loss_history}}
LOSS HISTORY:
{{loss_history}}
{{/if}}

{{#if inspection_data}}
INSPECTION DATA:
{{inspection_data}}
{{/if}}

{{#if financial_data}}
FINANCIAL DATA:
{{financial_data}}
{{/if}}

{{#if industry_data}}
INDUSTRY BENCHMARKS:
{{industry_data}}
{{/if}}

{{#if underwriting_guidelines}}
CARRIER GUIDELINES:
{{underwriting_guidelines}}
{{/if}}

RISK ASSESSMENT FRAMEWORK:

1. PROPERTY RISK FACTORS
   - Construction type (fire resistive to frame)
   - Age and condition of building
   - Protection class and distance to fire station
   - Occupancy type and hazards
   - Roof type and age
   - Electrical, plumbing, HVAC condition
   - Sprinkler and alarm systems
   - Catastrophe exposure (wind, flood, earthquake)
   - Crime score and neighborhood
   - Replacement cost adequacy

2. LIABILITY RISK FACTORS
   - Operations hazard class
   - Products/completed operations exposure
   - Contractual liability exposure
   - Premises exposure (foot traffic, conditions)
   - Professional services exposure
   - Prior claims and litigation history
   - Safety programs and training
   - Regulatory compliance history

3. MANAGEMENT/FINANCIAL FACTORS
   - Years in business
   - Management experience
   - Financial stability (revenue trend, credit)
   - Business continuity planning
   - Insurance history (prior coverage, gaps)
   - Risk management practices

4. LOSS ANALYSIS
   - Loss frequency (count per exposure unit)
   - Loss severity (average claim size)
   - Trend (improving, stable, deteriorating)
   - Large loss experience
   - Incurred but not reported (IBNR) considerations
   - Expected loss calculation

5. RISK GRADING SCALE
   A+: Highly preferred risk, all factors favorable
   A:  Preferred risk, predominantly favorable
   B+: Above average, minor concerns
   B:  Average risk, standard terms
   B-: Below average, additional conditions needed
   C:  Marginal risk, significant conditions or restrictions
   D:  Substandard, decline or specialized market

6. RECOMMENDATION OPTIONS
   - accept: Standard terms
   - accept_with_conditions: Specify conditions
   - accept_with_modifications: Pricing/coverage modifications
   - refer: To senior underwriter or specialty unit
   - decline: Outside appetite

7. PRICING CONSIDERATIONS
   - Rate adequacy for class
   - Schedule rating credits/debits
   - Experience modification
   - Minimum premium requirements
   - Deductible options
   - Coverage restrictions

8. CONDITIONS AND RECOMMENDATIONS
   - Pre-bind requirements
   - Policy conditions
   - Recommended endorsements
   - Risk improvement recommendations
   - Documentation requirements

REFERRAL TRIGGERS (flag these):
- Losses exceed 3x industry average
- Operations outside standard appetite
- Coverage limits exceed authority
- Unique or unusual exposures
- Prior declinations by other carriers
- Financial distress indicators

OUTPUT REQUIREMENTS:
- Comprehensive risk factor analysis
- Quantified risk scoring where possible
- Loss history analysis with trends
- Pricing recommendations
- Conditions for acceptance
- Clear recommendation with rationale

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{line_of_business}}` | string | Yes | Type of coverage being underwritten |
| `{{application_data}}` | string | Yes | Application details and submissions |
| `{{loss_history}}` | string | No | Prior claims and loss runs |
| `{{inspection_data}}` | string | No | Physical inspection reports |
| `{{financial_data}}` | string | No | Financial information |
| `{{industry_data}}` | string | No | Industry benchmarks |
| `{{underwriting_guidelines}}` | string | No | Carrier-specific guidelines |

## Examples

### Example 1: Commercial Property - Standard Risk

**Input:**
```
line_of_business: commercial_property
application_data: |
  APPLICANT: Main Street Bakery LLC
  LOCATION: 100 Main Street, Portland, OR 97201

  BUILDING:
  - Construction: Masonry non-combustible
  - Year built: 1985
  - Floors: 2 (ground floor retail, 2nd floor office/storage)
  - Square footage: 4,500 sq ft
  - Roof: Flat membrane, replaced 2019
  - Sprinklered: Yes (NFPA 13)
  - Alarm: Fire alarm, central station monitored

  OCCUPANCY:
  - Retail bakery (80%)
  - Office/storage (20%)
  - Commercial ovens, standard bakery equipment
  - Operating hours: 5 AM - 7 PM, 7 days

  COVERAGE REQUESTED:
  - Building: $850,000
  - Business Personal Property: $175,000
  - Business Income: $150,000 (ALS 12 months)

  PROTECTION:
  - Fire District: Portland Fire & Rescue
  - Protection Class: 3
  - Distance to fire station: 1.2 miles
  - Hydrant: 250 feet

loss_history: |
  5-YEAR LOSS HISTORY:
  2023: No losses
  2022: Water damage (pipe leak) - $4,500 paid
  2021: No losses
  2020: No losses
  2019: No losses

  Total losses: $4,500
  Loss-free years: 4 of 5

inspection_data: |
  INSPECTION DATE: December 15, 2023
  INSPECTOR: ABC Inspection Services

  FINDINGS:
  - Building in good condition for age
  - Electrical upgraded 2015, meets code
  - Sprinkler system inspected and certified
  - Fire extinguishers current
  - Hoods over ovens with automatic suppression
  - No housekeeping concerns noted
  - Roof in good condition (replaced 2019)

  RECOMMENDATIONS:
  - None
```

**Output:**
```json
{
  "assessment_summary": {
    "risk_id": "UW-2024-00456",
    "assessment_date": "2024-01-15",
    "line_of_business": "commercial_property",
    "overall_risk_grade": "A",
    "recommendation": "accept",
    "confidence": 0.92
  },
  "risk_factors": [
    {
      "factor": "Building construction",
      "current_value": "Masonry non-combustible",
      "impact": "positive",
      "severity": "high",
      "weight": 15,
      "notes": "Superior fire resistance"
    },
    {
      "factor": "Protection class",
      "current_value": "Class 3",
      "impact": "positive",
      "severity": "medium",
      "weight": 10,
      "notes": "Well-protected area with good fire response"
    },
    {
      "factor": "Sprinkler system",
      "current_value": "NFPA 13 compliant",
      "impact": "positive",
      "severity": "high",
      "weight": 15,
      "notes": "Full sprinkler coverage significantly reduces fire loss severity"
    },
    {
      "factor": "Roof age/condition",
      "current_value": "5 years old, good condition",
      "impact": "positive",
      "severity": "medium",
      "weight": 8,
      "notes": "Recent replacement (2019) with documented good condition"
    },
    {
      "factor": "Occupancy hazard",
      "current_value": "Retail bakery",
      "impact": "neutral",
      "severity": "low",
      "weight": 5,
      "notes": "Moderate hazard from commercial cooking, mitigated by hood suppression"
    },
    {
      "factor": "Building age",
      "current_value": "39 years (1985)",
      "impact": "slightly_negative",
      "severity": "low",
      "weight": 5,
      "notes": "Older building but electrical updated 2015"
    },
    {
      "factor": "Alarm system",
      "current_value": "Central station monitored",
      "impact": "positive",
      "severity": "medium",
      "weight": 8,
      "notes": "24/7 monitoring reduces response time"
    }
  ],
  "positive_factors": [
    "Masonry non-combustible construction",
    "Full NFPA 13 sprinkler system",
    "Protection Class 3",
    "Central station monitored fire alarm",
    "Recent roof replacement (2019)",
    "Clean 5-year loss history (1 minor water claim)",
    "Hood suppression over commercial cooking equipment",
    "Recent electrical upgrade (2015)",
    "Clean inspection with no recommendations"
  ],
  "negative_factors": [
    "Building age (39 years) - minor concern only, well-maintained",
    "Commercial cooking hazard - adequately controlled with suppression"
  ],
  "risk_scoring": {
    "property_score": 88,
    "protection_score": 90,
    "occupancy_score": 78,
    "management_score": 85,
    "overall_score": 85
  },
  "loss_analysis": {
    "frequency": "below_average",
    "severity": "below_average",
    "trend": "stable",
    "loss_ratio": 2.1,
    "five_year_total": 4500,
    "five_year_incurred": 4500,
    "annual_average": 900,
    "expected_losses": 3500,
    "notes": "Single minor water claim in 5 years. Excellent loss experience."
  },
  "pricing_considerations": {
    "base_rate_adequacy": "adequate",
    "suggested_modifications": [
      {
        "factor": "schedule_credit",
        "value": -10,
        "rationale": "Superior fire protection (sprinkler + masonry + Protection Class 3)"
      },
      {
        "factor": "loss_free_credit",
        "value": -5,
        "rationale": "4 of 5 years loss-free, only minor water claim"
      }
    ],
    "total_credit": -15,
    "estimated_premium": {
      "building": 4250,
      "bpp": 700,
      "business_income": 1200,
      "total": 6150
    },
    "minimum_premium": 5000,
    "notes": "Premium reflects scheduled credits for protection and loss experience"
  },
  "conditions": [],
  "recommendations": [
    {
      "priority": "low",
      "recommendation": "Verify sprinkler system inspection is current (annual requirement)",
      "type": "documentation",
      "rationale": "Standard documentation for sprinklered risks"
    },
    {
      "priority": "low",
      "recommendation": "Consider Equipment Breakdown coverage",
      "type": "coverage_enhancement",
      "rationale": "Commercial ovens and bakery equipment represent meaningful exposure"
    }
  ],
  "referral_triggers": [],
  "underwriting_notes": [
    "Straightforward bakery risk with excellent protection features",
    "Loss history demonstrates effective risk management",
    "Inspection confirms good maintenance and housekeeping",
    "Within standard appetite for retail food operations"
  ]
}
```

### Example 2: General Liability - Contractor with Concerns

**Input:**
```
line_of_business: general_liability
application_data: |
  APPLICANT: Premier Roofing Contractors Inc.
  YEARS IN BUSINESS: 8 years
  EMPLOYEES: 22 (including 15 field workers)
  ANNUAL REVENUE: $3.2 million

  OPERATIONS:
  - Residential roofing (60%)
  - Commercial roofing (40%)
  - New construction and re-roofing
  - Some metal roofing work
  - Uses subcontractors (about 20% of work)

  TERRITORY: Oregon and Washington

  COVERAGE REQUESTED:
  - Each Occurrence: $1,000,000
  - General Aggregate: $2,000,000
  - Products/Completed Ops: $2,000,000

  SAFETY PROGRAM:
  - Written safety manual: Yes
  - Regular toolbox talks: Yes
  - Fall protection training: Annual
  - OSHA citations: None in 3 years

  SUBCONTRACTORS:
  - Require certificates of insurance
  - Written subcontractor agreements
  - COI limit requirements: $1M GL, $500K Auto

loss_history: |
  5-YEAR LOSS HISTORY:
  2023: Completed operations claim - roof leak - $45,000 (reserved $60,000)
  2022: Premises liability - visitor fell at office - $8,500 (closed)
  2021: No losses
  2020: Products claim - defective shingles - $22,000 (closed, subrogated $15,000)
  2019: Workers fell through plywood, injured homeowner - $125,000 (closed)

  Total incurred: $215,500
  Net after subrogation: $200,500
  Claims count: 4

financial_data: |
  FINANCIALS (2023):
  - Revenue: $3.2M (up from $2.8M in 2022)
  - Net profit margin: 8%
  - Current ratio: 1.4
  - No bankruptcy history
  - Good credit (Dun & Bradstreet rating: 2A)
```

**Output:**
```json
{
  "assessment_summary": {
    "risk_id": "UW-2024-00789",
    "assessment_date": "2024-01-15",
    "line_of_business": "general_liability",
    "overall_risk_grade": "B-",
    "recommendation": "accept_with_conditions",
    "confidence": 0.78
  },
  "risk_factors": [
    {
      "factor": "Classification hazard",
      "current_value": "Roofing contractors",
      "impact": "negative",
      "severity": "high",
      "weight": 20,
      "notes": "Roofing is inherently high-hazard classification. Heights exposure, completed operations exposure."
    },
    {
      "factor": "Claims frequency",
      "current_value": "4 claims in 5 years",
      "impact": "negative",
      "severity": "medium",
      "weight": 15,
      "notes": "Higher than preferred for this class. 2023 claim still open."
    },
    {
      "factor": "Claim severity",
      "current_value": "Average $50K+ per claim",
      "impact": "negative",
      "severity": "medium",
      "weight": 12,
      "notes": "2019 claim of $125K indicates severity potential"
    },
    {
      "factor": "Safety program",
      "current_value": "Formal program in place",
      "impact": "positive",
      "severity": "medium",
      "weight": 10,
      "notes": "Written manual, fall protection training, no OSHA citations"
    },
    {
      "factor": "Experience",
      "current_value": "8 years in business",
      "impact": "positive",
      "severity": "medium",
      "weight": 8,
      "notes": "Established contractor with track record"
    },
    {
      "factor": "Subcontractor controls",
      "current_value": "COI requirements, written agreements",
      "impact": "positive",
      "severity": "medium",
      "weight": 8,
      "notes": "Proper subcontractor management reduces transferred liability"
    },
    {
      "factor": "Financial stability",
      "current_value": "Growing, profitable",
      "impact": "positive",
      "severity": "low",
      "weight": 5,
      "notes": "Revenue growth, positive margins, good credit"
    },
    {
      "factor": "Completed operations exposure",
      "current_value": "High - roofing warranty exposure",
      "impact": "negative",
      "severity": "high",
      "weight": 15,
      "notes": "Roofing completed ops claims often emerge 2-5 years post-installation"
    }
  ],
  "positive_factors": [
    "8 years in business with established operations",
    "Formal safety program with documented training",
    "No OSHA citations in 3 years",
    "Proper subcontractor insurance requirements",
    "Financial stability and growth",
    "Successful subrogation on 2020 defective products claim",
    "D&B 2A rating indicates financial responsibility"
  ],
  "negative_factors": [
    "High-hazard roofing classification",
    "4 claims in 5 years (above average frequency)",
    "2019 claim of $125,000 shows severity potential",
    "Open 2023 claim with $60,000 reserve",
    "Completed operations exposure on all installed roofs",
    "Mixed residential/commercial increases exposure complexity"
  ],
  "risk_scoring": {
    "operations_hazard_score": 45,
    "loss_history_score": 55,
    "management_score": 78,
    "financial_score": 82,
    "overall_score": 62
  },
  "loss_analysis": {
    "frequency": "above_average",
    "severity": "average",
    "trend": "concerning",
    "loss_ratio": 62,
    "five_year_total": 215500,
    "net_after_recovery": 200500,
    "annual_average": 40100,
    "expected_losses": 45000,
    "notes": "Frequency is primary concern. 2023 open claim adds uncertainty. 2019 large claim ($125K) indicates severity potential."
  },
  "pricing_considerations": {
    "base_rate_adequacy": "needs_loading",
    "suggested_modifications": [
      {
        "factor": "experience_debit",
        "value": 15,
        "rationale": "Loss frequency above class average"
      },
      {
        "factor": "safety_credit",
        "value": -5,
        "rationale": "Formal safety program with documented training"
      },
      {
        "factor": "subcontractor_credit",
        "value": -3,
        "rationale": "Proper COI and agreement requirements"
      }
    ],
    "total_modification": 7,
    "estimated_premium": {
      "base_premium": 32000,
      "modified_premium": 34240,
      "products_completed_ops": 12000
    },
    "minimum_premium": 35000,
    "target_premium": 48000,
    "notes": "Premium reflects experience debit partially offset by safety credits. Completed operations pricing reflects roofing exposure."
  },
  "conditions": [
    {
      "condition": "Deductible of $5,000 per occurrence",
      "type": "policy_term",
      "mandatory": true,
      "rationale": "Loss frequency warrants risk-sharing"
    },
    {
      "condition": "Completed operations aggregate sublimit of $1,000,000",
      "type": "coverage_restriction",
      "mandatory": true,
      "rationale": "Limit completed ops exposure given claim history"
    },
    {
      "condition": "Provide current subcontractor COI summary",
      "type": "documentation",
      "mandatory": true,
      "rationale": "Verify subcontractor insurance requirements are enforced"
    },
    {
      "condition": "Annual safety program documentation required at renewal",
      "type": "ongoing",
      "mandatory": true,
      "rationale": "Continued monitoring of safety practices"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Evaluate 2019 bodily injury claim details",
      "type": "further_review",
      "rationale": "Worker fell through plywood injuring homeowner suggests worksite control issues"
    },
    {
      "priority": "high",
      "recommendation": "Monitor 2023 open claim development",
      "type": "follow_up",
      "rationale": "$60K reserve may develop; completed ops claims can escalate"
    },
    {
      "priority": "medium",
      "recommendation": "Consider requiring Additional Insured status on subcontractor policies",
      "type": "risk_improvement",
      "rationale": "Strengthen protection from subcontractor operations"
    }
  ],
  "referral_triggers": [
    "Loss ratio of 62% warrants senior underwriter review for approval"
  ],
  "underwriting_notes": [
    "Roofing contractor with concerning loss frequency but manageable with conditions",
    "Safety program and subcontractor controls are positives",
    "2019 claim suggests worksite safety improvements may be needed",
    "Accept with deductible, completed ops sublimit, and ongoing monitoring",
    "Pricing must reflect experience debit to maintain adequate premium"
  ]
}
```

## Gotchas

### Common Failure Modes
1. **Over-reliance on loss history**: Recent years may not predict future. Consider exposures.
2. **Missing emerging risks**: Cyber, PFAS, climate exposures may not appear in traditional analysis.
3. **Industry classification errors**: Similar-sounding businesses may have very different risks.
4. **Ignoring policy terms**: Prior coverage may have had exclusions affecting loss history.

### Edge Cases to Handle
- **New ventures**: No loss history - rely on management experience and industry data
- **M&A situations**: Combined entities may have hidden exposures
- **Emerging industries**: Standard classification may not exist
- **Multi-state operations**: Different requirements and exposures

### When NOT to Use This Prompt
- **Specialty lines**: Specific prompts needed for D&O, cyber, environmental
- **Reinsurance**: Different considerations and metrics
- **Personal lines**: Consumer underwriting has different factors
- **Regulatory filings**: Rate and form filings need specific formats

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex commercial risks | Best nuanced analysis |
| **Best:** GPT-4o | Large submissions | Strong at maintaining context |
| **Acceptable:** Claude Sonnet 4 | Standard underwriting | Good balance |
| **Not Recommended:** Smaller models | - | Miss critical risk factors |

## Integration Notes

### Workflow Integration
```python
def process_submission(application):
    # Step 1: Gather data
    submission_data = compile_submission_data(application)

    # Step 2: Run assessment
    assessment = run_underwriting_assessment(submission_data)

    # Step 3: Check referral triggers
    if assessment['referral_triggers']:
        return route_to_senior_underwriter(assessment)

    # Step 4: Apply authority limits
    if exceeds_authority(assessment, current_user):
        return route_for_approval(assessment)

    # Step 5: Generate quote
    if assessment['recommendation'] in ['accept', 'accept_with_conditions']:
        quote = generate_quote(assessment)
        return present_quote(quote, assessment['conditions'])

    return present_declination(assessment)
```

### Decision Documentation
```python
def document_decision(assessment, decision):
    """Create audit trail for underwriting decision"""
    return {
        "submission_id": assessment['assessment_summary']['risk_id'],
        "assessment_date": assessment['assessment_summary']['assessment_date'],
        "risk_grade": assessment['assessment_summary']['overall_risk_grade'],
        "ai_recommendation": assessment['assessment_summary']['recommendation'],
        "human_decision": decision['action'],
        "human_override": decision['action'] != assessment['assessment_summary']['recommendation'],
        "override_rationale": decision.get('rationale', None),
        "conditions_applied": decision.get('conditions', []),
        "pricing": decision.get('pricing', {}),
        "underwriter": decision['underwriter_id'],
        "timestamp": datetime.now().isoformat()
    }
```
