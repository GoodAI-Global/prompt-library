"""
Deterministic tests for the metrics module.
No API keys required - tests core functionality only.
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from metrics.accuracy import (
    exact_match,
    field_accuracy,
    json_validity,
    semantic_similarity,
)
from metrics.cost import calculate_cost, compare_model_costs, estimate_monthly_cost
from metrics.latency import (
    calculate_latency_stats,
    check_latency_thresholds,
    format_latency,
)


class TestAccuracyMetrics:
    """Tests for accuracy.py"""

    def test_exact_match_case_insensitive(self):
        assert exact_match("Hello", "hello") is True
        assert exact_match("HELLO", "hello") is True
        assert exact_match("Hello World", "hello world") is True

    def test_exact_match_case_sensitive(self):
        assert exact_match("Hello", "hello", case_sensitive=True) is False
        assert exact_match("Hello", "Hello", case_sensitive=True) is True

    def test_exact_match_with_whitespace(self):
        assert exact_match("  hello  ", "hello") is True
        assert exact_match("hello", "  hello  ") is True

    def test_field_accuracy_all_correct(self):
        actual = {"name": "John", "age": 30}
        expected = {"name": "John", "age": 30}
        result = field_accuracy(actual, expected)
        assert result["accuracy"] == 1.0
        assert result["correct_fields"] == 2
        assert len(result["missing_fields"]) == 0
        assert len(result["incorrect_fields"]) == 0

    def test_field_accuracy_missing_field(self):
        actual = {"name": "John"}
        expected = {"name": "John", "age": 30}
        result = field_accuracy(actual, expected)
        assert result["accuracy"] == 0.5
        assert "age" in result["missing_fields"]

    def test_field_accuracy_incorrect_field(self):
        actual = {"name": "Jane", "age": 30}
        expected = {"name": "John", "age": 30}
        result = field_accuracy(actual, expected)
        assert result["accuracy"] == 0.5
        assert "name" in result["incorrect_fields"]

    def test_json_validity_valid(self):
        result = json_validity('{"name": "John"}')
        assert result["is_valid"] is True
        assert result["structure"] == "dict"
        assert result["field_count"] == 1

    def test_json_validity_with_markdown(self):
        result = json_validity('```json\n{"name": "John"}\n```')
        assert result["is_valid"] is True

    def test_json_validity_invalid(self):
        result = json_validity("not valid json")
        assert result["is_valid"] is False
        assert result["error"] is not None

    def test_json_validity_embedded(self):
        result = json_validity('Here is the result: {"value": 42} end')
        assert result["is_valid"] is True
        assert result["field_count"] == 1

    def test_semantic_similarity_identical(self):
        score = semantic_similarity("hello world", "hello world")
        assert score == 1.0

    def test_semantic_similarity_different(self):
        score = semantic_similarity("hello world", "goodbye moon")
        assert score < 1.0
        assert score >= 0.0

    def test_semantic_similarity_partial(self):
        score = semantic_similarity("hello world", "hello there")
        assert 0 < score < 1.0


class TestLatencyMetrics:
    """Tests for latency.py"""

    def test_calculate_latency_stats_empty(self):
        result = calculate_latency_stats([])
        assert result["count"] == 0
        assert result["mean"] == 0

    def test_calculate_latency_stats_single(self):
        result = calculate_latency_stats([100.0])
        assert result["count"] == 1
        assert result["mean"] == 100.0
        assert result["min"] == 100.0
        assert result["max"] == 100.0

    def test_calculate_latency_stats_multiple(self):
        result = calculate_latency_stats([100.0, 200.0, 300.0])
        assert result["count"] == 3
        assert result["mean"] == 200.0
        assert result["min"] == 100.0
        assert result["max"] == 300.0
        assert result["median"] == 200.0

    def test_calculate_latency_stats_percentiles(self):
        latencies = list(range(1, 101))  # 1 to 100
        result = calculate_latency_stats([float(x) for x in latencies])
        assert result["p50"] == pytest.approx(50.0, rel=0.1)
        assert result["p90"] == pytest.approx(90.0, rel=0.1)
        assert result["p95"] == pytest.approx(95.0, rel=0.1)
        assert result["p99"] == pytest.approx(99.0, rel=0.1)

    def test_check_latency_thresholds_pass(self):
        latencies = [100.0, 200.0, 300.0]
        thresholds = {"p50": 500, "p90": 1000}
        result = check_latency_thresholds(latencies, thresholds)
        assert result["passed"] is True

    def test_check_latency_thresholds_fail(self):
        latencies = [1000.0, 2000.0, 3000.0]
        thresholds = {"p50": 500}
        result = check_latency_thresholds(latencies, thresholds)
        assert result["passed"] is False

    def test_format_latency_milliseconds(self):
        assert format_latency(500) == "500ms"
        assert format_latency(50) == "50ms"

    def test_format_latency_seconds(self):
        assert format_latency(1500) == "1.50s"
        assert format_latency(30000) == "30.00s"

    def test_format_latency_minutes(self):
        assert format_latency(120000) == "2.00m"


class TestCostMetrics:
    """Tests for cost.py"""

    def test_calculate_cost_sonnet(self):
        result = calculate_cost(1000, 500, "claude-sonnet-4-20250514")
        assert result["input_tokens"] == 1000
        assert result["output_tokens"] == 500
        assert result["total_tokens"] == 1500
        # 1000 input * $3/1M + 500 output * $15/1M
        expected_cost = (1000 / 1_000_000) * 3.0 + (500 / 1_000_000) * 15.0
        assert result["total_cost_usd"] == pytest.approx(expected_cost)

    def test_calculate_cost_opus(self):
        result = calculate_cost(1000, 500, "claude-opus-4-20250514")
        # 1000 input * $15/1M + 500 output * $75/1M
        expected_cost = (1000 / 1_000_000) * 15.0 + (500 / 1_000_000) * 75.0
        assert result["total_cost_usd"] == pytest.approx(expected_cost)

    def test_calculate_cost_haiku(self):
        result = calculate_cost(1000, 500, "claude-haiku-3-5-20241022")
        # 1000 input * $0.25/1M + 500 output * $1.25/1M
        expected_cost = (1000 / 1_000_000) * 0.25 + (500 / 1_000_000) * 1.25
        assert result["total_cost_usd"] == pytest.approx(expected_cost)

    def test_calculate_cost_unknown_model(self):
        # Should use default pricing
        result = calculate_cost(1000, 500, "unknown-model")
        assert result["total_cost_usd"] > 0

    def test_estimate_monthly_cost(self):
        result = estimate_monthly_cost(
            avg_input_tokens=1000,
            avg_output_tokens=500,
            requests_per_day=100,
            model="claude-sonnet-4-20250514",
        )
        assert result["requests_per_day"] == 100
        assert result["requests_per_month"] == 3000
        assert result["monthly_cost_usd"] > 0

    def test_compare_model_costs(self):
        result = compare_model_costs(1000, 500)
        assert len(result) > 0
        # Should be sorted by cost
        costs = [r["total_cost_usd"] for r in result]
        assert costs == sorted(costs)


class TestPromptStructure:
    """Tests for prompt file structure validation"""

    def test_all_prompts_have_required_sections(self):
        required_sections = [
            "## Use Case",
            "## The Prompt",
            "## Variables",
            "## Examples",
            "## Gotchas",
            "## Model Recommendations",
        ]

        project_root = Path(__file__).parent.parent.parent
        categories = [
            "operations",
            "insurance",
            "manufacturing",
            "healthcare",
            "analysis",
        ]

        errors = []
        for category in categories:
            category_path = project_root / category
            if category_path.exists():
                for prompt_file in category_path.glob("*.md"):
                    content = prompt_file.read_text()
                    missing = [s for s in required_sections if s not in content]
                    if missing:
                        errors.append(f"{prompt_file.name}: missing {missing}")

        assert len(errors) == 0, f"Prompts with missing sections: {errors}"

    def test_test_cases_have_required_fields(self):
        import yaml

        required_fields = [
            "name",
            "prompt_file",
            "input",
            "expected_output",
            "evaluation_criteria",
        ]

        project_root = Path(__file__).parent.parent
        test_cases_dir = project_root / "test-cases"

        errors = []
        for tc_file in test_cases_dir.rglob("*.yaml"):
            with open(tc_file) as f:
                tc = yaml.safe_load(f)
            missing = [field for field in required_fields if field not in tc]
            if missing:
                errors.append(f"{tc_file.name}: missing {missing}")

        assert len(errors) == 0, f"Test cases with missing fields: {errors}"


class TestConfigValidation:
    """Tests for configuration validation"""

    def test_config_yaml_loads(self):
        import yaml

        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "default_model" in config
        assert "evaluation" in config
        assert "thresholds" in config

    def test_config_has_valid_thresholds(self):
        import yaml

        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        thresholds = config.get("thresholds", {})
        assert "pass" in thresholds
        assert "warn" in thresholds
        assert (
            thresholds["pass"]["field_accuracy"] >= thresholds["warn"]["field_accuracy"]
        )
