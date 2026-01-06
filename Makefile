# Makefile for Enterprise Prompt Library
# Usage: make <target>

.PHONY: help setup lint format test clean validate all build

# Default target
help:
	@echo "Enterprise Prompt Library - Development Commands"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  setup      Install development dependencies"
	@echo "  lint       Run linters (ruff, black --check)"
	@echo "  format     Format code with black"
	@echo "  test       Run all tests with coverage"
	@echo "  validate   Validate prompt structure and syntax"
	@echo "  build      Build distribution package"
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
	pip install -e ".[dev]"
	@echo "Setup complete. Run 'pip install -e .[eval]' for evaluation dependencies."

# Linting
lint:
	@echo "Running ruff..."
	ruff check evals/
	@echo "Checking black formatting..."
	black --check evals/
	@echo "Running yamllint..."
	yamllint -d relaxed evals/config.yaml evals/test-cases/
	@echo "Lint complete."

# Format code
format:
	@echo "Formatting with black..."
	black evals/
	@echo "Format complete."

# Testing
test:
	@echo "Running tests with coverage..."
	pytest evals/tests/ -v --cov=evals --cov-report=term-missing
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

# Build package
build:
	@echo "Building package..."
	pip install build
	python -m build
	@echo "Build complete. Artifacts in dist/"

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
	rm -rf .mypy_cache/ 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true
	rm -rf .coverage coverage.xml htmlcov/ 2>/dev/null || true
	@echo "Clean complete."

# Run all checks
all: lint validate test
	@echo "All checks passed."
