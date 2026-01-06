# Enterprise Prompt Library

[![CI](https://github.com/GoodAI-Global/prompt-library/actions/workflows/ci.yml/badge.svg)](https://github.com/GoodAI-Global/prompt-library/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A curated collection of prompt templates for enterprise AI applications.

---

## What This Is

- **20 prompt templates** across 5 industries (Healthcare, Insurance, Manufacturing, Operations, Analysis)
- **8 reusable patterns** for common prompt engineering challenges
- **Evaluation framework** for testing prompts against golden test cases
- **Consistent structure** with examples, gotchas, and model recommendations

## What This Is NOT

- **Not a plug-and-play SDK** - These are templates, not production code
- **Not exhaustively tested** - Prompts have been validated but not battle-tested at scale
- **Not a replacement for domain expertise** - Healthcare/insurance prompts require SME review
- **Not model-agnostic** - Optimized for Claude, may need adjustment for other models

---

## Quickstart (5 minutes)

### 1. Clone and explore

```bash
git clone https://github.com/GoodAI-Global/prompt-library.git
cd prompt-library
```

### 2. Pick a prompt

Browse by industry or function:

| Category | Prompts | Example |
|----------|---------|---------|
| [Healthcare](./healthcare/) | 4 | Clinical notes, medical coding |
| [Insurance](./insurance/) | 4 | Claims extraction, fraud detection |
| [Manufacturing](./manufacturing/) | 4 | Quality inspection, maintenance |
| [Operations](./operations/) | 4 | Document extraction, email routing |
| [Analysis](./analysis/) | 4 | Root cause, anomaly explanation |

### 3. Copy and customize

Each prompt uses `{{variable}}` placeholders:

```bash
# Read a prompt
cat operations/document-data-extraction.md

# Find variables
grep -o '{{[^}]*}}' operations/document-data-extraction.md
```

### 4. Run validation (optional)

```bash
make setup      # Install dependencies
make validate   # Check syntax
make test       # Run unit tests
```

---

## Prompt Templates

### By Industry

| Industry | Prompts | Description |
|----------|---------|-------------|
| [Healthcare](./healthcare/) | 4 | Clinical notes, prior auth, medical coding, intake |
| [Manufacturing](./manufacturing/) | 4 | Quality control, maintenance, anomaly detection |
| [Insurance](./insurance/) | 4 | Claims processing, fraud detection, underwriting |

### By Function

| Function | Prompts | Description |
|----------|---------|-------------|
| [Operations](./operations/) | 4 | Document extraction, email routing, summarization |
| [Analysis](./analysis/) | 4 | Data quality, anomaly explanation, root cause |

### Prompt Engineering Patterns

| Template | When to Use |
|----------|-------------|
| [Structured Output](./templates/structured-output.md) | Need consistent JSON/schema output |
| [Few-Shot Learning](./templates/few-shot-learning.md) | Complex classification or extraction |
| [Chain of Thought](./templates/chain-of-thought.md) | Multi-step reasoning required |
| [Error Handling](./templates/error-handling.md) | Graceful degradation for edge cases |

### Agentic & RAG Patterns

| Template | When to Use |
|----------|-------------|
| [Tool Use](./templates/tool-use.md) | Function calling and API integration |
| [Multi-Step Agent](./templates/multi-step-agent.md) | Complex task decomposition |
| [Human-in-the-Loop](./templates/human-in-the-loop.md) | Approval workflows and oversight |
| [Retrieval-Augmented](./templates/retrieval-augmented.md) | Document-grounded responses (RAG) |

---

## Prompt Structure

Every prompt follows this structure:

```markdown
# [Prompt Name]

## Use Case           - When to use this prompt
## Input Format       - Required and optional fields
## Output Format      - Expected JSON schema
## The Prompt         - Actual prompt with {{variables}}
## Variables          - Variable reference table
## Examples           - 2+ working examples
## Gotchas            - Common failure modes
## Model Recommendations - Which models work best
```

See [PRINCIPLES.md](./PRINCIPLES.md) for design philosophy.

---

## Development

### Setup

```bash
make setup   # Install Python dependencies
```

### Commands

```bash
make lint      # Run linters
make validate  # Check syntax
make test      # Run unit tests
make eval-dry  # Dry run evaluation (no API key)
make eval      # Run evaluation (requires ANTHROPIC_API_KEY)
make clean     # Remove generated files
```

### Evaluation Framework

```bash
cd evals

# List test cases
python run_evals.py --dry-run

# Run with API key
export ANTHROPIC_API_KEY="your-key"
python run_evals.py --category operations
```

See [evals/README.md](./evals/README.md) for details.

---

## Model Compatibility

| Model | Best For | Notes |
|-------|----------|-------|
| Claude Opus 4 | Complex reasoning, nuanced extraction | Highest accuracy |
| Claude Sonnet 4 | Balanced speed/accuracy | Recommended for most use |
| Claude Haiku 3.5 | High-volume, simple tasks | Cost-effective |
| GPT-4o | Complex reasoning, vision | Strong alternative |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

Requirements:
- Follow prompt structure template
- Include 2+ working examples
- Document failure modes
- Test with at least one model

---

## Security

See [SECURITY.md](./SECURITY.md) for security policy and reporting vulnerabilities.

---

## License

MIT License - See [LICENSE](./LICENSE)

---

## Links

- [Changelog](./CHANGELOG.md)
- [Contributing](./CONTRIBUTING.md)
- [Security Policy](./SECURITY.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Releasing](./RELEASING.md)
