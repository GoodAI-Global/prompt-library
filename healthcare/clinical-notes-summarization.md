# Clinical Notes Summarization

## Use Case

Summarize clinical notes and medical documentation for:
- Physician handoff summaries
- Care team coordination
- Patient chart reviews
- Discharge summary generation
- Specialist referral preparation

Use when clinical staff need concise, accurate summaries of patient encounters, histories, or treatment plans.

## Input Format

**Required:**
- `clinical_notes`: Raw clinical notes, progress notes, or encounter documentation

**Optional:**
- `patient_context`: Demographics, chief complaint, relevant history
- `summary_type`: Type of summary needed (handoff, discharge, referral, chart_review)
- `focus_areas`: Specific aspects to emphasize (medications, procedures, diagnoses)
- `recipient`: Who will receive the summary (specialist, PCP, patient)

## Output Format

```json
{
  "summary": {
    "type": "handoff",
    "generated_at": "2024-01-15T10:30:00Z",
    "patient_identifier": "MRN or encounter ID"
  },
  "clinical_summary": {
    "chief_complaint": "Primary reason for encounter",
    "history_of_present_illness": "Concise HPI summary",
    "assessment": "Clinical assessment and diagnoses",
    "plan": "Treatment plan summary"
  },
  "key_findings": [
    {
      "category": "vital_signs|labs|imaging|exam",
      "finding": "Description",
      "clinical_significance": "Why it matters"
    }
  ],
  "active_problems": [
    {
      "problem": "Diagnosis or condition",
      "status": "active|resolved|monitoring",
      "icd10": "Code if available"
    }
  ],
  "medications": {
    "current": ["List of current medications"],
    "changes": ["Any medication changes this encounter"],
    "allergies": ["Known allergies"]
  },
  "action_items": [
    {
      "action": "Required follow-up action",
      "responsible": "Who is responsible",
      "timeframe": "When it should happen",
      "priority": "high|medium|low"
    }
  ],
  "critical_alerts": [
    "Any critical findings requiring immediate attention"
  ],
  "follow_up": {
    "appointments": ["Scheduled follow-ups"],
    "pending_results": ["Outstanding tests/results"],
    "instructions": "Patient instructions summary"
  },
  "confidence": {
    "overall": 0.92,
    "notes": "Any limitations or uncertainties"
  }
}
```

## The Prompt

```
You are a clinical documentation specialist summarizing medical notes. Generate accurate, concise summaries while preserving critical clinical information.

CLINICAL NOTES:
{{clinical_notes}}

{{#if patient_context}}
PATIENT CONTEXT:
{{patient_context}}
{{/if}}

SUMMARY TYPE: {{summary_type | default: "chart_review"}}

{{#if focus_areas}}
FOCUS AREAS: {{focus_areas}}
{{/if}}

{{#if recipient}}
RECIPIENT: {{recipient}}
{{/if}}

SUMMARIZATION FRAMEWORK:

1. INFORMATION EXTRACTION
   Identify and extract:
   - Chief complaint and HPI
   - Review of systems findings
   - Physical exam findings
   - Vital signs (with abnormals flagged)
   - Laboratory results (with abnormals flagged)
   - Imaging results
   - Assessment/diagnoses
   - Treatment plan
   - Medications (current, new, discontinued)
   - Allergies
   - Follow-up instructions

2. CLINICAL PRIORITIZATION
   Order information by clinical importance:
   - Critical/urgent findings first
   - Active problems before resolved
   - Recent changes before stable findings
   - Actionable items prominently

3. SUMMARY TYPE ADAPTATION

   Handoff Summary:
   - Focus on active issues and pending actions
   - Highlight overnight/shift concerns
   - Emphasize "if-then" contingencies
   - Include code status and advance directives

   Discharge Summary:
   - Hospital course overview
   - Discharge diagnoses with ICD-10
   - Medication reconciliation
   - Follow-up appointments
   - Return precautions

   Referral Summary:
   - Reason for referral
   - Relevant history
   - Current treatments
   - Specific questions for specialist

   Chart Review:
   - Comprehensive but concise
   - Problem-oriented organization
   - Trend information where relevant

4. CLINICAL ACCURACY RULES
   - Never invent information not in the notes
   - Flag uncertain or ambiguous findings
   - Preserve exact values for vitals, labs, doses
   - Use standard medical terminology
   - Include relevant negatives (pertinent negatives)
   - Note information gaps

5. MEDICATION HANDLING
   - Include dose, route, frequency
   - Flag high-risk medications
   - Note allergies prominently
   - Highlight any changes from prior

6. ALERT GENERATION
   Critical alerts for:
   - Abnormal vital signs
   - Critical lab values
   - New concerning diagnoses
   - Medication safety issues
   - Pending urgent actions

QUALITY REQUIREMENTS:
- Accurate representation of source notes
- No clinical information fabrication
- Appropriate medical terminology
- Actionable and clear
- Confidence scoring for extracted elements

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{clinical_notes}}` | string | Yes | Raw clinical documentation |
| `{{patient_context}}` | string | No | Demographics and history |
| `{{summary_type}}` | string | No | handoff, discharge, referral, chart_review |
| `{{focus_areas}}` | string | No | Specific areas to emphasize |
| `{{recipient}}` | string | No | Intended audience for summary |

## Examples

### Example 1: ED Handoff Summary

**Input:**
```
clinical_notes: |
  ED PROGRESS NOTE
  Date: 01/15/2024 14:30

  CC: Chest pain

  HPI: 62 y/o male with hx of HTN, HLD, DM2, former smoker (quit 5 years ago)
  presents with substernal chest pain x 2 hours. Pain started at rest, 7/10,
  radiating to left arm, associated with diaphoresis and mild SOB. Took
  aspirin 325mg at home before arrival. No prior cardiac history. Last
  stress test 3 years ago was normal.

  ROS: Positive for chest pain, SOB, diaphoresis. Denies N/V, syncope,
  palpitations, leg swelling.

  PMH: HTN, HLD, DM2, BPH
  PSH: Appendectomy 1995
  Meds: Lisinopril 20mg daily, Atorvastatin 40mg daily, Metformin 1000mg BID,
        Tamsulosin 0.4mg daily
  Allergies: PCN (rash)
  Social: Former smoker 20 pack-years, quit 5 years ago. Rare alcohol. Retired.

  VITALS:
  BP: 158/92 (elevated)
  HR: 88 regular
  RR: 18
  SpO2: 97% RA
  Temp: 98.4F

  PHYSICAL EXAM:
  General: Alert, anxious, mild distress
  CV: Regular rhythm, no murmurs, no JVD
  Lungs: Clear bilaterally
  Abdomen: Soft, non-tender
  Extremities: No edema, pulses 2+ bilaterally

  EKG: ST depressions V3-V5, T wave inversions in leads II, III, aVF

  LABS:
  Troponin I: 0.08 (elevated, normal <0.04)
  BMP: Na 138, K 4.2, Cr 1.1, Glucose 186
  CBC: WBC 9.2, Hgb 14.1, Plt 245

  CXR: No acute findings

  ASSESSMENT:
  1. NSTEMI - elevated troponin with EKG changes
  2. Hypertension, uncontrolled
  3. Type 2 diabetes

  PLAN:
  - Admit to CCU
  - Heparin drip started
  - ASA 325, Plavix 600mg loading
  - Cardiology consult for cath in AM
  - Continue home meds except hold metformin
  - NPO after midnight for cath
  - Serial troponins q6h
  - Telemetry monitoring

summary_type: handoff
recipient: night_shift_physician
```

**Output:**
```json
{
  "summary": {
    "type": "handoff",
    "generated_at": "2024-01-15T14:45:00Z",
    "patient_identifier": "62M ED to CCU"
  },
  "clinical_summary": {
    "chief_complaint": "Chest pain x 2 hours",
    "history_of_present_illness": "62 y/o male with HTN, HLD, DM2, former smoker presenting with substernal chest pain at rest, 7/10 severity, radiating to left arm with diaphoresis and SOB. Took ASA 325mg prior to arrival.",
    "assessment": "NSTEMI with elevated troponin (0.08) and ischemic EKG changes (ST depressions V3-V5, TWI II, III, aVF)",
    "plan": "CCU admission, anticoagulation with heparin, dual antiplatelet therapy initiated, cardiology consulted for cath in AM"
  },
  "key_findings": [
    {
      "category": "labs",
      "finding": "Troponin I elevated at 0.08 (normal <0.04)",
      "clinical_significance": "Confirms myocardial injury, diagnostic for NSTEMI"
    },
    {
      "category": "diagnostic",
      "finding": "EKG with ST depressions V3-V5, T wave inversions II, III, aVF",
      "clinical_significance": "Ischemic changes consistent with ACS"
    },
    {
      "category": "vital_signs",
      "finding": "BP 158/92, otherwise stable",
      "clinical_significance": "Hypertensive, may need additional BP management"
    }
  ],
  "active_problems": [
    {
      "problem": "NSTEMI",
      "status": "active",
      "icd10": "I21.4"
    },
    {
      "problem": "Hypertension, uncontrolled",
      "status": "active",
      "icd10": "I10"
    },
    {
      "problem": "Type 2 diabetes mellitus",
      "status": "active",
      "icd10": "E11.9"
    }
  ],
  "medications": {
    "current": [
      "Heparin drip (new)",
      "Aspirin 325mg",
      "Plavix 600mg load then 75mg daily",
      "Lisinopril 20mg daily",
      "Atorvastatin 40mg daily",
      "Tamsulosin 0.4mg daily"
    ],
    "changes": [
      "HOLD Metformin (pre-cath contrast)",
      "NEW Heparin drip",
      "NEW Plavix"
    ],
    "allergies": ["PCN (rash)"]
  },
  "action_items": [
    {
      "action": "Serial troponin I q6h",
      "responsible": "Night team",
      "timeframe": "Next due ~20:30",
      "priority": "high"
    },
    {
      "action": "Maintain NPO for cardiac cath",
      "responsible": "Nursing",
      "timeframe": "After midnight",
      "priority": "high"
    },
    {
      "action": "Cardiology cath scheduled",
      "responsible": "Cardiology",
      "timeframe": "AM",
      "priority": "high"
    },
    {
      "action": "Monitor for chest pain recurrence",
      "responsible": "Night team",
      "timeframe": "Ongoing",
      "priority": "high"
    }
  ],
  "critical_alerts": [
    "NSTEMI - on heparin drip, watch for bleeding",
    "PCN ALLERGY - avoid penicillins",
    "If chest pain recurs or hemodynamic instability - call cardiology STAT for emergent cath"
  ],
  "follow_up": {
    "appointments": ["Cardiac cath AM"],
    "pending_results": ["Serial troponins q6h", "Repeat EKG if symptoms change"],
    "instructions": "Telemetry monitoring, bed rest, call for chest pain"
  },
  "confidence": {
    "overall": 0.95,
    "notes": "Complete clinical picture available; all critical data points documented"
  }
}
```

### Example 2: Discharge Summary

**Input:**
```
clinical_notes: |
  DISCHARGE SUMMARY

  Admission Date: 01/10/2024
  Discharge Date: 01/15/2024

  Patient: 78 y/o female

  ADMISSION DIAGNOSIS: Community-acquired pneumonia

  DISCHARGE DIAGNOSES:
  1. Community-acquired pneumonia, resolved
  2. Acute on chronic kidney disease, stage 3
  3. Atrial fibrillation, rate controlled
  4. Type 2 diabetes mellitus
  5. Hypertension

  HOSPITAL COURSE:
  Patient admitted with 3-day history of productive cough, fever, and dyspnea.
  CXR showed right lower lobe infiltrate. Started on ceftriaxone and
  azithromycin. Blood cultures negative. Procalcitonin elevated at 2.1.

  Day 2: Fever resolved. Creatinine bumped from baseline 1.4 to 1.9, likely
  prerenal from poor PO intake. IV fluids given with improvement to 1.6.

  Day 3-4: Continued improvement. Transitioned to oral levofloxacin.
  Ambulating well, O2 sats stable on room air.

  Day 5: Afebrile x48h, eating well, ambulating independently. Safe for
  discharge with oral antibiotics.

  MEDICATIONS AT DISCHARGE:
  1. Levofloxacin 750mg daily x 5 more days
  2. Metoprolol succinate 50mg daily
  3. Lisinopril 10mg daily (reduced from 20mg due to AKI)
  4. Eliquis 5mg BID
  5. Metformin 500mg BID (reduced from 1000mg due to AKI)
  6. Amlodipine 5mg daily

  FOLLOW-UP:
  - PCP Dr. Johnson in 1 week
  - Repeat BMP in 1 week (check creatinine)

  DISCHARGE INSTRUCTIONS:
  - Complete full antibiotic course
  - Return for fever >101, worsening cough, SOB, or confusion
  - Follow low sodium diet
  - Check weight daily, call if gain >3 lbs

summary_type: discharge
```

**Output:**
```json
{
  "summary": {
    "type": "discharge",
    "generated_at": "2024-01-15T12:00:00Z",
    "patient_identifier": "78F, 5-day admission"
  },
  "clinical_summary": {
    "chief_complaint": "Productive cough, fever, dyspnea x 3 days",
    "history_of_present_illness": "Community-acquired pneumonia with RLL infiltrate on CXR, complicated by acute on chronic kidney disease (Cr 1.4→1.9→1.6) likely prerenal from dehydration",
    "assessment": "CAP resolved with antibiotics, AKI improving, stable for discharge",
    "plan": "Complete oral levofloxacin course, reduced doses of lisinopril and metformin, close follow-up for renal function"
  },
  "key_findings": [
    {
      "category": "imaging",
      "finding": "CXR: Right lower lobe infiltrate",
      "clinical_significance": "Confirmed pneumonia diagnosis"
    },
    {
      "category": "labs",
      "finding": "Creatinine peaked at 1.9 (baseline 1.4), improved to 1.6",
      "clinical_significance": "AKI resolving but requires monitoring; medications adjusted"
    },
    {
      "category": "labs",
      "finding": "Blood cultures negative, procalcitonin 2.1",
      "clinical_significance": "Bacterial infection, no bacteremia"
    }
  ],
  "active_problems": [
    {
      "problem": "Community-acquired pneumonia",
      "status": "resolving",
      "icd10": "J18.9"
    },
    {
      "problem": "Acute kidney injury on CKD stage 3",
      "status": "improving",
      "icd10": "N17.9"
    },
    {
      "problem": "Atrial fibrillation",
      "status": "stable",
      "icd10": "I48.91"
    },
    {
      "problem": "Type 2 diabetes mellitus",
      "status": "stable",
      "icd10": "E11.9"
    },
    {
      "problem": "Hypertension",
      "status": "stable",
      "icd10": "I10"
    }
  ],
  "medications": {
    "current": [
      "Levofloxacin 750mg daily x 5 days",
      "Metoprolol succinate 50mg daily",
      "Lisinopril 10mg daily (REDUCED)",
      "Eliquis 5mg BID",
      "Metformin 500mg BID (REDUCED)",
      "Amlodipine 5mg daily"
    ],
    "changes": [
      "NEW: Levofloxacin 750mg daily x 5 days",
      "REDUCED: Lisinopril 20mg → 10mg (due to AKI)",
      "REDUCED: Metformin 1000mg → 500mg BID (due to AKI)",
      "STOPPED: Ceftriaxone (inpatient only)",
      "STOPPED: Azithromycin (completed)"
    ],
    "allergies": []
  },
  "action_items": [
    {
      "action": "Complete levofloxacin course (5 more days)",
      "responsible": "Patient",
      "timeframe": "Through 01/20/2024",
      "priority": "high"
    },
    {
      "action": "Repeat BMP to check creatinine",
      "responsible": "PCP",
      "timeframe": "1 week",
      "priority": "high"
    },
    {
      "action": "PCP follow-up with Dr. Johnson",
      "responsible": "Patient",
      "timeframe": "1 week",
      "priority": "medium"
    },
    {
      "action": "Consider uptitrating lisinopril and metformin once Cr stabilizes",
      "responsible": "PCP",
      "timeframe": "At follow-up",
      "priority": "medium"
    }
  ],
  "critical_alerts": [
    "REDUCED Lisinopril and Metformin doses - monitor renal function",
    "On anticoagulation (Eliquis) - fall precautions"
  ],
  "follow_up": {
    "appointments": ["PCP Dr. Johnson in 1 week"],
    "pending_results": ["Repeat BMP in 1 week"],
    "instructions": "Return for fever >101°F, worsening cough/SOB, or confusion. Complete antibiotics. Low sodium diet. Daily weights - call if gain >3 lbs."
  },
  "confidence": {
    "overall": 0.94,
    "notes": "Complete discharge documentation available"
  }
}
```

## Gotchas

### Common Failure Modes
1. **Hallucinated findings**: Model may infer findings not in notes. Always verify against source.
2. **Missed critical values**: Ensure abnormal labs/vitals are flagged.
3. **Medication errors**: Double-check doses, especially after changes.
4. **Date confusion**: Verify dates match source documentation.

### Edge Cases to Handle
- **Incomplete notes**: Flag missing sections rather than inferring
- **Conflicting information**: Note discrepancies between notes
- **Abbreviations**: Expand non-standard abbreviations when possible
- **Sensitive diagnoses**: Handle mental health, HIV, substance use appropriately

### When NOT to Use This Prompt
- **Legal documentation**: Summaries for medicolegal purposes
- **Patient-facing summaries**: Requires different language level
- **Billing/coding**: Use dedicated medical coding prompts
- **Real-time clinical decisions**: Not a substitute for clinical judgment

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex cases, multiple comorbidities | Highest accuracy for nuanced clinical content |
| **Acceptable:** Claude Sonnet 4 | Standard summaries | Good balance of speed and accuracy |
| **Acceptable:** GPT-4o | General clinical summarization | Strong medical knowledge |
| **Caution:** Smaller models | - | May miss clinical nuances |

## Compliance Notes

- **HIPAA**: Ensure proper PHI handling in your implementation
- **Clinical validation**: All summaries should be reviewed by qualified clinicians
- **Not for diagnosis**: This is a documentation aid, not a clinical decision support tool
