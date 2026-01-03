# Policy Comparison Analysis

## Use Case

Compare insurance policies to identify differences, coverage gaps, and recommendations:
- Renewal comparison (current vs proposed)
- Competitive analysis (carrier A vs carrier B)
- Coverage adequacy review
- Endorsement comparison
- Premium vs coverage trade-offs

Use when helping underwriters, agents, or customers understand policy differences.

## Input Format

**Required:**
- `policy_a`: First policy details (text, JSON, or structured description)
- `policy_b`: Second policy details (same format as policy_a)

**Optional:**
- `comparison_purpose`: renewal, competitive, coverage_review, cost_analysis
- `focus_areas`: Specific coverage areas to emphasize
- `risk_profile`: Client risk characteristics for context
- `budget_constraints`: Maximum premium or cost considerations

## Output Format

```json
{
  "comparison_summary": {
    "policy_a_name": "Current Policy - Carrier A",
    "policy_b_name": "Proposed Policy - Carrier B",
    "comparison_date": "2024-01-15",
    "overall_recommendation": "policy_b",
    "recommendation_confidence": 0.85,
    "recommendation_rationale": "Better coverage at comparable premium"
  },
  "coverage_comparison": [
    {
      "coverage_area": "Liability",
      "policy_a": {
        "limit": "$1,000,000",
        "deductible": "$1,000",
        "key_terms": ["occurrence form"]
      },
      "policy_b": {
        "limit": "$2,000,000",
        "deductible": "$1,000",
        "key_terms": ["claims-made form"]
      },
      "advantage": "policy_b",
      "significance": "high",
      "notes": "Higher limit but different trigger - claims-made vs occurrence"
    }
  ],
  "gaps_identified": [
    {
      "gap": "Cyber liability not included",
      "affected_policy": "both",
      "risk_level": "medium",
      "recommendation": "Add cyber endorsement"
    }
  ],
  "premium_analysis": {
    "policy_a_premium": 5000,
    "policy_b_premium": 5200,
    "difference": 200,
    "difference_percent": 4.0,
    "value_assessment": "policy_b offers better value despite higher premium"
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Switch to Policy B for higher liability limits",
      "trade_off": "4% premium increase",
      "rationale": "Risk exposure justifies additional cost"
    }
  ],
  "detailed_differences": [...],
  "equivalent_coverages": [...]
}
```

## The Prompt

```
You are an insurance policy analysis expert. Compare the two policies and provide detailed analysis for decision-making.

COMPARISON PURPOSE: {{comparison_purpose | default: "general"}}

POLICY A:
{{policy_a}}

POLICY B:
{{policy_b}}

{{#if focus_areas}}
FOCUS AREAS:
{{focus_areas}}
{{/if}}

{{#if risk_profile}}
RISK PROFILE:
{{risk_profile}}
{{/if}}

{{#if budget_constraints}}
BUDGET CONSTRAINTS:
{{budget_constraints}}
{{/if}}

COMPARISON FRAMEWORK:

1. COVERAGE AREAS TO COMPARE
   For each coverage type found in either policy:
   - Limits (per occurrence, aggregate, sub-limits)
   - Deductibles (per claim, annual aggregate)
   - Coverage triggers (occurrence vs claims-made)
   - Exclusions
   - Conditions and warranties
   - Territory
   - Named insureds

2. STANDARD COVERAGE AREAS BY POLICY TYPE:

   Commercial General Liability:
   - Bodily injury/property damage
   - Personal/advertising injury
   - Products/completed operations
   - Medical payments
   - Damage to rented premises

   Property:
   - Building coverage
   - Business personal property
   - Business income/extra expense
   - Equipment breakdown
   - Flood/earthquake (usually separate)

   Auto:
   - Liability (BI/PD)
   - Collision
   - Comprehensive
   - Uninsured/underinsured motorist
   - Medical payments

   Workers Compensation:
   - Part A (statutory)
   - Part B (employers liability)
   - Coverage extensions

3. SIGNIFICANCE RATING
   - high: Materially affects coverage in likely scenarios
   - medium: Affects coverage in possible scenarios
   - low: Technical difference, unlikely to matter

4. ADVANTAGE DETERMINATION
   - policy_a: Policy A clearly better
   - policy_b: Policy B clearly better
   - equivalent: No meaningful difference
   - depends: Situation-dependent (explain)

5. GAP ANALYSIS
   Identify coverages that:
   - Missing from both policies
   - Significantly reduced from typical coverage
   - Have unusual exclusions

6. PREMIUM VALUE ANALYSIS
   - Premium difference absolute and percentage
   - Cost per unit of coverage difference
   - Value assessment considering coverage differences

7. FORM DIFFERENCES
   Note differences in:
   - ISO forms vs manuscript
   - Edition dates
   - Endorsement packages

ANALYSIS GUIDELINES:
- Be specific about dollar amounts and percentages
- Note when terms have different definitions
- Highlight hidden differences (sub-limits, sublimits)
- Consider claims-made retroactive dates if applicable
- Flag any unusual conditions or warranties
- Consider practical impact, not just technical differences

OUTPUT REQUIREMENTS:
- Overall recommendation with confidence level
- Side-by-side comparison of all coverage areas
- Gaps and exposures identified
- Premium analysis with value assessment
- Prioritized recommendations

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{policy_a}}` | string | Yes | First policy details |
| `{{policy_b}}` | string | Yes | Second policy details |
| `{{comparison_purpose}}` | string | No | Context for comparison |
| `{{focus_areas}}` | array | No | Specific areas to emphasize |
| `{{risk_profile}}` | string | No | Client risk characteristics |
| `{{budget_constraints}}` | string | No | Cost limitations |

## Examples

### Example 1: Renewal Comparison

**Input:**
```
comparison_purpose: renewal
policy_a: |
  CURRENT POLICY - ABC Insurance
  Policy Period: Jan 1, 2024 - Jan 1, 2025
  Annual Premium: $12,500

  General Liability:
  - Each Occurrence: $1,000,000
  - General Aggregate: $2,000,000
  - Products-Completed Ops: $2,000,000
  - Personal/Advertising Injury: $1,000,000
  - Damage to Rented Premises: $100,000
  - Medical Payments: $5,000
  - Deductible: $0

  Property:
  - Building: $500,000
  - Business Personal Property: $150,000
  - Business Income: $100,000 (ALS 12 months)
  - Deductible: $1,000
  - Coinsurance: 80%

  Auto:
  - Liability: $1,000,000 CSL
  - Collision: Actual Cash Value, $500 deductible
  - Comprehensive: ACV, $250 deductible
  - UM/UIM: $1,000,000

  Endorsements: None

policy_b: |
  RENEWAL QUOTE - ABC Insurance
  Policy Period: Jan 1, 2025 - Jan 1, 2026
  Annual Premium: $14,200

  General Liability:
  - Each Occurrence: $1,000,000
  - General Aggregate: $2,000,000
  - Products-Completed Ops: $2,000,000
  - Personal/Advertising Injury: $1,000,000
  - Damage to Rented Premises: $100,000
  - Medical Payments: $5,000
  - Deductible: $1,000 (NEW)

  Property:
  - Building: $550,000 (increased)
  - Business Personal Property: $175,000 (increased)
  - Business Income: $125,000 (ALS 12 months)
  - Deductible: $2,500 (increased)
  - Coinsurance: 80%
  - Equipment Breakdown: Included (NEW)

  Auto:
  - Liability: $1,000,000 CSL
  - Collision: Actual Cash Value, $1,000 deductible (increased)
  - Comprehensive: ACV, $500 deductible (increased)
  - UM/UIM: $1,000,000
  - Hired/Non-Owned Auto: Included (NEW)

  Endorsements: Employment Practices Liability $100,000 (NEW)

risk_profile: |
  Manufacturing company
  15 employees
  $3M annual revenue
  5 company vehicles
```

**Output:**
```json
{
  "comparison_summary": {
    "policy_a_name": "Current Policy - ABC Insurance (2024)",
    "policy_b_name": "Renewal Quote - ABC Insurance (2025)",
    "comparison_date": "2024-01-15",
    "overall_recommendation": "policy_b",
    "recommendation_confidence": 0.78,
    "recommendation_rationale": "Despite 13.6% premium increase, renewal adds valuable coverage (EPLI, Equipment Breakdown, Hired/Non-Owned Auto) that addresses gaps. Deductible increases are reasonable trade-off for new coverage."
  },
  "coverage_comparison": [
    {
      "coverage_area": "General Liability - Limits",
      "policy_a": {
        "limit": "$1,000,000 occurrence / $2,000,000 aggregate",
        "deductible": "$0",
        "key_terms": []
      },
      "policy_b": {
        "limit": "$1,000,000 occurrence / $2,000,000 aggregate",
        "deductible": "$1,000",
        "key_terms": []
      },
      "advantage": "policy_a",
      "significance": "medium",
      "notes": "Same limits but renewal adds $1,000 deductible. Annual exposure: $1,000-5,000 depending on claim frequency."
    },
    {
      "coverage_area": "Property - Building",
      "policy_a": {
        "limit": "$500,000",
        "deductible": "$1,000",
        "key_terms": ["80% coinsurance"]
      },
      "policy_b": {
        "limit": "$550,000",
        "deductible": "$2,500",
        "key_terms": ["80% coinsurance"]
      },
      "advantage": "depends",
      "significance": "medium",
      "notes": "10% limit increase ($50,000) offset by 150% deductible increase ($1,500). Better for large losses, worse for small claims."
    },
    {
      "coverage_area": "Property - Business Personal Property",
      "policy_a": {
        "limit": "$150,000",
        "deductible": "$1,000",
        "key_terms": []
      },
      "policy_b": {
        "limit": "$175,000",
        "deductible": "$2,500",
        "key_terms": []
      },
      "advantage": "depends",
      "significance": "low",
      "notes": "17% limit increase with higher deductible. Evaluate current BPP value."
    },
    {
      "coverage_area": "Equipment Breakdown",
      "policy_a": {
        "limit": "Not covered",
        "deductible": "N/A",
        "key_terms": []
      },
      "policy_b": {
        "limit": "Included",
        "deductible": "Same as property",
        "key_terms": []
      },
      "advantage": "policy_b",
      "significance": "high",
      "notes": "NEW COVERAGE: Critical for manufacturing operations. Covers mechanical/electrical breakdown excluded from standard property forms."
    },
    {
      "coverage_area": "Auto - Physical Damage",
      "policy_a": {
        "limit": "ACV",
        "deductible": "$500 collision / $250 comprehensive",
        "key_terms": []
      },
      "policy_b": {
        "limit": "ACV",
        "deductible": "$1,000 collision / $500 comprehensive",
        "key_terms": []
      },
      "advantage": "policy_a",
      "significance": "low",
      "notes": "Deductibles doubled. With 5 vehicles, exposure is ~$2,500/claim increase. Minor for fleet operations."
    },
    {
      "coverage_area": "Hired/Non-Owned Auto",
      "policy_a": {
        "limit": "Not covered",
        "deductible": "N/A",
        "key_terms": []
      },
      "policy_b": {
        "limit": "Included",
        "deductible": "Same as auto",
        "key_terms": []
      },
      "advantage": "policy_b",
      "significance": "high",
      "notes": "NEW COVERAGE: Critical if employees ever use personal vehicles for business or company rents vehicles. Significant liability gap addressed."
    },
    {
      "coverage_area": "Employment Practices Liability (EPLI)",
      "policy_a": {
        "limit": "Not covered",
        "deductible": "N/A",
        "key_terms": []
      },
      "policy_b": {
        "limit": "$100,000",
        "deductible": "TBD",
        "key_terms": []
      },
      "advantage": "policy_b",
      "significance": "high",
      "notes": "NEW COVERAGE: With 15 employees, EPLI is essential. Covers wrongful termination, discrimination, harassment claims. $100,000 is minimum; consider increasing."
    }
  ],
  "gaps_identified": [
    {
      "gap": "Cyber Liability not included",
      "affected_policy": "both",
      "risk_level": "medium",
      "recommendation": "Add standalone cyber policy. Manufacturing increasingly targeted; protects against ransomware, data breach, business interruption."
    },
    {
      "gap": "EPLI limit may be insufficient",
      "affected_policy": "policy_b",
      "risk_level": "medium",
      "recommendation": "$100,000 is entry-level. EPLI claims average $75,000; one significant claim exhausts limit. Consider $250,000-500,000."
    },
    {
      "gap": "Umbrella/Excess not mentioned",
      "affected_policy": "both",
      "risk_level": "high",
      "recommendation": "$3M revenue manufacturing should carry $2-5M umbrella over primary GL and Auto."
    }
  ],
  "premium_analysis": {
    "policy_a_premium": 12500,
    "policy_b_premium": 14200,
    "difference": 1700,
    "difference_percent": 13.6,
    "value_assessment": "Premium increase justified by new coverages. Equipment Breakdown alone would cost $500-1,000 standalone. EPLI adds $400-800 value. Hired/Non-Owned Auto adds $200-300 value. Net new coverage value: $1,100-2,100 vs $1,700 increase. Reasonable given market conditions.",
    "deductible_impact": {
      "annual_additional_exposure": "$2,500 - $5,000 (if claims match prior history)",
      "notes": "Higher deductibles reduce premium but increase out-of-pocket per claim"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Accept renewal with EPLI limit increase request",
      "trade_off": "$14,200 premium + potential EPLI increase (~$200-400)",
      "rationale": "New coverages address significant gaps. Equipment Breakdown and EPLI are critical for manufacturing operations."
    },
    {
      "priority": "high",
      "recommendation": "Add umbrella/excess liability policy",
      "trade_off": "Additional $1,500-3,000 premium for $2M umbrella",
      "rationale": "$1M underlying limits insufficient for manufacturing exposures. Single serious injury claim can exceed limits."
    },
    {
      "priority": "medium",
      "recommendation": "Evaluate cyber liability coverage",
      "trade_off": "$1,000-2,500 for $1M cyber policy",
      "rationale": "Manufacturing increasingly targeted. Protects against operational disruption from ransomware."
    },
    {
      "priority": "low",
      "recommendation": "Consider negotiating GL deductible reduction",
      "trade_off": "May add $200-400 to premium",
      "rationale": "$1,000 per claim adds up. Prior $0 deductible was better for cash flow."
    }
  ],
  "detailed_differences": [
    {
      "category": "New Coverages in Renewal",
      "items": [
        "Equipment Breakdown (high value)",
        "Hired/Non-Owned Auto (high value)",
        "Employment Practices Liability $100K (high value)"
      ]
    },
    {
      "category": "Increased Limits in Renewal",
      "items": [
        "Building: $500K → $550K (+10%)",
        "BPP: $150K → $175K (+17%)",
        "Business Income: $100K → $125K (+25%)"
      ]
    },
    {
      "category": "Increased Deductibles in Renewal",
      "items": [
        "GL: $0 → $1,000",
        "Property: $1,000 → $2,500",
        "Auto Collision: $500 → $1,000",
        "Auto Comprehensive: $250 → $500"
      ]
    }
  ],
  "equivalent_coverages": [
    {
      "coverage": "General Liability limits",
      "notes": "Both $1M/$2M - no change"
    },
    {
      "coverage": "Auto Liability",
      "notes": "Both $1M CSL - no change"
    },
    {
      "coverage": "UM/UIM",
      "notes": "Both $1M - no change"
    }
  ]
}
```

### Example 2: Competitive Quote Analysis

**Input:**
```
comparison_purpose: competitive
policy_a: |
  CURRENT - State Insurance Co
  Premium: $8,200/year

  BOP Policy:
  - GL: $1M/$2M
  - Property: $300,000
  - Deductible: $1,000
  - Business Income: Actual Loss 12 months
  - Equipment Breakdown: Included
  - Employee Dishonesty: $25,000

policy_b: |
  QUOTE - National Mutual
  Premium: $7,100/year

  BOP Policy:
  - GL: $1M/$2M
  - Property: $300,000
  - Deductible: $1,000
  - Business Income: $50,000 limit
  - Equipment Breakdown: NOT included
  - Employee Dishonesty: $10,000

focus_areas: ["business income coverage", "total cost of risk"]
```

**Output:**
```json
{
  "comparison_summary": {
    "policy_a_name": "Current - State Insurance Co",
    "policy_b_name": "Quote - National Mutual",
    "comparison_date": "2024-01-15",
    "overall_recommendation": "policy_a",
    "recommendation_confidence": 0.82,
    "recommendation_rationale": "Despite $1,100 higher premium, current policy provides substantially better coverage. Business Income and Equipment Breakdown differences create significant exposure gaps in the cheaper quote."
  },
  "coverage_comparison": [
    {
      "coverage_area": "Business Income",
      "policy_a": {
        "limit": "Actual Loss Sustained (12 months)",
        "deductible": "Included in property deductible",
        "key_terms": ["ALS provision - pays actual loss up to 12 months"]
      },
      "policy_b": {
        "limit": "$50,000",
        "deductible": "Included in property deductible",
        "key_terms": ["Fixed limit - may be insufficient"]
      },
      "advantage": "policy_a",
      "significance": "high",
      "notes": "CRITICAL DIFFERENCE: ALS coverage pays actual business income loss for 12 months. $50,000 limit could be exhausted in 1-2 months for most businesses. A 6-month interruption could cost $150,000+."
    },
    {
      "coverage_area": "Equipment Breakdown",
      "policy_a": {
        "limit": "Included",
        "deductible": "Likely shared with property",
        "key_terms": []
      },
      "policy_b": {
        "limit": "NOT INCLUDED",
        "deductible": "N/A",
        "key_terms": []
      },
      "advantage": "policy_a",
      "significance": "high",
      "notes": "Mechanical/electrical breakdown excluded from standard property forms. Without this, HVAC failure, electrical surge damage, etc. not covered. Standalone policy costs $500-1,500."
    },
    {
      "coverage_area": "Employee Dishonesty",
      "policy_a": {
        "limit": "$25,000",
        "deductible": "TBD",
        "key_terms": []
      },
      "policy_b": {
        "limit": "$10,000",
        "deductible": "TBD",
        "key_terms": []
      },
      "advantage": "policy_a",
      "significance": "medium",
      "notes": "60% lower limit in quote. $10,000 may be insufficient for meaningful theft by trusted employee."
    }
  ],
  "gaps_identified": [
    {
      "gap": "Business income severely limited in Policy B",
      "affected_policy": "policy_b",
      "risk_level": "high",
      "recommendation": "If switching to Policy B, MUST add Business Income endorsement to increase limit to ALS or minimum $200,000"
    },
    {
      "gap": "Equipment Breakdown missing from Policy B",
      "affected_policy": "policy_b",
      "risk_level": "high",
      "recommendation": "Would need to add Equipment Breakdown endorsement (~$500-800) or standalone policy"
    }
  ],
  "premium_analysis": {
    "policy_a_premium": 8200,
    "policy_b_premium": 7100,
    "difference": -1100,
    "difference_percent": -13.4,
    "value_assessment": "Policy B is NOT actually cheaper when coverage gaps addressed. Equipment Breakdown: +$500-800. Business Income upgrade: +$300-600. Adjusted Policy B cost: $7,900-8,500. Net savings: $0-300 with still-inferior coverage.",
    "true_cost_comparison": {
      "policy_a_total_cost": 8200,
      "policy_b_adjusted_cost": "7,900 - 8,500 (with essential endorsements)",
      "net_difference": "Minimal savings or slight increase for Policy B"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "recommendation": "Stay with Policy A (State Insurance Co)",
      "trade_off": "$1,100 higher premium",
      "rationale": "Apparent savings disappear when Policy B's coverage gaps are addressed. Current policy provides better protection without endorsement complexity."
    },
    {
      "priority": "medium",
      "recommendation": "If switching is required, get revised Policy B quote with Equipment Breakdown and BI increase",
      "trade_off": "Likely reduces/eliminates savings",
      "rationale": "Cannot accept Policy B as quoted - gaps are too significant for business continuity."
    }
  ],
  "equivalent_coverages": [
    {
      "coverage": "General Liability",
      "notes": "Both $1M/$2M - equivalent"
    },
    {
      "coverage": "Property",
      "notes": "Both $300,000 - equivalent"
    },
    {
      "coverage": "Deductibles",
      "notes": "Both $1,000 - equivalent"
    }
  ]
}
```

## Gotchas

### Common Failure Modes
1. **Form differences**: Same limit but different form (occurrence vs claims-made) is NOT equivalent.
2. **Sub-limit traps**: "$1M limit with $25,000 sub-limit for X" buries significant restrictions.
3. **Definition differences**: "Pollutants" defined differently can dramatically change coverage.
4. **Retroactive dates**: Claims-made policies without full prior acts coverage create gaps.

### Edge Cases to Handle
- **Bundled vs monoline**: BOP vs separate policies may have hidden differences
- **ISO vs manuscript**: Custom forms may have non-standard exclusions
- **Endorsement stacking**: Multiple endorsements may conflict
- **Aggregates shared across coverage**: May exhaust faster than expected

### When NOT to Use This Prompt
- **Complex manuscript policies**: Need human underwriter review
- **Surplus lines**: Non-admitted carriers may have unusual terms
- **Lloyd's subscriptions**: Multiple underwriters, varying terms
- **Reinsurance treaties**: Different structure entirely

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex commercial policies | Best at catching subtle differences |
| **Best:** GPT-4o | Long policy documents | Strong context maintenance |
| **Acceptable:** Claude Sonnet 4 | Standard comparisons | Good balance |
| **Not Recommended:** Smaller models | - | Miss critical coverage differences |

## Integration Notes

### Comparison Report Template
```python
def generate_comparison_report(analysis_json):
    """Generate client-facing comparison report"""
    report = f"""
# Policy Comparison Analysis

## Summary
**Recommendation:** {analysis_json['comparison_summary']['overall_recommendation']}
**Confidence:** {analysis_json['comparison_summary']['recommendation_confidence']:.0%}

{analysis_json['comparison_summary']['recommendation_rationale']}

## Premium Comparison
| Policy | Annual Premium |
|--------|----------------|
| {analysis_json['comparison_summary']['policy_a_name']} | ${analysis_json['premium_analysis']['policy_a_premium']:,} |
| {analysis_json['comparison_summary']['policy_b_name']} | ${analysis_json['premium_analysis']['policy_b_premium']:,} |
| **Difference** | ${analysis_json['premium_analysis']['difference']:,} ({analysis_json['premium_analysis']['difference_percent']}%) |

## Coverage Comparison
"""
    for coverage in analysis_json['coverage_comparison']:
        if coverage['significance'] == 'high':
            report += f"\n### {coverage['coverage_area']} ⚠️\n"
        else:
            report += f"\n### {coverage['coverage_area']}\n"
        report += f"**Advantage:** {coverage['advantage']}\n"
        report += f"**Notes:** {coverage['notes']}\n"

    return report
```
