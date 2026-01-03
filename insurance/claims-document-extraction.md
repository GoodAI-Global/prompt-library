# Claims Document Extraction

## Use Case

Extract structured data from insurance claims documents:
- First Notice of Loss (FNOL) forms
- Claims intake documents
- Supporting documentation (police reports, medical records, repair estimates)
- Correspondence with claimants
- Adjuster notes

Use when processing claims for automated triage, data entry reduction, or claims analytics.

## Input Format

**Required:**
- `document_text`: The OCR'd text or transcribed content of the claim document
- `claim_type`: auto, property, health, life, liability, workers_comp

**Optional:**
- `policy_number`: Known policy number for validation
- `document_type`: fnol, supporting_doc, correspondence, adjuster_notes
- `existing_claim_data`: Previously extracted data to supplement

## Output Format

```json
{
  "success": true,
  "extraction_timestamp": "2024-01-15T10:30:00Z",
  "claim_type": "auto",
  "document_type": "fnol",
  "claimant": {
    "name": {
      "value": "John Smith",
      "confidence": 0.95
    },
    "contact": {
      "phone": {"value": "555-123-4567", "confidence": 0.9},
      "email": {"value": "john@email.com", "confidence": 0.85},
      "address": {"value": {...}, "confidence": 0.88}
    },
    "relationship_to_insured": "self"
  },
  "policy": {
    "number": {"value": "POL-12345678", "confidence": 0.98},
    "holder_name": {"value": "John Smith", "confidence": 0.95},
    "effective_date": {"value": "2024-01-01", "confidence": 0.9}
  },
  "incident": {
    "date": {"value": "2024-01-10", "confidence": 0.95},
    "time": {"value": "14:30", "confidence": 0.8},
    "location": {"value": {...}, "confidence": 0.85},
    "description": {"value": "...", "confidence": 0.9}
  },
  "damages": {
    "estimated_amount": {"value": 5000, "confidence": 0.7},
    "currency": "USD",
    "damage_description": {"value": "...", "confidence": 0.85}
  },
  "parties_involved": [...],
  "witnesses": [...],
  "injuries": {...},
  "police_report": {...},
  "metadata": {
    "fields_extracted": 15,
    "fields_missing": ["witness_contact"],
    "average_confidence": 0.87,
    "flags": ["handwritten_notes_detected", "multiple_vehicles"]
  }
}
```

## The Prompt

```
You are an insurance claims document extraction specialist. Extract all relevant claim information with high precision.

CLAIM TYPE: {{claim_type}}
DOCUMENT TYPE: {{document_type | default: "unknown"}}

{{#if policy_number}}
EXPECTED POLICY NUMBER: {{policy_number}}
{{/if}}

DOCUMENT CONTENT:
{{document_text}}

{{#if existing_claim_data}}
EXISTING CLAIM DATA (supplement, don't override unless higher confidence):
{{existing_claim_data}}
{{/if}}

EXTRACTION REQUIREMENTS:

1. CLAIMANT INFORMATION
   - Full name (first, middle, last)
   - Contact: phone, email, mailing address
   - Relationship to policyholder (self, spouse, dependent, other)
   - Date of birth (if available)
   - Driver's license (for auto claims)

2. POLICY INFORMATION
   - Policy number (validate format: typically XXX-########)
   - Policyholder name
   - Policy effective date
   - Coverage type mentioned

3. INCIDENT DETAILS
   - Date of incident (normalize to YYYY-MM-DD)
   - Time of incident (24-hour format)
   - Location (structured: street, city, state, zip)
   - Description (verbatim from document, max 500 chars)
   - Incident type (collision, theft, water damage, etc.)

4. DAMAGES/LOSSES
   - Estimated amount (numeric, USD assumed unless stated)
   - Damage description
   - Items affected (for property claims)
   - Vehicle info (for auto: year, make, model, VIN)

5. OTHER PARTIES (for liability/auto)
   - Name, contact information
   - Insurance company and policy
   - Vehicle information
   - Fault assessment mentioned

6. WITNESSES
   - Name, contact information
   - Statement summary

7. INJURIES (if applicable)
   - Injured party name
   - Injury description
   - Medical treatment sought
   - Medical provider

8. POLICE/AUTHORITY REPORT
   - Report number
   - Jurisdiction
   - Officer name/badge
   - Report date

CONFIDENCE SCORING:
- 1.0: Clearly labeled, typed, unambiguous
- 0.85-0.95: Clearly present, minor interpretation needed
- 0.70-0.85: Inferred from context, some ambiguity
- 0.50-0.70: Partial information, needs verification
- Below 0.50: Do not extract, mark as missing

SPECIAL HANDLING:

Handwritten content:
- Note as "handwritten" in source_type
- Reduce confidence by 0.1
- Flag for human review if confidence < 0.7

Dates:
- Normalize all dates to YYYY-MM-DD
- If only partial date (e.g., "January 2024"), note as approximate

Amounts:
- Extract numeric value only
- Note currency if specified (default USD)
- Distinguish estimate vs actual

Multiple pages/sections:
- Combine information across sections
- Use highest confidence extraction for duplicates
- Note section source for each field

FLAGS TO APPLY:
- handwritten_notes_detected
- multiple_vehicles
- injury_reported
- fatality_mentioned
- prior_claim_referenced
- fraud_indicators (inconsistent dates, excessive claims)
- incomplete_contact_info
- missing_police_report (for required claim types)

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{claim_type}}` | string | Yes | Type: auto, property, health, life, liability, workers_comp |
| `{{document_text}}` | string | Yes | The OCR'd or transcribed document content |
| `{{document_type}}` | string | No | Document category for context |
| `{{policy_number}}` | string | No | Expected policy number for validation |
| `{{existing_claim_data}}` | JSON | No | Previously extracted data to supplement |

## Examples

### Example 1: Clean Auto Claim FNOL

**Input:**
```
claim_type: auto
document_type: fnol
document_text: |
  FIRST NOTICE OF LOSS - AUTO CLAIM

  Date: January 15, 2024
  Claim Reference: CLM-2024-00892

  POLICYHOLDER INFORMATION
  Name: Sarah M. Johnson
  Policy Number: AUTO-98765432
  Phone: (555) 234-5678
  Email: sarah.johnson@email.com
  Address: 1234 Oak Street, Apt 5B
           Portland, OR 97201

  INCIDENT DETAILS
  Date of Accident: January 10, 2024
  Time: 2:45 PM
  Location: Intersection of Main St and 5th Ave, Portland, OR

  Description of Incident:
  I was traveling northbound on Main Street when another vehicle ran a red
  light and struck my vehicle on the passenger side. The other driver admitted
  fault at the scene.

  VEHICLE INFORMATION
  Year: 2022
  Make: Honda
  Model: Accord
  VIN: 1HGCV1F34NA123456
  Damage: Passenger side door and fender, significant denting and scratches

  OTHER PARTY INFORMATION
  Name: Robert Williams
  Phone: (555) 345-6789
  Insurance: State Farm Policy #SF-11223344
  Vehicle: 2020 Ford F-150, Blue

  POLICE REPORT
  Report #: PDX-2024-12345
  Officer: Badge #4521
  Filed: January 10, 2024

  ESTIMATED DAMAGES: $4,500

  Signature: Sarah M. Johnson
  Date: January 15, 2024
```

**Output:**
```json
{
  "success": true,
  "extraction_timestamp": "2024-01-15T14:30:00Z",
  "claim_type": "auto",
  "document_type": "fnol",
  "claim_reference": {
    "value": "CLM-2024-00892",
    "confidence": 1.0
  },
  "claimant": {
    "name": {
      "value": {
        "first": "Sarah",
        "middle": "M",
        "last": "Johnson"
      },
      "confidence": 1.0
    },
    "contact": {
      "phone": {"value": "+15552345678", "confidence": 1.0, "normalized": "(555) 234-5678"},
      "email": {"value": "sarah.johnson@email.com", "confidence": 1.0},
      "address": {
        "value": {
          "street": "1234 Oak Street, Apt 5B",
          "city": "Portland",
          "state": "OR",
          "postal": "97201",
          "country": "US"
        },
        "confidence": 0.98
      }
    },
    "relationship_to_insured": "self"
  },
  "policy": {
    "number": {"value": "AUTO-98765432", "confidence": 1.0},
    "holder_name": {"value": "Sarah M. Johnson", "confidence": 1.0}
  },
  "incident": {
    "date": {"value": "2024-01-10", "confidence": 1.0},
    "time": {"value": "14:45", "confidence": 1.0},
    "location": {
      "value": {
        "description": "Intersection of Main St and 5th Ave",
        "city": "Portland",
        "state": "OR"
      },
      "confidence": 0.95
    },
    "description": {
      "value": "I was traveling northbound on Main Street when another vehicle ran a red light and struck my vehicle on the passenger side. The other driver admitted fault at the scene.",
      "confidence": 1.0
    },
    "incident_type": "collision"
  },
  "vehicle": {
    "year": {"value": 2022, "confidence": 1.0},
    "make": {"value": "Honda", "confidence": 1.0},
    "model": {"value": "Accord", "confidence": 1.0},
    "vin": {"value": "1HGCV1F34NA123456", "confidence": 1.0},
    "damage_description": {
      "value": "Passenger side door and fender, significant denting and scratches",
      "confidence": 0.95
    }
  },
  "damages": {
    "estimated_amount": {"value": 4500, "confidence": 1.0},
    "currency": "USD",
    "is_estimate": true
  },
  "parties_involved": [
    {
      "role": "other_driver",
      "name": {"value": "Robert Williams", "confidence": 1.0},
      "contact": {
        "phone": {"value": "+15553456789", "confidence": 1.0}
      },
      "insurance": {
        "company": {"value": "State Farm", "confidence": 1.0},
        "policy_number": {"value": "SF-11223344", "confidence": 1.0}
      },
      "vehicle": {
        "year": {"value": 2020, "confidence": 1.0},
        "make": {"value": "Ford", "confidence": 1.0},
        "model": {"value": "F-150", "confidence": 1.0},
        "color": {"value": "Blue", "confidence": 1.0}
      },
      "fault_admitted": true
    }
  ],
  "witnesses": [],
  "injuries": null,
  "police_report": {
    "report_number": {"value": "PDX-2024-12345", "confidence": 1.0},
    "officer_badge": {"value": "4521", "confidence": 1.0},
    "filed_date": {"value": "2024-01-10", "confidence": 1.0}
  },
  "metadata": {
    "fields_extracted": 28,
    "fields_missing": ["witness_info", "injury_details"],
    "average_confidence": 0.98,
    "flags": []
  }
}
```

### Example 2: Handwritten/Messy Property Claim

**Input:**
```
claim_type: property
document_type: fnol
document_text: |
  [HANDWRITTEN FORM - OCR'd]

  PROPERTY CLAIM FORM

  Name: J0hn Doe [possibly John - handwriting unclear]
  Policy #: PROP-5544####  [last 4 digits illegible]
  Phone: 555 987 6[?]43

  What happened:
  Water damage in basement - pipe burst during cold snap
  came home from work Jan 12 and found 2-3 inches of water
  had to call emergency plumber $450
  Ruined carpet, some furniture, boxes of belongings

  [written in margin]: "maybe mold?? not sure yet"

  Estimate from contractor: ~$8,000-12,000

  Address: 789 Elm Street
          Chicago IL
          [zip not written]

  Signed: J. Doe
  1/14/24
```

**Output:**
```json
{
  "success": true,
  "extraction_timestamp": "2024-01-15T14:35:00Z",
  "claim_type": "property",
  "document_type": "fnol",
  "claimant": {
    "name": {
      "value": {
        "first": "John",
        "last": "Doe"
      },
      "confidence": 0.75,
      "source_type": "handwritten",
      "notes": "First name OCR uncertain - 'J0hn' may be 'John'"
    },
    "contact": {
      "phone": {
        "value": "555-987-6?43",
        "confidence": 0.6,
        "source_type": "handwritten",
        "notes": "One digit illegible"
      },
      "address": {
        "value": {
          "street": "789 Elm Street",
          "city": "Chicago",
          "state": "IL",
          "postal": null,
          "country": "US"
        },
        "confidence": 0.8,
        "notes": "ZIP code not provided"
      }
    },
    "relationship_to_insured": "self"
  },
  "policy": {
    "number": {
      "value": "PROP-5544XXXX",
      "confidence": 0.5,
      "notes": "Last 4 digits illegible",
      "partial": true
    }
  },
  "incident": {
    "date": {
      "value": "2024-01-12",
      "confidence": 0.9,
      "notes": "Year inferred from claim date"
    },
    "time": null,
    "location": {
      "value": {
        "description": "Basement",
        "property_address": "789 Elm Street, Chicago, IL"
      },
      "confidence": 0.85
    },
    "description": {
      "value": "Water damage in basement - pipe burst during cold snap. Came home from work and found 2-3 inches of water. Called emergency plumber ($450). Ruined carpet, some furniture, boxes of belongings.",
      "confidence": 0.9
    },
    "incident_type": "water_damage"
  },
  "damages": {
    "estimated_amount": {
      "value": {
        "low": 8000,
        "high": 12000
      },
      "confidence": 0.75,
      "notes": "Range provided: $8,000-12,000"
    },
    "currency": "USD",
    "is_estimate": true,
    "damage_description": {
      "value": "Carpet, furniture, and belongings damaged by water",
      "confidence": 0.85
    },
    "emergency_expenses": {
      "plumber": {"value": 450, "confidence": 0.95}
    }
  },
  "additional_concerns": [
    {
      "concern": "Potential mold",
      "confidence": 0.7,
      "source": "Margin note: 'maybe mold?? not sure yet'"
    }
  ],
  "metadata": {
    "fields_extracted": 12,
    "fields_missing": ["policy_number_complete", "phone_complete", "postal_code", "incident_time"],
    "average_confidence": 0.76,
    "flags": [
      "handwritten_notes_detected",
      "incomplete_contact_info",
      "partial_policy_number",
      "potential_secondary_damage_mold"
    ]
  }
}
```

### Example 3: Edge Case - Insufficient Information

**Input:**
```
claim_type: auto
document_type: correspondence
document_text: |
  From: angry.customer@email.com
  To: claims@insurance.com
  Subject: RE: My accident claim

  Hi,

  I already submitted my claim last week. Why hasn't anyone called me back?
  This is ridiculous. I need my car fixed.

  - Mike
```

**Output:**
```json
{
  "success": false,
  "extraction_timestamp": "2024-01-15T14:40:00Z",
  "claim_type": "auto",
  "document_type": "correspondence",
  "error": {
    "code": "INSUFFICIENT_CLAIM_DATA",
    "message": "Document is correspondence without claim details. Cannot extract standard claim fields.",
    "extractable_fields": ["claimant_email", "claimant_first_name"],
    "suggestion": "This appears to be a follow-up email. Retrieve original claim submission for extraction."
  },
  "claimant": {
    "name": {
      "value": {
        "first": "Mike"
      },
      "confidence": 0.7,
      "notes": "Only first name available from signature"
    },
    "contact": {
      "email": {
        "value": "angry.customer@email.com",
        "confidence": 1.0
      }
    }
  },
  "claim_status_indicators": {
    "previously_submitted": true,
    "customer_sentiment": "frustrated",
    "urgency": "high",
    "follow_up_requested": true
  },
  "metadata": {
    "fields_extracted": 2,
    "fields_missing": ["policy_number", "incident_date", "incident_location", "damages", "vehicle_info"],
    "average_confidence": 0.85,
    "flags": [
      "insufficient_claim_data",
      "follow_up_correspondence",
      "frustrated_claimant"
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Policy number formats**: Different insurers use different formats. Don't over-validate.
2. **Date ambiguity**: "1/2/24" - Jan 2 or Feb 1? Check for locale hints, use context.
3. **Amount confusion**: "$5000" deductible vs "$5000" claim amount. Context matters.
4. **Name variations**: "Bob" on one page, "Robert" on another. Same person.

### Edge Cases to Handle
- **Third-party claims**: Claimant may not be policyholder
- **Multi-vehicle accidents**: Multiple other parties, multiple vehicles
- **Claim amendments**: Updates to original claim - merge, don't replace
- **Subrogation notes**: Other insurance references for recovery
- **Reservation of rights**: Legal language about coverage questions

### Fraud Indicators to Flag
- Date of incident after date of claim
- Excessive damage for described incident
- Multiple claims in short period
- Inconsistent contact information
- Delayed reporting without explanation
- Prior claim references that don't match records

### When NOT to Use This Prompt
- **Litigation documents**: Need legal review, not automation
- **Medical records**: HIPAA considerations, specialized extraction
- **Heavily redacted documents**: Insufficient information
- **Non-English documents**: Use translated version or language-specific prompt

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex/messy claims | Best accuracy on handwritten, partial info |
| **Best:** GPT-4o | Multi-page claims | Strong context maintenance |
| **Acceptable:** Claude Sonnet 4 | Standard typed claims | Good balance |
| **Acceptable:** GPT-4o-mini | High-volume processing | Cost-effective for clean forms |
| **Not Recommended:** Smaller models | - | Miss nuances, fraud indicators |

## Integration Notes

### Validation Rules
```python
def validate_auto_claim(extracted):
    errors = []
    warnings = []

    # Required fields for auto claims
    required = ['claimant.name', 'policy.number', 'incident.date', 'vehicle']
    for field in required:
        if not get_nested(extracted, field):
            errors.append(f"Missing required field: {field}")

    # VIN validation
    if vin := get_nested(extracted, 'vehicle.vin.value'):
        if len(vin) != 17:
            warnings.append(f"VIN length incorrect: {len(vin)} chars (expected 17)")

    # Date logic
    incident_date = get_nested(extracted, 'incident.date.value')
    claim_date = get_nested(extracted, 'extraction_timestamp')
    if incident_date and claim_date:
        if parse_date(incident_date) > parse_date(claim_date):
            errors.append("Incident date is after claim date - possible fraud indicator")

    # Confidence thresholds
    avg_confidence = extracted.get('metadata', {}).get('average_confidence', 0)
    if avg_confidence < 0.7:
        warnings.append("Low overall confidence - recommend manual review")

    return errors, warnings
```

### Workflow Integration
```python
def process_claim_document(document):
    # Step 1: Extract
    extracted = extract_claim_data(document)

    # Step 2: Validate
    errors, warnings = validate_claim(extracted)

    # Step 3: Route
    if errors:
        return route_to_manual_review(extracted, errors)

    if 'fraud_indicators' in extracted.get('metadata', {}).get('flags', []):
        return route_to_siu(extracted)  # Special Investigations Unit

    if extracted['metadata']['average_confidence'] < 0.8:
        return route_to_quality_check(extracted)

    return route_to_adjuster_queue(extracted)
```
