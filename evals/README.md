# Prompt Evaluation Framework

**Systematic testing for production prompt reliability.**

This framework provides automated evaluation of prompts against golden test cases, enabling regression testing across model updates and prompt iterations.

---

## Overview

```
evals/
├── README.md                 # This file
├── run_evals.py              # Main evaluation runner
├── config.yaml               # Evaluation configuration
├── metrics/
│   ├── accuracy.py           # Accuracy metrics
│   ├── latency.py            # Performance metrics
│   └── cost.py               # Token/cost tracking
└── test-cases/
    ├── operations/           # Test cases for operations prompts
    ├── insurance/            # Test cases for insurance prompts
    ├── manufacturing/        # Test cases for manufacturing prompts
    └── analysis/             # Test cases for analysis prompts
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install anthropic openai pyyaml pytest rich
```

### 2. Set API Keys

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"  # Optional, for comparison
```

### 3. Run Evaluations

```bash
# Run all evaluations
python evals/run_evals.py

# Run specific prompt category
python evals/run_evals.py --category operations

# Run specific prompt
python evals/run_evals.py --prompt document-data-extraction

# Run with specific model
python evals/run_evals.py --model claude-sonnet-4-20250514
```

---

## Test Case Format

Each test case is a YAML file with the following structure:

```yaml
# test-cases/operations/document-data-extraction/invoice-clean.yaml
name: "Clean Invoice Extraction"
description: "Standard invoice with all fields clearly visible"
prompt_file: "operations/document-data-extraction.md"

input:
  document_text: |
    INVOICE #INV-2024-001
    Date: January 15, 2024

    From: Acme Corporation
    123 Business Ave, New York, NY 10001

    To: Customer Inc
    456 Client Street, Boston, MA 02101

    Items:
    - Widget A (10 units @ $50.00): $500.00
    - Widget B (5 units @ $100.00): $500.00

    Subtotal: $1,000.00
    Tax (8%): $80.00
    Total Due: $1,080.00

    Payment Terms: Net 30
    Due Date: February 14, 2024

expected_output:
  vendor_name: "Acme Corporation"
  invoice_number: "INV-2024-001"
  invoice_date: "2024-01-15"
  total_amount: 1080.00
  due_date: "2024-02-14"
  line_items:
    - description: "Widget A"
      quantity: 10
      unit_price: 50.00
      total: 500.00
    - description: "Widget B"
      quantity: 5
      unit_price: 100.00
      total: 500.00

evaluation_criteria:
  - field: "vendor_name"
    match_type: "exact"
    required: true
  - field: "invoice_number"
    match_type: "exact"
    required: true
  - field: "total_amount"
    match_type: "numeric"
    tolerance: 0.01
    required: true
  - field: "line_items"
    match_type: "array_contains"
    required: false

tags:
  - "happy-path"
  - "invoice"
  - "complete-data"
```

---

## Evaluation Metrics

### Accuracy Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| `exact_match` | Output exactly matches expected | > 95% |
| `field_accuracy` | Per-field correctness | > 98% |
| `semantic_similarity` | Meaning equivalence (for text) | > 0.90 |
| `json_validity` | Output is valid JSON | 100% |

### Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| `latency_p50` | Median response time | < 2s |
| `latency_p95` | 95th percentile latency | < 5s |
| `tokens_input` | Average input tokens | Monitor |
| `tokens_output` | Average output tokens | Monitor |

### Cost Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| `cost_per_request` | USD per API call | Monitor |
| `cost_per_1k` | USD per 1000 requests | Budget |

---

## Writing Effective Test Cases

### Coverage Categories

1. **Happy Path** (`happy-path`)
   - Clean, complete inputs
   - Expected to pass with high confidence

2. **Edge Cases** (`edge-case`)
   - Missing fields
   - Unusual formats
   - Boundary values

3. **Adversarial** (`adversarial`)
   - Malformed inputs
   - Injection attempts
   - Conflicting data

4. **Scale** (`scale`)
   - Very long inputs
   - Very short inputs
   - Context window limits

### Example Test Case Categories

```yaml
# Happy path
- invoice-clean.yaml
- invoice-multiple-pages.yaml

# Edge cases
- invoice-missing-date.yaml
- invoice-handwritten.yaml
- invoice-foreign-currency.yaml

# Adversarial
- invoice-conflicting-totals.yaml
- invoice-injection-attempt.yaml

# Scale
- invoice-100-line-items.yaml
- invoice-minimal.yaml
```

---

## Regression Testing

### Continuous Integration

Add to your CI pipeline:

```yaml
# .github/workflows/prompt-eval.yml
name: Prompt Evaluation

on:
  push:
    paths:
      - 'operations/**'
      - 'insurance/**'
      - 'manufacturing/**'
      - 'analysis/**'
      - 'templates/**'
      - 'evals/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install anthropic openai pyyaml pytest rich

      - name: Run evaluations
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python evals/run_evals.py --fail-under 95
```

### Model Update Testing

When a new model version is released:

```bash
# Compare current model vs new model
python evals/run_evals.py --model claude-sonnet-4-20250514 --output results-current.json
python evals/run_evals.py --model claude-sonnet-4-new --output results-new.json
python evals/compare_results.py results-current.json results-new.json
```

---

## Interpreting Results

### Pass/Fail Criteria

```
✅ PASS: All required fields match expected values
⚠️ WARN: Optional fields missing or low confidence
❌ FAIL: Required field mismatch or invalid output
```

### Sample Output

```
================================================================================
PROMPT EVALUATION REPORT
================================================================================
Prompt: document-data-extraction
Model: claude-sonnet-4-20250514
Test Cases: 12
--------------------------------------------------------------------------------

Results:
  ✅ Passed: 11 (91.7%)
  ⚠️ Warnings: 1 (8.3%)
  ❌ Failed: 0 (0.0%)

Metrics:
  Field Accuracy: 98.2%
  JSON Validity: 100%
  Avg Latency: 1.23s
  Avg Cost: $0.0034

Failed Cases:
  (none)

Warnings:
  - invoice-handwritten.yaml: confidence below threshold (0.72)

================================================================================
```

---

## Best Practices

1. **Maintain Golden Test Sets**
   - Review and update quarterly
   - Add cases from production failures
   - Remove obsolete scenarios

2. **Version Test Cases**
   - Tag test cases with prompt version
   - Track which tests apply to which prompt versions

3. **Monitor Trends**
   - Track accuracy over time
   - Alert on regression
   - Compare across model versions

4. **Production Feedback Loop**
   - Log production failures
   - Convert failures to test cases
   - Validate fixes with new tests

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Low accuracy | Prompt drift | Review recent prompt changes |
| High latency | Long inputs | Consider chunking strategy |
| JSON errors | Format issues | Add format enforcement |
| Flaky tests | Non-deterministic | Set temperature=0 |

---

## Contributing Test Cases

When adding new test cases:

1. Follow the YAML schema above
2. Include at least one happy-path case
3. Include at least one edge case
4. Tag appropriately
5. Document expected behavior
