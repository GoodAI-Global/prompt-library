# Changelog

All notable changes to the Enterprise Prompt Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Financial Services vertical (KYC, regulatory reporting, trade surveillance)
- Legal vertical (contract analysis, due diligence, clause extraction)
- Multi-modal prompt patterns (document + image analysis)
- Additional test cases for all prompts

---

## [0.1.0] - 2025-01-06

First tagged release. Establishes baseline with CI/CD infrastructure.

### Added

#### Prompt Templates (20 total)
- **Healthcare** (4): Clinical notes, prior auth, medical coding, patient intake
- **Insurance** (4): Claims extraction, policy comparison, fraud detection, underwriting
- **Manufacturing** (4): Quality inspection, maintenance logs, anomaly explanation, failure prediction
- **Operations** (4): Document extraction, email routing, meeting notes, report generation
- **Analysis** (4): Data quality, anomaly explanation, trend interpretation, root cause

#### Prompt Engineering Patterns (8 total)
- Core: Structured output, few-shot learning, chain-of-thought, error handling
- Agentic: Tool use, multi-step agent, human-in-the-loop, retrieval-augmented

#### Evaluation Framework
- `evals/run_evals.py` - Test runner with accuracy, latency, cost metrics
- `evals/metrics/` - Modular metrics (accuracy, latency, cost)
- `evals/test-cases/` - Golden test cases (3 initial)
- `evals/tests/` - Deterministic unit tests (no API key required)
- `evals/config.yaml` - Configuration for thresholds and models

#### Infrastructure (MVEGS Compliance)
- `.github/workflows/ci.yml` - Lint, validate, test (no secrets required)
- `.github/dependabot.yml` - Automated dependency updates
- `Makefile` - Standard development commands
- `SECURITY.md` - Security policy and vulnerability reporting
- `CODE_OF_CONDUCT.md` - Contributor Covenant
- `CODEOWNERS` - Code ownership for reviews
- `CONTRIBUTING.md` - Contribution guidelines
- `RELEASING.md` - Release process documentation

#### Documentation
- `README.md` - Truthful overview with "What it is / What it isn't"
- `PRINCIPLES.md` - Prompt engineering principles
- `CHANGELOG.md` - This file

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 0.1.0 | 2025-01-06 | First tagged release, MVEGS infrastructure |

---

## Versioning Guidelines

This project uses [Semantic Versioning](https://semver.org/):

- **0.x.x**: Pre-1.0 development, API may change
- **MAJOR**: Breaking changes to prompt output formats
- **MINOR**: New prompts, templates, or features
- **PATCH**: Bug fixes, documentation updates

### Pre-1.0 Note

While in 0.x.x versions:
- Prompt output formats may change without major version bump
- Test coverage is still being expanded
- Breaking changes will be documented but may occur in minor versions

---

## Migration Notes

### Future: 0.x.x to 1.0.0

When 1.0.0 is released:
- All prompt output formats will be locked
- Breaking changes will require major version bumps
- Comprehensive test coverage will be required
