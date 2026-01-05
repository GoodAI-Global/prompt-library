# Prior Authorization Extraction

## Use Case

Extract and structure prior authorization request information:
- Parsing prior auth request forms
- Extracting clinical justification elements
- Identifying required supporting documentation
- Preparing authorization submissions
- Tracking authorization status and requirements

Use when processing prior authorization requests for procedures, medications, or services.

## Input Format

**Required:**
- `authorization_document`: Prior authorization form, request letter, or clinical documentation

**Optional:**
- `payer_requirements`: Specific payer criteria for the requested service
- `service_type`: medication, procedure, dme, imaging, specialist_referral
- `urgency`: routine, urgent, emergent

## Output Format

```json
{
  "authorization_request": {
    "request_id": "PA-2024-001234",
    "request_date": "2024-01-15",
    "urgency_level": "routine",
    "status": "pending"
  },
  "patient_information": {
    "name": "Patient Name",
    "dob": "1965-03-22",
    "member_id": "ABC123456789",
    "group_number": "GRP-001"
  },
  "provider_information": {
    "requesting_provider": "Dr. Provider Name",
    "npi": "1234567890",
    "facility": "Medical Center Name",
    "tax_id": "XX-XXXXXXX",
    "contact": "Phone/fax"
  },
  "requested_service": {
    "type": "procedure|medication|imaging|dme",
    "description": "Specific service requested",
    "codes": {
      "cpt": ["Code list"],
      "hcpcs": ["Code list"],
      "icd10": ["Diagnosis codes"],
      "ndc": "Drug code if medication"
    },
    "quantity": "Amount/duration requested",
    "frequency": "How often",
    "duration": "Length of treatment",
    "site_of_service": "inpatient|outpatient|home"
  },
  "clinical_information": {
    "primary_diagnosis": {
      "description": "Diagnosis",
      "icd10": "Code"
    },
    "secondary_diagnoses": [],
    "clinical_history": "Relevant history summary",
    "previous_treatments": [
      {
        "treatment": "Prior treatment tried",
        "dates": "When tried",
        "outcome": "Result/why failed"
      }
    ],
    "clinical_rationale": "Why this service is needed"
  },
  "medical_necessity": {
    "criteria_met": ["List of criteria satisfied"],
    "supporting_evidence": ["Clinical evidence supporting request"],
    "alternatives_considered": ["Why alternatives won't work"]
  },
  "documentation_checklist": {
    "included": ["Documents attached"],
    "missing": ["Documents still needed"],
    "recommendations": ["Suggested additional documentation"]
  },
  "payer_specific": {
    "payer_name": "Insurance company",
    "plan_type": "HMO|PPO|Medicare|Medicaid",
    "auth_requirements": ["Specific payer requirements"],
    "submission_method": "portal|fax|phone"
  },
  "extraction_confidence": {
    "overall": 0.88,
    "missing_fields": ["Fields not found in document"],
    "uncertain_fields": ["Fields with low confidence"]
  }
}
```

## The Prompt

```
You are a prior authorization specialist extracting information from authorization requests. Accurately identify all required elements for authorization processing.

AUTHORIZATION DOCUMENT:
{{authorization_document}}

{{#if payer_requirements}}
PAYER REQUIREMENTS:
{{payer_requirements}}
{{/if}}

SERVICE TYPE: {{service_type | default: "unspecified"}}
URGENCY: {{urgency | default: "routine"}}

EXTRACTION FRAMEWORK:

1. PATIENT IDENTIFICATION
   Required elements:
   - Full name
   - Date of birth
   - Member/subscriber ID
   - Group number
   - Plan type

2. PROVIDER INFORMATION
   Required elements:
   - Requesting provider name
   - NPI number
   - Practice/facility name
   - Tax ID
   - Contact information (phone, fax)
   - Servicing provider if different

3. SERVICE DETAILS
   For procedures:
   - CPT/HCPCS codes
   - Procedure description
   - Site of service
   - Planned date

   For medications:
   - Drug name (brand and generic)
   - NDC code
   - Strength/dosage
   - Quantity
   - Days supply
   - Directions for use

   For DME:
   - HCPCS codes
   - Equipment description
   - Rental vs purchase
   - Duration of need

   For imaging:
   - CPT codes
   - Type of study
   - Body part
   - With/without contrast

4. DIAGNOSIS INFORMATION
   - Primary diagnosis with ICD-10
   - Secondary/related diagnoses
   - Onset date if relevant
   - Current clinical status

5. CLINICAL JUSTIFICATION
   Extract:
   - Why service is medically necessary
   - What conditions/symptoms support need
   - Previous treatments tried
   - Why alternatives insufficient
   - Expected outcome/benefit

6. STEP THERAPY / PRIOR TREATMENTS
   For each prior treatment:
   - What was tried
   - Duration of trial
   - Outcome (effective, ineffective, adverse reaction)
   - Reason for discontinuation

7. SUPPORTING DOCUMENTATION
   Identify:
   - Lab results mentioned
   - Imaging studies referenced
   - Specialist notes
   - Treatment records
   - Letters of medical necessity

8. PAYER-SPECIFIC ELEMENTS
   Look for:
   - Pre-service vs concurrent review
   - Expedited/urgent request indicators
   - Peer-to-peer request
   - Appeal vs initial request

EXTRACTION RULES:
- Extract exact values where available
- Note when required fields are missing
- Flag ambiguous or unclear information
- Preserve original codes exactly
- Indicate confidence for inferred values

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{authorization_document}}` | string | Yes | Prior auth form or supporting docs |
| `{{payer_requirements}}` | string | No | Payer-specific criteria |
| `{{service_type}}` | string | No | Type of service requested |
| `{{urgency}}` | string | No | Urgency level |

## Examples

### Example 1: Medication Prior Authorization

**Input:**
```
authorization_document: |
  PRIOR AUTHORIZATION REQUEST FORM

  Date: January 15, 2024
  ☑ Urgent Request (response needed within 24 hours)

  PATIENT INFORMATION
  Name: Robert Martinez
  DOB: 08/15/1958
  Member ID: UHC-789456123
  Group #: 12345-A

  PRESCRIBER INFORMATION
  Name: Dr. Sarah Chen, MD
  NPI: 1234567890
  Practice: Valley Rheumatology Associates
  Address: 123 Medical Plaza, Suite 200, Phoenix, AZ 85001
  Phone: (555) 123-4567
  Fax: (555) 123-4568

  MEDICATION REQUESTED
  Drug Name: Humira (adalimumab)
  Strength: 40mg/0.4mL
  Quantity: 2 pens
  Days Supply: 28
  Directions: Inject 40mg subcutaneously every other week

  DIAGNOSIS
  Primary: M05.79 - Rheumatoid arthritis with rheumatoid factor, unspecified
  Secondary: M06.09 - Rheumatoid arthritis without rheumatoid factor, unspecified site

  CLINICAL INFORMATION

  Patient History:
  65-year-old male with rheumatoid arthritis diagnosed in 2019. Disease has been
  progressively active despite conventional DMARD therapy.

  Previous Treatments Tried:
  1. Methotrexate 25mg weekly x 6 months (2019-2020)
     - Inadequate response, DAS28 remained >5.1
     - Continued as background therapy

  2. Sulfasalazine 2g daily added x 4 months (2020)
     - GI intolerance, discontinued

  3. Leflunomide 20mg daily x 6 months (2020-2021)
     - Partial response but continued active disease
     - DAS28: 4.8

  4. Hydroxychloroquine 400mg daily added (2021-present)
     - Still on triple therapy with inadequate control

  Current Disease Status:
  - DAS28 score: 5.4 (high disease activity)
  - Swollen joint count: 8
  - Tender joint count: 12
  - CRP: 2.8 mg/dL (elevated, normal <0.5)
  - ESR: 45 mm/hr (elevated)
  - RF positive, Anti-CCP positive

  Medical Necessity:
  Patient has failed multiple conventional DMARDs including methotrexate,
  leflunomide, and hydroxychloroquine with persistently high disease activity.
  Per ACR guidelines, biologic therapy is indicated after DMARD failure.
  Humira is first-line biologic for RA with proven efficacy.

  ATTACHED DOCUMENTATION
  ☑ Recent labs (CBC, CMP, CRP, ESR)
  ☑ RF and Anti-CCP results
  ☑ Last 3 office visit notes
  ☑ Letter of Medical Necessity
  ☐ Imaging studies

service_type: medication
urgency: urgent
```

**Output:**
```json
{
  "authorization_request": {
    "request_id": null,
    "request_date": "2024-01-15",
    "urgency_level": "urgent",
    "status": "pending"
  },
  "patient_information": {
    "name": "Robert Martinez",
    "dob": "1958-08-15",
    "member_id": "UHC-789456123",
    "group_number": "12345-A"
  },
  "provider_information": {
    "requesting_provider": "Dr. Sarah Chen, MD",
    "npi": "1234567890",
    "facility": "Valley Rheumatology Associates",
    "address": "123 Medical Plaza, Suite 200, Phoenix, AZ 85001",
    "phone": "(555) 123-4567",
    "fax": "(555) 123-4568",
    "tax_id": null
  },
  "requested_service": {
    "type": "medication",
    "description": "Humira (adalimumab) 40mg/0.4mL subcutaneous injection",
    "codes": {
      "cpt": [],
      "hcpcs": ["J0135"],
      "icd10": ["M05.79", "M06.09"],
      "ndc": null
    },
    "quantity": "2 pens",
    "frequency": "Every other week",
    "duration": "28 days supply",
    "directions": "Inject 40mg subcutaneously every other week"
  },
  "clinical_information": {
    "primary_diagnosis": {
      "description": "Rheumatoid arthritis with rheumatoid factor, unspecified site",
      "icd10": "M05.79"
    },
    "secondary_diagnoses": [
      {
        "description": "Rheumatoid arthritis without rheumatoid factor, unspecified site",
        "icd10": "M06.09"
      }
    ],
    "clinical_history": "65-year-old male with rheumatoid arthritis diagnosed in 2019, progressively active despite conventional DMARD therapy",
    "previous_treatments": [
      {
        "treatment": "Methotrexate 25mg weekly",
        "dates": "2019-2020 (6 months)",
        "outcome": "Inadequate response, DAS28 remained >5.1, continued as background therapy"
      },
      {
        "treatment": "Sulfasalazine 2g daily",
        "dates": "2020 (4 months)",
        "outcome": "GI intolerance, discontinued"
      },
      {
        "treatment": "Leflunomide 20mg daily",
        "dates": "2020-2021 (6 months)",
        "outcome": "Partial response but continued active disease, DAS28: 4.8"
      },
      {
        "treatment": "Hydroxychloroquine 400mg daily",
        "dates": "2021-present",
        "outcome": "Triple therapy with inadequate control"
      }
    ],
    "clinical_rationale": "Patient has failed multiple conventional DMARDs with persistently high disease activity (DAS28: 5.4). Per ACR guidelines, biologic therapy is indicated after DMARD failure."
  },
  "medical_necessity": {
    "criteria_met": [
      "Failed first-line DMARD (methotrexate)",
      "Failed/intolerant to multiple conventional DMARDs",
      "Documented high disease activity (DAS28 >5.1)",
      "Elevated inflammatory markers (CRP, ESR)",
      "Positive serology (RF, Anti-CCP)"
    ],
    "supporting_evidence": [
      "DAS28 score: 5.4 (high disease activity)",
      "Swollen joint count: 8",
      "Tender joint count: 12",
      "CRP: 2.8 mg/dL (elevated)",
      "ESR: 45 mm/hr (elevated)",
      "RF positive, Anti-CCP positive"
    ],
    "alternatives_considered": [
      "Methotrexate - inadequate response",
      "Sulfasalazine - GI intolerance",
      "Leflunomide - partial response only",
      "Triple DMARD therapy - ongoing with inadequate control"
    ]
  },
  "documentation_checklist": {
    "included": [
      "Recent labs (CBC, CMP, CRP, ESR)",
      "RF and Anti-CCP results",
      "Last 3 office visit notes",
      "Letter of Medical Necessity"
    ],
    "missing": [
      "Imaging studies"
    ],
    "recommendations": [
      "Consider adding X-rays of affected joints if available",
      "Tax ID for provider may be needed"
    ]
  },
  "payer_specific": {
    "payer_name": "United Healthcare (inferred from member ID prefix)",
    "plan_type": null,
    "auth_requirements": null,
    "submission_method": "fax"
  },
  "extraction_confidence": {
    "overall": 0.92,
    "missing_fields": ["request_id", "tax_id", "NDC", "plan_type"],
    "uncertain_fields": ["payer_name (inferred from member ID prefix)"]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Code accuracy**: Always verify extracted codes against reference
2. **Date formats**: Standardize to YYYY-MM-DD
3. **Missing vs unclear**: Distinguish between absent and illegible information
4. **Payer inference**: Don't assume payer from incomplete information

### Edge Cases to Handle
- **Incomplete forms**: Flag missing required fields
- **Handwritten additions**: Note if information is handwritten/unclear
- **Multiple requests**: Handle forms requesting multiple services
- **Appeal vs initial**: Identify if this is an initial request or appeal

### When NOT to Use This Prompt
- **Auto-adjudication**: Not for automated approval decisions
- **Benefits verification**: Different from authorization request
- **Claims processing**: Separate workflow from prior auth
- **Patient communication**: Requires different format

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-page requests | Best at synthesizing medical criteria |
| **Acceptable:** Claude Sonnet 4 | Standard PA forms | Good balance for high volume |
| **Acceptable:** GPT-4o | Clinical justification extraction | Strong medical reasoning |
| **Caution:** Smaller models | - | May miss clinical nuances |
