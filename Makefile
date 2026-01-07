# Makefile for Enterprise Prompt Library
# Usage: make <target>

.PHONY: help setup lint format test validate clean all eval eval-dry build

# Default target
help:
	@echo "Enterprise Prompt Library - Development Commands"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Offline Commands (no API key required):"
	@echo "  setup      Install development dependencies"
	@echo "  lint       Run linters (ruff, black --check, yamllint)"
	@echo "  format     Format code with black"
	@echo "  validate   Run offline validator (prompts, templates, test cases)"
	@echo "  test       Run all unit tests with coverage"
	@echo "  all        Run lint, validate, and test"
	@echo "  clean      Remove generated files"
	@echo "  build      Build distribution package"
	@echo ""
	@echo "Online Commands (requires ANTHROPIC_API_KEY):"
	@echo "  eval-dry   Dry run evaluation (lists test cases)"
	@echo "  eval       Run full evaluation against Claude API"
	@echo ""

# =============================================================================
# OFFLINE COMMANDS - No API key required
# =============================================================================

# Install dependencies
setup:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	@echo ""
	@echo "Setup complete!"
	@echo "  - Run 'make validate' to check prompts (no API key needed)"
	@echo "  - Run 'make test' to run unit tests"
	@echo "  - Run 'pip install -e .[eval]' for evaluation dependencies"

# Linting
lint:
	@echo "Running ruff..."
	ruff check src/ evals/ tests/
	@echo "Checking black formatting..."
	black --check src/ evals/ tests/
	@echo "Running yamllint..."
	yamllint -d relaxed evals/config.yaml evals/test-cases/
	@echo ""
	@echo "✓ Lint complete."

# Format code
format:
	@echo "Formatting with black..."
	black src/ evals/ tests/
	@echo "Sorting imports with ruff..."
	ruff check src/ evals/ tests/ --fix --select I
	@echo ""
	@echo "✓ Format complete."

# Offline validation - validates structure without API calls
validate:
	@echo "Running offline validator..."
	python src/validate.py --verbose
	@echo ""
	@echo "✓ Validation complete (no API key required)."

# Unit tests - no API key required
test:
	@echo "Running validator tests..."
	python -m pytest tests/ -v --cov=src --cov-report=term-missing
	@echo ""
	@echo "Running eval framework tests..."
	python -m pytest evals/tests/ -v
	@echo ""
	@echo "✓ Tests complete."

# Build package
build:
	@echo "Building package..."
	pip install build
	python -m build
	@echo ""
	@echo "✓ Build complete. Artifacts in dist/"

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
	rm -rf evals/results/ 2>/dev/null || true
	@echo "✓ Clean complete."

# Run all offline checks
all: lint validate test
	@echo ""
	@echo "✓ All offline checks passed."

# =============================================================================
# ONLINE COMMANDS - Requires ANTHROPIC_API_KEY
# =============================================================================

# Dry run evaluation (lists what would be tested)
eval-dry:
	@echo "Dry run - listing test cases..."
	cd evals && python run_evals.py --dry-run

# Full evaluation (requires ANTHROPIC_API_KEY)
eval:
ifndef ANTHROPIC_API_KEY
	$(error ANTHROPIC_API_KEY is not set. Run: export ANTHROPIC_API_KEY=your-key)
endif
	@echo "Running evaluation against Claude API..."
	cd evals && python run_evals.py

# =============================================================================
# CI TARGETS - Used by GitHub Actions
# =============================================================================

.PHONY: ci ci-lint ci-validate ci-test

# Full CI check (used by GitHub Actions)
ci: ci-lint ci-validate ci-test
	@echo "✓ CI checks passed."

ci-lint: lint

ci-validate: validate

ci-test: test
