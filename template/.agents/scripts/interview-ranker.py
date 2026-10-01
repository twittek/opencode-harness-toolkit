#!/usr/bin/env python3
"""Rank adaptive interview questions by weighted expected information gain.

The LLM supplies coarse beliefs and hypothetical posteriors. This helper performs
the entropy arithmetic deterministically and returns a sorted JSON result.
It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def entropy(probabilities: list[float]) -> float:
    if any(not math.isfinite(value) or value < 0 for value in probabilities):
        raise ValueError("probabilities must be finite and non-negative")
    total = sum(probabilities)
    if not probabilities or total <= 0:
        raise ValueError("probability distributions must contain positive mass")
    normalized = [value / total for value in probabilities]
    return -sum(value * math.log2(value) for value in normalized if value > 0)


def weighted_entropy(dimensions: dict[str, Any]) -> float:
    result = 0.0
    for dimension_id, dimension in dimensions.items():
        probabilities = dimension.get("probabilities")
        if not isinstance(probabilities, list):
            raise ValueError(f"dimension {dimension_id!r} has no probability list")
        impact = float(dimension.get("impactWeight", 1.0))
        risk = float(dimension.get("riskWeight", 1.0))
        if impact < 0 or risk < 0:
            raise ValueError(f"dimension {dimension_id!r} has a negative weight")
        result += entropy([float(value) for value in probabilities]) * impact * risk
    return result


def posterior_dimensions(
    current: dict[str, Any], posteriors: dict[str, list[float]]
) -> dict[str, Any]:
    result = {
        dimension_id: {
            "probabilities": list(dimension["probabilities"]),
            "impactWeight": dimension.get("impactWeight", 1.0),
            "riskWeight": dimension.get("riskWeight", 1.0),
        }
        for dimension_id, dimension in current.items()
    }
    for dimension_id, probabilities in posteriors.items():
        if dimension_id not in result:
            raise ValueError(f"posterior references unknown dimension {dimension_id!r}")
        result[dimension_id]["probabilities"] = probabilities
    return result


def rank(payload: dict[str, Any]) -> dict[str, Any]:
    dimensions = payload.get("dimensions")
    candidates = payload.get("candidates")
    if not isinstance(dimensions, dict) or not isinstance(candidates, list):
        raise ValueError("input requires object 'dimensions' and array 'candidates'")

    current_entropy = weighted_entropy(dimensions)
    critical_unknowns = payload.get("criticalUnknowns", [])
    restrict_to_blocking = bool(critical_unknowns)
    ranked: list[dict[str, Any]] = []

    for candidate in candidates:
        candidate_id = candidate.get("id")
        if not candidate_id:
            raise ValueError("every candidate requires an id")
        eligible = bool(candidate.get("eligible", True))
        resolves_blocking = bool(candidate.get("resolvesBlockingSafetyUnknown", False))
        if restrict_to_blocking and not resolves_blocking:
            eligible = False

        answers = candidate.get("answers", [])
        if not answers:
            raise ValueError(f"candidate {candidate_id!r} requires answer branches")

        branch_probabilities = [
            float(answer.get("probability", 0)) for answer in answers
        ]
        if any(
            not math.isfinite(probability) or probability < 0
            for probability in branch_probabilities
        ):
            raise ValueError(
                f"candidate {candidate_id!r} has invalid answer probabilities"
            )
        branch_mass = sum(branch_probabilities)
        if branch_mass <= 0:
            raise ValueError(f"candidate {candidate_id!r} has no answer probability mass")

        expected_posterior = 0.0
        for answer, branch_probability in zip(answers, branch_probabilities):
            probability = branch_probability / branch_mass
            posterior = posterior_dimensions(dimensions, answer.get("posteriors", {}))
            expected_posterior += probability * weighted_entropy(posterior)

        information_gain = max(0.0, current_entropy - expected_posterior)
        interaction_cost = float(candidate.get("interactionCost", 1.0))
        if not math.isfinite(interaction_cost) or interaction_cost <= 0:
            raise ValueError(f"candidate {candidate_id!r} has non-positive interaction cost")

        ranked.append(
            {
                "id": candidate_id,
                "eligible": eligible,
                "resolvesBlockingSafetyUnknown": resolves_blocking,
                "expectedPosteriorEntropy": round(expected_posterior, 6),
                "informationGain": round(information_gain, 6),
                "interactionCost": interaction_cost,
                "questionValue": round(information_gain / interaction_cost, 6),
            }
        )

    ranked.sort(key=lambda item: (item["eligible"], item["questionValue"]), reverse=True)
    selected = next((item["id"] for item in ranked if item["eligible"]), None)

    return {
        "currentWeightedEntropy": round(current_entropy, 6),
        "criticalRestrictionActive": restrict_to_blocking,
        "selectedCandidate": selected,
        "ranking": ranked,
    }


def load_payload(path: str | None) -> dict[str, Any]:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank interview candidates by weighted expected information gain."
    )
    parser.add_argument("input", nargs="?", help="JSON input file; stdin when omitted")
    args = parser.parse_args()

    try:
        result = rank(load_payload(args.input))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
