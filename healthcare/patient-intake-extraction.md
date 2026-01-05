# Patient Intake Form Extraction

## Use Case

Extract structured patient information from intake forms and questionnaires:
- New patient registration processing
- Pre-visit questionnaire digitization
- Health history form extraction
- Insurance information capture
- Consent form processing

Use when onboarding patients or processing paper/PDF intake forms into EHR-compatible structured data.

## Input Format

**Required:**
- `intake_form`: Patient intake form content (text, OCR output, or form fields)

**Optional:**
- `form_type`: registration, health_history, insurance, consent
- `practice_type`: primary_care, specialty, dental, mental_health
- `required_fields`: List of fields that must be extracted

## Output Format

```json
{
  "extraction_metadata": {
    "form_type": "registration",
    "extraction_date": "2024-01-15",
    "completeness": 0.92
  },
  "patient_demographics": {
    "legal_name": {
      "first": "First",
      "middle": "Middle",
      "last": "Last",
      "suffix": "Jr/Sr/etc"
    },
    "preferred_name": "Nickname",
    "date_of_birth": "YYYY-MM-DD",
    "age": 45,
    "sex_assigned_at_birth": "male|female",
    "gender_identity": "Response if collected",
    "pronouns": "Response if collected",
    "ssn_last_four": "1234",
    "marital_status": "single|married|divorced|widowed",
    "race": ["Response(s)"],
    "ethnicity": "Response",
    "preferred_language": "English",
    "interpreter_needed": false
  },
  "contact_information": {
    "address": {
      "street1": "123 Main St",
      "street2": "Apt 4B",
      "city": "City",
      "state": "ST",
      "zip": "12345",
      "country": "USA"
    },
    "phone": {
      "home": "555-123-4567",
      "mobile": "555-987-6543",
      "work": "555-456-7890",
      "preferred": "mobile"
    },
    "email": "email@example.com",
    "preferred_contact_method": "phone|email|text",
    "ok_to_leave_message": true
  },
  "emergency_contact": {
    "name": "Contact Name",
    "relationship": "Spouse",
    "phone": "555-111-2222",
    "alternate_phone": "555-333-4444"
  },
  "insurance_information": {
    "primary": {
      "company": "Insurance Co",
      "plan_name": "Plan Name",
      "member_id": "ABC123456",
      "group_number": "GRP001",
      "subscriber_name": "Subscriber Name",
      "subscriber_dob": "YYYY-MM-DD",
      "relationship_to_subscriber": "self|spouse|child",
      "effective_date": "YYYY-MM-DD"
    },
    "secondary": null,
    "pharmacy_benefit": {
      "pbm": "Pharmacy Benefit Manager",
      "rx_bin": "123456",
      "rx_pcn": "ABC",
      "rx_group": "GRP"
    }
  },
  "primary_care_provider": {
    "name": "Dr. Provider Name",
    "practice": "Practice Name",
    "phone": "555-PCP-PHON",
    "fax": "555-PCP-FAX"
  },
  "pharmacy": {
    "name": "Pharmacy Name",
    "address": "Pharmacy Address",
    "phone": "555-RX-PHONE"
  },
  "medical_history": {
    "current_conditions": [
      {
        "condition": "Hypertension",
        "diagnosed_year": 2019,
        "current_treatment": "Medication"
      }
    ],
    "past_conditions": [
      {
        "condition": "Appendectomy",
        "year": 2010
      }
    ],
    "surgical_history": [
      {
        "procedure": "Procedure Name",
        "year": 2010,
        "facility": "Hospital Name"
      }
    ],
    "hospitalizations": [],
    "family_history": [
      {
        "condition": "Diabetes",
        "relation": "Mother",
        "age_of_onset": 55
      }
    ]
  },
  "medications": {
    "current": [
      {
        "name": "Medication Name",
        "dose": "10mg",
        "frequency": "Once daily",
        "prescriber": "Dr. Name"
      }
    ],
    "supplements": ["Vitamin D", "Fish Oil"]
  },
  "allergies": {
    "medications": [
      {
        "allergen": "Penicillin",
        "reaction": "Rash"
      }
    ],
    "food": [],
    "environmental": [],
    "no_known_allergies": false
  },
  "social_history": {
    "tobacco": {
      "status": "never|former|current",
      "type": "cigarettes|vape|chew",
      "amount": "1 pack per day",
      "years": 10,
      "quit_date": "YYYY-MM-DD"
    },
    "alcohol": {
      "status": "none|occasional|moderate|heavy",
      "drinks_per_week": 3
    },
    "substances": {
      "status": "none|past|current",
      "details": null
    },
    "occupation": "Job Title",
    "exercise": "3 times per week"
  },
  "health_screening": {
    "last_physical": "YYYY-MM-DD",
    "last_dental": "YYYY-MM-DD",
    "last_eye_exam": "YYYY-MM-DD",
    "immunizations_up_to_date": true,
    "screening_tests": [
      {
        "test": "Colonoscopy",
        "date": "YYYY-MM-DD",
        "result": "Normal"
      }
    ]
  },
  "consent_and_acknowledgments": {
    "hipaa_notice_received": true,
    "financial_policy_accepted": true,
    "consent_to_treat": true,
    "authorization_to_release": true,
    "signature_date": "YYYY-MM-DD"
  },
  "extraction_quality": {
    "overall_confidence": 0.88,
    "fields_extracted": 45,
    "fields_missing": ["pharmacy_fax", "secondary_insurance"],
    "fields_unclear": [
      {
        "field": "medication_dose",
        "issue": "Handwriting unclear",
        "extracted_value": "10mg or 100mg"
      }
    ],
    "validation_warnings": [
      "Phone number format may need verification"
    ]
  }
}
```

## The Prompt

```
You are a medical records specialist extracting patient information from intake forms. Accurately capture all provided information while flagging unclear or missing data.

INTAKE FORM:
{{intake_form}}

FORM TYPE: {{form_type | default: "registration"}}
PRACTICE TYPE: {{practice_type | default: "primary_care"}}

{{#if required_fields}}
REQUIRED FIELDS:
{{required_fields}}
{{/if}}

EXTRACTION FRAMEWORK:

1. DEMOGRAPHIC INFORMATION
   Extract:
   - Full legal name (first, middle, last, suffix)
   - Preferred name/nickname if different
   - Date of birth (convert to YYYY-MM-DD)
   - Sex assigned at birth
   - Gender identity (if collected)
   - Pronouns (if collected)
   - SSN (extract last 4 only for security)
   - Marital status
   - Race/ethnicity
   - Preferred language
   - Interpreter needs

2. CONTACT INFORMATION
   Extract:
   - Full address (street, city, state, zip)
   - All phone numbers with type (home/mobile/work)
   - Preferred contact method
   - Email address
   - Permission to leave messages
   - Best time to contact

3. EMERGENCY CONTACT
   Extract:
   - Name
   - Relationship
   - Phone number(s)

4. INSURANCE INFORMATION
   Primary insurance:
   - Company name
   - Plan/product name
   - Member/subscriber ID
   - Group number
   - Subscriber information if not self
   - Policy effective date

   Secondary insurance if applicable

   Pharmacy benefits:
   - RX BIN, PCN, Group if listed
   - PBM name

5. MEDICAL HISTORY
   Current conditions:
   - Active diagnoses
   - Year diagnosed
   - Current treatment

   Past medical history:
   - Resolved conditions
   - Surgeries with year and facility
   - Hospitalizations

   Family history:
   - Conditions
   - Affected relatives
   - Age of onset if noted

6. MEDICATIONS
   For each medication:
   - Drug name
   - Dose/strength
   - Frequency
   - Prescribing provider
   - Reason for taking

   Also capture:
   - OTC medications
   - Supplements/vitamins

7. ALLERGIES
   For each allergy:
   - Allergen (medication/food/environmental)
   - Reaction type
   - Severity if noted

   Flag if "NKDA" or "No Known Allergies" indicated

8. SOCIAL HISTORY
   Tobacco:
   - Status (never/former/current)
   - Type, amount, duration
   - Quit date if former

   Alcohol:
   - Status and frequency
   - Type and amount

   Substances:
   - Status and details

   Other:
   - Occupation
   - Exercise habits
   - Living situation

9. REFERRAL/PCP INFORMATION
   - Primary care provider
   - Referring provider
   - Pharmacy preference

10. CONSENTS AND SIGNATURES
    - HIPAA acknowledgment
    - Financial policy
    - Consent to treat
    - Release authorizations
    - Signature dates

DATA QUALITY RULES:
- Preserve exact values where possible
- Standardize dates to YYYY-MM-DD
- Standardize phone to XXX-XXX-XXXX
- Flag unclear or illegible entries
- Note when required fields are missing
- Don't infer information not provided
- Mark checkboxes as true/false
- Capture "none" and "N/A" responses

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{intake_form}}` | string | Yes | Patient intake form content |
| `{{form_type}}` | string | No | Type of form being processed |
| `{{practice_type}}` | string | No | Type of medical practice |
| `{{required_fields}}` | string | No | List of required fields |

## Examples

### Example 1: New Patient Registration

**Input:**
```
intake_form: |
  NEW PATIENT REGISTRATION FORM

  Date: 01/15/2024

  PATIENT INFORMATION
  Name: Johnson, Emily Rose
  Preferred Name: Emmy
  Date of Birth: 03/22/1985
  Sex: Female
  Gender Identity: Female
  Pronouns: She/Her
  SSN: XXX-XX-7890
  Marital Status: [X] Married  [ ] Single  [ ] Divorced  [ ] Widowed

  Race: [X] White  [ ] Black  [ ] Asian  [ ] Other: _______
  Ethnicity: [ ] Hispanic  [X] Non-Hispanic
  Preferred Language: English
  Interpreter Needed: [ ] Yes  [X] No

  ADDRESS
  Street: 456 Oak Avenue, Apt 12B
  City: Portland          State: OR          Zip: 97201

  PHONE
  Home: (503) 555-1234
  Cell: (503) 555-9876  [X] Preferred
  Work: (503) 555-4567

  Email: emily.johnson@email.com
  Preferred Contact: [X] Phone  [ ] Email  [ ] Text
  OK to Leave Message: [X] Yes  [ ] No

  EMERGENCY CONTACT
  Name: Michael Johnson (Husband)
  Phone: (503) 555-8765
  Alt Phone: (503) 555-4567

  INSURANCE INFORMATION

  Primary Insurance:
  Company: Blue Cross Blue Shield of Oregon
  Plan: PPO 500
  Member ID: XYZ789456123
  Group #: TECH-2024
  Subscriber Name: Michael Johnson
  Subscriber DOB: 07/15/1982
  Relationship: Spouse

  Secondary Insurance: None

  Pharmacy:
  Name: Walgreens
  Address: 789 Main Street, Portland OR
  Phone: (503) 555-7890

  PRIMARY CARE PHYSICIAN
  Name: Dr. Sarah Chen
  Practice: Portland Family Medicine
  Phone: (503) 555-0000

  MEDICAL HISTORY

  Current Medical Conditions:
  [X] High Blood Pressure - Diagnosed 2020, on medication
  [X] Anxiety - Diagnosed 2018, on medication
  [ ] Diabetes
  [ ] Heart Disease
  [X] Asthma - Childhood, well controlled
  [X] Migraines - Occasional, last one 6 months ago

  Past Surgeries:
  - Appendectomy, 2010, Providence Hospital
  - C-Section, 2019, OHSU

  Family History:
  Mother: High blood pressure (age 50), Diabetes (age 60)
  Father: Heart disease (age 65)
  Siblings: None significant

  CURRENT MEDICATIONS
  1. Lisinopril 10mg - once daily - for blood pressure
  2. Sertraline 50mg - once daily - for anxiety
  3. Albuterol inhaler - as needed - for asthma
  4. Sumatriptan 50mg - as needed - for migraines

  Supplements: Vitamin D 2000 IU, Prenatal vitamin

  ALLERGIES
  [X] Penicillin - Reaction: Hives
  [X] Sulfa drugs - Reaction: Rash
  [ ] No Known Drug Allergies

  Food Allergies: Shellfish (hives)
  Environmental: Seasonal pollen

  SOCIAL HISTORY
  Tobacco Use: [ ] Never  [X] Former  [ ] Current
    If former/current: Cigarettes, 1/2 pack/day for 5 years, quit 2015

  Alcohol Use: [X] Occasional (2-3 drinks per week)
  Recreational Drugs: None

  Occupation: Software Engineer
  Exercise: Yoga 2x/week, Walking daily

  HEALTH MAINTENANCE
  Last Physical Exam: 06/2023
  Last Dental Exam: 09/2023
  Last Eye Exam: 03/2023
  Last Mammogram: 01/2023 - Normal
  Last Pap Smear: 06/2022 - Normal

  ACKNOWLEDGMENTS
  [X] I have received the Notice of Privacy Practices
  [X] I have read and agree to the Financial Policy
  [X] I consent to treatment

  Signature: Emily Johnson    Date: 01/15/2024

form_type: registration
practice_type: primary_care
```

**Output:**
```json
{
  "extraction_metadata": {
    "form_type": "registration",
    "extraction_date": "2024-01-15",
    "completeness": 0.96
  },
  "patient_demographics": {
    "legal_name": {
      "first": "Emily",
      "middle": "Rose",
      "last": "Johnson",
      "suffix": null
    },
    "preferred_name": "Emmy",
    "date_of_birth": "1985-03-22",
    "age": 38,
    "sex_assigned_at_birth": "female",
    "gender_identity": "Female",
    "pronouns": "She/Her",
    "ssn_last_four": "7890",
    "marital_status": "married",
    "race": ["White"],
    "ethnicity": "Non-Hispanic",
    "preferred_language": "English",
    "interpreter_needed": false
  },
  "contact_information": {
    "address": {
      "street1": "456 Oak Avenue",
      "street2": "Apt 12B",
      "city": "Portland",
      "state": "OR",
      "zip": "97201",
      "country": "USA"
    },
    "phone": {
      "home": "503-555-1234",
      "mobile": "503-555-9876",
      "work": "503-555-4567",
      "preferred": "mobile"
    },
    "email": "emily.johnson@email.com",
    "preferred_contact_method": "phone",
    "ok_to_leave_message": true
  },
  "emergency_contact": {
    "name": "Michael Johnson",
    "relationship": "Husband",
    "phone": "503-555-8765",
    "alternate_phone": "503-555-4567"
  },
  "insurance_information": {
    "primary": {
      "company": "Blue Cross Blue Shield of Oregon",
      "plan_name": "PPO 500",
      "member_id": "XYZ789456123",
      "group_number": "TECH-2024",
      "subscriber_name": "Michael Johnson",
      "subscriber_dob": "1982-07-15",
      "relationship_to_subscriber": "spouse",
      "effective_date": null
    },
    "secondary": null,
    "pharmacy_benefit": null
  },
  "primary_care_provider": {
    "name": "Dr. Sarah Chen",
    "practice": "Portland Family Medicine",
    "phone": "503-555-0000",
    "fax": null
  },
  "pharmacy": {
    "name": "Walgreens",
    "address": "789 Main Street, Portland OR",
    "phone": "503-555-7890"
  },
  "medical_history": {
    "current_conditions": [
      {
        "condition": "Hypertension",
        "diagnosed_year": 2020,
        "current_treatment": "Medication (Lisinopril)"
      },
      {
        "condition": "Anxiety",
        "diagnosed_year": 2018,
        "current_treatment": "Medication (Sertraline)"
      },
      {
        "condition": "Asthma",
        "diagnosed_year": null,
        "current_treatment": "Albuterol as needed, well controlled"
      },
      {
        "condition": "Migraines",
        "diagnosed_year": null,
        "current_treatment": "Sumatriptan as needed, occasional"
      }
    ],
    "past_conditions": [],
    "surgical_history": [
      {
        "procedure": "Appendectomy",
        "year": 2010,
        "facility": "Providence Hospital"
      },
      {
        "procedure": "Cesarean Section",
        "year": 2019,
        "facility": "OHSU"
      }
    ],
    "hospitalizations": [],
    "family_history": [
      {
        "condition": "Hypertension",
        "relation": "Mother",
        "age_of_onset": 50
      },
      {
        "condition": "Diabetes",
        "relation": "Mother",
        "age_of_onset": 60
      },
      {
        "condition": "Heart disease",
        "relation": "Father",
        "age_of_onset": 65
      }
    ]
  },
  "medications": {
    "current": [
      {
        "name": "Lisinopril",
        "dose": "10mg",
        "frequency": "Once daily",
        "reason": "Blood pressure"
      },
      {
        "name": "Sertraline",
        "dose": "50mg",
        "frequency": "Once daily",
        "reason": "Anxiety"
      },
      {
        "name": "Albuterol inhaler",
        "dose": null,
        "frequency": "As needed",
        "reason": "Asthma"
      },
      {
        "name": "Sumatriptan",
        "dose": "50mg",
        "frequency": "As needed",
        "reason": "Migraines"
      }
    ],
    "supplements": ["Vitamin D 2000 IU", "Prenatal vitamin"]
  },
  "allergies": {
    "medications": [
      {
        "allergen": "Penicillin",
        "reaction": "Hives"
      },
      {
        "allergen": "Sulfa drugs",
        "reaction": "Rash"
      }
    ],
    "food": [
      {
        "allergen": "Shellfish",
        "reaction": "Hives"
      }
    ],
    "environmental": ["Seasonal pollen"],
    "no_known_allergies": false
  },
  "social_history": {
    "tobacco": {
      "status": "former",
      "type": "cigarettes",
      "amount": "1/2 pack per day",
      "years": 5,
      "quit_date": "2015"
    },
    "alcohol": {
      "status": "occasional",
      "drinks_per_week": 3
    },
    "substances": {
      "status": "none",
      "details": null
    },
    "occupation": "Software Engineer",
    "exercise": "Yoga 2x/week, Walking daily"
  },
  "health_screening": {
    "last_physical": "2023-06",
    "last_dental": "2023-09",
    "last_eye_exam": "2023-03",
    "immunizations_up_to_date": null,
    "screening_tests": [
      {
        "test": "Mammogram",
        "date": "2023-01",
        "result": "Normal"
      },
      {
        "test": "Pap Smear",
        "date": "2022-06",
        "result": "Normal"
      }
    ]
  },
  "consent_and_acknowledgments": {
    "hipaa_notice_received": true,
    "financial_policy_accepted": true,
    "consent_to_treat": true,
    "authorization_to_release": null,
    "signature_date": "2024-01-15"
  },
  "extraction_quality": {
    "overall_confidence": 0.94,
    "fields_extracted": 52,
    "fields_missing": [
      "insurance_effective_date",
      "pharmacy_benefit_info",
      "pcp_fax",
      "immunization_status"
    ],
    "fields_unclear": [],
    "validation_warnings": []
  }
}
```

## Gotchas

### Common Failure Modes
1. **Name parsing**: Watch for prefixes (Dr., Mrs.) vs. name parts
2. **Date formats**: Multiple formats in same form (MM/DD/YYYY, YYYY, etc.)
3. **Checkbox interpretation**: Distinguish checked vs unchecked
4. **Handwriting OCR**: Flag unclear handwritten entries

### Edge Cases to Handle
- **Incomplete forms**: Track which required fields are missing
- **Multi-page forms**: Combine information across pages
- **Corrections/strikethroughs**: Note when values are crossed out
- **Multiple insurance cards**: Primary vs secondary

### When NOT to Use This Prompt
- **Insurance verification**: Need real-time eligibility check
- **Identity verification**: Requires separate ID validation
- **Consent interpretation**: Legal review for complex consents
- **Clinical triage**: Medical assessment requires clinical judgment

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-page forms | Best at handling varied formats |
| **Acceptable:** Claude Sonnet 4 | Standard intake forms | Good for high volume |
| **Acceptable:** GPT-4o | Mixed format forms | Strong structure extraction |
| **Caution:** Smaller models | - | May miss nuanced fields |

## Compliance Notes

- **PHI Handling**: Ensure proper security for extracted patient data
- **Data Validation**: All extracted data should be verified before EHR entry
- **Consent Verification**: Human review required for consent acknowledgments
- **Audit Trail**: Log extraction for compliance purposes
