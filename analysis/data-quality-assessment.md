# Data Quality Assessment

## Use Case

Evaluate data quality for analytics, reporting, and AI/ML applications:
- Dataset validation before analysis
- Data pipeline quality monitoring
- Pre-migration data assessment
- Training data evaluation for ML
- Regulatory compliance data audits

Use when you need structured assessment of data fitness for purpose.

## Input Format

**Required:**
- `data_sample`: Representative sample of the dataset (can be JSON, CSV excerpt, or description)
- `data_description`: Description of what the data represents

**Optional:**
- `quality_requirements`: Specific quality thresholds or requirements
- `use_case`: Intended use (analytics, ML training, reporting, migration)
- `schema`: Expected schema or data dictionary
- `known_issues`: Previously identified data issues

## Output Format

```json
{
  "assessment_summary": {
    "dataset_name": "customer_transactions",
    "assessment_date": "2024-01-15",
    "overall_quality_score": 78,
    "fitness_for_purpose": "acceptable_with_caveats",
    "records_sampled": 1000,
    "critical_issues": 2,
    "recommendation": "proceed_with_remediation"
  },
  "dimension_scores": {
    "completeness": {"score": 85, "grade": "B"},
    "accuracy": {"score": 72, "grade": "C"},
    "consistency": {"score": 80, "grade": "B"},
    "timeliness": {"score": 90, "grade": "A"},
    "validity": {"score": 75, "grade": "C"},
    "uniqueness": {"score": 88, "grade": "B"}
  },
  "field_analysis": [
    {
      "field": "email",
      "completeness": 0.95,
      "validity": 0.88,
      "issues": ["5% missing", "12% invalid format"],
      "recommendation": "implement validation"
    }
  ],
  "issues_found": [
    {
      "severity": "critical",
      "dimension": "accuracy",
      "description": "Duplicate customer IDs with conflicting data",
      "affected_records": 150,
      "impact": "Breaks customer aggregation logic"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "action": "Deduplicate customer records",
      "rationale": "Critical for accurate analytics"
    }
  ],
  "data_profile": {
    "total_fields": 15,
    "total_records": 50000,
    "date_range": {"min": "2023-01-01", "max": "2024-01-15"}
  }
}
```

## The Prompt

```
You are a data quality analyst. Assess the provided data against quality dimensions and provide actionable findings.

DATA DESCRIPTION:
{{data_description}}

DATA SAMPLE:
{{data_sample}}

{{#if quality_requirements}}
QUALITY REQUIREMENTS:
{{quality_requirements}}
{{/if}}

{{#if use_case}}
INTENDED USE CASE: {{use_case}}
{{/if}}

{{#if schema}}
EXPECTED SCHEMA:
{{schema}}
{{/if}}

{{#if known_issues}}
KNOWN ISSUES:
{{known_issues}}
{{/if}}

DATA QUALITY DIMENSIONS:

1. COMPLETENESS (0-100)
   - Missing values: What percentage of required fields are populated?
   - Null handling: Are nulls appropriate or problematic?
   - Coverage: Does data cover expected range/scope?

2. ACCURACY (0-100)
   - Value correctness: Do values represent reality?
   - Format correctness: Are formats consistent and valid?
   - Range validity: Are values within expected bounds?

3. CONSISTENCY (0-100)
   - Internal consistency: Do related fields align?
   - Cross-system consistency: Does data match external sources?
   - Temporal consistency: Is data consistent over time?

4. TIMELINESS (0-100)
   - Currency: How recent is the data?
   - Latency: Is there delay in data availability?
   - Relevance: Is data still applicable?

5. VALIDITY (0-100)
   - Schema compliance: Does data match expected structure?
   - Domain validity: Are values from valid domains?
   - Referential integrity: Do foreign keys resolve?

6. UNIQUENESS (0-100)
   - Duplicate records: What percentage are duplicates?
   - Key uniqueness: Are primary keys unique?
   - Entity resolution: Are entities properly deduplicated?

SCORING GUIDELINES:
- 90-100: Excellent - No significant issues
- 80-89: Good - Minor issues, usable as-is
- 70-79: Acceptable - Issues requiring attention
- 60-69: Poor - Significant issues, use with caution
- Below 60: Critical - Major remediation required

ISSUE SEVERITY:
- critical: Prevents use, data integrity compromised
- major: Significant impact on analysis/operations
- minor: Limited impact, cosmetic or edge cases
- informational: Observations, not blocking

ANALYSIS APPROACH:
1. Profile each field for completeness, validity, format
2. Identify patterns suggesting quality issues
3. Check relationships between fields
4. Assess fitness for stated use case
5. Provide specific, actionable recommendations

OUTPUT REQUIREMENTS:
- Overall quality score with dimensional breakdown
- Field-level analysis for key fields
- Issues categorized by severity
- Specific remediation recommendations
- Assessment of fitness for intended use

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{data_description}}` | string | Yes | What the data represents |
| `{{data_sample}}` | string | Yes | Sample data for analysis |
| `{{quality_requirements}}` | string | No | Specific quality thresholds |
| `{{use_case}}` | string | No | Intended use for the data |
| `{{schema}}` | string | No | Expected data structure |
| `{{known_issues}}` | string | No | Previously identified issues |

## Examples

### Example 1: Customer Data Assessment

**Input:**
```
data_description: |
  Customer master data from CRM system
  Used for: Marketing segmentation, sales analytics, customer 360 view
  Source: Salesforce CRM
  Refresh: Daily

data_sample: |
  customer_id,first_name,last_name,email,phone,city,state,country,created_date,last_purchase,lifetime_value
  C001,John,Smith,john.smith@email.com,555-123-4567,New York,NY,USA,2021-03-15,2024-01-10,15234.50
  C002,Jane,Doe,jane.doe@company,5551234567,Los Angeles,CA,USA,2022-06-20,2023-12-05,8721.00
  C003,Bob,,bob.wilson@email.com,,Chicago,IL,USA,2020-01-01,2024-01-12,42156.75
  C004,Alice,Johnson,INVALID_EMAIL,555-987-6543,Houston,Texas,USA,2023-11-30,,1250.00
  C005,John,Smith,john.smith@email.com,555-123-4567,New York,NY,US,2021-03-15,2024-01-10,15234.50
  C006,María,García,maria.garcia@email.com,+1-555-111-2222,Miami,FL,USA,2022-08-15,2024-01-08,6543.21
  C007,NULL,Williams,t.williams@email.com,555-333-4444,Seattle,Washington,United States,2019-05-22,2023-06-15,28765.00
  C008,Sarah,Connor,s.connor@email.com,555.444.5555,Phoenix,AZ,USA,2024-01-20,NULL,0.00

  Total records in full dataset: 125,000

use_case: ML model for customer churn prediction

quality_requirements: |
  - Email: Must be valid format, 100% required
  - Phone: Preferred, consistent format
  - State: Two-letter abbreviation required
  - Country: ISO 3166-1 alpha-3 required
  - Lifetime value: Must be non-negative
  - No duplicate customers
```

**Output:**
```json
{
  "assessment_summary": {
    "dataset_name": "customer_master_crm",
    "source": "Salesforce CRM",
    "assessment_date": "2024-01-15",
    "overall_quality_score": 68,
    "fitness_for_purpose": "problematic",
    "records_sampled": 8,
    "estimated_total_records": 125000,
    "critical_issues": 2,
    "major_issues": 3,
    "recommendation": "remediation_required_before_ml"
  },
  "dimension_scores": {
    "completeness": {
      "score": 75,
      "grade": "C",
      "findings": "Missing values in last_name (12.5%), phone (12.5%), last_purchase (12.5%)"
    },
    "accuracy": {
      "score": 62,
      "grade": "D",
      "findings": "Invalid emails, inconsistent phone formats, state/country inconsistencies"
    },
    "consistency": {
      "score": 58,
      "grade": "D",
      "findings": "State format inconsistent (NY vs Texas vs Washington), country format inconsistent (USA vs US vs United States)"
    },
    "timeliness": {
      "score": 92,
      "grade": "A",
      "findings": "Data refreshed daily, recent transactions present"
    },
    "validity": {
      "score": 65,
      "grade": "D",
      "findings": "Email format violations, state/country not matching required formats"
    },
    "uniqueness": {
      "score": 75,
      "grade": "C",
      "findings": "Apparent duplicate (C001/C005), 'NULL' string in name field"
    }
  },
  "field_analysis": [
    {
      "field": "customer_id",
      "type": "identifier",
      "completeness": 1.0,
      "uniqueness": 0.875,
      "issues": ["Duplicate ID pattern detected (C001 = C005)"],
      "severity": "critical",
      "recommendation": "Implement deduplication logic"
    },
    {
      "field": "email",
      "type": "contact",
      "completeness": 1.0,
      "validity": 0.75,
      "issues": [
        "Invalid format: 'jane.doe@company' (missing TLD)",
        "Invalid format: 'INVALID_EMAIL' (not an email)",
        "Duplicate: 'john.smith@email.com' appears twice"
      ],
      "severity": "critical",
      "recommendation": "Apply email validation regex, deduplicate by email"
    },
    {
      "field": "phone",
      "type": "contact",
      "completeness": 0.875,
      "validity": 0.57,
      "issues": [
        "Inconsistent formats: '555-123-4567', '5551234567', '+1-555-111-2222', '555.444.5555'",
        "12.5% missing values"
      ],
      "severity": "major",
      "recommendation": "Normalize to E.164 format (+1XXXXXXXXXX)"
    },
    {
      "field": "first_name",
      "type": "demographic",
      "completeness": 0.875,
      "validity": 0.75,
      "issues": [
        "'NULL' as string value (likely data entry error)",
        "Missing value for Bob (C003)"
      ],
      "severity": "minor",
      "recommendation": "Convert 'NULL' strings to actual null, review missing names"
    },
    {
      "field": "last_name",
      "type": "demographic",
      "completeness": 0.875,
      "validity": 1.0,
      "issues": ["12.5% missing"],
      "severity": "minor",
      "recommendation": "Investigate source of missing last names"
    },
    {
      "field": "state",
      "type": "geographic",
      "completeness": 1.0,
      "validity": 0.625,
      "issues": [
        "Inconsistent format: 'NY' vs 'Texas' vs 'Washington'",
        "Requirement: Two-letter abbreviation"
      ],
      "severity": "major",
      "recommendation": "Standardize to two-letter state codes"
    },
    {
      "field": "country",
      "type": "geographic",
      "completeness": 1.0,
      "validity": 0.25,
      "issues": [
        "Multiple formats: 'USA', 'US', 'United States'",
        "Requirement: ISO 3166-1 alpha-3 (should be 'USA')"
      ],
      "severity": "major",
      "recommendation": "Standardize to ISO 3166-1 alpha-3"
    },
    {
      "field": "last_purchase",
      "type": "behavioral",
      "completeness": 0.75,
      "validity": 0.83,
      "issues": [
        "25% missing (NULL values)",
        "'NULL' string vs actual null ambiguity"
      ],
      "severity": "minor",
      "recommendation": "For churn model, distinguish 'never purchased' from 'unknown'"
    },
    {
      "field": "lifetime_value",
      "type": "metric",
      "completeness": 1.0,
      "validity": 1.0,
      "issues": ["$0.00 value for new customer - valid but verify"],
      "severity": "informational",
      "recommendation": "Confirm $0 is appropriate for new customers"
    }
  ],
  "issues_found": [
    {
      "id": "ISS-001",
      "severity": "critical",
      "dimension": "uniqueness",
      "description": "Duplicate customer records detected",
      "detail": "C001 and C005 appear to be the same customer (same name, email, phone, address) but have different customer_ids",
      "affected_records": "Estimated 2-5% based on sample",
      "impact": "Will cause duplicate counts in churn model, inflated customer counts",
      "remediation": "Implement entity resolution using email + name matching"
    },
    {
      "id": "ISS-002",
      "severity": "critical",
      "dimension": "validity",
      "description": "Invalid email formats will break communication features",
      "detail": "12.5% of emails in sample are invalid (missing TLD, non-email strings)",
      "affected_records": "Estimated 10-15% of 125,000",
      "impact": "Cannot use email for churn model features or outreach",
      "remediation": "Apply regex validation, flag/remove invalid emails"
    },
    {
      "id": "ISS-003",
      "severity": "major",
      "dimension": "consistency",
      "description": "Geographic fields not standardized",
      "detail": "State and country use inconsistent formats",
      "affected_records": "Estimated 40-60%",
      "impact": "Geographic analysis unreliable, regional churn patterns will be skewed",
      "remediation": "Apply standardization mapping to ISO codes"
    },
    {
      "id": "ISS-004",
      "severity": "major",
      "dimension": "consistency",
      "description": "Phone format inconsistency",
      "detail": "4+ different phone formats observed",
      "affected_records": "Estimated 80%+ use non-standard format",
      "impact": "Cannot use phone as consistent feature, contact campaigns affected",
      "remediation": "Parse and normalize to E.164"
    },
    {
      "id": "ISS-005",
      "severity": "minor",
      "dimension": "validity",
      "description": "'NULL' string values instead of null",
      "detail": "first_name contains string 'NULL' instead of null value",
      "affected_records": "At least 1 in sample",
      "impact": "Data processing may treat 'NULL' as valid name",
      "remediation": "Replace 'NULL' strings with actual null values"
    }
  ],
  "ml_readiness_assessment": {
    "use_case": "Customer churn prediction",
    "readiness": "not_ready",
    "critical_blockers": [
      "Duplicate records will leak data between train/test sets",
      "Invalid emails cannot be used as features"
    ],
    "feature_impacts": {
      "email_features": "Blocked - too many invalid",
      "phone_features": "Blocked - inconsistent format",
      "geographic_features": "Degraded - need standardization",
      "behavioral_features": "Usable with caveats - handle null purchase dates"
    },
    "recommended_preprocessing": [
      "Deduplicate by email + name combination",
      "Remove or flag invalid emails",
      "Standardize phone to E.164",
      "Standardize state/country to ISO codes",
      "Convert 'NULL' strings to null",
      "Create 'never_purchased' flag for null last_purchase"
    ]
  },
  "recommendations": [
    {
      "priority": "critical",
      "action": "Implement customer deduplication",
      "rationale": "Duplicate records will contaminate ML model and inflate metrics",
      "effort": "medium",
      "impact": "high"
    },
    {
      "priority": "critical",
      "action": "Validate and clean email field",
      "rationale": "Required field with 25%+ quality issues",
      "effort": "low",
      "impact": "high"
    },
    {
      "priority": "high",
      "action": "Standardize geographic fields",
      "rationale": "Critical for regional analysis and feature engineering",
      "effort": "low",
      "impact": "medium"
    },
    {
      "priority": "high",
      "action": "Normalize phone numbers",
      "rationale": "Enables phone-based features and contact campaigns",
      "effort": "medium",
      "impact": "medium"
    },
    {
      "priority": "medium",
      "action": "Implement data validation at source (CRM)",
      "rationale": "Prevent quality issues from entering the system",
      "effort": "high",
      "impact": "high"
    }
  ],
  "data_profile": {
    "total_fields": 11,
    "total_records": 125000,
    "date_range": {
      "created_date": {"min": "2019-05-22", "max": "2024-01-20"},
      "last_purchase": {"min": "2023-06-15", "max": "2024-01-12"}
    },
    "value_ranges": {
      "lifetime_value": {"min": 0.0, "max": 42156.75}
    }
  }
}
```

## Gotchas

### Common Failure Modes
1. **Sample bias**: Small samples may miss issues. Note sample size limitations.
2. **Domain ignorance**: "Invalid" values may be valid in context.
3. **Score inflation**: Don't average dimensions equally—weight by importance for use case.
4. **Missing context**: Data issues may be known and accepted.

### Edge Cases to Handle
- **Empty datasets**: Report inability to assess
- **Single value columns**: May be valid (status field) or error
- **Outliers**: May be errors or legitimate extreme values
- **Derived fields**: Quality depends on source fields

### When NOT to Use This Prompt
- **Real-time validation**: Needs different architecture
- **Large-scale profiling**: Use dedicated data quality tools
- **Compliance audits**: Need certified methodologies
- **Automated pipelines**: Integrate quality checks in code

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex datasets | Best pattern recognition |
| **Acceptable:** Claude Sonnet 4 | Standard assessments | Good balance |
| **Acceptable:** GPT-4o | Varied formats | Strong format handling |
| **Caution:** Smaller models | - | May miss subtle issues |
