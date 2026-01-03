# Fraud Indicator Detection

## Use Case

Analyze insurance claims and applications to identify potential fraud indicators:
- Claims fraud screening
- Application misrepresentation detection
- Staged accident indicators
- Medical billing irregularities
- Pattern recognition across multiple claims

Use as a screening layer to prioritize claims for Special Investigations Unit (SIU) review.

**Important:** This is a screening tool, not a fraud determination system. All flagged cases require human investigation.

## Input Format

**Required:**
- `claim_data`: Claim details, documents, or application information
- `claim_type`: auto, property, health, workers_comp, life, disability

**Optional:**
- `policy_data`: Policy details for cross-reference
- `claimant_history`: Prior claims by this claimant
- `external_data`: Third-party data (weather reports, police records, etc.)
- `comparison_claims`: Similar claims for pattern analysis

## Output Format

```json
{
  "screening_result": {
    "risk_score": 72,
    "risk_level": "medium-high",
    "siu_referral_recommended": true,
    "priority": "standard",
    "screening_timestamp": "2024-01-15T10:30:00Z"
  },
  "indicators_found": [
    {
      "indicator_type": "timing_suspicious",
      "indicator_name": "Claim filed shortly after policy inception",
      "severity": "medium",
      "confidence": 0.85,
      "evidence": "Policy effective 12/01/2024, loss date 12/15/2024, claim filed 12/16/2024",
      "weight": 15
    }
  ],
  "patterns_detected": [
    {
      "pattern_name": "Soft fraud indicators",
      "description": "Multiple minor indicators suggest possible exaggeration",
      "related_indicators": ["indicator_1", "indicator_2"]
    }
  ],
  "red_flags": ["Critical issues requiring immediate attention"],
  "yellow_flags": ["Issues requiring investigation"],
  "mitigating_factors": ["Factors that reduce suspicion"],
  "recommended_actions": [
    {
      "action": "Request repair shop documentation",
      "priority": "high",
      "rationale": "Verify damage estimate authenticity"
    }
  ],
  "investigation_questions": [
    "Specific questions for adjuster or SIU to pursue"
  ],
  "disclaimer": "This screening is for prioritization only. Fraud determination requires investigation."
}
```

## The Prompt

```
You are an insurance fraud screening specialist. Analyze the claim data to identify fraud indicators and risk factors.

IMPORTANT: This is a SCREENING tool. You are identifying indicators for further investigation, NOT making fraud determinations. All flagged cases require human review.

CLAIM TYPE: {{claim_type}}

CLAIM DATA:
{{claim_data}}

{{#if policy_data}}
POLICY DATA:
{{policy_data}}
{{/if}}

{{#if claimant_history}}
CLAIMANT HISTORY:
{{claimant_history}}
{{/if}}

{{#if external_data}}
EXTERNAL DATA:
{{external_data}}
{{/if}}

{{#if comparison_claims}}
SIMILAR CLAIMS FOR PATTERN ANALYSIS:
{{comparison_claims}}
{{/if}}

FRAUD INDICATOR CATEGORIES:

1. TIMING INDICATORS
   - Claim shortly after policy inception (< 30 days)
   - Loss date close to policy cancellation/lapse
   - Delayed reporting without explanation
   - Weekend/holiday losses without witnesses
   - Loss timing matches financial distress indicators

2. DOCUMENTATION INDICATORS
   - Missing or incomplete documentation
   - Inconsistent handwriting/signatures
   - Altered documents
   - Unusual document quality (too perfect or too poor)
   - Third-party documents from unfamiliar sources

3. CLAIMANT BEHAVIOR INDICATORS
   - Excessive knowledge of claims process
   - Resistance to recorded statements
   - Unable to provide basic details
   - Changing story/inconsistencies
   - Pressuring for quick settlement
   - Cash payment preference
   - Refusing inspection/examination

4. CLAIM CHARACTERISTICS
   - Amount just below investigation threshold
   - Round number estimates
   - Expensive items with no proof of ownership
   - Recent purchase of coverage increase
   - Maximum coverage claimed
   - Previous similar claims
   - Claims on multiple policies

5. PROVIDER/VENDOR INDICATORS
   - Unfamiliar repair shops/contractors
   - Inflated estimates
   - Billing irregularities
   - Prior association between claimant and provider
   - Out-of-area providers

6. BY CLAIM TYPE:

AUTO:
- Phantom vehicles (no registration found)
- Conflicting damage patterns
- Prior damage claimed as new
- Low-impact with high injury claims
- Rented/borrowed vehicle claims
- Frequent lane-change/rear-end "accidents"

PROPERTY:
- Inventory lists too detailed (suggests pre-planning)
- No photos of items before loss
- Recent appraisals/riders on stolen items
- Arson indicators (accelerants, financial motive)
- Claim exceeds property value
- Multiple losses at same location

HEALTH/MEDICAL:
- Unnecessary procedures
- Upcoding
- Unbundling services
- Phantom patients
- Unusual treatment patterns
- Out-of-network specialists for routine care

WORKERS COMP:
- No witnesses to injury
- Monday morning claims
- Injury near termination/layoff
- Prior similar claims
- Delay seeking treatment
- Working elsewhere while on disability

LIFE/DISABILITY:
- Contestable period deaths
- Recent coverage increase
- Beneficiary changes before loss
- Inconsistent medical history
- Application misrepresentation

RISK SCORING:
Calculate score (0-100) based on:
- Number of indicators
- Severity of each indicator
- Confidence in each indicator
- Presence of red flags
- Mitigating factors

Score interpretation:
- 0-30: Low risk, standard processing
- 31-50: Low-medium, enhanced review
- 51-70: Medium, adjuster investigation recommended
- 71-85: Medium-high, SIU referral recommended
- 86-100: High, priority SIU referral

OUTPUT REQUIREMENTS:
- List all indicators with evidence
- Weight indicators by severity
- Identify patterns across indicators
- Note mitigating factors
- Provide specific investigation questions
- Recommend concrete next actions
- Include required disclaimer

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{claim_type}}` | string | Yes | Type of claim being analyzed |
| `{{claim_data}}` | string | Yes | Claim details and documentation |
| `{{policy_data}}` | string | No | Policy information for cross-reference |
| `{{claimant_history}}` | string | No | Prior claims history |
| `{{external_data}}` | string | No | Third-party verification data |
| `{{comparison_claims}}` | string | No | Similar claims for pattern detection |

## Examples

### Example 1: Auto Claim with Multiple Indicators

**Input:**
```
claim_type: auto
claim_data: |
  CLAIM #: CLM-2024-98765
  Date of Loss: January 5, 2024
  Date Reported: January 6, 2024
  Loss Type: Collision
  Location: Parking lot, 123 Main St

  CLAIMANT: Michael Brown
  Vehicle: 2022 BMW 530i
  Damage: Front end collision damage
  Estimate: $18,500 from Quality Auto Body

  STATEMENT:
  "I was backing out of a parking space when another car backed into me.
  The other driver drove off before I could get their info. There were no
  witnesses. I didn't call police because it was just a fender bender."

  DOCUMENTS:
  - Repair estimate from Quality Auto Body
  - Photos of damage (taken by claimant)

policy_data: |
  Policy #: AUTO-5544332211
  Effective Date: December 15, 2023
  Premium: $2,400/year (paid in full at inception)
  Prior Policy: No prior coverage (new customer)
  Coverage: Full coverage, $500 deductible
  Added endorsement: $0 deductible glass (12/20/2023)

claimant_history: |
  Claims history (from ISO ClaimSearch):
  - 2022: Auto claim, rear-end collision, $12,000 (different policy)
  - 2021: Auto claim, parking lot damage, $8,500 (different policy)
  - 2020: Auto claim, hit and run, $15,000 (different policy)
```

**Output:**
```json
{
  "screening_result": {
    "risk_score": 78,
    "risk_level": "medium-high",
    "siu_referral_recommended": true,
    "priority": "standard",
    "screening_timestamp": "2024-01-15T10:30:00Z"
  },
  "indicators_found": [
    {
      "indicator_id": "IND-001",
      "indicator_type": "timing_suspicious",
      "indicator_name": "Claim filed within 30 days of policy inception",
      "severity": "high",
      "confidence": 1.0,
      "evidence": "Policy effective 12/15/2023, loss date 01/05/2024 = 21 days from inception",
      "weight": 20
    },
    {
      "indicator_id": "IND-002",
      "indicator_type": "claim_history",
      "indicator_name": "Pattern of similar claims",
      "severity": "high",
      "confidence": 0.95,
      "evidence": "4 auto claims in 4 years, including 2 prior parking lot/hit-and-run claims. Pattern: unwitnessed, no police, moderate-high damage.",
      "weight": 25
    },
    {
      "indicator_id": "IND-003",
      "indicator_type": "circumstances_suspicious",
      "indicator_name": "No witnesses and no police report",
      "severity": "medium",
      "confidence": 0.9,
      "evidence": "Claimant states 'no witnesses' and 'didn't call police' despite $18,500 damage",
      "weight": 15
    },
    {
      "indicator_id": "IND-004",
      "indicator_type": "circumstances_suspicious",
      "indicator_name": "Phantom vehicle (other party fled)",
      "severity": "medium",
      "confidence": 0.85,
      "evidence": "Other driver allegedly fled. No plate number, vehicle description, or witness. Common in staged claims.",
      "weight": 12
    },
    {
      "indicator_id": "IND-005",
      "indicator_type": "documentation_issue",
      "indicator_name": "Single-source repair estimate",
      "severity": "low",
      "confidence": 0.7,
      "evidence": "Only one estimate provided from 'Quality Auto Body'. Relationship between claimant and shop unknown.",
      "weight": 8
    },
    {
      "indicator_id": "IND-006",
      "indicator_type": "claim_characteristic",
      "indicator_name": "High-value luxury vehicle claim",
      "severity": "low",
      "confidence": 0.6,
      "evidence": "2022 BMW 530i with $18,500 claimed damage. Higher-value vehicles more frequently involved in fraud.",
      "weight": 5
    },
    {
      "indicator_id": "IND-007",
      "indicator_type": "timing_suspicious",
      "indicator_name": "Coverage enhancement shortly before loss",
      "severity": "medium",
      "confidence": 0.8,
      "evidence": "$0 deductible glass endorsement added 12/20/2023, 16 days before loss. Minor but contributes to pattern.",
      "weight": 8
    }
  ],
  "patterns_detected": [
    {
      "pattern_name": "Repeat claim pattern",
      "description": "Claimant has established pattern of auto claims across multiple policies over 4 years. Claims share characteristics: unwitnessed, no police involvement, parking lot or hit-and-run scenarios.",
      "related_indicators": ["IND-002", "IND-003", "IND-004"]
    },
    {
      "pattern_name": "New policy, quick claim",
      "description": "Policy purchased with full premium, claim filed within 3 weeks. Combined with claim history suggests potential policy acquisition for known damage.",
      "related_indicators": ["IND-001", "IND-002"]
    }
  ],
  "red_flags": [
    "4 claims in 4 years across different insurers - possible claim jumping",
    "Pattern of unverifiable loss circumstances",
    "Claim within 30 days of policy inception on a new policy"
  ],
  "yellow_flags": [
    "No police report for $18,500 damage",
    "Other party fled - cannot verify",
    "Single repair estimate from unknown shop",
    "Coverage enhancement shortly before loss"
  ],
  "mitigating_factors": [
    "Claim was reported promptly (next day)",
    "Claimant paid premium in full (not financed)",
    "Photos of damage provided"
  ],
  "recommended_actions": [
    {
      "action": "Obtain claimant's recorded statement",
      "priority": "high",
      "rationale": "Document exact circumstances and lock in timeline details"
    },
    {
      "action": "Request prior claims files from previous carriers",
      "priority": "high",
      "rationale": "Verify circumstances and damage types of prior claims"
    },
    {
      "action": "Inspect vehicle with independent appraiser",
      "priority": "high",
      "rationale": "Verify damage consistent with reported circumstances; check for prior damage"
    },
    {
      "action": "Investigate Quality Auto Body",
      "priority": "medium",
      "rationale": "Check for prior relationship with claimant; verify estimate legitimacy"
    },
    {
      "action": "Obtain parking lot surveillance video",
      "priority": "medium",
      "rationale": "May capture incident or prove/disprove claim"
    },
    {
      "action": "Run comprehensive background check",
      "priority": "medium",
      "rationale": "Financial distress indicators may suggest motive"
    }
  ],
  "investigation_questions": [
    "Why did claimant switch insurers in December 2023?",
    "Did claimant's prior policies lapse or were they cancelled?",
    "What is claimant's relationship with Quality Auto Body?",
    "Can claimant provide any additional details about the other vehicle?",
    "Why was $0 deductible glass coverage added 5 days after policy inception?",
    "Were there any pre-existing damage or repair work on the vehicle?",
    "Does the damage pattern match the described backing collision?"
  ],
  "claim_search_flags": [
    "Query ISO ClaimSearch for Quality Auto Body - volume and patterns",
    "Query NICB for VIN - prior total loss or salvage history",
    "Query NICB for claimant - questionable claims database"
  ],
  "disclaimer": "This screening is for prioritization only. The indicators identified suggest elevated risk warranting investigation, but fraud determination requires thorough investigation and cannot be concluded from this analysis alone. All constitutional and regulatory requirements for investigation must be followed."
}
```

### Example 2: Property Claim - Lower Risk

**Input:**
```
claim_type: property
claim_data: |
  CLAIM #: CLM-2024-11223
  Date of Loss: January 12, 2024
  Date Reported: January 12, 2024
  Loss Type: Water damage - burst pipe
  Location: 456 Residential Lane, Minneapolis, MN

  CLAIMANT: Susan Miller
  Property: Single family home
  Damage: Kitchen and basement flooding from burst pipe
  Estimate: $22,000 (contractor estimate)

  STATEMENT:
  "I came home from work around 6 PM and found water everywhere.
  A pipe under the kitchen sink had burst - probably from the cold.
  The kitchen floor is ruined and water went down to the basement
  affecting the carpet and some stored items."

  WEATHER DATA: Minneapolis recorded -15°F on January 12, 2024.
  Pipe burst claims up 300% in region that week.

  DOCUMENTS:
  - Contractor estimate (licensed, bonded contractor)
  - Photos of damage (time-stamped same day)
  - Plumber emergency service receipt ($350)

policy_data: |
  Policy #: HOME-9988776655
  Effective Date: March 1, 2019 (5 years with company)
  Premium: $1,800/year
  Claims history with carrier: 1 prior claim in 2020 (storm damage, $3,500)
  Coverage: HO-3, $350,000 dwelling, $1,000 deductible
```

**Output:**
```json
{
  "screening_result": {
    "risk_score": 18,
    "risk_level": "low",
    "siu_referral_recommended": false,
    "priority": "none",
    "screening_timestamp": "2024-01-15T10:45:00Z"
  },
  "indicators_found": [
    {
      "indicator_id": "IND-001",
      "indicator_type": "documentation_positive",
      "indicator_name": "Complete documentation provided",
      "severity": "none",
      "confidence": 0.95,
      "evidence": "Time-stamped photos, licensed contractor estimate, plumber receipt all present",
      "weight": -5
    }
  ],
  "patterns_detected": [],
  "red_flags": [],
  "yellow_flags": [],
  "mitigating_factors": [
    "Long-term policyholder (5 years)",
    "Only one prior claim in 5 years (unrelated weather event)",
    "Claim consistent with regional weather event (-15°F, 300% increase in pipe claims)",
    "Same-day reporting with complete documentation",
    "Licensed, bonded contractor estimate",
    "Plumber emergency service receipt corroborates timeline",
    "Time-stamped photos support claim timing"
  ],
  "recommended_actions": [
    {
      "action": "Process claim through standard adjustment",
      "priority": "standard",
      "rationale": "No indicators warrant enhanced scrutiny"
    },
    {
      "action": "Verify contractor license",
      "priority": "low",
      "rationale": "Standard due diligence for repair estimates"
    }
  ],
  "investigation_questions": [],
  "disclaimer": "This screening is for prioritization only. Low risk score indicates standard processing is appropriate, but adjusters should apply normal due diligence."
}
```

### Example 3: Workers' Comp with Mixed Indicators

**Input:**
```
claim_type: workers_comp
claim_data: |
  CLAIM #: WC-2024-5566
  Date of Injury: January 8, 2024 (Monday)
  Date Reported: January 9, 2024
  Injury Type: Lower back strain
  Location: Warehouse, ABC Distribution

  EMPLOYEE: James Wilson, 52
  Job Title: Warehouse Associate (2 years tenure)
  Description: "Injured back lifting heavy boxes during shift"

  MEDICAL:
  - ER visit 01/08/2024
  - MRI ordered 01/10/2024
  - Off work per doctor

  EMPLOYER NOTES:
  - No witnesses to injury
  - Employee was scheduled for performance review 01/15/2024
  - Employee had called out sick previous Friday (01/05/2024)

claimant_history: |
  Prior claims:
  - 2019: Workers comp claim at different employer (back strain, 6 weeks off)
  - No claims with current employer in 2 years
```

**Output:**
```json
{
  "screening_result": {
    "risk_score": 52,
    "risk_level": "medium",
    "siu_referral_recommended": false,
    "priority": "adjuster_review",
    "screening_timestamp": "2024-01-15T11:00:00Z"
  },
  "indicators_found": [
    {
      "indicator_id": "IND-001",
      "indicator_type": "timing_suspicious",
      "indicator_name": "Monday morning injury",
      "severity": "low",
      "confidence": 0.7,
      "evidence": "Injury reported on Monday. Known fraud indicator but also common for legitimate injuries.",
      "weight": 8
    },
    {
      "indicator_id": "IND-002",
      "indicator_type": "circumstances_suspicious",
      "indicator_name": "No witnesses to injury",
      "severity": "medium",
      "confidence": 0.8,
      "evidence": "Employer notes indicate no witnesses to the injury event",
      "weight": 12
    },
    {
      "indicator_id": "IND-003",
      "indicator_type": "employment_issue",
      "indicator_name": "Performance review pending",
      "severity": "medium",
      "confidence": 0.85,
      "evidence": "Employee scheduled for performance review one week after injury (01/15/2024)",
      "weight": 15
    },
    {
      "indicator_id": "IND-004",
      "indicator_type": "claim_history",
      "indicator_name": "Prior similar claim",
      "severity": "medium",
      "confidence": 0.9,
      "evidence": "Previous back strain claim in 2019 with different employer. Same body part, similar injury type.",
      "weight": 12
    },
    {
      "indicator_id": "IND-005",
      "indicator_type": "timing_suspicious",
      "indicator_name": "Recent sick day before claim",
      "severity": "low",
      "confidence": 0.65,
      "evidence": "Employee called out sick Friday 01/05/2024, injured Monday 01/08/2024",
      "weight": 8
    }
  ],
  "patterns_detected": [
    {
      "pattern_name": "Pre-existing condition concern",
      "description": "Prior back injury (2019) combined with sick day before injury suggests possible pre-existing condition being claimed as work injury",
      "related_indicators": ["IND-004", "IND-005"]
    },
    {
      "pattern_name": "Adverse employment timing",
      "description": "Pending performance review creates potential motive for protected leave status",
      "related_indicators": ["IND-003"]
    }
  ],
  "red_flags": [],
  "yellow_flags": [
    "Monday injury with no witnesses",
    "Performance review scheduled for week after injury",
    "Prior same-body-part injury in 2019",
    "Sick day shortly before claimed injury"
  ],
  "mitigating_factors": [
    "2 years with employer without claims - established work history",
    "No claims in 5 years since 2019 incident",
    "Sought medical treatment same day",
    "Job duties (warehouse associate) consistent with back strain risk",
    "Age (52) consistent with increased injury risk",
    "Reported injury next business day - prompt reporting"
  ],
  "recommended_actions": [
    {
      "action": "Obtain detailed recorded statement from employee",
      "priority": "high",
      "rationale": "Document exact mechanism of injury, timeline, and Friday absence explanation"
    },
    {
      "action": "Interview supervisor about performance issues",
      "priority": "high",
      "rationale": "Understand context of pending performance review"
    },
    {
      "action": "Request medical records for past 12 months",
      "priority": "high",
      "rationale": "Determine if back treatment predates claimed injury"
    },
    {
      "action": "Obtain 2019 claim file",
      "priority": "medium",
      "rationale": "Compare injury mechanism and treatment to current claim"
    },
    {
      "action": "Interview potential witnesses in warehouse",
      "priority": "medium",
      "rationale": "Someone may have observed injury or employee's condition that day"
    }
  ],
  "investigation_questions": [
    "What was the reason for the sick day on Friday 01/05?",
    "Has employee received any back treatment in the past year?",
    "What are the specific concerns in the pending performance review?",
    "Can employee describe the exact mechanism of lifting injury?",
    "Were there any job performance issues related to physical capability?",
    "Did employee report any back pain before Monday's injury?"
  ],
  "disclaimer": "This screening is for prioritization only. Medium risk score indicates adjuster should conduct thorough investigation, but indicators alone do not establish fraud. The employee may have a legitimate compensable injury."
}
```

## Gotchas

### Common Failure Modes
1. **False positives from common patterns**: Monday injuries, no witnesses, prior claims are common in legitimate claims too. Weight accordingly.
2. **Bias reinforcement**: Don't let demographics or socioeconomic factors influence screening.
3. **Over-weighting single indicators**: Multiple low-severity indicators shouldn't sum to high risk without pattern coherence.
4. **Missing context**: Weather events, regional trends, industry norms affect baseline expectations.

### Edge Cases to Handle
- **First-party vs third-party**: Different indicators apply
- **Represented claimants**: Attorney involvement is not itself an indicator
- **Catastrophe claims**: Different fraud patterns in CAT events
- **Medical-only vs lost time**: Different risk profiles

### Legal/Ethical Considerations
- **Discrimination risk**: Never use protected class characteristics
- **Bad faith exposure**: Overzealous investigation can create liability
- **Privacy laws**: State-specific requirements for investigation activities
- **Documentation**: All screening rationale must be defensible

### When NOT to Use This Prompt
- **Fraud determination**: Screening only, not determination
- **Denial justification**: Cannot deny claims based on screening alone
- **Subrogation investigation**: Different purpose and indicators
- **Agent/broker fraud**: Different investigation framework

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex claims with nuance | Best at weighing competing indicators |
| **Acceptable:** Claude Sonnet 4 | Standard screening | Good balance of speed/accuracy |
| **Acceptable:** GPT-4o | Pattern detection | Strong at identifying connections |
| **Not Recommended:** Smaller models | - | May miss nuances, create false positives |

## Integration Notes

### Risk Score Calibration
```python
def calibrate_risk_score(raw_score, claim_type, region):
    """Adjust risk score based on baseline rates"""
    # Get baseline fraud rate for claim type and region
    baseline = get_fraud_baseline(claim_type, region)

    # Adjust score relative to baseline
    # Higher baseline = need higher threshold for referral
    adjusted = raw_score * (1 + (baseline - 0.05))  # 5% baseline reference

    return min(100, max(0, adjusted))
```

### SIU Referral Workflow
```python
def process_screening_result(result, claim):
    """Route claim based on screening result"""
    if result['screening_result']['risk_score'] >= 85:
        # Priority SIU referral
        create_siu_case(claim, result, priority='high')
        notify_siu_manager(claim.id)

    elif result['screening_result']['siu_referral_recommended']:
        # Standard SIU referral
        create_siu_case(claim, result, priority='standard')

    elif result['screening_result']['risk_score'] >= 50:
        # Enhanced adjuster review
        flag_for_review(claim, result)
        assign_senior_adjuster(claim.id)

    else:
        # Standard processing
        assign_adjuster(claim.id)

    # Always log screening result
    log_screening(claim.id, result)
```
