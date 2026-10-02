# Machine-Evaluable Policy Contract

This contract defines how project policies and compliance rules must be represented so an observer and policy engine can evaluate them without interpreting normative prose.

## Separation of responsibilities

```text
Harness policy registry
→ defines versioned rules, typed signals, predicates, weights and thresholds

Observer or telemetry sidecar
→ emits typed facts with timestamps, provenance and task correlation

Decision model
→ may emit a typed score or classification only when declared as a signal source

Policy evaluator
→ evaluates predicates and calculates rule and aggregate results deterministically

Control plane or enforcer
→ maps evaluator results to observe, warn, repair, block or escalate actions
```

The decision model does not invent policies and does not choose enforcement actions.

## Canonical files

```text
.agents/policies/policy-registry.json
.agents/policies/policy-registry.schema.json
.agents/policies/task-evidence.schema.json
.agents/policies/evaluation-result.schema.json
.agents/policies/policy-contract.md
```

`policy-registry.json` is the normative source. Markdown context files may explain it, but explanatory prose must not override or weaken a machine rule.

Minimal registry shape:

```json
{
  "schemaVersion": "1.0",
  "registryId": "example.project-policy",
  "registryVersion": 1,
  "subject": "Example Project",
  "enforcementMode": "observe",
  "signals": [
    {
      "path": "action.requiresApproval",
      "type": "boolean",
      "source": "observer",
      "requiredProvenance": ["eventId"],
      "maxAgeSeconds": 86400
    },
    {
      "path": "approval.present",
      "type": "boolean",
      "source": "observer",
      "requiredProvenance": ["eventId", "approvalId"],
      "maxAgeSeconds": 86400
    }
  ],
  "thresholds": {
    "warnAt": 0.25,
    "escalateAt": 0.5,
    "blockAt": 0.8,
    "minimumCoverage": 0.8
  },
  "rules": [
    {
      "id": "governance.approval-present",
      "version": 1,
      "title": "Approval-gated actions have approval",
      "rationale": "Configured high-impact actions require explicit approval.",
      "severity": "critical",
      "weight": 5,
      "hardGate": true,
      "appliesWhen": { "op": "eq", "fact": "action.requiresApproval", "value": true },
      "assertion": { "op": "eq", "fact": "approval.present", "value": true },
      "requiredSignals": ["action.requiresApproval", "approval.present"],
      "onUnknown": "block",
      "reasonCodes": {
        "fail": "REQUIRED_APPROVAL_MISSING",
        "unknown": "APPROVAL_STATE_NOT_OBSERVED"
      },
      "source": "project-autonomy-policy"
    }
  ]
}
```

The generated registry must contain at least one rule. `enforcementMode` changes whether the control plane executes the recommendation; it does not change evaluation truth or scores.

## Rule requirements

Every normative rule must define:

```text
stable rule id and integer version
human-readable title and rationale
scope and applicability predicate
typed signal declarations
signal freshness through maxAgeSeconds or an explicit null for immutable evidence
deterministic assertion predicate
severity and positive weight
behavior for missing evidence
stable reason codes
source or owner reference
```

A statement such as "changes should be well tested" is prohibited as a normative rule. It must be operationalized, for example:

```json
{
  "id": "quality.required-checks-pass",
  "version": 1,
  "title": "Required checks pass before completion",
  "severity": "high",
  "weight": 3,
  "hardGate": true,
  "appliesWhen": { "op": "eq", "fact": "task.hasCodeChanges", "value": true },
  "assertion": { "op": "eq", "fact": "verification.requiredChecksPassed", "value": true },
  "requiredSignals": ["task.hasCodeChanges", "verification.requiredChecksPassed"],
  "onUnknown": "escalate",
  "reasonCodes": {
    "fail": "REQUIRED_CHECKS_FAILED",
    "unknown": "REQUIRED_CHECKS_NOT_OBSERVED"
  },
  "source": "project-quality-policy"
}
```

## Predicate language

Only these operators are allowed:

```text
all, any, not
exists
eq, ne
in, not_in
gt, gte, lt, lte
matches
```

Predicates operate only on declared fact paths. No natural-language condition, executable code, shell expression or implicit coercion is allowed.

## Evaluation states

Every rule produces exactly one state:

| Status | Boolean result | Meaning |
|---|---:|---|
| `PASS` | `true` | Rule applies and its assertion is true. |
| `FAIL` | `false` | Rule applies and its assertion is false. |
| `UNKNOWN` | `null` | Applicability or assertion cannot be evaluated from valid evidence. |
| `NOT_APPLICABLE` | `null` | Applicability predicate is definitively false. |
| `ERROR` | `null` | Registry, type contract or evaluator execution is invalid. |

`UNKNOWN`, `NOT_APPLICABLE` and `ERROR` must never be collapsed into `PASS`.

The standalone evaluator exits non-zero when the registry or evaluation process is invalid. A hosting control plane must represent that failure as `ERROR` and escalate it; evaluator failure must never be interpreted as compliance.

## Scoring

For evaluable applicable rules:

```text
PASS violation value = 0
FAIL violation value = 1

violationScore
  = Σ(rule weight × violation value)
    / Σ(weight of PASS and FAIL rules)

coverage
  = Σ(weight of PASS and FAIL rules)
    / Σ(weight of PASS, FAIL and UNKNOWN rules)

complianceScore = 1 - violationScore
```

Scores are in `[0, 1]`. If no applicable rule is evaluable, scores are `null` and coverage is `0`.

Unknown handling is explicit per rule:

```text
record    → retain UNKNOWN and let minimumCoverage govern aggregate escalation
escalate  → recommend escalation immediately
block     → recommend block immediately
```

## Thresholds and enforcement

The registry defines ordered thresholds:

```text
warnAt <= escalateAt <= blockAt
minimumCoverage in [0, 1]
```

Recommended action is derived deterministically:

```text
hard-gate FAIL or onUnknown=block → block
onUnknown=escalate                → escalate
coverage < minimumCoverage        → escalate
violationScore >= blockAt         → block
violationScore >= escalateAt      → escalate
violationScore >= warnAt          → warn
otherwise                         → continue
```

An observer may report the recommendation without enforcing it. An enforcer may execute it according to control-plane configuration. Both use the same evaluation result.

## Decision-model signals

A decision model may supply facts such as:

```text
decision.architectureComplianceProbability: number
decision.classification: string
decision.confidence: number
```

The registry must declare their types, source as `decision-model`, model/version provenance requirements and exact thresholds. The policy engine evaluates the threshold; the model does not decide the action.

If model confidence or provenance is missing, the affected rule is `UNKNOWN`.

## Observer fact envelope

The evaluator expects task evidence in this shape:

```json
{
  "taskId": "4711",
  "facts": {
    "verification.requiredChecksPassed": {
      "value": true,
      "source": "observer",
      "observedAt": "2026-10-02T12:00:00Z",
      "provenance": {
        "eventId": "evt-123",
        "checkRunId": "ci-456"
      }
    }
  }
}
```

The fact value must match the type declared in the registry. `source` must match the declared source. Every key listed in `requiredProvenance` must be present and non-empty. `observedAt` must be a timezone-aware timestamp; when `maxAgeSeconds` is an integer, older evidence is rejected. Use `null` only for immutable evidence whose age does not affect truth. Invalid, stale or incomplete facts are treated as missing evidence and therefore produce `UNKNOWN` where required.

## Prohibited policy forms

Do not generate normative rules that rely on:

```text
"appropriate", "reasonable", "sufficient", "high quality" or similar terms without a measurable rubric
unstated evidence
free-form LLM judgment as the final decision
implicit defaults for missing signals
unversioned model scores
a score without reason codes and evidence references
```

When a requirement cannot yet be operationalized, record it as an open policy-design item, not as an enforceable rule.
