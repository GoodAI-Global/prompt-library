"""
Cost Metrics for Prompt Evaluation

Provides cost calculation and estimation functions for LLM API usage.
"""

from typing import Optional


# Pricing per 1 million tokens (USD) - Updated January 2025
MODEL_PRICING = {
    # Anthropic Claude models
    "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
    "claude-haiku-3-5-20241022": {"input": 0.25, "output": 1.25},

    # OpenAI models (for comparison)
    "gpt-4o": {"input": 2.50, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.0, "output": 30.0},

    # Default fallback
    "default": {"input": 3.0, "output": 15.0}
}


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "default"
) -> dict:
    """
    Calculate cost for a single API call.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Model identifier

    Returns:
        Dictionary with cost breakdown
    """
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["default"])

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "total_cost_usd": total_cost,
        "model": model,
        "pricing": pricing
    }


def estimate_monthly_cost(
    avg_input_tokens: int,
    avg_output_tokens: int,
    requests_per_day: int,
    model: str = "default"
) -> dict:
    """
    Estimate monthly cost based on usage patterns.

    Args:
        avg_input_tokens: Average input tokens per request
        avg_output_tokens: Average output tokens per request
        requests_per_day: Expected requests per day
        model: Model identifier

    Returns:
        Dictionary with monthly cost estimate
    """
    single_cost = calculate_cost(avg_input_tokens, avg_output_tokens, model)
    requests_per_month = requests_per_day * 30

    monthly_input_tokens = avg_input_tokens * requests_per_month
    monthly_output_tokens = avg_output_tokens * requests_per_month

    monthly_cost = calculate_cost(monthly_input_tokens, monthly_output_tokens, model)

    return {
        "requests_per_day": requests_per_day,
        "requests_per_month": requests_per_month,
        "cost_per_request": single_cost["total_cost_usd"],
        "daily_cost_usd": single_cost["total_cost_usd"] * requests_per_day,
        "monthly_cost_usd": monthly_cost["total_cost_usd"],
        "monthly_input_tokens": monthly_input_tokens,
        "monthly_output_tokens": monthly_output_tokens,
        "model": model
    }


def compare_model_costs(
    input_tokens: int,
    output_tokens: int,
    models: Optional[list[str]] = None
) -> list[dict]:
    """
    Compare costs across different models.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        models: List of model identifiers to compare

    Returns:
        List of cost comparisons sorted by total cost
    """
    if models is None:
        models = list(MODEL_PRICING.keys())
        models.remove("default")

    comparisons = []
    for model in models:
        cost = calculate_cost(input_tokens, output_tokens, model)
        comparisons.append({
            "model": model,
            "total_cost_usd": cost["total_cost_usd"],
            "input_cost_usd": cost["input_cost_usd"],
            "output_cost_usd": cost["output_cost_usd"],
            "pricing": cost["pricing"]
        })

    # Sort by total cost
    comparisons.sort(key=lambda x: x["total_cost_usd"])

    # Add relative cost compared to cheapest
    if comparisons:
        cheapest = comparisons[0]["total_cost_usd"]
        for comp in comparisons:
            comp["relative_cost"] = (
                comp["total_cost_usd"] / cheapest
                if cheapest > 0 else 1.0
            )

    return comparisons


def calculate_batch_cost(
    requests: list[dict],
    model: str = "default"
) -> dict:
    """
    Calculate total cost for a batch of requests.

    Args:
        requests: List of dicts with 'input_tokens' and 'output_tokens'
        model: Model identifier

    Returns:
        Dictionary with batch cost summary
    """
    total_input = sum(r.get("input_tokens", 0) for r in requests)
    total_output = sum(r.get("output_tokens", 0) for r in requests)

    batch_cost = calculate_cost(total_input, total_output, model)

    return {
        "request_count": len(requests),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cost_usd": batch_cost["total_cost_usd"],
        "avg_cost_per_request": (
            batch_cost["total_cost_usd"] / len(requests)
            if requests else 0
        ),
        "model": model
    }


def format_cost(usd: float) -> str:
    """
    Format cost value for display.

    Args:
        usd: Cost in USD

    Returns:
        Human-readable cost string
    """
    if usd < 0.01:
        return f"${usd:.4f}"
    elif usd < 1:
        return f"${usd:.3f}"
    elif usd < 100:
        return f"${usd:.2f}"
    else:
        return f"${usd:,.0f}"
