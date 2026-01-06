# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

1. **Do NOT open a public GitHub issue** for security vulnerabilities
2. Email security concerns to: security@good.ai
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Timeline**: Depends on severity

### Severity Levels

| Level | Response Time | Examples |
|-------|---------------|----------|
| Critical | 24 hours | Exposed credentials, code injection |
| High | 72 hours | PII exposure, authentication bypass |
| Medium | 1 week | Information disclosure |
| Low | 2 weeks | Minor issues |

## Security Best Practices

When using this prompt library:

### 1. API Keys
- Never commit API keys to version control
- Use environment variables for credentials
- Rotate keys regularly

### 2. Sensitive Data
- All example data uses safe placeholders (@example.com, 555-XXX-XXXX)
- Never use real customer data in prompts
- Sanitize inputs before sending to LLM APIs

### 3. Prompt Injection
- Be aware of prompt injection risks
- Validate and sanitize user inputs
- Use structured outputs when possible
- Consider input length limits

### 4. Output Validation
- Validate LLM outputs before use
- Don't trust extracted data without verification
- Implement human review for high-stakes decisions

## Security Features

This library includes:

- **No hardcoded credentials**: All examples use placeholder data
- **Safe example data**: Emails use @example.com, phones use 555-XXX-XXXX
- **Gitignore**: Excludes .env and credential files
- **Lint checks**: CI validates no secrets in commits

## Dependencies

The evaluation framework uses:
- `anthropic`: Official Anthropic SDK
- `pyyaml`: YAML parsing
- `rich`: Terminal formatting (optional)

Keep dependencies updated via Dependabot.

## Acknowledgments

We appreciate responsible security researchers who help keep this project safe.
