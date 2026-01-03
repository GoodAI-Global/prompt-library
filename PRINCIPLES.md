# Prompt Engineering Principles

**Production-tested principles for enterprise AI applications.**

These aren't theoretical best practices. They're lessons from production failures.

---

## Core Principles

### 1. Be Specific About Format

**Bad:**
```
Extract the important information from this document.
```

**Good:**
```
Extract the following fields from this invoice:
- vendor_name: string, the company issuing the invoice
- invoice_number: string, alphanumeric identifier
- total_amount: number, final amount due in USD
- due_date: string, format YYYY-MM-DD

Return as JSON. If a field cannot be found, use null.
```

**Why it matters:** Ambiguous format instructions cause inconsistent outputs. Production systems break when output structure varies.

---

### 2. Provide Examples (Few-Shot > Instructions)

Showing beats telling. For complex tasks, 2-3 examples outperform paragraphs of instructions.

**Instruction-only approach:**
```
Classify the sentiment as positive, negative, or neutral.
Consider sarcasm and implicit meanings.
```

**Few-shot approach:**
```
Classify the sentiment as: positive, negative, or neutral.

Examples:
"This product exceeded my expectations!" → positive
"Worst purchase I've ever made." → negative
"It arrived on Tuesday." → neutral
"Oh great, another software update." → negative (sarcasm)

Now classify: {{text}}
```

**When to use few-shot:**
- Classification with subtle distinctions
- Extraction with specific formatting
- Tasks where examples clarify ambiguity

**When instructions work better:**
- Simple, unambiguous tasks
- When examples would be too verbose
- Highly variable inputs

---

### 3. Define Edge Cases Explicitly

Edge cases aren't exceptions—they're guarantees. Define handling upfront.

**Common edge cases to address:**
- Missing data: "If field not found, return null"
- Ambiguous values: "If amount unclear, return best estimate with confidence < 0.8"
- Multiple matches: "Return all matches as array"
- Conflicting information: "Prefer most recent date if dates conflict"
- Empty input: "Return error object with code 'EMPTY_INPUT'"

**Template:**
```
Handle the following edge cases:
- If {{field}} is missing: {{action}}
- If {{field}} is ambiguous: {{action}}
- If multiple {{field}} values exist: {{action}}
- If input is empty or invalid: {{action}}
```

---

### 4. Set Confidence Thresholds

Not all extractions are equal. Quantify certainty.

**Confidence schema:**
```json
{
  "value": "extracted value",
  "confidence": 0.95,
  "source": "location in document",
  "reasoning": "why this confidence level"
}
```

**Threshold guidelines:**
| Confidence | Meaning | Action |
|------------|---------|--------|
| ≥ 0.95 | High certainty | Auto-process |
| 0.80-0.94 | Moderate certainty | Flag for review |
| 0.60-0.79 | Low certainty | Require human verification |
| < 0.60 | Uncertain | Reject or escalate |

**Prompt pattern:**
```
For each extracted field, provide a confidence score:
- 1.0: Explicitly stated, unambiguous
- 0.8-0.9: Clearly implied or minor interpretation
- 0.6-0.8: Requires inference, some ambiguity
- Below 0.6: Uncertain, flag for review
```

---

### 5. Include Context Limits

Models have context windows. Plan for truncation.

**Strategies:**
1. **Prioritize:** Put critical info first
2. **Chunk:** Split large documents, process separately
3. **Summarize:** Compress context before detailed extraction
4. **Reference:** Use document sections, not full text

**Prompt pattern for long documents:**
```
Document excerpt ({{section}} of {{total_sections}}):
{{content}}

Focus on extracting {{fields}} from this section only.
Note any references to information in other sections.
```

---

### 6. Handle Errors Gracefully

Failures will happen. Define fallback behavior.

**Error response schema:**
```json
{
  "success": false,
  "error": {
    "code": "PARSING_FAILED",
    "message": "Could not parse date format",
    "field": "due_date",
    "input_value": "next Tuesday",
    "suggestion": "Provide date in YYYY-MM-DD format"
  },
  "partial_results": {
    "vendor_name": "Acme Corp",
    "invoice_number": "INV-001"
  }
}
```

**Error categories:**
| Code | Description | Recovery |
|------|-------------|----------|
| `EMPTY_INPUT` | No content provided | Return empty result |
| `PARSING_FAILED` | Cannot parse specific field | Return partial results |
| `AMBIGUOUS_DATA` | Multiple interpretations | Return options with confidence |
| `UNSUPPORTED_FORMAT` | Input format not handled | Return format guidance |
| `CONFIDENCE_TOO_LOW` | Below threshold | Flag for human review |

---

## Advanced Principles

### 7. Chain Prompts for Complex Tasks

Single prompts handling multiple concerns fail more often.

**Bad:** One prompt that extracts, validates, and transforms.

**Good:** Pipeline of focused prompts:
1. Extract raw data
2. Validate extracted data
3. Transform to target format
4. Generate summary

**Benefits:**
- Easier debugging (which step failed?)
- Selective retry (only re-run failed step)
- Modular improvement (upgrade one step)

---

### 8. Version Your Prompts

Prompts are code. Treat them accordingly.

**Versioning scheme:**
```
prompt-name-v1.2.3
         │ │ │
         │ │ └── Patch: wording tweaks, typo fixes
         │ └──── Minor: new examples, edge cases
         └────── Major: structural changes, output format
```

**Track:**
- Prompt text
- Model used
- Test results
- Production performance

---

### 9. Test with Adversarial Inputs

Production data is messier than test data.

**Test categories:**
1. **Happy path:** Clean, complete inputs
2. **Missing data:** Required fields absent
3. **Malformed data:** Wrong formats, encoding issues
4. **Adversarial:** Injection attempts, edge cases
5. **Scale:** Very long or very short inputs

**Adversarial examples:**
```
- Empty string
- Only whitespace
- Non-English characters
- Extremely long text (context overflow)
- Special characters: <script>, {{variable}}, ${{interpolation}}
- Conflicting information in same document
```

---

### 10. Measure and Iterate

Production is the only real test.

**Metrics to track:**
| Metric | Target | Action if missed |
|--------|--------|------------------|
| Accuracy | > 95% | Add examples, refine instructions |
| Latency | < 2s | Simplify prompt, use faster model |
| Error rate | < 2% | Improve edge case handling |
| Human override | < 10% | Adjust confidence thresholds |

**Feedback loop:**
1. Log all inputs and outputs
2. Sample for human review
3. Identify failure patterns
4. Update prompt
5. A/B test changes
6. Deploy improvements

---

## Anti-Patterns

### Don't Do This

1. **Vague instructions**
   - "Be thorough" → What does thorough mean?
   - "Extract relevant info" → Relevant to what?

2. **Implicit assumptions**
   - Assuming date formats
   - Assuming currency
   - Assuming language

3. **No error handling**
   - What happens with bad input?
   - What if the model is uncertain?

4. **Overcomplicated prompts**
   - If prompt > 1000 words, consider splitting
   - If instructions conflict, simplify

5. **No examples**
   - "You know what I mean" → Model doesn't
   - Show, don't tell

---

## Checklist for Production Prompts

Before deploying, verify:

- [ ] Output format explicitly defined (JSON schema if applicable)
- [ ] At least 2 examples provided
- [ ] Edge cases documented and handled
- [ ] Confidence thresholds set
- [ ] Error responses defined
- [ ] Context limits considered
- [ ] Tested with adversarial inputs
- [ ] Metrics baseline established
- [ ] Fallback behavior defined
- [ ] Version tagged

---

**Remember: Production is where prompts prove themselves.**
