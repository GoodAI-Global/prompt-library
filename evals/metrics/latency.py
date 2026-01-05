"""
Latency Metrics for Prompt Evaluation

Provides latency measurement and analysis functions.
"""

import statistics
from typing import Optional


def calculate_latency_stats(latencies: list[float]) -> dict:
    """
    Calculate latency statistics from a list of measurements.

    Args:
        latencies: List of latency values in milliseconds

    Returns:
        Dictionary with latency statistics
    """
    if not latencies:
        return {
            "count": 0,
            "min": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "p50": 0,
            "p90": 0,
            "p95": 0,
            "p99": 0,
            "std_dev": 0
        }

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)

    def percentile(p: float) -> float:
        """Calculate percentile value."""
        if n == 1:
            return sorted_latencies[0]
        k = (n - 1) * (p / 100)
        f = int(k)
        c = f + 1 if f + 1 < n else f
        return sorted_latencies[f] + (k - f) * (sorted_latencies[c] - sorted_latencies[f])

    return {
        "count": n,
        "min": min(latencies),
        "max": max(latencies),
        "mean": statistics.mean(latencies),
        "median": statistics.median(latencies),
        "p50": percentile(50),
        "p90": percentile(90),
        "p95": percentile(95),
        "p99": percentile(99),
        "std_dev": statistics.stdev(latencies) if n > 1 else 0
    }


def check_latency_thresholds(
    latencies: list[float],
    thresholds: Optional[dict] = None
) -> dict:
    """
    Check if latencies meet specified thresholds.

    Args:
        latencies: List of latency values in milliseconds
        thresholds: Dictionary with threshold values (p50, p90, p95, p99)

    Returns:
        Dictionary with pass/fail status for each threshold
    """
    if thresholds is None:
        thresholds = {
            "p50": 2000,   # 2 seconds
            "p90": 4000,   # 4 seconds
            "p95": 5000,   # 5 seconds
            "p99": 10000   # 10 seconds
        }

    stats = calculate_latency_stats(latencies)

    results = {
        "passed": True,
        "details": {}
    }

    for metric, threshold in thresholds.items():
        actual = stats.get(metric, 0)
        passed = actual <= threshold

        results["details"][metric] = {
            "threshold": threshold,
            "actual": actual,
            "passed": passed,
            "margin": threshold - actual
        }

        if not passed:
            results["passed"] = False

    return results


def format_latency(ms: float) -> str:
    """
    Format latency value for display.

    Args:
        ms: Latency in milliseconds

    Returns:
        Human-readable latency string
    """
    if ms < 1000:
        return f"{ms:.0f}ms"
    elif ms < 60000:
        return f"{ms / 1000:.2f}s"
    else:
        return f"{ms / 60000:.2f}m"


def detect_latency_anomalies(
    latencies: list[float],
    threshold_std: float = 2.0
) -> list[dict]:
    """
    Detect anomalous latency values.

    Args:
        latencies: List of latency values in milliseconds
        threshold_std: Number of standard deviations for anomaly detection

    Returns:
        List of detected anomalies
    """
    if len(latencies) < 3:
        return []

    mean = statistics.mean(latencies)
    std = statistics.stdev(latencies)

    anomalies = []
    for i, latency in enumerate(latencies):
        z_score = (latency - mean) / std if std > 0 else 0

        if abs(z_score) > threshold_std:
            anomalies.append({
                "index": i,
                "value": latency,
                "z_score": z_score,
                "type": "slow" if z_score > 0 else "fast"
            })

    return anomalies
