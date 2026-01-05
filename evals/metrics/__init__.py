"""
Evaluation Metrics Module

Provides accuracy, latency, and cost metrics for prompt evaluation.
"""

from .accuracy import (
    exact_match,
    field_accuracy,
    semantic_similarity,
    json_validity,
    calculate_accuracy_report
)

from .latency import (
    calculate_latency_stats,
    check_latency_thresholds
)

from .cost import (
    calculate_cost,
    estimate_monthly_cost,
    compare_model_costs
)

__all__ = [
    # Accuracy
    "exact_match",
    "field_accuracy",
    "semantic_similarity",
    "json_validity",
    "calculate_accuracy_report",
    # Latency
    "calculate_latency_stats",
    "check_latency_thresholds",
    # Cost
    "calculate_cost",
    "estimate_monthly_cost",
    "compare_model_costs"
]
