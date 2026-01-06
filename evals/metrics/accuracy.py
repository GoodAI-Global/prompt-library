"""
Accuracy Metrics for Prompt Evaluation

Provides various accuracy measurement functions for comparing
LLM outputs against expected values.
"""

import json
import re
from typing import Any, Optional


def exact_match(actual: str, expected: str, case_sensitive: bool = False) -> bool:
    """
    Check if actual output exactly matches expected output.

    Args:
        actual: The actual output from the LLM
        expected: The expected output
        case_sensitive: Whether comparison should be case-sensitive

    Returns:
        True if outputs match exactly
    """
    if not case_sensitive:
        return actual.strip().lower() == expected.strip().lower()
    return actual.strip() == expected.strip()


def field_accuracy(
    actual: dict, expected: dict, required_fields: Optional[list] = None
) -> dict:
    """
    Calculate per-field accuracy between actual and expected dictionaries.

    Args:
        actual: The actual output dictionary
        expected: The expected output dictionary
        required_fields: List of fields that must be present and correct

    Returns:
        Dictionary with accuracy metrics per field and overall
    """
    if required_fields is None:
        required_fields = list(expected.keys())

    results = {
        "total_fields": len(required_fields),
        "correct_fields": 0,
        "missing_fields": [],
        "incorrect_fields": [],
        "field_details": {},
    }

    for field in required_fields:
        expected_value = expected.get(field)
        actual_value = actual.get(field) if actual else None

        if actual_value is None:
            results["missing_fields"].append(field)
            results["field_details"][field] = {
                "status": "missing",
                "expected": expected_value,
                "actual": None,
            }
        elif _values_match(actual_value, expected_value):
            results["correct_fields"] += 1
            results["field_details"][field] = {
                "status": "correct",
                "expected": expected_value,
                "actual": actual_value,
            }
        else:
            results["incorrect_fields"].append(field)
            results["field_details"][field] = {
                "status": "incorrect",
                "expected": expected_value,
                "actual": actual_value,
            }

    results["accuracy"] = (
        results["correct_fields"] / results["total_fields"]
        if results["total_fields"] > 0
        else 0
    )

    return results


def _values_match(actual: Any, expected: Any, tolerance: float = 0.01) -> bool:
    """Check if two values match, handling different types."""
    # Handle None
    if actual is None and expected is None:
        return True
    if actual is None or expected is None:
        return False

    # Handle numeric comparison with tolerance
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return abs(float(actual) - float(expected)) <= tolerance

    # Handle string comparison (case-insensitive, whitespace-normalized)
    if isinstance(expected, str) and isinstance(actual, str):
        return actual.strip().lower() == expected.strip().lower()

    # Handle list comparison
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return False
        return all(_values_match(a, e) for a, e in zip(actual, expected))

    # Handle dict comparison
    if isinstance(expected, dict) and isinstance(actual, dict):
        if set(expected.keys()) != set(actual.keys()):
            return False
        return all(_values_match(actual.get(k), v) for k, v in expected.items())

    # Fallback to string comparison
    return str(actual).strip().lower() == str(expected).strip().lower()


def semantic_similarity(actual: str, expected: str) -> float:
    """
    Calculate semantic similarity between two strings.

    This is a simplified implementation using token overlap.
    For production, consider using embeddings.

    Args:
        actual: The actual output text
        expected: The expected output text

    Returns:
        Similarity score between 0 and 1
    """
    # Tokenize (simple word-based)
    actual_tokens = set(re.findall(r"\w+", actual.lower()))
    expected_tokens = set(re.findall(r"\w+", expected.lower()))

    if not expected_tokens:
        return 1.0 if not actual_tokens else 0.0

    # Jaccard similarity
    intersection = len(actual_tokens & expected_tokens)
    union = len(actual_tokens | expected_tokens)

    return intersection / union if union > 0 else 0.0


def json_validity(output: str) -> dict:
    """
    Check if output is valid JSON and analyze its structure.

    Args:
        output: The raw output string

    Returns:
        Dictionary with validity status and details
    """
    result = {"is_valid": False, "error": None, "structure": None, "field_count": 0}

    # Clean up output
    cleaned = output.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [line for line in lines if not line.startswith("```")]
        cleaned = "\n".join(lines)

    try:
        parsed = json.loads(cleaned)
        result["is_valid"] = True
        result["structure"] = type(parsed).__name__

        if isinstance(parsed, dict):
            result["field_count"] = len(parsed)
        elif isinstance(parsed, list):
            result["field_count"] = len(parsed)

    except json.JSONDecodeError as e:
        result["error"] = str(e)

        # Try to extract JSON
        start = cleaned.find("{")
        if start != -1:
            end = cleaned.rfind("}") + 1
            if end > start:
                try:
                    parsed = json.loads(cleaned[start:end])
                    result["is_valid"] = True
                    result["structure"] = "dict"
                    result["field_count"] = (
                        len(parsed) if isinstance(parsed, dict) else 0
                    )
                    result["error"] = None
                    result["note"] = "Extracted from surrounding text"
                except json.JSONDecodeError:
                    pass

    return result


def calculate_accuracy_report(results: list, weights: Optional[dict] = None) -> dict:
    """
    Calculate aggregated accuracy report from multiple test results.

    Args:
        results: List of individual test results
        weights: Optional weights for different test categories

    Returns:
        Aggregated accuracy report
    """
    if not results:
        return {
            "total_tests": 0,
            "overall_accuracy": 0,
            "json_validity_rate": 0,
            "field_accuracy": 0,
        }

    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get("passed", False))
    valid_json = sum(1 for r in results if r.get("json_valid", False))

    total_fields = 0
    correct_fields = 0
    for result in results:
        field_results = result.get("field_results", {})
        for field, data in field_results.items():
            total_fields += 1
            if data.get("passed", False):
                correct_fields += 1

    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "overall_accuracy": passed_tests / total_tests * 100,
        "json_validity_rate": valid_json / total_tests * 100,
        "field_accuracy": (
            correct_fields / total_fields * 100 if total_fields > 0 else 0
        ),
        "total_fields_evaluated": total_fields,
        "correct_fields": correct_fields,
    }
