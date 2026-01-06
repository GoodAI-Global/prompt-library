#!/usr/bin/env python3
"""
Prompt Evaluation Runner

Executes test cases against prompts and generates evaluation reports.
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    from rich.console import Console
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Import metrics module
from metrics import (
    calculate_cost as metrics_calculate_cost,
)
from metrics import (
    calculate_latency_stats,
    check_latency_thresholds,
)

# Paths
EVALS_DIR = Path(__file__).parent
PROJECT_ROOT = EVALS_DIR.parent
TEST_CASES_DIR = EVALS_DIR / "test-cases"
CONFIG_FILE = EVALS_DIR / "config.yaml"


def load_config() -> dict:
    """Load configuration from config.yaml."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)
    return {}


# Load configuration
CONFIG = load_config()

# Configuration with fallbacks to config.yaml or defaults
DEFAULT_MODEL = CONFIG.get("default_model", "claude-sonnet-4-20250514")
DEFAULT_TEMPERATURE = CONFIG.get("evaluation", {}).get("temperature", 0)
DEFAULT_MAX_TOKENS = CONFIG.get("evaluation", {}).get("max_tokens", 4096)
TIMEOUT_SECONDS = CONFIG.get("evaluation", {}).get("timeout_seconds", 30)
RETRY_ATTEMPTS = CONFIG.get("evaluation", {}).get("retry_attempts", 2)

# Thresholds from config
THRESHOLDS = CONFIG.get(
    "thresholds",
    {
        "pass": {"field_accuracy": 95, "json_validity": 100},
        "warn": {"field_accuracy": 85, "json_validity": 95},
    },
)

# Performance targets from config
PERFORMANCE_TARGETS = CONFIG.get(
    "performance",
    {"latency_p50_ms": 2000, "latency_p95_ms": 5000, "latency_p99_ms": 10000},
)


@dataclass
class EvalResult:
    """Result of a single test case evaluation."""

    test_case: str
    prompt_file: str
    passed: bool
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    field_results: dict = field(default_factory=dict)
    latency_ms: float = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0
    raw_output: str = ""
    parsed_output: dict = field(default_factory=dict)


@dataclass
class EvalReport:
    """Aggregated evaluation report."""

    prompt: str
    model: str
    timestamp: str
    total_cases: int = 0
    passed: int = 0
    warnings: int = 0
    failed: int = 0
    field_accuracy: float = 0
    json_validity: float = 0
    avg_latency_ms: float = 0
    avg_cost_usd: float = 0
    total_cost_usd: float = 0
    latency_stats: dict = field(default_factory=dict)
    latency_check: dict = field(default_factory=dict)
    results: list = field(default_factory=list)


def load_prompt(prompt_file: str) -> str:
    """Load and extract prompt from markdown file."""
    prompt_path = PROJECT_ROOT / prompt_file
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    content = prompt_path.read_text()

    # Extract prompt between ```  markers in "## The Prompt" section
    prompt_match = re.search(r"## The Prompt\s*```[^\n]*\n(.*?)```", content, re.DOTALL)

    if prompt_match:
        return prompt_match.group(1).strip()

    raise ValueError(f"Could not extract prompt from {prompt_file}")


def load_test_case(test_case_path: Path) -> dict:
    """Load test case from YAML file."""
    with open(test_case_path) as f:
        return yaml.safe_load(f)


def substitute_variables(prompt: str, variables: dict) -> str:
    """Replace {{variable}} placeholders with values."""
    result = prompt

    for key, value in variables.items():
        # Handle both {{var}} and {{#if var}} patterns
        pattern = r"\{\{" + re.escape(key) + r"\}\}"
        result = re.sub(pattern, str(value), result)

    # Remove unfilled optional blocks {{#if ...}} ... {{/if}}
    result = re.sub(r"\{\{#if\s+\w+\}\}.*?\{\{/if\}\}", "", result, flags=re.DOTALL)

    return result


def call_llm(
    prompt: str, model: str, temperature: float = 0
) -> tuple[str, float, int, int]:
    """
    Call the LLM and return (response, latency_ms, input_tokens, output_tokens).
    """
    if Anthropic is None:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)

    start_time = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = (time.time() - start_time) * 1000

    output = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    return output, latency_ms, input_tokens, output_tokens


def parse_json_output(output: str) -> Optional[dict]:
    """Parse JSON from LLM output, handling common issues."""
    output = output.strip()

    # Remove markdown code blocks
    if output.startswith("```"):
        lines = output.split("\n")
        lines = [line for line in lines if not line.startswith("```")]
        output = "\n".join(lines)

    # Try direct parse
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object
    start = output.find("{")
    if start != -1:
        end = output.rfind("}") + 1
        if end > start:
            try:
                return json.loads(output[start:end])
            except json.JSONDecodeError:
                pass

    return None


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate API cost in USD using the metrics module."""
    cost_result = metrics_calculate_cost(input_tokens, output_tokens, model)
    return cost_result["total_cost_usd"]


def evaluate_field(
    actual: Any, expected: Any, match_type: str, tolerance: float = 0.01
) -> tuple[bool, str]:
    """Evaluate a single field against expected value."""
    if actual is None and expected is not None:
        return False, "Field missing"

    if match_type == "exact":
        if str(actual).lower().strip() == str(expected).lower().strip():
            return True, "Exact match"
        return False, f"Expected '{expected}', got '{actual}'"

    elif match_type == "numeric":
        try:
            actual_num = float(actual)
            expected_num = float(expected)
            if abs(actual_num - expected_num) <= tolerance:
                return True, "Numeric match"
            return False, f"Expected {expected_num}, got {actual_num}"
        except (ValueError, TypeError):
            return False, f"Could not parse as number: {actual}"

    elif match_type == "contains":
        if str(expected).lower() in str(actual).lower():
            return True, "Contains match"
        return False, f"'{expected}' not found in '{actual}'"

    elif match_type == "regex":
        if re.match(expected, str(actual)):
            return True, "Regex match"
        return False, f"'{actual}' does not match pattern '{expected}'"

    elif match_type == "array_contains":
        if not isinstance(actual, list):
            return False, "Expected array"
        # Simplified array check
        return True, "Array present"

    else:
        return False, f"Unknown match type: {match_type}"


def run_test_case(test_case: dict, model: str, temperature: float = 0) -> EvalResult:
    """Run a single test case and return result."""
    result = EvalResult(
        test_case=test_case.get("name", "unknown"),
        prompt_file=test_case.get("prompt_file", "unknown"),
    )

    try:
        # Load and prepare prompt
        prompt_template = load_prompt(test_case["prompt_file"])
        prompt = substitute_variables(prompt_template, test_case.get("input", {}))

        # Call LLM
        output, latency, input_tokens, output_tokens = call_llm(
            prompt, model, temperature
        )

        result.raw_output = output
        result.latency_ms = latency
        result.input_tokens = input_tokens
        result.output_tokens = output_tokens
        result.cost_usd = calculate_cost(input_tokens, output_tokens, model)

        # Parse output
        parsed = parse_json_output(output)
        if parsed is None:
            result.errors.append("Failed to parse JSON output")
            result.passed = False
            return result

        result.parsed_output = parsed

        # Evaluate fields
        expected = test_case.get("expected_output", {})
        criteria = test_case.get("evaluation_criteria", [])

        all_passed = True
        for criterion in criteria:
            field_name = criterion["field"]
            match_type = criterion.get("match_type", "exact")
            required = criterion.get("required", True)
            tolerance = criterion.get("tolerance", 0.01)

            # Get nested field value
            actual_value = parsed
            for key in field_name.split("."):
                if isinstance(actual_value, dict):
                    actual_value = actual_value.get(key)
                else:
                    actual_value = None
                    break

            expected_value = expected
            for key in field_name.split("."):
                if isinstance(expected_value, dict):
                    expected_value = expected_value.get(key)
                else:
                    expected_value = None
                    break

            passed, message = evaluate_field(
                actual_value, expected_value, match_type, tolerance
            )

            result.field_results[field_name] = {
                "passed": passed,
                "message": message,
                "required": required,
            }

            if not passed:
                if required:
                    result.errors.append(f"{field_name}: {message}")
                    all_passed = False
                else:
                    result.warnings.append(f"{field_name}: {message}")

        result.passed = all_passed

    except Exception as e:
        result.errors.append(str(e))
        result.passed = False

    return result


def discover_test_cases(
    category: Optional[str] = None, prompt: Optional[str] = None
) -> list[Path]:
    """Discover test case files based on filters."""
    test_cases = []

    if not TEST_CASES_DIR.exists():
        return test_cases

    for yaml_file in TEST_CASES_DIR.rglob("*.yaml"):
        # Apply filters
        if category and category not in str(yaml_file):
            continue
        if prompt and prompt not in str(yaml_file):
            continue
        test_cases.append(yaml_file)

    return sorted(test_cases)


def generate_report(
    results: list[EvalResult], model: str, prompt_name: str
) -> EvalReport:
    """Generate aggregated report from results."""
    report = EvalReport(
        prompt=prompt_name, model=model, timestamp=datetime.now().isoformat()
    )

    report.total_cases = len(results)
    report.results = results

    valid_json = 0
    total_fields = 0
    correct_fields = 0
    latencies = []
    total_cost = 0

    for result in results:
        if result.passed:
            report.passed += 1
        elif result.warnings and not result.errors:
            report.warnings += 1
        else:
            report.failed += 1

        if result.parsed_output:
            valid_json += 1

        for field_name, field_result in result.field_results.items():
            total_fields += 1
            if field_result["passed"]:
                correct_fields += 1

        latencies.append(result.latency_ms)
        total_cost += result.cost_usd

    if report.total_cases > 0:
        report.json_validity = (valid_json / report.total_cases) * 100
        report.avg_cost_usd = total_cost / report.total_cases
        report.total_cost_usd = total_cost

    if total_fields > 0:
        report.field_accuracy = (correct_fields / total_fields) * 100

    # Use metrics module for latency statistics
    if latencies:
        report.latency_stats = calculate_latency_stats(latencies)
        report.avg_latency_ms = report.latency_stats.get("mean", 0)

        # Check against performance targets from config
        latency_thresholds = {
            "p50": PERFORMANCE_TARGETS.get("latency_p50_ms", 2000),
            "p95": PERFORMANCE_TARGETS.get("latency_p95_ms", 5000),
            "p99": PERFORMANCE_TARGETS.get("latency_p99_ms", 10000),
        }
        report.latency_check = check_latency_thresholds(latencies, latency_thresholds)

    return report


def print_report(report: EvalReport):
    """Print formatted evaluation report."""
    if RICH_AVAILABLE:
        console = Console()

        console.print("\n" + "=" * 80)
        console.print("[bold]PROMPT EVALUATION REPORT[/bold]", justify="center")
        console.print("=" * 80)

        console.print(f"\nPrompt: [cyan]{report.prompt}[/cyan]")
        console.print(f"Model: [cyan]{report.model}[/cyan]")
        console.print(f"Test Cases: [cyan]{report.total_cases}[/cyan]")
        console.print("-" * 80)

        # Results table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status", justify="center")
        table.add_column("Count", justify="right")
        table.add_column("Percentage", justify="right")

        total = report.total_cases or 1
        table.add_row(
            "[green]✅ Passed[/green]",
            str(report.passed),
            f"{(report.passed / total) * 100:.1f}%",
        )
        table.add_row(
            "[yellow]⚠️ Warnings[/yellow]",
            str(report.warnings),
            f"{(report.warnings / total) * 100:.1f}%",
        )
        table.add_row(
            "[red]❌ Failed[/red]",
            str(report.failed),
            f"{(report.failed / total) * 100:.1f}%",
        )

        console.print("\n[bold]Results:[/bold]")
        console.print(table)

        # Metrics
        console.print("\n[bold]Metrics:[/bold]")
        console.print(f"  Field Accuracy: {report.field_accuracy:.1f}%")
        console.print(f"  JSON Validity: {report.json_validity:.1f}%")
        console.print(f"  Total Cost: ${report.total_cost_usd:.4f}")
        console.print(f"  Avg Cost/Request: ${report.avg_cost_usd:.4f}")

        # Latency stats from metrics module
        if report.latency_stats:
            console.print("\n[bold]Latency:[/bold]")
            stats = report.latency_stats
            console.print(f"  Mean: {stats.get('mean', 0):.0f}ms")
            console.print(f"  P50: {stats.get('p50', 0):.0f}ms")
            console.print(f"  P95: {stats.get('p95', 0):.0f}ms")
            console.print(f"  P99: {stats.get('p99', 0):.0f}ms")

            # Show latency threshold check
            if report.latency_check:
                status = (
                    "[green]PASSED[/green]"
                    if report.latency_check.get("passed")
                    else "[red]FAILED[/red]"
                )
                console.print(f"  Performance Check: {status}")

        # Failures
        if report.failed > 0:
            console.print("\n[bold red]Failed Cases:[/bold red]")
            for result in report.results:
                if not result.passed and result.errors:
                    console.print(f"  - {result.test_case}")
                    for error in result.errors:
                        console.print(f"    [red]{error}[/red]")

        # Warnings
        if report.warnings > 0:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for result in report.results:
                if result.warnings:
                    console.print(f"  - {result.test_case}")
                    for warning in result.warnings:
                        console.print(f"    [yellow]{warning}[/yellow]")

        console.print("\n" + "=" * 80)

    else:
        # Fallback plain text output
        print("\n" + "=" * 80)
        print("PROMPT EVALUATION REPORT")
        print("=" * 80)
        print(f"\nPrompt: {report.prompt}")
        print(f"Model: {report.model}")
        print(f"Test Cases: {report.total_cases}")
        print("-" * 80)

        total = report.total_cases or 1
        print("\nResults:")
        print(f"  Passed: {report.passed} ({(report.passed / total) * 100:.1f}%)")
        print(f"  Warnings: {report.warnings} ({(report.warnings / total) * 100:.1f}%)")
        print(f"  Failed: {report.failed} ({(report.failed / total) * 100:.1f}%)")

        print("\nMetrics:")
        print(f"  Field Accuracy: {report.field_accuracy:.1f}%")
        print(f"  JSON Validity: {report.json_validity:.1f}%")
        print(f"  Total Cost: ${report.total_cost_usd:.4f}")
        print(f"  Avg Cost/Request: ${report.avg_cost_usd:.4f}")

        if report.latency_stats:
            print("\nLatency:")
            stats = report.latency_stats
            print(f"  Mean: {stats.get('mean', 0):.0f}ms")
            print(f"  P50: {stats.get('p50', 0):.0f}ms")
            print(f"  P95: {stats.get('p95', 0):.0f}ms")
            print(f"  P99: {stats.get('p99', 0):.0f}ms")
            if report.latency_check:
                status = "PASSED" if report.latency_check.get("passed") else "FAILED"
                print(f"  Performance Check: {status}")

        print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Run prompt evaluations")
    parser.add_argument(
        "--category", help="Filter by category (operations, insurance, etc.)"
    )
    parser.add_argument("--prompt", help="Filter by prompt name")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--output", help="Output file for JSON results")
    parser.add_argument(
        "--fail-under", type=float, help="Fail if accuracy below threshold"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List test cases without running"
    )

    args = parser.parse_args()

    # Discover test cases
    test_cases = discover_test_cases(args.category, args.prompt)

    if not test_cases:
        print("No test cases found. Add test cases to evals/test-cases/")
        print("\nExpected structure:")
        print("  evals/test-cases/<category>/<prompt-name>/<test-name>.yaml")
        sys.exit(0)

    if args.dry_run:
        print(f"Found {len(test_cases)} test cases:")
        for tc in test_cases:
            print(f"  - {tc.relative_to(EVALS_DIR)}")
        sys.exit(0)

    # Run evaluations
    results = []
    print(f"\nRunning {len(test_cases)} test cases with {args.model}...\n")

    for test_case_path in test_cases:
        test_case = load_test_case(test_case_path)
        print(f"  Running: {test_case.get('name', test_case_path.stem)}...", end=" ")

        result = run_test_case(test_case, args.model, args.temperature)
        results.append(result)

        if result.passed:
            print("✅")
        elif result.warnings and not result.errors:
            print("⚠️")
        else:
            print("❌")

    # Generate and print report
    prompt_name = args.prompt or args.category or "all"
    report = generate_report(results, args.model, prompt_name)
    print_report(report)

    # Save results if requested
    if args.output:
        output_data = {
            "prompt": report.prompt,
            "model": report.model,
            "timestamp": report.timestamp,
            "summary": {
                "total": report.total_cases,
                "passed": report.passed,
                "warnings": report.warnings,
                "failed": report.failed,
                "field_accuracy": report.field_accuracy,
                "json_validity": report.json_validity,
                "avg_latency_ms": report.avg_latency_ms,
                "avg_cost_usd": report.avg_cost_usd,
            },
            "results": [
                {
                    "test_case": r.test_case,
                    "passed": r.passed,
                    "warnings": r.warnings,
                    "errors": r.errors,
                    "latency_ms": r.latency_ms,
                    "cost_usd": r.cost_usd,
                }
                for r in results
            ],
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to {args.output}")

    # Check threshold
    if args.fail_under:
        accuracy = (
            (report.passed / report.total_cases * 100) if report.total_cases > 0 else 0
        )
        if accuracy < args.fail_under:
            print(
                f"\n❌ Accuracy {accuracy:.1f}% is below threshold {args.fail_under}%"
            )
            sys.exit(1)

    sys.exit(0 if report.failed == 0 else 1)


if __name__ == "__main__":
    main()
