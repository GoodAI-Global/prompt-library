# Makefile for Enterprise Prompt Library
# Usage: make <target>

.PHONY: help setup lint test clean validate all

# Default target
help:
	@echo "Enterprise Prompt Library - Development Commands"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  setup      Install development dependencies"
	@echo "  lint       Run linters (ruff, yamllint)"
	@echo "  test       Run all tests"
	@echo "  validate   Validate prompt structure and syntax"
	@echo "  clean      Remove generated files"
	@echo "  all        Run lint, validate, and test"
	@echo ""
	@echo "Evaluation:"
	@echo "  eval-dry   Dry run evaluation (no API key needed)"
	@echo "  eval       Run evaluation (requires ANTHROPIC_API_KEY)"
	@echo ""

# Install dependencies
setup:
	python -m pip install --upgrade pip
	pip install pyyaml ruff yamllint pytest rich anthropic
	@echo "Setup complete. Set ANTHROPIC_API_KEY to run evaluations."

# Linting
lint:
	@echo "Running Python linter..."
	ruff check evals/
	@echo "Running YAML linter..."
	yamllint -d relaxed evals/config.yaml evals/test-cases/
	@echo "Lint complete."

# Testing
test:
	@echo "Running unit tests..."
	pytest evals/tests/ -v
	@echo "Tests complete."

# Validation
validate:
	@echo "Validating Python syntax..."
	python -m py_compile evals/run_evals.py
	python -m py_compile evals/metrics/__init__.py
	python -m py_compile evals/metrics/accuracy.py
	python -m py_compile evals/metrics/latency.py
	python -m py_compile evals/metrics/cost.py
	@echo "Validating YAML syntax..."
	python -c "import yaml; [yaml.safe_load(open(f)) for f in __import__('pathlib').Path('evals/test-cases').rglob('*.yaml')]"
	@echo "Validating prompt structure..."
	python -c "\
	from pathlib import Path; \
	sections = ['## Use Case', '## The Prompt', '## Variables', '## Examples', '## Gotchas', '## Model Recommendations']; \
	[print(f'ERROR: {f} missing {[s for s in sections if s not in f.read_text()]}') or exit(1) \
	 for cat in ['operations', 'insurance', 'manufacturing', 'healthcare', 'analysis'] \
	 for f in Path(cat).glob('*.md') \
	 if any(s not in f.read_text() for s in sections)] or print('All prompts valid')"
	@echo "Validation complete."

# Dry run evaluation (no API key needed)
eval-dry:
	cd evals && python run_evals.py --dry-run

# Full evaluation (requires ANTHROPIC_API_KEY)
eval:
ifndef ANTHROPIC_API_KEY
	$(error ANTHROPIC_API_KEY is not set. Run: export ANTHROPIC_API_KEY=your-key)
endif
	cd evals && python run_evals.py

# Clean generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	rm -rf .ruff_cache/ 2>/dev/null || true
	@echo "Clean complete."

# Run all checks
all: lint validate test
	@echo "All checks passed."
