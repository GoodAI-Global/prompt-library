# Document Data Extraction

## Use Case

Extract structured data from unstructured business documents including:
- Invoices and purchase orders
- Contracts and agreements
- Application forms
- Receipts and expense reports
- Shipping documents

Use when you need consistent, machine-readable output from variable document formats.

## Input Format

**Required:**
- `document_text`: The OCR'd text or raw content of the document
- `document_type`: One of: invoice, contract, form, receipt, purchase_order, shipping, other

**Optional:**
- `target_fields`: Array of specific fields to extract (if omitted, extracts all standard fields for document type)
- `language`: ISO language code (default: en)
- `context`: Additional context about the document source

## Output Format

```json
{
  "success": true,
  "document_type": "invoice",
  "extraction_timestamp": "2025-01-15T10:30:00Z",
  "fields": {
    "field_name": {
      "value": "extracted value",
      "confidence": 0.95,
      "source_text": "original text snippet",
      "normalized": "standardized format if applicable"
    }
  },
  "metadata": {
    "total_fields_requested": 10,
    "fields_extracted": 8,
    "fields_missing": ["field1", "field2"],
    "average_confidence": 0.89,
    "warnings": []
  }
}
```

## The Prompt

```
You are a document data extraction specialist. Extract structured data from the provided document with high precision.

DOCUMENT TYPE: {{document_type}}

DOCUMENT CONTENT:
{{document_text}}

{{#if target_fields}}
FIELDS TO EXTRACT:
{{target_fields}}
{{else}}
Extract all standard fields for this document type.
{{/if}}

EXTRACTION RULES:
1. For each field, provide:
   - value: The extracted value
   - confidence: 0.0-1.0 score
   - source_text: The exact text you extracted from
   - normalized: Standardized format (dates as YYYY-MM-DD, currency as numbers, etc.)

2. Confidence scoring:
   - 1.0: Explicitly labeled and unambiguous
   - 0.9: Clearly present but requires minor interpretation
   - 0.7-0.8: Inferred from context or format
   - 0.5-0.7: Educated guess, needs verification
   - Below 0.5: Do not extract, mark as missing

3. Handle edge cases:
   - Missing field: Include in fields_missing array
   - Ambiguous value: Extract most likely, note alternatives in warnings
   - Multiple values: Return as array if field supports it
   - Illegible text: Mark confidence below 0.5, note in warnings

4. Normalization:
   - Dates: YYYY-MM-DD
   - Currency: Numeric value only, separate currency field
   - Phone: E.164 format when possible
   - Addresses: Structured with street, city, state, postal, country

STANDARD FIELDS BY DOCUMENT TYPE:

Invoice:
- vendor_name, vendor_address, vendor_tax_id
- invoice_number, invoice_date, due_date
- line_items (array): description, quantity, unit_price, amount
- subtotal, tax_amount, tax_rate, total_amount
- currency, payment_terms

Contract:
- parties (array): name, role, address
- effective_date, expiration_date, term_length
- contract_type, contract_value
- key_terms (array): term_name, term_value
- signatures (array): name, title, date

Form:
- form_type, form_id, submission_date
- applicant_name, applicant_contact
- All labeled fields as key-value pairs

Receipt:
- merchant_name, merchant_address
- transaction_date, transaction_time
- items (array): description, quantity, price
- subtotal, tax, total, payment_method

Return ONLY valid JSON matching the output schema.
```

## Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{document_type}}` | string | Yes | Type of document: invoice, contract, form, receipt, purchase_order, shipping, other |
| `{{document_text}}` | string | Yes | The raw text content of the document |
| `{{target_fields}}` | array | No | Specific fields to extract; if omitted, extracts all standard fields |

## Examples

### Example 1: Clean Invoice

**Input:**
```
document_type: invoice
document_text: |
  ACME CORPORATION
  123 Business Park, Suite 400
  Austin, TX 78701
  Tax ID: 12-3456789

  INVOICE #INV-2024-0892
  Date: January 15, 2024
  Due Date: February 14, 2024

  Bill To:
  TechStart Inc.
  456 Innovation Drive
  San Francisco, CA 94102

  Description                  Qty    Unit Price    Amount
  --------------------------------------------------------
  Consulting Services          40     $150.00       $6,000.00
  Software License             1      $2,500.00     $2,500.00
  Support Package (Annual)     1      $1,200.00     $1,200.00

  Subtotal:                                         $9,700.00
  Tax (8.25%):                                      $800.25
  Total Due:                                        $10,500.25

  Payment Terms: Net 30
  Please remit payment to: ACH details on file
```

**Output:**
```json
{
  "success": true,
  "document_type": "invoice",
  "extraction_timestamp": "2024-01-16T14:22:00Z",
  "fields": {
    "vendor_name": {
      "value": "ACME CORPORATION",
      "confidence": 1.0,
      "source_text": "ACME CORPORATION",
      "normalized": "Acme Corporation"
    },
    "vendor_address": {
      "value": {
        "street": "123 Business Park, Suite 400",
        "city": "Austin",
        "state": "TX",
        "postal": "78701",
        "country": "US"
      },
      "confidence": 0.95,
      "source_text": "123 Business Park, Suite 400\nAustin, TX 78701"
    },
    "vendor_tax_id": {
      "value": "12-3456789",
      "confidence": 1.0,
      "source_text": "Tax ID: 12-3456789"
    },
    "invoice_number": {
      "value": "INV-2024-0892",
      "confidence": 1.0,
      "source_text": "INVOICE #INV-2024-0892"
    },
    "invoice_date": {
      "value": "2024-01-15",
      "confidence": 1.0,
      "source_text": "Date: January 15, 2024",
      "normalized": "2024-01-15"
    },
    "due_date": {
      "value": "2024-02-14",
      "confidence": 1.0,
      "source_text": "Due Date: February 14, 2024",
      "normalized": "2024-02-14"
    },
    "line_items": {
      "value": [
        {
          "description": "Consulting Services",
          "quantity": 40,
          "unit_price": 150.00,
          "amount": 6000.00
        },
        {
          "description": "Software License",
          "quantity": 1,
          "unit_price": 2500.00,
          "amount": 2500.00
        },
        {
          "description": "Support Package (Annual)",
          "quantity": 1,
          "unit_price": 1200.00,
          "amount": 1200.00
        }
      ],
      "confidence": 0.98,
      "source_text": "Consulting Services 40 $150.00 $6,000.00..."
    },
    "subtotal": {
      "value": 9700.00,
      "confidence": 1.0,
      "source_text": "Subtotal: $9,700.00"
    },
    "tax_amount": {
      "value": 800.25,
      "confidence": 1.0,
      "source_text": "Tax (8.25%): $800.25"
    },
    "tax_rate": {
      "value": 0.0825,
      "confidence": 1.0,
      "source_text": "Tax (8.25%)",
      "normalized": "8.25%"
    },
    "total_amount": {
      "value": 10500.25,
      "confidence": 1.0,
      "source_text": "Total Due: $10,500.25"
    },
    "currency": {
      "value": "USD",
      "confidence": 0.95,
      "source_text": "$",
      "normalized": "USD"
    },
    "payment_terms": {
      "value": "Net 30",
      "confidence": 1.0,
      "source_text": "Payment Terms: Net 30"
    }
  },
  "metadata": {
    "total_fields_requested": 12,
    "fields_extracted": 12,
    "fields_missing": [],
    "average_confidence": 0.99,
    "warnings": []
  }
}
```

### Example 2: Messy/Partial Document

**Input:**
```
document_type: invoice
document_text: |
  [OCR quality poor - some text illegible]

  Sup####r Corp
  [address partially visible]
  ...mento, CA 9###2

  INV 20240115-A

  1/15/24

  Widget Assembly    25    $45     $1,125
  Rush Fee                         $150
  [text cut off]

  Total: $1,382.50
```

**Output:**
```json
{
  "success": true,
  "document_type": "invoice",
  "extraction_timestamp": "2024-01-16T14:25:00Z",
  "fields": {
    "vendor_name": {
      "value": "Sup####r Corp",
      "confidence": 0.4,
      "source_text": "Sup####r Corp",
      "normalized": null
    },
    "vendor_address": {
      "value": {
        "city": "Sacramento",
        "state": "CA",
        "postal": null
      },
      "confidence": 0.5,
      "source_text": "...mento, CA 9###2"
    },
    "invoice_number": {
      "value": "20240115-A",
      "confidence": 0.9,
      "source_text": "INV 20240115-A"
    },
    "invoice_date": {
      "value": "2024-01-15",
      "confidence": 0.85,
      "source_text": "1/15/24",
      "normalized": "2024-01-15"
    },
    "line_items": {
      "value": [
        {
          "description": "Widget Assembly",
          "quantity": 25,
          "unit_price": 45.00,
          "amount": 1125.00
        },
        {
          "description": "Rush Fee",
          "quantity": 1,
          "unit_price": 150.00,
          "amount": 150.00
        }
      ],
      "confidence": 0.75,
      "source_text": "Widget Assembly 25 $45 $1,125\nRush Fee $150"
    },
    "total_amount": {
      "value": 1382.50,
      "confidence": 1.0,
      "source_text": "Total: $1,382.50"
    },
    "currency": {
      "value": "USD",
      "confidence": 0.95,
      "source_text": "$"
    }
  },
  "metadata": {
    "total_fields_requested": 12,
    "fields_extracted": 7,
    "fields_missing": ["vendor_tax_id", "due_date", "subtotal", "tax_amount", "tax_rate"],
    "average_confidence": 0.77,
    "warnings": [
      "OCR quality issues detected - vendor name partially illegible",
      "Address incomplete - city inferred from partial postal code",
      "Line items may be incomplete - document appears truncated",
      "Tax information not present - total may include embedded tax"
    ]
  }
}
```

### Example 3: Edge Case - Empty/Invalid Document

**Input:**
```
document_type: invoice
document_text: |
  [blank page]

  ----
  Page intentionally left blank
  ----
```

**Output:**
```json
{
  "success": false,
  "document_type": "invoice",
  "extraction_timestamp": "2024-01-16T14:30:00Z",
  "error": {
    "code": "NO_EXTRACTABLE_CONTENT",
    "message": "Document contains no extractable invoice data",
    "suggestion": "Verify correct document was provided. Check if multi-page document has content on other pages."
  },
  "fields": {},
  "metadata": {
    "total_fields_requested": 12,
    "fields_extracted": 0,
    "fields_missing": ["vendor_name", "vendor_address", "vendor_tax_id", "invoice_number", "invoice_date", "due_date", "line_items", "subtotal", "tax_amount", "tax_rate", "total_amount", "currency"],
    "average_confidence": 0,
    "warnings": [
      "Document appears to be intentionally blank",
      "No structured data patterns detected"
    ]
  }
}
```

## Gotchas

### Common Failure Modes
1. **OCR errors**: Poor scan quality leads to character substitution (0/O, 1/l/I). Always check confidence and source_text.
2. **Currency confusion**: $, €, £ without explicit currency code. Infer from address/context but reduce confidence.
3. **Date format ambiguity**: 01/02/2024 - is this Jan 2 or Feb 1? Check for locale hints.
4. **Line item alignment**: Columns misaligned in OCR. Verify quantity × unit_price = amount.

### Edge Cases to Handle
- **Multi-currency documents**: Some invoices show amounts in multiple currencies
- **Negative amounts**: Credits, discounts, adjustments
- **Handwritten additions**: Notes, corrections on printed forms
- **Watermarks/stamps**: "PAID", "VOID", "COPY" overlaid on content

### When NOT to Use This Prompt
- **Image-only documents**: Use vision model first, then this prompt
- **Multi-page documents**: Split and process separately, then merge
- **Non-standard formats**: Highly custom documents need specialized prompts
- **High-security documents**: Add additional validation layer for financial/legal

## Model Recommendations

| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | Complex/messy documents | Highest accuracy on ambiguous extractions |
| **Best:** GPT-4o | Documents with visual elements | Strong OCR error correction |
| **Acceptable:** Claude Sonnet 4 | Standard documents | Good balance of speed/accuracy |
| **Acceptable:** GPT-4o-mini | High-volume processing | Cost-effective for clean documents |
| **Not Recommended:** Smaller models | - | Miss nuances, lower confidence accuracy |

## Integration Notes

### Preprocessing
```python
# Recommended preprocessing before extraction
def preprocess_document(raw_text):
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', raw_text)
    # Normalize unicode
    text = unicodedata.normalize('NFKC', text)
    # Remove null bytes
    text = text.replace('\x00', '')
    return text.strip()
```

### Post-processing Validation
```python
# Validate extracted invoice
def validate_invoice(result):
    errors = []

    # Check line item math
    if 'line_items' in result['fields']:
        calculated_subtotal = sum(
            item['amount'] for item in result['fields']['line_items']['value']
        )
        if 'subtotal' in result['fields']:
            if abs(calculated_subtotal - result['fields']['subtotal']['value']) > 0.01:
                errors.append("Line items don't sum to subtotal")

    # Check total = subtotal + tax
    if all(k in result['fields'] for k in ['subtotal', 'tax_amount', 'total_amount']):
        expected_total = (
            result['fields']['subtotal']['value'] +
            result['fields']['tax_amount']['value']
        )
        if abs(expected_total - result['fields']['total_amount']['value']) > 0.01:
            errors.append("Subtotal + tax doesn't equal total")

    return errors
```
