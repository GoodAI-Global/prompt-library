"""
Tests for the offline validator.
No API keys required.
"""

import sys
from pathlib import Path
from unittest.mock import patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validate import (
    ValidationResult,
    validate_all,
    validate_config,
    validate_prompt_file,
    validate_prompts,
    validate_templates,
    validate_test_case,
    validate_test_cases,
    validate_yaml_syntax,
)


class TestYamlValidation:
    """Tests for YAML syntax validation."""

    def test_valid_yaml(self, tmp_path):
        yaml_file = tmp_path / "valid.yaml"
        yaml_file.write_text("key: value\nlist:\n  - item1\n  - item2\n")
        valid, error = validate_yaml_syntax(yaml_file)
        assert valid is True
        assert error is None

    def test_invalid_yaml(self, tmp_path):
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("key: value\n  bad indent: oops\n")
        valid, error = validate_yaml_syntax(yaml_file)
        assert valid is False
        assert error is not None


class TestPromptValidation:
    """Tests for prompt file validation."""

    def test_valid_prompt(self, tmp_path):
        prompt_file = tmp_path / "valid.md"
        prompt_file.write_text(
            """# Test Prompt

## Use Case
Test use case.

## Input Format
Test input.

## Output Format
Test output.

## The Prompt
```
This is a prompt with {{variable}}.
```

## Variables
| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| variable | string | Yes | Test |

## Examples
### Example 1
Test example.

## Gotchas
- Test gotcha

## Model Recommendations
- Claude Sonnet 4
"""
        )
        result = validate_prompt_file(prompt_file)
        assert result.valid is True
        assert len(result.errors) == 0

    def test_missing_sections(self, tmp_path):
        prompt_file = tmp_path / "incomplete.md"
        prompt_file.write_text(
            """# Incomplete Prompt

## Use Case
Test use case.
"""
        )
        result = validate_prompt_file(prompt_file)
        assert result.valid is False
        assert len(result.errors) > 0
        assert any("Missing section" in e for e in result.errors)

    def test_all_prompts_valid(self):
        """Validate all actual prompts in the repository."""
        project_root = Path(__file__).parent.parent
        result = validate_prompts(project_root)
        assert result.valid is True, f"Prompt errors: {result.errors}"
        assert result.files_checked >= 20  # We have 20 prompts


class TestTemplateValidation:
    """Tests for template validation."""

    def test_all_templates_valid(self):
        """Validate all actual templates in the repository."""
        project_root = Path(__file__).parent.parent
        result = validate_templates(project_root)
        assert result.valid is True, f"Template errors: {result.errors}"
        assert result.files_checked >= 8  # We have 8 templates


class TestTestCaseValidation:
    """Tests for test case validation."""

    def test_valid_test_case(self, tmp_path):
        # Create a mock prompt file
        prompt_dir = tmp_path / "operations"
        prompt_dir.mkdir()
        prompt_file = prompt_dir / "test.md"
        prompt_file.write_text("# Test")

        # Create test case
        test_file = tmp_path / "test.yaml"
        test_file.write_text(
            """name: "Test Case"
prompt_file: "operations/test.md"
input:
  key: value
expected_output:
  result: expected
evaluation_criteria:
  - field: result
    match_type: exact
"""
        )

        # Use patch to mock get_project_root in the validate module
        with patch("validate.get_project_root", return_value=tmp_path):
            result = validate_test_case(test_file)
            assert result.valid is True, f"Errors: {result.errors}"

    def test_missing_required_fields(self, tmp_path):
        test_file = tmp_path / "incomplete.yaml"
        test_file.write_text(
            """name: "Incomplete Test"
"""
        )
        result = validate_test_case(test_file)
        assert result.valid is False
        assert any("Missing required field" in e for e in result.errors)

    def test_all_test_cases_valid(self):
        """Validate all actual test cases in the repository."""
        project_root = Path(__file__).parent.parent
        result = validate_test_cases(project_root)
        assert result.valid is True, f"Test case errors: {result.errors}"
        assert result.files_checked >= 3  # We have 3 test cases


class TestConfigValidation:
    """Tests for config validation."""

    def test_config_valid(self):
        """Validate actual config file."""
        project_root = Path(__file__).parent.parent
        result = validate_config(project_root)
        assert result.valid is True, f"Config errors: {result.errors}"

    def test_config_missing_keys(self, tmp_path):
        config_file = tmp_path / "evals" / "config.yaml"
        config_file.parent.mkdir(parents=True)
        config_file.write_text("random_key: value\n")

        # Use patch to mock get_project_root
        with patch("validate.get_project_root", return_value=tmp_path):
            result = validate_config(tmp_path)
            assert result.valid is False
            assert any("missing required key" in e.lower() for e in result.errors)


class TestFullValidation:
    """Tests for full validation."""

    def test_validate_all(self):
        """Run full validation on actual repository."""
        project_root = Path(__file__).parent.parent
        result = validate_all(project_root)
        assert result.valid is True, f"Validation errors: {result.errors}"
        assert result.files_checked >= 30  # Prompts + templates + test cases + config


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_default_values(self):
        result = ValidationResult(valid=True)
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []
        assert result.files_checked == 0

    def test_with_errors(self):
        result = ValidationResult(
            valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
            files_checked=5,
        )
        assert result.valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1
        assert result.files_checked == 5
