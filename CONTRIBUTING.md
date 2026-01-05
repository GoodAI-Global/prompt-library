# Contributing to Enterprise Prompt Library

Thank you for your interest in contributing! This guide will help you create high-quality, production-ready prompts.

## Core Philosophy

**"Leverage, not lore."**

This isn't a collection of experiments. Every prompt must be:
- Tested with real production data
- Validated against edge cases
- Structured for consistent outputs
- Documented with failure modes

## Quick Start

1. Fork the repository
2. Create a branch: `git checkout -b feature/prompt-name`
3. Add your prompt following the structure below
4. Test with at least 3 examples
5. Submit a pull request

---

## Prompt File Structure

Every prompt must follow this exact structure:

```markdown
# [Prompt Name]

## Use Case
- Primary use cases (3-5 bullet points)
- When to use this prompt
- Industry/function context

## Input Format
**Required:**
- Field descriptions with types

**Optional:**
- Optional field descriptions

## Output Format
\`\`\`json
{
  // Complete JSON schema with example values
  // All fields must be documented
}
\`\`\`

## The Prompt
\`\`\`
[Complete prompt text with {{variable}} placeholders]
\`\`\`

## Variables
| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{variable_name}}` | string | Yes | Description |

## Examples

### Example 1: [Happy Path Scenario]
**Input:**
\`\`\`
[Complete input example]
\`\`\`

**Output:**
\`\`\`json
[Complete output example]
\`\`\`

### Example 2: [Edge Case Scenario]
[Second complete example]

### Example 3: [Edge Case or Error Scenario]
[Third complete example]

## Gotchas
### Common Failure Modes
1. [Specific failure with explanation]
2. [Another failure mode]

### Edge Cases to Handle
- [Edge case 1]
- [Edge case 2]

### When NOT to Use This Prompt
- [Scenario where prompt isn't appropriate]

## Model Recommendations
| Model | Use Case | Notes |
|-------|----------|-------|
| **Best:** Claude Opus 4.1 | [Use case] | [Notes] |
| **Acceptable:** Claude Sonnet 4 | [Use case] | [Notes] |
| **Caution:** [Model] | - | [Why to avoid] |
```

---

## Quality Requirements

### 1. Examples (Minimum 2, Recommended 3)

Every prompt must include:

| Example Type | Description | Required |
|--------------|-------------|----------|
| Happy Path | Clean input, expected output | Yes |
| Edge Case | Missing data, ambiguous values | Yes |
| Error/Limit | Invalid input, boundary case | Recommended |

**Example Quality Checklist:**
- [ ] Inputs are realistic (not obviously fake)
- [ ] Outputs are complete (not truncated)
- [ ] JSON is valid and properly formatted
- [ ] Examples match the output schema exactly
- [ ] Confidence scores reflect realistic uncertainty

### 2. Gotchas Section

Document failure modes you've observed:

```markdown
### Common Failure Modes
1. **Hallucinated fields**: Model may invent data not in input
   - Mitigation: Add explicit "only extract what's present" instruction

2. **Date format confusion**: MM/DD vs DD/MM ambiguity
   - Mitigation: Specify expected format in prompt
```

### 3. Model Recommendations

Base recommendations on actual testing:

| Model | Tested? | Notes |
|-------|---------|-------|
| Claude Opus 4.1 | Required | Best for complex reasoning |
| Claude Sonnet 4 | Required | Production balanced |
| GPT-4o | Recommended | For comparison |
| Smaller models | Required | Document limitations |

---

## Testing Requirements

### Before Submitting

1. **Syntax Validation**
   ```bash
   # Verify JSON examples are valid
   python -c "import json; json.loads('''YOUR_JSON''')"
   ```

2. **Run Against Examples**
   - Test with Claude Sonnet 4 minimum
   - Verify output matches expected schema
   - Document any deviations

3. **Edge Case Testing**
   - Test with empty inputs
   - Test with malformed data
   - Test with very long inputs

### Adding Test Cases (Optional but Encouraged)

Add test cases to `evals/test-cases/[category]/[prompt-name]/`:

```yaml
# evals/test-cases/operations/your-prompt/test-case-1.yaml
name: "Test Case Name"
description: "What this tests"
prompt_file: "operations/your-prompt.md"
category: "happy-path"

input:
  variable_1: "value"
  variable_2: "value"

expected_output:
  field_1: "expected"
  field_2: 123

evaluation_criteria:
  - field: "field_1"
    match_type: "exact"
    required: true
```

---

## Style Guide

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Prompt files | `kebab-case.md` | `email-classification.md` |
| Variables | `snake_case` | `{{document_text}}` |
| JSON fields | `snake_case` | `"invoice_number"` |
| Sections | Title Case | `## Model Recommendations` |

### Prompt Writing

**Do:**
- Be specific about output format
- Include edge case handling in the prompt
- Use numbered steps for complex reasoning
- Provide context for why instructions matter

**Don't:**
- Use vague instructions ("be thorough")
- Assume model knows context
- Leave edge cases undefined
- Skip error handling

### Example Data

**Do:**
- Use realistic but fake data
- Use standard fake identifiers:
  - Emails: `@example.com`, `@email.com`
  - Phones: `555-XXX-XXXX`
  - SSNs: `XXX-XX-XXXX` (masked)
  - Names: Common fake names

**Don't:**
- Use real customer data
- Include actual API keys or secrets
- Use potentially valid identifiers

---

## Pull Request Process

### 1. PR Title Format
```
feat(category): Add prompt-name prompt
fix(category): Fix issue in prompt-name
docs: Update documentation for prompt-name
```

### 2. PR Description Template

```markdown
## Summary
Brief description of the prompt and its use case.

## Testing Done
- [ ] Tested with Claude Sonnet 4
- [ ] Tested with [other models]
- [ ] Verified all examples work
- [ ] Tested edge cases

## Production Validation
How was this prompt validated in production?
- Data source:
- Volume tested:
- Accuracy observed:

## Checklist
- [ ] Follows file structure template
- [ ] Includes 2+ examples
- [ ] Documents gotchas/failure modes
- [ ] Includes model recommendations
- [ ] JSON examples are valid
- [ ] No real customer data
- [ ] Updated CHANGELOG.md
```

### 3. Review Criteria

PRs are reviewed for:
- **Completeness**: All sections present
- **Quality**: Examples are realistic and helpful
- **Accuracy**: JSON is valid, schema matches examples
- **Production-readiness**: Failure modes documented
- **Security**: No sensitive data exposed

---

## Adding New Categories

To add a new industry or function category:

1. **Create Directory**
   ```
   mkdir new-category/
   ```

2. **Add 3+ Prompts**
   - Minimum 3 prompts per category
   - Must be production-tested

3. **Update README.md**
   - Add to navigation table
   - Add to directory structure

4. **Update CHANGELOG.md**
   - Document under appropriate version

---

## Code of Conduct

- Be respectful and constructive
- Focus on production value
- Share knowledge generously
- Credit prior work

---

## Questions?

- Open an issue for general questions
- Tag maintainers for urgent items
- Check existing prompts for examples

---

**Remember: Every prompt should be one you'd trust in production.**
