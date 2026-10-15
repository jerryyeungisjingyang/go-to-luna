#!/usr/bin/env python3
"""Estimate main-model workload offload and credit-weighted savings."""

from __future__ import annotations

import argparse
import json
from typing import Any


RATE_CARD_DATE = "2026-10-15"
RATES = {
    "gpt-6.1-sol": (50.0, 250.0),
    "gpt-6-astra": (250.0, 1250.0),
    "gpt-6-sol": (50.0, 250.0),
    "gpt-6-luna": (2.5, 12.5),
    "gpt-5.6-sol": (100.0, 500.0),
    "gpt-5.6-terra": (50.0, 300.0),
    "gpt-5.6-luna": (5.0, 30.0),
    "gpt-5.5": (125.0, 750.0),
}
ALIASES = {
    "astra": "gpt-6-astra",
    "gpt-6.1": "gpt-6.1-sol",
    "sol6.1": "gpt-6.1-sol",
    "gpt-6": "gpt-6-sol",
    "sol6": "gpt-6-sol",
    "luna": "gpt-6-luna",
    "luna6": "gpt-6-luna",
    "luna5.6": "gpt-5.6-luna",
    "gpt-5.6": "gpt-5.6-sol",
    "sol": "gpt-5.6-sol",
    "terra": "gpt-5.6-terra",
}


def normalize_model(model: str) -> str:
    normalized = ALIASES.get(model.lower(), model.lower())
    if normalized not in RATES:
        supported = ", ".join(sorted(RATES))
        raise ValueError(f"unsupported main model: {model}; choose one of {supported}")
    return normalized


def calculate(
    main_model: str,
    coordinator_input: int,
    coordinator_output: int,
    worker_input: int,
    worker_output: int,
    source: str = "estimated",
    worker_model: str = "gpt-6-luna",
) -> dict[str, Any]:
    counts = (coordinator_input, coordinator_output, worker_input, worker_output)
    if any(value < 0 for value in counts):
        raise ValueError("token counts must be non-negative")

    normalized_model = normalize_model(main_model)
    normalized_worker_model = normalize_model(worker_model)
    main_input_rate, main_output_rate = RATES[normalized_model]
    worker_input_rate, worker_output_rate = RATES[normalized_worker_model]

    coordinator_tokens = coordinator_input + coordinator_output
    worker_tokens = worker_input + worker_output
    routed_tokens = coordinator_tokens + worker_tokens

    baseline_credits = (
        (coordinator_input + worker_input) * main_input_rate
        + (coordinator_output + worker_output) * main_output_rate
    ) / 1_000_000
    actual_credits = (
        coordinator_input * main_input_rate
        + coordinator_output * main_output_rate
        + worker_input * worker_input_rate
        + worker_output * worker_output_rate
    ) / 1_000_000
    saved_credits = max(0.0, baseline_credits - actual_credits)

    return {
        "source": source,
        "rate_card_date": RATE_CARD_DATE,
        "main_model": normalized_model,
        "worker_model": normalized_worker_model,
        "coordinator_tokens": coordinator_tokens,
        "worker_tokens": worker_tokens,
        "estimated_main_model_tokens_offloaded": worker_tokens,
        "estimated_main_workload_reduction_percent": round(
            worker_tokens / routed_tokens * 100, 2
        )
        if routed_tokens
        else 0.0,
        "baseline_weighted_credits": round(baseline_credits, 6),
        "actual_weighted_credits": round(actual_credits, 6),
        "estimated_weighted_credits_saved": round(saved_credits, 6),
        "estimated_weighted_saving_percent": round(
            saved_credits / baseline_credits * 100, 2
        )
        if baseline_credits
        else 0.0,
        "raw_total_token_saving": None,
        "note": (
            "Worker tokens are treated as work the current model would otherwise perform. "
            "Total raw-token savings are not claimed."
        ),
    }


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-model", required=True)
    parser.add_argument("--coordinator-input", type=non_negative_int, required=True)
    parser.add_argument("--coordinator-output", type=non_negative_int, required=True)
    parser.add_argument("--worker-input", type=non_negative_int, required=True)
    parser.add_argument("--worker-output", type=non_negative_int, required=True)
    parser.add_argument("--worker-model", default="gpt-6-luna")
    parser.add_argument("--source", choices=("actual", "estimated"), default="estimated")
    args = parser.parse_args()

    result = calculate(
        main_model=args.main_model,
        coordinator_input=args.coordinator_input,
        coordinator_output=args.coordinator_output,
        worker_input=args.worker_input,
        worker_output=args.worker_output,
        source=args.source,
        worker_model=args.worker_model,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
