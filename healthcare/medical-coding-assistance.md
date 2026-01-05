# Medical Coding Assistance

## Use Case

Assist with medical coding tasks for billing and documentation:
- Suggesting appropriate ICD-10-CM diagnosis codes
- Identifying potential CPT/HCPCS procedure codes
- Flagging coding compliance considerations
- Supporting documentation improvement
- Identifying missing or unspecified codes

Use as a coding support tool to assist certified medical coders, not as a replacement for professional coding review.

## Input Format

**Required:**
- `clinical_documentation`: Clinical notes, operative reports, or encounter documentation

**Optional:**
- `encounter_type`: inpatient, outpatient, emergency, office_visit
- `specialty`: Medical specialty context
- `focus`: diagnosis, procedure, or both
- `existing_codes`: Previously assigned codes for review

## Output Format

```json
{
  "coding_analysis": {
    "encounter_type": "outpatient",
    "date_of_service": "2024-01-15",
    "specialty": "cardiology"
  },
  "diagnosis_codes": {
    "principal": {
      "code": "I25.10",
      "description": "Atherosclerotic heart disease of native coronary artery without angina pectoris",
      "confidence": 0.95,
      "documentation_support": "Documented as 'CAD' with positive stress test"
    },
    "secondary": [
      {
        "code": "E11.9",
        "description": "Type 2 diabetes mellitus without complications",
        "confidence": 0.90,
        "documentation_support": "Listed in PMH as 'diabetes type 2'"
      }
    ],
    "additional_considerations": [
      {
        "potential_code": "I10",
        "description": "Essential hypertension",
        "reason": "HTN mentioned but not clearly documented as current diagnosis"
      }
    ]
  },
  "procedure_codes": {
    "primary": {
      "code": "93000",
      "description": "Electrocardiogram, routine ECG with interpretation",
      "confidence": 0.95,
      "documentation_support": "12-lead EKG performed and interpreted"
    },
    "additional": []
  },
  "documentation_gaps": [
    {
      "issue": "Diabetes type not specified",
      "current": "Diabetes mentioned",
      "recommendation": "Clarify Type 1 vs Type 2 for code specificity",
      "impact": "May affect code selection and risk adjustment"
    }
  ],
  "compliance_flags": [
    {
      "type": "query_opportunity",
      "description": "Consider querying for CAD laterality and vessel involvement",
      "rationale": "More specific codes may be available (I25.11x)"
    }
  ],
  "coding_notes": {
    "sequencing_rationale": "Principal diagnosis based on primary reason for encounter",
    "excludes_notes": "Relevant excludes1/excludes2 considerations",
    "combination_codes": "Any relevant combination code opportunities"
  },
  "confidence_summary": {
    "overall": 0.88,
    "limitations": ["Documentation query recommended for specificity"]
  }
}
```

## The Prompt

```
You are a medical coding assistant supporting certified coders. Analyze clinical documentation and suggest appropriate diagnosis and procedure codes with documentation support.

CLINICAL DOCUMENTATION:
{{clinical_documentation}}

ENCOUNTER TYPE: {{encounter_type | default: "outpatient"}}
{{#if specialty}}SPECIALTY: {{specialty}}{{/if}}
CODING FOCUS: {{focus | default: "both"}}

{{#if existing_codes}}
EXISTING CODES FOR REVIEW:
{{existing_codes}}
{{/if}}

CODING ANALYSIS FRAMEWORK:

1. DOCUMENTATION REVIEW
   Read documentation for:
   - Chief complaint / reason for visit
   - History of present illness
   - Physical examination findings
   - Assessment / diagnoses stated
   - Procedures performed
   - Test results
   - Medical decision making level

2. DIAGNOSIS CODE SELECTION (ICD-10-CM)
   For each condition identified:

   a) Code to highest specificity supported by documentation:
      - Anatomical site
      - Laterality (right/left/bilateral)
      - Severity (mild/moderate/severe)
      - Stage/phase
      - Episode (initial/subsequent/sequela)
      - With/without complications

   b) Check for combination codes:
      - Condition + manifestation
      - Condition + complication
      - Condition + associated condition

   c) Follow coding guidelines:
      - Code documented conditions
      - Don't code suspected/ruled out (outpatient)
      - Code confirmed conditions only
      - Apply excludes1/excludes2 rules

   d) Sequencing:
      - Principal/first-listed based on reason for encounter
      - Secondary codes for comorbidities affecting care
      - External cause codes if applicable

3. PROCEDURE CODE SELECTION (CPT/HCPCS)
   For each procedure documented:

   a) Identify components:
      - Procedure performed
      - Approach/technique
      - Extent/level
      - Number/units

   b) Check for bundling:
      - Separate procedure rules
      - Global surgical package
      - Modifier requirements

   c) E/M level if applicable:
      - History
      - Exam
      - Medical decision making
      - Time-based if documented

4. DOCUMENTATION QUALITY ASSESSMENT
   Flag opportunities for:
   - Missing specificity
   - Unsigned/incomplete notes
   - Discrepancies between sections
   - Query opportunities
   - Addendum needs

5. COMPLIANCE CONSIDERATIONS
   Note:
   - Medical necessity alignment
   - LCD/NCD considerations
   - Frequency limits
   - Modifier requirements
   - Bundling edits

CRITICAL RULES:
- Only suggest codes supported by documentation
- Do not code based on inference
- Flag when documentation is insufficient
- Note confidence level for each code
- Identify query opportunities
- This is DECISION SUPPORT, not final coding

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{clinical_documentation}}` | string | Yes | Clinical notes or reports |
| `{{encounter_type}}` | string | No | Type of encounter |
| `{{specialty}}` | string | No | Medical specialty |
| `{{focus}}` | string | No | diagnosis, procedure, or both |
| `{{existing_codes}}` | string | No | Codes to review |

## Examples

### Example 1: Outpatient Office Visit

**Input:**
```
clinical_documentation: |
  OFFICE VISIT NOTE

  Date: 01/15/2024
  Provider: Dr. James Wilson, MD
  Specialty: Internal Medicine

  PATIENT: 58 y/o female

  CHIEF COMPLAINT: Follow-up diabetes and hypertension

  HPI: Patient returns for routine follow-up of her type 2 diabetes and
  hypertension. Reports good compliance with medications. Home glucose
  readings range 120-180 fasting. No hypoglycemic episodes. Denies chest
  pain, shortness of breath, visual changes, or foot numbness.

  MEDICATIONS:
  1. Metformin 1000mg BID
  2. Lisinopril 20mg daily
  3. Atorvastatin 40mg daily

  REVIEW OF SYSTEMS:
  Constitutional: No fever, fatigue, or weight change
  CV: No chest pain or palpitations
  Respiratory: No dyspnea or cough
  Neuro: No numbness, tingling, or weakness

  PHYSICAL EXAM:
  Vitals: BP 138/84, HR 72, Wt 185 lbs, BMI 31.2
  General: Well-appearing, no acute distress
  CV: RRR, no murmurs
  Lungs: Clear
  Extremities: No edema, pulses intact, monofilament exam normal bilaterally

  LABS (today):
  HbA1c: 7.4% (previous 7.8%)
  Fasting glucose: 142
  Creatinine: 0.9, eGFR >60
  Lipid panel: TC 195, LDL 98, HDL 52, TG 148

  ASSESSMENT & PLAN:
  1. Type 2 diabetes mellitus - improved control, HbA1c 7.4%
     - Continue metformin
     - Recheck HbA1c in 3 months
     - Annual eye exam ordered

  2. Essential hypertension - slightly above goal today
     - Continue lisinopril
     - Recheck BP in 1 month, may increase if not at goal

  3. Hyperlipidemia - at LDL goal
     - Continue statin

  4. Obesity
     - Discussed diet and exercise
     - Referral to nutritionist offered

  Follow up: 3 months

  Total face-to-face time: 25 minutes, majority spent counseling on
  diabetes management and lifestyle modifications.

encounter_type: office_visit
specialty: internal_medicine
focus: both
```

**Output:**
```json
{
  "coding_analysis": {
    "encounter_type": "office_visit",
    "date_of_service": "2024-01-15",
    "specialty": "internal_medicine"
  },
  "diagnosis_codes": {
    "principal": {
      "code": "E11.65",
      "description": "Type 2 diabetes mellitus with hyperglycemia",
      "confidence": 0.92,
      "documentation_support": "Type 2 diabetes documented with elevated fasting glucose (142) and HbA1c 7.4%; hyperglycemia supports .65 specificity"
    },
    "secondary": [
      {
        "code": "I10",
        "description": "Essential (primary) hypertension",
        "confidence": 0.95,
        "documentation_support": "Essential hypertension documented in assessment, BP 138/84 noted"
      },
      {
        "code": "E78.5",
        "description": "Hyperlipidemia, unspecified",
        "confidence": 0.88,
        "documentation_support": "Hyperlipidemia documented in assessment, on statin therapy"
      },
      {
        "code": "E66.9",
        "description": "Obesity, unspecified",
        "confidence": 0.90,
        "documentation_support": "Obesity documented in assessment, BMI 31.2 supports diagnosis"
      },
      {
        "code": "Z68.31",
        "description": "BMI 31.0-31.9, adult",
        "confidence": 0.95,
        "documentation_support": "BMI 31.2 documented in vitals"
      }
    ],
    "additional_considerations": [
      {
        "potential_code": "E78.00",
        "description": "Pure hypercholesterolemia, unspecified",
        "reason": "Could use more specific code if documentation clarified type of hyperlipidemia"
      },
      {
        "potential_code": "E11.9",
        "description": "Type 2 diabetes without complications",
        "reason": "Alternative if hyperglycemia code deemed too specific; however glucose 142 supports hyperglycemia"
      }
    ]
  },
  "procedure_codes": {
    "primary": {
      "code": "99214",
      "description": "Office visit, established patient, moderate complexity",
      "confidence": 0.85,
      "documentation_support": "25-minute visit with counseling; moderate complexity MDM with multiple chronic conditions, prescription drug management"
    },
    "additional": [
      {
        "code": "83036",
        "description": "Hemoglobin A1c",
        "confidence": 0.95,
        "documentation_support": "HbA1c 7.4% documented as performed today"
      },
      {
        "code": "82947",
        "description": "Glucose, quantitative, blood",
        "confidence": 0.95,
        "documentation_support": "Fasting glucose 142 documented"
      },
      {
        "code": "80061",
        "description": "Lipid panel",
        "confidence": 0.95,
        "documentation_support": "Complete lipid panel results documented"
      },
      {
        "code": "82565",
        "description": "Creatinine",
        "confidence": 0.90,
        "documentation_support": "Creatinine 0.9 documented; may be bundled in metabolic panel"
      }
    ],
    "e_and_m_support": {
      "level_rationale": "99214 - Moderate complexity MDM based on: Multiple chronic conditions (diabetes, HTN, hyperlipidemia, obesity) requiring prescription management; data reviewed includes labs; 25-minute time documented with majority counseling also supports this level",
      "time_based_option": "If coding on time: 99214 covers 30-39 minutes; documented 25 minutes would support 99213 by time alone",
      "recommended_code": "99214"
    }
  },
  "documentation_gaps": [
    {
      "issue": "Hyperlipidemia type not specified",
      "current": "Hyperlipidemia, unspecified (E78.5)",
      "recommendation": "Document specific type: pure hypercholesterolemia, hypertriglyceridemia, or mixed",
      "impact": "More specific coding available (E78.0x, E78.1, E78.2)"
    },
    {
      "issue": "Obesity type not specified",
      "current": "Obesity, unspecified (E66.9)",
      "recommendation": "Document if due to excess calories (E66.01) or specify type",
      "impact": "Minor - E66.9 acceptable for BMI-confirmed obesity"
    }
  ],
  "compliance_flags": [
    {
      "type": "bundling_consideration",
      "description": "Lab codes may need review for bundling if comprehensive metabolic panel ordered",
      "rationale": "Creatinine may be included in CMP (80053) rather than billed separately"
    },
    {
      "type": "documentation_strength",
      "description": "Time documented supports E/M level selected",
      "rationale": "25 minutes with majority counseling documented; good audit protection"
    }
  ],
  "coding_notes": {
    "sequencing_rationale": "Type 2 DM as principal - primary reason for visit (follow-up diabetes and hypertension), with DM addressed first in assessment",
    "excludes_notes": "E11.65 (DM with hyperglycemia) does not exclude hypertension codes",
    "combination_codes": "E11.65 is appropriate combination code for DM with hyperglycemia; no E11.6x with kidney/eye/neuro complications documented"
  },
  "confidence_summary": {
    "overall": 0.90,
    "limitations": [
      "E/M level based on MDM assessment - verify with coding guidelines",
      "Lab bundling rules should be verified per payer"
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **Overcoding**: Suggesting codes not supported by documentation
2. **Specificity errors**: Defaulting to unspecified when specifics are documented
3. **Sequencing errors**: Incorrect principal diagnosis selection
4. **Bundling misses**: Not identifying code bundling issues

### Edge Cases to Handle
- **Incomplete documentation**: Flag and recommend queries
- **Conflicting information**: Note discrepancies in assessment
- **Rule-out diagnoses**: Different handling for inpatient vs outpatient
- **Historical vs current**: Distinguish past medical history from current problems

### When NOT to Use This Prompt
- **Final code assignment**: Requires certified coder review
- **Audit defense**: Documentation must support codes independently
- **Compliance decisions**: Need human review for complex cases
- **Automated billing**: Not for unreviewed automated coding

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex multi-diagnosis cases | Best medical knowledge and reasoning |
| **Acceptable:** Claude Sonnet 4 | Routine coding assistance | Good for standard encounters |
| **Acceptable:** GPT-4o | Procedure coding | Strong technical detail |
| **Caution:** Smaller models | - | May miss specificity requirements |

## Compliance Notes

- **Not a replacement for certified coders**: This is a decision support tool
- **Documentation must support codes**: Always verify documentation supports suggested codes
- **Payer-specific rules**: May vary from general coding guidelines
- **Regular updates needed**: ICD-10 and CPT codes update annually
