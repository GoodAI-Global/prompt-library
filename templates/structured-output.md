# Structured Output Template

## Purpose

Ensure consistent, machine-parseable output from AI models. Use this template when you need:
- JSON responses for API integration
- Consistent field structures across requests
- Reliable parsing in production pipelines

## The Pattern

### Basic Structure

```
You are a [role]. [Task description].

[Input section with data]

OUTPUT REQUIREMENTS:
Return ONLY valid JSON matching this schema:
{
  "field_1": "description of field_1",
  "field_2": {
    "nested_field": "description"
  },
  "array_field": [
    {
      "item_field": "description"
    }
  ]
}

Do not include any text before or after the JSON.
Do not wrap in markdown code blocks.
Do not include comments in the JSON.
```

### Key Elements

1. **Role definition**: Set context for the task
2. **Clear input section**: Labeled input data
3. **Explicit schema**: Show exact structure expected
4. **Output constraints**: Emphasize JSON-only output

## Template Variants

### Variant 1: Simple JSON

```
Extract the following information from the text below.

TEXT:
{{input_text}}

Return ONLY valid JSON with these fields:
{
  "name": "string - full name of person",
  "email": "string - email address or null if not found",
  "phone": "string - phone number or null if not found"
}

Output JSON only, no additional text.
```

### Variant 2: Complex Nested Structure

```
Analyze the document and extract structured data.

DOCUMENT:
{{document_content}}

Return ONLY valid JSON matching this schema:

{
  "document_type": "invoice|contract|receipt|other",
  "confidence": 0.0-1.0,
  "extracted_data": {
    "header": {
      "document_id": "string",
      "date": "YYYY-MM-DD",
      "parties": [
        {
          "name": "string",
          "role": "sender|recipient|other",
          "address": "string or null"
        }
      ]
    },
    "body": {
      "summary": "string - brief summary",
      "key_terms": ["array of key terms"],
      "amounts": [
        {
          "description": "string",
          "value": number,
          "currency": "USD|EUR|etc"
        }
      ]
    }
  },
  "metadata": {
    "processing_notes": ["any relevant notes"],
    "fields_missing": ["list of expected but not found fields"]
  }
}
```

### Variant 3: Array Output

```
Classify each item in the list below.

ITEMS:
{{items_list}}

Return ONLY a JSON array with one object per item:

[
  {
    "original_item": "the input item text",
    "category": "category_a|category_b|category_c",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
  }
]

Maintain the same order as the input list.
```

### Variant 4: Conditional Fields

```
Analyze the input and return appropriate structure based on type.

INPUT:
{{input}}

Return JSON matching ONE of these schemas based on input type:

For type "error":
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": "Additional context"
  }
}

For type "success":
{
  "success": true,
  "data": {
    "result": "the extracted/processed result",
    "confidence": 0.0-1.0
  }
}

Always include the "success" boolean field first.
```

## Best Practices

### 1. Type Annotations

Be explicit about types:
```json
{
  "count": "integer",
  "ratio": "float between 0 and 1",
  "active": "boolean",
  "created_at": "ISO 8601 datetime string",
  "tags": "array of strings",
  "metadata": "object with string keys and any values"
}
```

### 2. Null Handling

Specify when nulls are acceptable:
```
{
  "required_field": "string - always present",
  "optional_field": "string or null if not available",
  "conditional_field": "string - only present when status is 'active'"
}
```

### 3. Enum Values

List valid options explicitly:
```
{
  "status": "pending|approved|rejected|cancelled",
  "priority": "low|medium|high|critical",
  "category": "One of: sales, support, billing, technical, other"
}
```

### 4. Validation Hints

Include validation requirements:
```
{
  "email": "valid email format (user@domain.com)",
  "phone": "E.164 format (+1XXXXXXXXXX)",
  "date": "YYYY-MM-DD format",
  "amount": "positive number, max 2 decimal places",
  "percentage": "integer 0-100"
}
```

## Common Gotchas

### Problem: Model wraps JSON in markdown

**Solution:** Add explicit instruction:
```
Return ONLY the JSON object.
Do not wrap in ```json``` code blocks.
Do not include any text before or after the JSON.
```

### Problem: Model adds commentary

**Solution:** Reinforce at end:
```
Your response must be valid JSON only. No explanatory text.
```

### Problem: Inconsistent field names

**Solution:** Show exact casing:
```
Use exactly these field names (camelCase):
- firstName (not first_name, FirstName, or first-name)
- emailAddress (not email_address or email)
```

### Problem: Missing fields

**Solution:** Require explicit nulls:
```
Include ALL fields in the schema.
Use null for missing values, do not omit fields.
```

### Problem: Invalid JSON characters

**Solution:** Escape requirements:
```
Properly escape special characters in strings:
- Newlines as \n
- Quotes as \"
- Backslashes as \\
```

## Validation Code

### Python Validation

```python
import json
from typing import Optional

def parse_llm_response(response: str) -> Optional[dict]:
    """Parse LLM response, handling common issues."""
    # Strip whitespace
    response = response.strip()

    # Remove markdown code blocks if present
    if response.startswith('```'):
        lines = response.split('\n')
        lines = [l for l in lines if not l.startswith('```')]
        response = '\n'.join(lines)

    # Try to extract JSON if surrounded by text
    try:
        # First try: direct parse
        return json.loads(response)
    except json.JSONDecodeError:
        # Second try: find JSON object/array
        start_obj = response.find('{')
        start_arr = response.find('[')

        if start_obj == -1 and start_arr == -1:
            return None

        start = min(
            start_obj if start_obj != -1 else float('inf'),
            start_arr if start_arr != -1 else float('inf')
        )

        # Find matching end
        if response[start] == '{':
            end = response.rfind('}') + 1
        else:
            end = response.rfind(']') + 1

        if end > start:
            try:
                return json.loads(response[start:end])
            except json.JSONDecodeError:
                return None

    return None

def validate_schema(data: dict, required_fields: list) -> list:
    """Check for missing required fields."""
    missing = []
    for field in required_fields:
        if '.' in field:
            # Nested field
            parts = field.split('.')
            obj = data
            for part in parts:
                if isinstance(obj, dict) and part in obj:
                    obj = obj[part]
                else:
                    missing.append(field)
                    break
        elif field not in data:
            missing.append(field)
    return missing
```

### JavaScript Validation

```javascript
function parseLLMResponse(response) {
  // Strip whitespace
  response = response.trim();

  // Remove markdown code blocks
  if (response.startsWith('```')) {
    response = response
      .split('\n')
      .filter(line => !line.startsWith('```'))
      .join('\n');
  }

  try {
    return JSON.parse(response);
  } catch (e) {
    // Try to extract JSON
    const startObj = response.indexOf('{');
    const startArr = response.indexOf('[');

    if (startObj === -1 && startArr === -1) return null;

    const start = Math.min(
      startObj !== -1 ? startObj : Infinity,
      startArr !== -1 ? startArr : Infinity
    );

    const isObject = response[start] === '{';
    const end = isObject
      ? response.lastIndexOf('}') + 1
      : response.lastIndexOf(']') + 1;

    if (end > start) {
      try {
        return JSON.parse(response.slice(start, end));
      } catch (e) {
        return null;
      }
    }
  }

  return null;
}
```

## Model-Specific Notes

| Model | Notes |
|-------|-------|
| Claude | Generally reliable JSON output. Use "Return ONLY valid JSON" |
| GPT-4 | json_mode available in API for guaranteed JSON |
| GPT-3.5 | More prone to adding commentary. Be very explicit |
| Smaller models | May struggle with complex nested structures. Simplify schema |

## When to Use Structured Output

**Good candidates:**
- API integrations needing consistent format
- Data extraction pipelines
- Classification systems
- Any automation requiring parsing

**Consider alternatives:**
- Human-readable reports (use markdown instead)
- Open-ended analysis (free-form may be better)
- Very simple responses (might be over-engineering)
