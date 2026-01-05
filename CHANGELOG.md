# Changelog

All notable changes to the Enterprise Prompt Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Financial Services vertical (KYC, regulatory reporting, trade surveillance)
- Legal vertical (contract analysis, due diligence, clause extraction)
- Multi-modal prompt patterns (document + image analysis)

---

## [1.1.0] - 2025-01-05

### Added

#### Healthcare Vertical (New)
- `healthcare/clinical-notes-summarization.md` - Physician handoff and discharge summaries
- `healthcare/prior-authorization-extraction.md` - Prior auth form processing
- `healthcare/medical-coding-assistance.md` - ICD-10/CPT coding support
- `healthcare/patient-intake-extraction.md` - Patient registration form extraction

#### Evaluation Framework (New)
- `evals/README.md` - Comprehensive evaluation documentation
- `evals/run_evals.py` - Automated test runner with accuracy/latency/cost metrics
- `evals/config.yaml` - Evaluation configuration
- `evals/metrics/` - Accuracy, latency, and cost metric modules
- `evals/test-cases/` - Golden test cases for regression testing

#### Templates (New)
- `templates/tool-use.md` - Function calling patterns (coming soon)
- `templates/multi-step-agent.md` - Task decomposition patterns (coming soon)
- `templates/human-in-the-loop.md` - Approval workflow patterns (coming soon)
- `templates/retrieval-augmented.md` - RAG patterns (coming soon)

#### Infrastructure
- `.gitignore` - Python, IDE, and secret file exclusions
- `CHANGELOG.md` - This file
- `CONTRIBUTING.md` - Contribution guidelines

### Changed
- Updated `README.md` with Testing & Evaluation section
- Updated directory structure to include new verticals
- Added Healthcare to industry navigation

### Fixed
- Added missing `import json` to error-handling.md Python example

---

## [1.0.0] - 2025-01-05

### Added

#### Core Documentation
- `README.md` - Main documentation with navigation and getting started guide
- `PRINCIPLES.md` - 10 production-tested prompt engineering principles
- `LICENSE` - MIT License

#### Manufacturing Vertical
- `manufacturing/quality-inspection-analysis.md` - Pass/fail with Cpk calculations
- `manufacturing/maintenance-log-interpretation.md` - Pattern detection from technician notes
- `manufacturing/production-anomaly-explanation.md` - Stakeholder-ready explanations
- `manufacturing/equipment-failure-prediction.md` - RUL estimates with monitoring plans

#### Insurance Vertical
- `insurance/claims-document-extraction.md` - FNOL extraction with handwritten note handling
- `insurance/policy-comparison-analysis.md` - Side-by-side policy analysis
- `insurance/fraud-indicator-detection.md` - Risk scoring for SIU referral
- `insurance/underwriting-risk-assessment.md` - Multi-factor risk grading

#### Operations Prompts
- `operations/document-data-extraction.md` - Generic document extraction
- `operations/email-classification-routing.md` - Email classification with sentiment
- `operations/meeting-notes-summarization.md` - Meeting transcript to action items
- `operations/report-generation.md` - Status/executive/incident reports

#### Analysis Prompts
- `analysis/data-quality-assessment.md` - 6-dimension data quality scoring
- `analysis/anomaly-explanation.md` - Cause hypothesis with stakeholder messaging
- `analysis/trend-interpretation.md` - Pattern analysis with projections
- `analysis/root-cause-analysis.md` - 5-Whys with verification framework

#### Prompt Engineering Templates
- `templates/structured-output.md` - JSON schema enforcement patterns
- `templates/few-shot-learning.md` - Example-based instruction patterns
- `templates/chain-of-thought.md` - Step-by-step reasoning frameworks
- `templates/error-handling.md` - Graceful degradation patterns

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|------------|
| 1.1.0 | 2025-01-05 | Healthcare vertical, evaluation framework |
| 1.0.0 | 2025-01-05 | Initial release with 16 prompts |

---

## Versioning Guidelines

### Prompt Versioning

Individual prompts can be versioned using this scheme:

```
prompt-name-v1.2.3
         │ │ │
         │ │ └── Patch: Wording tweaks, typo fixes, example improvements
         │ └──── Minor: New examples, edge cases, variable additions
         └────── Major: Output format changes, structural changes
```

### When to Update

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Fix typo in prompt | Patch | 1.0.0 → 1.0.1 |
| Add new example | Minor | 1.0.1 → 1.1.0 |
| Change output schema | Major | 1.1.0 → 2.0.0 |
| Add new variable | Minor | 1.1.0 → 1.2.0 |
| Improve instructions | Patch | 1.2.0 → 1.2.1 |

---

## Migration Notes

### From 1.0.0 to 1.1.0

No breaking changes. New features are additive:
- New healthcare prompts can be adopted incrementally
- Evaluation framework is optional but recommended
- Existing prompts unchanged except for error-handling.md fix

### Future Considerations

When major versions are released with breaking changes, migration guides will be provided here.
