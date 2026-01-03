# Error Handling Template

## Purpose

Build robust prompts that handle edge cases gracefully. Use when:
- Input quality varies
- Automation requires predictable behavior
- Failures need structured responses
- Upstream systems depend on consistent output

## The Pattern

### Basic Structure

```
[Task description]

[Input data]

HANDLING REQUIREMENTS:

If the task can be completed normally:
- Return the standard response format

If the input is empty or invalid:
- Return an error response with code "INVALID_INPUT"

If the task cannot be completed:
- Return an error response explaining why

If you are uncertain:
- Complete what you can and flag uncertainty

ERROR RESPONSE FORMAT:
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable explanation",
    "details": "Additional context"
  },
  "partial_results": null or {...}
}
```

### Key Elements

1. **Explicit error conditions**: Define what constitutes an error
2. **Error response schema**: Structured error format
3. **Graceful degradation**: What to do with partial success
4. **Uncertainty handling**: How to flag low confidence

## Template Variants

### Variant 1: Input Validation

```
Extract information from the provided document.

DOCUMENT:
{{document_content}}

VALIDATION RULES:
1. Document must contain readable text
2. Document must be in English (or specify language)
3. Document must be under 10,000 words

HANDLING:

If document is empty:
{
  "success": false,
  "error": {
    "code": "EMPTY_INPUT",
    "message": "No document content provided",
    "details": "Please provide document text to analyze"
  }
}

If document is not in English:
{
  "success": false,
  "error": {
    "code": "UNSUPPORTED_LANGUAGE",
    "message": "Document appears to be in [detected language]",
    "details": "This prompt only supports English documents",
    "detected_language": "[language code]"
  }
}

If document is too long:
{
  "success": false,
  "error": {
    "code": "INPUT_TOO_LARGE",
    "message": "Document exceeds maximum length",
    "details": "Document has approximately [X] words. Maximum is 10,000."
  }
}

If valid, proceed with extraction.
```

### Variant 2: Partial Success Handling

```
Extract the following fields from the document:
- Name (required)
- Email (required)
- Phone (optional)
- Address (optional)

DOCUMENT:
{{document_content}}

HANDLING:

If all required fields found:
{
  "success": true,
  "data": {
    "name": "extracted value",
    "email": "extracted value",
    "phone": "extracted value or null",
    "address": "extracted value or null"
  },
  "confidence": {
    "name": 0.95,
    "email": 0.90,
    "phone": 0.85,
    "address": null
  }
}

If some required fields missing:
{
  "success": false,
  "error": {
    "code": "MISSING_REQUIRED_FIELDS",
    "message": "Could not extract all required fields",
    "missing_fields": ["email"]
  },
  "partial_results": {
    "name": "extracted value",
    "email": null,
    "phone": "extracted value",
    "address": null
  },
  "confidence": {
    "name": 0.95,
    "phone": 0.80
  }
}

If document unparseable:
{
  "success": false,
  "error": {
    "code": "UNPARSEABLE_CONTENT",
    "message": "Could not extract meaningful data from document",
    "details": "Document may be corrupted, encrypted, or in unsupported format"
  }
}
```

### Variant 3: Confidence-Based Flagging

```
Classify the support ticket.

TICKET:
{{ticket_content}}

CLASSIFICATION:
Return one of: billing, technical, sales, general

CONFIDENCE HANDLING:

If confidence >= 0.8:
{
  "success": true,
  "classification": "technical",
  "confidence": 0.92,
  "requires_review": false
}

If confidence 0.5 - 0.8:
{
  "success": true,
  "classification": "technical",
  "confidence": 0.65,
  "requires_review": true,
  "review_reason": "Ticket mentions both billing and technical issues",
  "alternative_classifications": [
    {"class": "billing", "confidence": 0.35}
  ]
}

If confidence < 0.5:
{
  "success": true,
  "classification": "general",
  "confidence": 0.45,
  "requires_review": true,
  "review_reason": "Low confidence - content is ambiguous",
  "alternative_classifications": [
    {"class": "technical", "confidence": 0.35},
    {"class": "billing", "confidence": 0.20}
  ]
}
```

### Variant 4: Multi-Item Processing

```
Process each item in the list below.

ITEMS:
{{items_list}}

For each item, classify and extract data.
If an item fails, continue with the remaining items.

RESPONSE FORMAT:
{
  "success": true,
  "summary": {
    "total": 5,
    "succeeded": 4,
    "failed": 1
  },
  "results": [
    {
      "item_index": 0,
      "success": true,
      "data": {...}
    },
    {
      "item_index": 1,
      "success": false,
      "error": {
        "code": "PARSING_FAILED",
        "message": "Could not parse item"
      }
    },
    ...
  ]
}

Overall success is true if any items succeeded.
```

### Variant 5: Cascading Fallbacks

```
Answer the question using the provided context.

QUESTION:
{{question}}

CONTEXT:
{{context}}

FALLBACK STRATEGY:

Level 1 - Direct Answer:
If the answer is clearly stated in the context:
{
  "success": true,
  "answer_type": "direct",
  "answer": "The exact answer from context",
  "source": "Quote from context",
  "confidence": 0.95
}

Level 2 - Inferred Answer:
If the answer can be reasonably inferred:
{
  "success": true,
  "answer_type": "inferred",
  "answer": "The inferred answer",
  "reasoning": "How you arrived at this answer",
  "confidence": 0.75
}

Level 3 - Partial Answer:
If only part of the question can be answered:
{
  "success": true,
  "answer_type": "partial",
  "answer": "What can be answered",
  "unanswerable_parts": ["What cannot be answered"],
  "confidence": 0.60
}

Level 4 - Cannot Answer:
If the question cannot be answered from context:
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_CONTEXT",
    "message": "Cannot answer this question from the provided context"
  },
  "suggestions": ["What additional information would help"]
}
```

## Error Code Taxonomy

### Standard Error Codes

| Code | Meaning | Recovery Action |
|------|---------|-----------------|
| `EMPTY_INPUT` | No input provided | Request input |
| `INVALID_INPUT` | Input malformed | Provide format guidance |
| `INPUT_TOO_LARGE` | Exceeds size limit | Split or truncate |
| `UNSUPPORTED_FORMAT` | Format not handled | Convert format |
| `UNSUPPORTED_LANGUAGE` | Language not supported | Translate first |
| `MISSING_REQUIRED_FIELDS` | Required data absent | Provide missing fields |
| `PARSING_FAILED` | Could not parse content | Check content quality |
| `CONFIDENCE_TOO_LOW` | Below threshold | Human review needed |
| `AMBIGUOUS_INPUT` | Multiple interpretations | Clarify intent |
| `INSUFFICIENT_CONTEXT` | Need more information | Provide context |
| `TIMEOUT` | Processing too long | Simplify request |
| `INTERNAL_ERROR` | Unexpected failure | Retry or escalate |

### Severity Levels

```json
{
  "error": {
    "code": "MISSING_REQUIRED_FIELDS",
    "severity": "warning",  // error, warning, info
    "recoverable": true,
    "action_required": "human_review"
  }
}
```

## Best Practices

### 1. Fail Gracefully

Always return structured response, even on failure:

```
# Bad - unpredictable output
"I couldn't process this because the input was empty"

# Good - structured error
{
  "success": false,
  "error": {
    "code": "EMPTY_INPUT",
    "message": "No input provided"
  }
}
```

### 2. Preserve Partial Work

Don't discard partial results:

```json
{
  "success": false,
  "error": {
    "code": "INCOMPLETE_EXTRACTION",
    "message": "Could not extract all fields"
  },
  "partial_results": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": null
  },
  "fields_missing": ["phone"]
}
```

### 3. Provide Actionable Information

Tell the user what to do:

```json
{
  "success": false,
  "error": {
    "code": "UNSUPPORTED_FORMAT",
    "message": "PDF format is not supported",
    "suggestion": "Please convert to plain text or extract text from PDF first",
    "supported_formats": ["txt", "csv", "json"]
  }
}
```

### 4. Rate Confidence Honestly

```json
{
  "success": true,
  "data": {...},
  "confidence": 0.72,
  "confidence_factors": {
    "input_quality": "medium",
    "pattern_match": "strong",
    "ambiguity": "low"
  },
  "requires_review": true,
  "review_reason": "Overall confidence below 0.80 threshold"
}
```

## Integration Patterns

### Python Error Handler

```python
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class LLMResponse:
    success: bool
    data: Optional[Any] = None
    error: Optional[dict] = None
    partial_results: Optional[Any] = None
    confidence: Optional[float] = None
    requires_review: bool = False

def process_llm_response(raw_response: str) -> LLMResponse:
    parsed = json.loads(raw_response)

    if parsed.get('success'):
        return LLMResponse(
            success=True,
            data=parsed.get('data'),
            confidence=parsed.get('confidence'),
            requires_review=parsed.get('requires_review', False)
        )
    else:
        return LLMResponse(
            success=False,
            error=parsed.get('error'),
            partial_results=parsed.get('partial_results')
        )

def handle_response(response: LLMResponse):
    if response.success:
        if response.requires_review:
            queue_for_review(response.data, response.confidence)
        else:
            process_result(response.data)
    else:
        error_code = response.error.get('code')
        if error_code in RETRYABLE_ERRORS:
            retry_with_backoff(original_request)
        elif response.partial_results:
            handle_partial(response.partial_results)
        else:
            escalate_error(response.error)
```

### JavaScript Error Handler

```javascript
class LLMResponseHandler {
  handle(rawResponse) {
    const parsed = JSON.parse(rawResponse);

    if (parsed.success) {
      return this.handleSuccess(parsed);
    } else {
      return this.handleError(parsed);
    }
  }

  handleSuccess(response) {
    if (response.requires_review) {
      return {
        status: 'review_needed',
        data: response.data,
        confidence: response.confidence
      };
    }
    return { status: 'complete', data: response.data };
  }

  handleError(response) {
    const { error, partial_results } = response;

    if (this.isRetryable(error.code)) {
      return { status: 'retry', error };
    }

    if (partial_results) {
      return {
        status: 'partial',
        data: partial_results,
        error
      };
    }

    return { status: 'failed', error };
  }

  isRetryable(code) {
    return ['TIMEOUT', 'RATE_LIMITED', 'TEMPORARY_ERROR'].includes(code);
  }
}
```

## When to Use Comprehensive Error Handling

**Essential for:**
- Production automation pipelines
- Customer-facing applications
- Data processing workflows
- Integration with other systems
- Any use case where failures have cost

**May be overkill for:**
- Interactive exploration
- One-off analysis
- Simple queries
- Low-stakes applications
