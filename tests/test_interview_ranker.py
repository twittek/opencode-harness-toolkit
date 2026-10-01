#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "template/.agents/scripts/interview-ranker.py"
SPEC = importlib.util.spec_from_file_location("interview_ranker", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class InterviewRankerTest(unittest.TestCase):
    def test_selects_highest_information_gain(self):
        result = MODULE.rank(
            {
                "dimensions": {
                    "intent": {
                        "probabilities": [0.5, 0.5],
                        "impactWeight": 2,
                        "riskWeight": 1,
                    },
                    "testRunner": {
                        "probabilities": [0.5, 0.5],
                        "impactWeight": 0.25,
                        "riskWeight": 1,
                    },
                },
                "candidates": [
                    {
                        "id": "resolve-intent",
                        "answers": [
                            {"probability": 0.5, "posteriors": {"intent": [1, 0]}},
                            {"probability": 0.5, "posteriors": {"intent": [0, 1]}},
                        ],
                    },
                    {
                        "id": "resolve-test-runner",
                        "answers": [
                            {
                                "probability": 0.5,
                                "posteriors": {"testRunner": [1, 0]},
                            },
                            {
                                "probability": 0.5,
                                "posteriors": {"testRunner": [0, 1]},
                            },
                        ],
                    },
                ],
            }
        )
        self.assertEqual(result["selectedCandidate"], "resolve-intent")
        self.assertGreater(
            result["ranking"][0]["questionValue"],
            result["ranking"][1]["questionValue"],
        )

    def test_critical_unknown_restricts_eligible_candidates(self):
        result = MODULE.rank(
            {
                "criticalUnknowns": ["external-write-policy"],
                "dimensions": {
                    "safety": {"probabilities": [0.5, 0.5]},
                    "architecture": {"probabilities": [0.5, 0.5]},
                },
                "candidates": [
                    {
                        "id": "architecture",
                        "resolvesBlockingSafetyUnknown": False,
                        "answers": [
                            {
                                "probability": 1,
                                "posteriors": {"architecture": [1, 0]},
                            }
                        ],
                    },
                    {
                        "id": "safety",
                        "resolvesBlockingSafetyUnknown": True,
                        "answers": [
                            {
                                "probability": 1,
                                "posteriors": {"safety": [1, 0]},
                            }
                        ],
                    },
                ],
            }
        )
        self.assertEqual(result["selectedCandidate"], "safety")
        architecture = next(
            item for item in result["ranking"] if item["id"] == "architecture"
        )
        self.assertFalse(architecture["eligible"])

    def test_rejects_unknown_posterior_dimension(self):
        with self.assertRaises(ValueError):
            MODULE.rank(
                {
                    "dimensions": {"known": {"probabilities": [0.5, 0.5]}},
                    "candidates": [
                        {
                            "id": "bad",
                            "answers": [
                                {
                                    "probability": 1,
                                    "posteriors": {"unknown": [1, 0]},
                                }
                            ],
                        }
                    ],
                }
            )

    def test_rejects_negative_probabilities(self):
        with self.assertRaises(ValueError):
            MODULE.rank(
                {
                    "dimensions": {"intent": {"probabilities": [1.2, -0.2]}},
                    "candidates": [
                        {
                            "id": "intent",
                            "answers": [
                                {
                                    "probability": 1,
                                    "posteriors": {"intent": [1, 0]},
                                }
                            ],
                        }
                    ],
                }
            )


if __name__ == "__main__":
    unittest.main()
