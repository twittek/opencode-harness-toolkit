#!/usr/bin/env python3

"""Validate and deterministically evaluate OpenCode Harness policy registries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {"boolean", "number", "integer", "string", "string-array"}
ALLOWED_SOURCES = {"observer", "decision-model", "static-policy"}
ALLOWED_UNKNOWN = {"record", "escalate", "block"}
ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}
ALLOWED_OPERATORS = {
    "all",
    "any",
    "not",
    "exists",
    "eq",
    "ne",
    "in",
    "not_in",
    "gt",
    "gte",
    "lt",
    "lte",
    "matches",
}
REASON_CODE = re.compile(r"^[A-Z][A-Z0-9_]+$")
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._-]+$")
FACT_PATH = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]+$")


class PolicyError(ValueError):
    pass


def load_json(path: str) -> Any:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def validate_keys(value: dict[str, Any], required: set[str], allowed: set[str], location: str) -> None:
    missing = required - set(value)
    extra = set(value) - allowed
    require(not missing, f"{location} is missing keys: {', '.join(sorted(missing))}")
    require(not extra, f"{location} has unsupported keys: {', '.join(sorted(extra))}")


def validate_predicate(predicate: Any, declared: dict[str, dict[str, Any]], location: str) -> None:
    require(isinstance(predicate, dict), f"{location} must be an object")
    op = predicate.get("op")
    require(op in ALLOWED_OPERATORS, f"{location}.op is unsupported: {op!r}")

    if op in {"all", "any"}:
        validate_keys(predicate, {"op", "args"}, {"op", "args"}, location)
        args = predicate.get("args")
        require(isinstance(args, list) and args, f"{location}.args must be non-empty")
        for index, child in enumerate(args):
            validate_predicate(child, declared, f"{location}.args[{index}]")
        return

    if op == "not":
        validate_keys(predicate, {"op", "arg"}, {"op", "arg"}, location)
        require("arg" in predicate, f"{location}.arg is required")
        validate_predicate(predicate["arg"], declared, f"{location}.arg")
        return

    fact = predicate.get("fact")
    require(isinstance(fact, str), f"{location}.fact is required")
    require(fact in declared, f"{location}.fact is not declared: {fact}")
    declared_type = declared[fact]["type"]

    if op in {"eq", "ne", "gt", "gte", "lt", "lte", "matches"}:
        validate_keys(predicate, {"op", "fact", "value"}, {"op", "fact", "value"}, location)
        require("value" in predicate, f"{location}.value is required")
        value = predicate["value"]
        if op in {"eq", "ne"}:
            require(value_matches_type(value, declared_type), f"{location}.value does not match signal type {declared_type}")
        elif op in {"gt", "gte", "lt", "lte"}:
            require(declared_type in {"number", "integer"}, f"{location}.{op} requires a numeric signal")
            require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{location}.value must be numeric")
        else:
            require(declared_type == "string" and isinstance(value, str), f"{location}.matches requires string operands")
            try:
                re.compile(value)
            except re.error as error:
                raise PolicyError(f"{location}.value is not a valid regular expression: {error}") from error
    elif op in {"in", "not_in"}:
        validate_keys(predicate, {"op", "fact", "values"}, {"op", "fact", "values"}, location)
        values = predicate.get("values")
        require(isinstance(values, list) and values, f"{location}.values must be non-empty")
        require(all(value_matches_type(value, declared_type) for value in values), f"{location}.values do not match signal type {declared_type}")
    else:
        validate_keys(predicate, {"op", "fact"}, {"op", "fact"}, location)


def validate_registry(registry: Any) -> dict[str, dict[str, Any]]:
    require(isinstance(registry, dict), "registry must be an object")
    validate_keys(
        registry,
        {"schemaVersion", "registryId", "registryVersion", "subject", "enforcementMode", "signals", "thresholds", "rules"},
        {"schemaVersion", "registryId", "registryVersion", "subject", "enforcementMode", "signals", "thresholds", "rules"},
        "registry",
    )
    require(registry.get("schemaVersion") == "1.0", "schemaVersion must be '1.0'")
    require(bool(IDENTIFIER.fullmatch(str(registry.get("registryId", "")))), "registryId is invalid")
    require(isinstance(registry.get("registryVersion"), int) and registry["registryVersion"] >= 1, "registryVersion must be a positive integer")
    require(isinstance(registry.get("subject"), str) and registry["subject"], "subject is required")
    require(registry.get("enforcementMode") in {"observe", "advise", "enforce"}, "enforcementMode is invalid")

    thresholds = registry.get("thresholds")
    require(isinstance(thresholds, dict), "thresholds must be an object")
    validate_keys(
        thresholds,
        {"warnAt", "escalateAt", "blockAt", "minimumCoverage"},
        {"warnAt", "escalateAt", "blockAt", "minimumCoverage"},
        "thresholds",
    )
    threshold_values = []
    for name in ("warnAt", "escalateAt", "blockAt", "minimumCoverage"):
        value = thresholds.get(name)
        require(isinstance(value, (int, float)) and not isinstance(value, bool), f"thresholds.{name} must be a number")
        require(0 <= value <= 1, f"thresholds.{name} must be in [0, 1]")
        if name != "minimumCoverage":
            threshold_values.append(float(value))
    require(threshold_values == sorted(threshold_values), "thresholds must satisfy warnAt <= escalateAt <= blockAt")

    signals = registry.get("signals")
    require(isinstance(signals, list), "signals must be an array")
    declarations: dict[str, dict[str, Any]] = {}
    for index, signal in enumerate(signals):
        location = f"signals[{index}]"
        require(isinstance(signal, dict), f"{location} must be an object")
        validate_keys(
            signal,
            {"path", "type", "source", "requiredProvenance", "maxAgeSeconds"},
            {"path", "type", "source", "requiredProvenance", "maxAgeSeconds", "description"},
            location,
        )
        path = signal.get("path")
        require(isinstance(path, str) and bool(FACT_PATH.fullmatch(path)), f"{location}.path is invalid")
        require(path not in declarations, f"duplicate signal path: {path}")
        require(signal.get("type") in ALLOWED_TYPES, f"{location}.type is invalid")
        require(signal.get("source") in ALLOWED_SOURCES, f"{location}.source is invalid")
        provenance = signal.get("requiredProvenance")
        require(isinstance(provenance, list) and all(isinstance(item, str) and item for item in provenance), f"{location}.requiredProvenance must be a string array")
        require(len(provenance) == len(set(provenance)), f"{location}.requiredProvenance contains duplicates")
        max_age = signal.get("maxAgeSeconds")
        require(max_age is None or (isinstance(max_age, int) and not isinstance(max_age, bool) and max_age >= 0), f"{location}.maxAgeSeconds must be a non-negative integer or null")
        declarations[path] = signal

    rules = registry.get("rules")
    require(isinstance(rules, list) and rules, "rules must be a non-empty array")
    rule_ids: set[str] = set()
    for index, rule in enumerate(rules):
        location = f"rules[{index}]"
        require(isinstance(rule, dict), f"{location} must be an object")
        validate_keys(
            rule,
            {"id", "version", "title", "rationale", "severity", "weight", "hardGate", "appliesWhen", "assertion", "requiredSignals", "onUnknown", "reasonCodes", "source"},
            {"id", "version", "title", "rationale", "severity", "weight", "hardGate", "appliesWhen", "assertion", "requiredSignals", "onUnknown", "reasonCodes", "source"},
            location,
        )
        rule_id = rule.get("id")
        require(isinstance(rule_id, str) and bool(IDENTIFIER.fullmatch(rule_id)), f"{location}.id is invalid")
        require(rule_id not in rule_ids, f"duplicate rule id: {rule_id}")
        rule_ids.add(rule_id)
        require(isinstance(rule.get("version"), int) and rule["version"] >= 1, f"{location}.version must be positive")
        for field in ("title", "rationale", "source"):
            require(isinstance(rule.get(field), str) and rule[field], f"{location}.{field} is required")
        require(rule.get("severity") in ALLOWED_SEVERITIES, f"{location}.severity is invalid")
        weight = rule.get("weight")
        require(isinstance(weight, (int, float)) and not isinstance(weight, bool) and weight > 0, f"{location}.weight must be positive")
        require(isinstance(rule.get("hardGate"), bool), f"{location}.hardGate must be boolean")
        require(rule.get("onUnknown") in ALLOWED_UNKNOWN, f"{location}.onUnknown is invalid")
        required = rule.get("requiredSignals")
        require(isinstance(required, list) and all(isinstance(item, str) for item in required), f"{location}.requiredSignals must be a string array")
        require(len(required) == len(set(required)), f"{location}.requiredSignals contains duplicates")
        for fact in required:
            require(fact in declarations, f"{location} requires undeclared signal: {fact}")
        reasons = rule.get("reasonCodes")
        require(isinstance(reasons, dict), f"{location}.reasonCodes must be an object")
        validate_keys(reasons, {"fail", "unknown"}, {"fail", "unknown"}, f"{location}.reasonCodes")
        for key in ("fail", "unknown"):
            require(bool(REASON_CODE.fullmatch(str(reasons.get(key, "")))), f"{location}.reasonCodes.{key} is invalid")
        validate_predicate(rule.get("appliesWhen"), declarations, f"{location}.appliesWhen")
        validate_predicate(rule.get("assertion"), declarations, f"{location}.assertion")

    return declarations


def value_matches_type(value: Any, declared_type: str) -> bool:
    if declared_type == "boolean":
        return isinstance(value, bool)
    if declared_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared_type == "string":
        return isinstance(value, str)
    if declared_type == "string-array":
        return isinstance(value, list) and all(isinstance(item, str) for item in value)
    return False


def usable_facts(evidence: Any, declarations: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, list[str]]]:
    require(isinstance(evidence, dict), "evidence must be an object")
    require(isinstance(evidence.get("taskId"), str) and evidence["taskId"], "evidence.taskId is required")
    supplied = evidence.get("facts")
    require(isinstance(supplied, dict), "evidence.facts must be an object")
    values: dict[str, Any] = {}
    refs: dict[str, list[str]] = {}
    for path, declaration in declarations.items():
        envelope = supplied.get(path)
        if not isinstance(envelope, dict):
            continue
        if envelope.get("source") != declaration["source"]:
            continue
        value = envelope.get("value")
        if not value_matches_type(value, declaration["type"]):
            continue
        provenance = envelope.get("provenance")
        if not isinstance(provenance, dict):
            continue
        required = declaration["requiredProvenance"]
        if any(key not in provenance or provenance[key] in (None, "") for key in required):
            continue
        observed_at = envelope.get("observedAt")
        if not isinstance(observed_at, str):
            continue
        try:
            observed = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        except ValueError:
            continue
        if observed.tzinfo is None:
            continue
        max_age = declaration["maxAgeSeconds"]
        if max_age is not None and (datetime.now(timezone.utc) - observed).total_seconds() > max_age:
            continue
        values[path] = value
        refs[path] = [str(provenance[key]) for key in required]
    return values, refs


def evaluate_predicate(predicate: dict[str, Any], facts: dict[str, Any]) -> bool | None:
    op = predicate["op"]
    if op in {"all", "any"}:
        results = [evaluate_predicate(item, facts) for item in predicate["args"]]
        if op == "all":
            if False in results:
                return False
            return None if None in results else True
        if True in results:
            return True
        return None if None in results else False
    if op == "not":
        result = evaluate_predicate(predicate["arg"], facts)
        return None if result is None else not result

    fact = predicate["fact"]
    if op == "exists":
        return fact in facts
    if fact not in facts:
        return None

    actual = facts[fact]
    expected = predicate.get("value")
    if op == "eq":
        return actual == expected
    if op == "ne":
        return actual != expected
    if op == "in":
        return actual in predicate["values"]
    if op == "not_in":
        return actual not in predicate["values"]
    if op == "matches":
        return isinstance(actual, str) and re.search(str(expected), actual) is not None
    if op in {"gt", "gte", "lt", "lte"}:
        if not isinstance(actual, (int, float)) or isinstance(actual, bool):
            return None
        if not isinstance(expected, (int, float)) or isinstance(expected, bool):
            return None
        return {
            "gt": actual > expected,
            "gte": actual >= expected,
            "lt": actual < expected,
            "lte": actual <= expected,
        }[op]
    raise PolicyError(f"unsupported operator during evaluation: {op}")


def predicate_facts(predicate: dict[str, Any]) -> set[str]:
    op = predicate["op"]
    if op in {"all", "any"}:
        return set().union(*(predicate_facts(item) for item in predicate["args"]))
    if op == "not":
        return predicate_facts(predicate["arg"])
    return {predicate["fact"]}


def action_rank(action: str) -> int:
    return {"continue": 0, "warn": 1, "escalate": 2, "block": 3}[action]


def maximum_action(current: str, candidate: str) -> str:
    return candidate if action_rank(candidate) > action_rank(current) else current


def evaluate_registry(registry: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    declarations = validate_registry(registry)
    facts, refs = usable_facts(evidence, declarations)
    results = []
    evaluable_weight = 0.0
    applicable_weight = 0.0
    failed_weight = 0.0
    action = "continue"
    reason_codes: set[str] = set()

    for rule in registry["rules"]:
        weight = float(rule["weight"])
        applies = evaluate_predicate(rule["appliesWhen"], facts)
        status: str
        result: bool | None
        violation: float | None
        reason: str | None = None

        if applies is False:
            status, result, violation = "NOT_APPLICABLE", None, None
        elif applies is None:
            status, result, violation = "UNKNOWN", None, None
            applicable_weight += weight
            reason = rule["reasonCodes"]["unknown"]
        elif any(path not in facts for path in rule["requiredSignals"]):
            status, result, violation = "UNKNOWN", None, None
            applicable_weight += weight
            reason = rule["reasonCodes"]["unknown"]
        else:
            assertion = evaluate_predicate(rule["assertion"], facts)
            applicable_weight += weight
            if assertion is None:
                status, result, violation = "UNKNOWN", None, None
                reason = rule["reasonCodes"]["unknown"]
            elif assertion:
                status, result, violation = "PASS", True, 0.0
                evaluable_weight += weight
            else:
                status, result, violation = "FAIL", False, 1.0
                evaluable_weight += weight
                failed_weight += weight
                reason = rule["reasonCodes"]["fail"]

        if status == "FAIL" and rule["hardGate"]:
            action = maximum_action(action, "block")
        if status == "UNKNOWN":
            action = maximum_action(action, {"record": "continue", "escalate": "escalate", "block": "block"}[rule["onUnknown"]])
        if reason:
            reason_codes.add(reason)

        used_paths = predicate_facts(rule["appliesWhen"]) | predicate_facts(rule["assertion"]) | set(rule["requiredSignals"])
        evidence_refs = sorted({ref for path in used_paths for ref in refs.get(path, [])})
        results.append(
            {
                "ruleId": rule["id"],
                "ruleVersion": rule["version"],
                "status": status,
                "result": result,
                "violationValue": violation,
                "reasonCode": reason,
                "evidenceRefs": evidence_refs,
            }
        )

    violation_score = None if evaluable_weight == 0 else failed_weight / evaluable_weight
    compliance_score = None if violation_score is None else 1.0 - violation_score
    coverage = 0.0 if applicable_weight == 0 else evaluable_weight / applicable_weight
    thresholds = registry["thresholds"]

    if applicable_weight > 0 and coverage < thresholds["minimumCoverage"]:
        action = maximum_action(action, "escalate")
        reason_codes.add("POLICY_EVIDENCE_COVERAGE_LOW")
    if violation_score is not None:
        if violation_score >= thresholds["blockAt"]:
            action = maximum_action(action, "block")
        elif violation_score >= thresholds["escalateAt"]:
            action = maximum_action(action, "escalate")
        elif violation_score >= thresholds["warnAt"]:
            action = maximum_action(action, "warn")

    return {
        "registryId": registry["registryId"],
        "registryVersion": registry["registryVersion"],
        "enforcementMode": registry["enforcementMode"],
        "taskId": evidence["taskId"],
        "evaluatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "complianceScore": compliance_score,
        "violationScore": violation_score,
        "coverage": coverage,
        "recommendedAction": action,
        "reasonCodes": sorted(reason_codes),
        "rules": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a policy registry")
    validate.add_argument("registry")
    evaluate = subparsers.add_parser("evaluate", help="evaluate a registry against task evidence")
    evaluate.add_argument("registry")
    evaluate.add_argument("evidence")
    args = parser.parse_args()

    try:
        registry = load_json(args.registry)
        if args.command == "validate":
            declarations = validate_registry(registry)
            print(json.dumps({"valid": True, "signals": len(declarations), "rules": len(registry["rules"])}, indent=2))
        else:
            result = evaluate_registry(registry, load_json(args.evidence))
            print(json.dumps(result, indent=2, sort_keys=True))
    except (OSError, json.JSONDecodeError, PolicyError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
