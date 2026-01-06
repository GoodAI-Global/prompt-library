#!/usr/bin/env python3
"""
Offline Prompt Library Validator

Validates prompt structure, YAML syntax, and required fields without requiring API keys.
Use this for CI/CD pipelines and local development.

Usage:
    python src/validate.py              # Validate all
    python src/validate.py --prompts    # Validate prompts only
    python src/validate.py --tests      # Validate test cases only
    python src/validate.py --config     # Validate config only
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class ValidationResult:
    """Result of a validation check."""

    valid: bool
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    files_checked: int = 0


# Required sections for prompt files
REQUIRED_PROMPT_SECTIONS = [
    "## Use Case",
    "## The Prompt",
    "## Variables",
    "## Examples",
    "## Gotchas",
    "## Model Recommendations",
]

# Required fields for test cases
REQUIRED_TEST_CASE_FIELDS = [
    "name",
    "prompt_file",
    "input",
    "expected_output",
    "evaluation_criteria",
]

# Prompt categories to validate
PROMPT_CATEGORIES = [
    "operations",
    "insurance",
    "manufacturing",
    "healthcare",
    "analysis",
]

# Template categories
TEMPLATE_CATEGORIES = ["templates"]


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def validate_yaml_syntax(file_path: Path) -> tuple[bool, Optional[str]]:
    """Validate YAML file syntax."""
    try:
        with open(file_path) as f:
            yaml.safe_load(f)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)


def validate_json_in_markdown(content: str, file_path: Path) -> list[str]:
    """Validate JSON blocks in markdown files."""
    errors = []
    json_blocks = re.findall(r"```json\n(.*?)```", content, re.DOTALL)

    for i, block in enumerate(json_blocks, 1):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{file_path}: JSON block {i} invalid: {e}")

    return errors


def validate_prompt_file(file_path: Path) -> ValidationResult:
    """Validate a single prompt file."""
    result = ValidationResult(valid=True, files_checked=1)

    try:
        content = file_path.read_text()
    except Exception as e:
        result.valid = False
        result.errors.append(f"{file_path}: Cannot read file: {e}")
        return result

    # Check required sections
    for section in REQUIRED_PROMPT_SECTIONS:
        if section not in content:
            result.valid = False
            result.errors.append(f"{file_path}: Missing section '{section}'")

    # Check for {{variable}} placeholders in The Prompt section
    prompt_match = re.search(r"## The Prompt\s*```[^\n]*\n(.*?)```", content, re.DOTALL)
    if prompt_match:
        prompt_text = prompt_match.group(1)
        variables = re.findall(r"\{\{(\w+)\}\}", prompt_text)
        if not variables:
            result.warnings.append(f"{file_path}: No {{{{variables}}}} found in prompt")

    # Validate JSON blocks
    json_errors = validate_json_in_markdown(content, file_path)
    if json_errors:
        result.warnings.extend(json_errors)  # JSON errors are warnings, not failures

    # Check for safe example data patterns
    if re.search(r"[0-9]{3}-[0-9]{2}-[0-9]{4}", content):  # SSN pattern
        if not re.search(r"XXX-XX-XXXX|000-00-0000|123-45-6789", content):
            result.warnings.append(f"{file_path}: Potential real SSN pattern detected")

    return result


def validate_prompts(project_root: Path) -> ValidationResult:
    """Validate all prompt files."""
    result = ValidationResult(valid=True)

    for category in PROMPT_CATEGORIES:
        category_path = project_root / category
        if not category_path.exists():
            result.warnings.append(f"Category directory not found: {category}")
            continue

        for prompt_file in category_path.glob("*.md"):
            file_result = validate_prompt_file(prompt_file)
            result.files_checked += file_result.files_checked
            result.errors.extend(file_result.errors)
            result.warnings.extend(file_result.warnings)
            if not file_result.valid:
                result.valid = False

    return result


def validate_templates(project_root: Path) -> ValidationResult:
    """Validate all template files."""
    result = ValidationResult(valid=True)

    templates_path = project_root / "templates"
    if not templates_path.exists():
        result.warnings.append("Templates directory not found")
        return result

    for template_file in templates_path.glob("*.md"):
        result.files_checked += 1
        try:
            content = template_file.read_text()
            # Templates have more flexible structure, just check they exist and are readable
            if len(content) < 100:
                result.warnings.append(f"{template_file}: Template seems too short")
        except Exception as e:
            result.valid = False
            result.errors.append(f"{template_file}: Cannot read file: {e}")

    return result


def validate_test_case(file_path: Path) -> ValidationResult:
    """Validate a single test case file."""
    result = ValidationResult(valid=True, files_checked=1)

    # Validate YAML syntax
    valid, error = validate_yaml_syntax(file_path)
    if not valid:
        result.valid = False
        result.errors.append(f"{file_path}: YAML syntax error: {error}")
        return result

    # Load and validate structure
    try:
        with open(file_path) as f:
            test_case = yaml.safe_load(f)
    except Exception as e:
        result.valid = False
        result.errors.append(f"{file_path}: Cannot parse YAML: {e}")
        return result

    # Check required fields
    for field_name in REQUIRED_TEST_CASE_FIELDS:
        if field_name not in test_case:
            result.valid = False
            result.errors.append(f"{file_path}: Missing required field '{field_name}'")

    # Check prompt_file reference exists
    if "prompt_file" in test_case:
        prompt_path = get_project_root() / test_case["prompt_file"]
        if not prompt_path.exists():
            result.valid = False
            result.errors.append(
                f"{file_path}: Referenced prompt not found: {test_case['prompt_file']}"
            )

    # Validate evaluation_criteria structure
    if "evaluation_criteria" in test_case:
        criteria = test_case["evaluation_criteria"]
        if not isinstance(criteria, list):
            result.valid = False
            result.errors.append(f"{file_path}: evaluation_criteria must be a list")
        else:
            for i, criterion in enumerate(criteria):
                if not isinstance(criterion, dict):
                    result.errors.append(
                        f"{file_path}: evaluation_criteria[{i}] must be a dict"
                    )
                elif "field" not in criterion:
                    result.warnings.append(
                        f"{file_path}: evaluation_criteria[{i}] missing 'field'"
                    )

    return result


def validate_test_cases(project_root: Path) -> ValidationResult:
    """Validate all test case files."""
    result = ValidationResult(valid=True)

    test_cases_dir = project_root / "evals" / "test-cases"
    if not test_cases_dir.exists():
        result.warnings.append("Test cases directory not found: evals/test-cases")
        return result

    for yaml_file in test_cases_dir.rglob("*.yaml"):
        file_result = validate_test_case(yaml_file)
        result.files_checked += file_result.files_checked
        result.errors.extend(file_result.errors)
        result.warnings.extend(file_result.warnings)
        if not file_result.valid:
            result.valid = False

    return result


def validate_config(project_root: Path) -> ValidationResult:
    """Validate the config.yaml file."""
    result = ValidationResult(valid=True)

    config_path = project_root / "evals" / "config.yaml"
    if not config_path.exists():
        result.valid = False
        result.errors.append("Config file not found: evals/config.yaml")
        return result

    result.files_checked = 1

    # Validate YAML syntax
    valid, error = validate_yaml_syntax(config_path)
    if not valid:
        result.valid = False
        result.errors.append(f"Config YAML syntax error: {error}")
        return result

    # Load and validate structure
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        result.valid = False
        result.errors.append(f"Cannot parse config: {e}")
        return result

    # Check required top-level keys
    required_keys = ["default_model", "evaluation", "thresholds"]
    for key in required_keys:
        if key not in config:
            result.valid = False
            result.errors.append(f"Config missing required key: {key}")

    # Validate thresholds structure
    if "thresholds" in config:
        thresholds = config["thresholds"]
        if "pass" not in thresholds or "warn" not in thresholds:
            result.warnings.append("Config thresholds missing 'pass' or 'warn' levels")

    return result


def validate_all(project_root: Path) -> ValidationResult:
    """Run all validations."""
    result = ValidationResult(valid=True)

    # Validate prompts
    prompt_result = validate_prompts(project_root)
    result.files_checked += prompt_result.files_checked
    result.errors.extend(prompt_result.errors)
    result.warnings.extend(prompt_result.warnings)
    if not prompt_result.valid:
        result.valid = False

    # Validate templates
    template_result = validate_templates(project_root)
    result.files_checked += template_result.files_checked
    result.errors.extend(template_result.errors)
    result.warnings.extend(template_result.warnings)
    if not template_result.valid:
        result.valid = False

    # Validate test cases
    test_result = validate_test_cases(project_root)
    result.files_checked += test_result.files_checked
    result.errors.extend(test_result.errors)
    result.warnings.extend(test_result.warnings)
    if not test_result.valid:
        result.valid = False

    # Validate config
    config_result = validate_config(project_root)
    result.files_checked += config_result.files_checked
    result.errors.extend(config_result.errors)
    result.warnings.extend(config_result.warnings)
    if not config_result.valid:
        result.valid = False

    return result


def print_result(result: ValidationResult, verbose: bool = False) -> None:
    """Print validation result."""
    if result.errors:
        print("\n❌ ERRORS:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings and verbose:
        print("\n⚠️  WARNINGS:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print(f"\n📊 Files checked: {result.files_checked}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Warnings: {len(result.warnings)}")

    if result.valid:
        print("\n✅ Validation PASSED")
    else:
        print("\n❌ Validation FAILED")


def main():
    parser = argparse.ArgumentParser(
        description="Validate prompt library structure and syntax"
    )
    parser.add_argument("--prompts", action="store_true", help="Validate prompts only")
    parser.add_argument(
        "--templates", action="store_true", help="Validate templates only"
    )
    parser.add_argument("--tests", action="store_true", help="Validate test cases only")
    parser.add_argument("--config", action="store_true", help="Validate config only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show warnings")

    args = parser.parse_args()

    project_root = get_project_root()

    # If no specific target, validate all
    if not any([args.prompts, args.templates, args.tests, args.config]):
        result = validate_all(project_root)
    else:
        result = ValidationResult(valid=True)

        if args.prompts:
            r = validate_prompts(project_root)
            result.files_checked += r.files_checked
            result.errors.extend(r.errors)
            result.warnings.extend(r.warnings)
            if not r.valid:
                result.valid = False

        if args.templates:
            r = validate_templates(project_root)
            result.files_checked += r.files_checked
            result.errors.extend(r.errors)
            result.warnings.extend(r.warnings)
            if not r.valid:
                result.valid = False

        if args.tests:
            r = validate_test_cases(project_root)
            result.files_checked += r.files_checked
            result.errors.extend(r.errors)
            result.warnings.extend(r.warnings)
            if not r.valid:
                result.valid = False

        if args.config:
            r = validate_config(project_root)
            result.files_checked += r.files_checked
            result.errors.extend(r.errors)
            result.warnings.extend(r.warnings)
            if not r.valid:
                result.valid = False

    print_result(result, verbose=args.verbose)
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
