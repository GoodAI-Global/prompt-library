# Enterprise Prompt Library

**Production-tested prompts for enterprise AI applications.**

Built by [Good AI](https://good.ai) — "Leverage, not lore."

---

## Philosophy

This isn't a collection of experiments. Every prompt here has been:
- Tested with real production data
- Refined through multiple iterations
- Validated against edge cases
- Structured for consistent outputs

**Evidence over opinions.** Each prompt includes specific examples and documented failure modes.

---

## Quick Navigation

### By Industry

| Industry | Prompts | Description |
|----------|---------|-------------|
| [Manufacturing](./manufacturing/) | 4 prompts | Quality control, maintenance, anomaly detection |
| [Insurance](./insurance/) | 4 prompts | Claims processing, fraud detection, underwriting |

### By Function

| Function | Prompts | Description |
|----------|---------|-------------|
| [Operations](./operations/) | 4 prompts | Document extraction, email routing, summarization |
| [Analysis](./analysis/) | 4 prompts | Data quality, anomaly explanation, root cause |

### Prompt Engineering Patterns

| Template | When to Use |
|----------|-------------|
| [Structured Output](./templates/structured-output.md) | Need consistent JSON/schema output |
| [Few-Shot Learning](./templates/few-shot-learning.md) | Complex classification or extraction |
| [Chain of Thought](./templates/chain-of-thought.md) | Multi-step reasoning required |
| [Error Handling](./templates/error-handling.md) | Graceful degradation for edge cases |

---

## Directory Structure

```
prompt-library/
├── README.md                 # You are here
├── LICENSE                   # MIT License
├── PRINCIPLES.md             # Core prompt engineering principles
├── manufacturing/
│   ├── quality-inspection-analysis.md
│   ├── maintenance-log-interpretation.md
│   ├── production-anomaly-explanation.md
│   └── equipment-failure-prediction.md
├── insurance/
│   ├── claims-document-extraction.md
│   ├── policy-comparison-analysis.md
│   ├── fraud-indicator-detection.md
│   └── underwriting-risk-assessment.md
├── operations/
│   ├── document-data-extraction.md
│   ├── email-classification-routing.md
│   ├── meeting-notes-summarization.md
│   └── report-generation.md
├── analysis/
│   ├── data-quality-assessment.md
│   ├── anomaly-explanation.md
│   ├── trend-interpretation.md
│   └── root-cause-analysis.md
└── templates/
    ├── structured-output.md
    ├── few-shot-learning.md
    ├── chain-of-thought.md
    └── error-handling.md
```

---

## Prompt File Structure

Every prompt in this library follows a consistent structure:

```markdown
# [Prompt Name]

## Use Case
When to use this prompt. Specific scenarios.

## Input Format
What data to provide. Required fields. Optional fields.

## Output Format
Exact structure expected. JSON schema if applicable.

## The Prompt
[Actual prompt text with {{variables}}]

## Variables
| Variable | Type | Required | Description |
|----------|------|----------|-------------|

## Examples
### Example 1: [Scenario Name]
### Example 2: [Edge Case]

## Gotchas
- Common failure modes
- Edge cases to handle
- When NOT to use this prompt

## Model Recommendations
- Best: [models]
- Acceptable: [models]
- Not recommended: [models]
```

---

## Getting Started

### 1. Choose Your Prompt
Browse by [industry](#by-industry) or [function](#by-function).

### 2. Understand the Template
Read the [PRINCIPLES.md](./PRINCIPLES.md) for core concepts.

### 3. Customize Variables
Each prompt uses `{{variable}}` syntax. Replace with your data.

### 4. Test with Examples
Run the provided examples first to validate your integration.

### 5. Handle Edge Cases
Review the "Gotchas" section before production deployment.

---

## Model Compatibility

| Model | Best For | Notes |
|-------|----------|-------|
| Claude Opus 4.1 | Complex reasoning, nuanced extraction | Highest accuracy for ambiguous cases |
| Claude Sonnet 4 | Balanced speed/accuracy | Good for most production use |
| GPT-4o | Complex reasoning, vision tasks | Strong alternative |
| GPT-4o-mini | High-volume, simpler tasks | Cost-effective for classification |
| Claude Haiku 3.5 | High-volume processing | Fastest, use for simple extraction |

---

## Contributing

This is a production library. Contributions must include:
1. Real-world test results
2. At least 2 working examples
3. Documented failure modes
4. Edge case handling

---

## License

MIT License - See [LICENSE](./LICENSE)

---

**Built for practitioners who ship.**
