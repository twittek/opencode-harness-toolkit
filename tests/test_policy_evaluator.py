#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "template/.agents/scripts/policy-evaluator.py"
SPEC = importlib.util.spec_from_file_location("policy_evaluator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def registry():
    return {
        "schemaVersion": "1.0",
        "registryId": "example.project-policy",
        "registryVersion": 1,
        "subject": "Example Project",
        "enforcementMode": "observe",
        "signals": [
            {
                "path": "task.hasCodeChanges",
                "type": "boolean",
                "source": "observer",
                "requiredProvenance": ["eventId"],
                "maxAgeSeconds": None,
            },
            {
                "path": "verification.requiredChecksPassed",
                "type": "boolean",
                "source": "observer",
                "requiredProvenance": ["eventId", "checkRunId"],
                "maxAgeSeconds": None,
            },
        ],
        "thresholds": {
            "warnAt": 0.25,
            "escalateAt": 0.5,
            "blockAt": 0.8,
            "minimumCoverage": 0.8,
        },
        "rules": [
            {
                "id": "quality.required-checks-pass",
                "version": 1,
                "title": "Required checks pass",
                "rationale": "Completion requires successful verification.",
                "severity": "critical",
                "weight": 3,
                "hardGate": True,
                "appliesWhen": {
                    "op": "eq",
                    "fact": "task.hasCodeChanges",
                    "value": True,
                },
                "assertion": {
                    "op": "eq",
                    "fact": "verification.requiredChecksPassed",
                    "value": True,
                },
                "requiredSignals": [
                    "task.hasCodeChanges",
                    "verification.requiredChecksPassed",
                ],
                "onUnknown": "escalate",
                "reasonCodes": {
                    "fail": "REQUIRED_CHECKS_FAILED",
                    "unknown": "REQUIRED_CHECKS_NOT_OBSERVED",
                },
                "source": "project-quality-policy",
            }
        ],
    }


def fact(value, **provenance):
    return {
        "value": value,
        "source": "observer",
        "observedAt": "2026-10-02T12:00:00Z",
        "provenance": provenance,
    }


class PolicyEvaluatorTest(unittest.TestCase):
    def test_pass_is_scored_without_escalation(self):
        result = MODULE.evaluate_registry(
            registry(),
            {
                "taskId": "task-1",
                "facts": {
                    "task.hasCodeChanges": fact(True, eventId="evt-1"),
                    "verification.requiredChecksPassed": fact(
                        True, eventId="evt-2", checkRunId="ci-1"
                    ),
                },
            },
        )

        self.assertEqual(result["rules"][0]["status"], "PASS")
        self.assertEqual(result["complianceScore"], 1.0)
        self.assertEqual(result["violationScore"], 0.0)
        self.assertEqual(result["coverage"], 1.0)
        self.assertEqual(result["recommendedAction"], "continue")

    def test_hard_gate_failure_blocks(self):
        result = MODULE.evaluate_registry(
            registry(),
            {
                "taskId": "task-2",
                "facts": {
                    "task.hasCodeChanges": fact(True, eventId="evt-1"),
                    "verification.requiredChecksPassed": fact(
                        False, eventId="evt-2", checkRunId="ci-1"
                    ),
                },
            },
        )

        self.assertEqual(result["rules"][0]["status"], "FAIL")
        self.assertEqual(result["violationScore"], 1.0)
        self.assertEqual(result["recommendedAction"], "block")
        self.assertIn("REQUIRED_CHECKS_FAILED", result["reasonCodes"])

    def test_missing_evidence_is_unknown_and_escalates(self):
        result = MODULE.evaluate_registry(
            registry(),
            {
                "taskId": "task-3",
                "facts": {
                    "task.hasCodeChanges": fact(True, eventId="evt-1")
                },
            },
        )

        self.assertEqual(result["rules"][0]["status"], "UNKNOWN")
        self.assertIsNone(result["rules"][0]["result"])
        self.assertIsNone(result["complianceScore"])
        self.assertEqual(result["coverage"], 0.0)
        self.assertEqual(result["recommendedAction"], "escalate")
        self.assertIn("POLICY_EVIDENCE_COVERAGE_LOW", result["reasonCodes"])

    def test_false_applicability_is_not_applicable(self):
        result = MODULE.evaluate_registry(
            registry(),
            {
                "taskId": "task-4",
                "facts": {
                    "task.hasCodeChanges": fact(False, eventId="evt-1")
                },
            },
        )

        self.assertEqual(result["rules"][0]["status"], "NOT_APPLICABLE")
        self.assertIsNone(result["complianceScore"])
        self.assertEqual(result["recommendedAction"], "continue")

    def test_registry_rejects_undeclared_predicate_fact(self):
        invalid = registry()
        invalid["rules"][0]["assertion"]["fact"] = "missing.signal"

        with self.assertRaises(MODULE.PolicyError):
            MODULE.validate_registry(invalid)

    def test_registry_rejects_unordered_thresholds(self):
        invalid = registry()
        invalid["thresholds"]["warnAt"] = 0.9

        with self.assertRaises(MODULE.PolicyError):
            MODULE.validate_registry(invalid)

    def test_registry_rejects_untyped_comparison_literal(self):
        invalid = registry()
        invalid["rules"][0]["assertion"]["value"] = "true"

        with self.assertRaises(MODULE.PolicyError):
            MODULE.validate_registry(invalid)

    def test_invalid_fact_type_is_unknown_not_pass(self):
        result = MODULE.evaluate_registry(
            registry(),
            {
                "taskId": "task-5",
                "facts": {
                    "task.hasCodeChanges": fact("true", eventId="evt-1")
                },
            },
        )

        self.assertEqual(result["rules"][0]["status"], "UNKNOWN")
        self.assertIsNone(result["rules"][0]["result"])
        self.assertEqual(result["recommendedAction"], "escalate")

    def test_decision_model_score_is_input_to_deterministic_threshold(self):
        model_registry = registry()
        model_registry["signals"] = [
            {
                "path": "decision.complianceProbability",
                "type": "number",
                "source": "decision-model",
                "requiredProvenance": ["eventId", "modelVersion", "confidence"],
                "maxAgeSeconds": None,
            }
        ]
        model_registry["rules"] = [
            {
                "id": "architecture.model-compliance",
                "version": 1,
                "title": "Architecture compliance exceeds threshold",
                "rationale": "The versioned decision model classifies the implementation.",
                "severity": "high",
                "weight": 2,
                "hardGate": False,
                "appliesWhen": {
                    "op": "gte",
                    "fact": "decision.complianceProbability",
                    "value": 0,
                },
                "assertion": {
                    "op": "gte",
                    "fact": "decision.complianceProbability",
                    "value": 0.8,
                },
                "requiredSignals": ["decision.complianceProbability"],
                "onUnknown": "escalate",
                "reasonCodes": {
                    "fail": "ARCHITECTURE_COMPLIANCE_BELOW_THRESHOLD",
                    "unknown": "ARCHITECTURE_MODEL_RESULT_MISSING",
                },
                "source": "architecture-policy",
            }
        ]

        result = MODULE.evaluate_registry(
            model_registry,
            {
                "taskId": "task-6",
                "facts": {
                    "decision.complianceProbability": {
                        "value": 0.7,
                        "source": "decision-model",
                        "observedAt": "2026-10-02T12:00:00Z",
                        "provenance": {
                            "eventId": "evt-model-1",
                            "modelVersion": "tdm-7",
                            "confidence": 0.92,
                        },
                    }
                },
            },
        )

        self.assertEqual(result["rules"][0]["status"], "FAIL")
        self.assertEqual(result["recommendedAction"], "block")
        self.assertEqual(result["enforcementMode"], "observe")


if __name__ == "__main__":
    unittest.main()
