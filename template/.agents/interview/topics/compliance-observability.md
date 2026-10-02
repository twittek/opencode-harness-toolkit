---
id: compliance-observability
version: 1
dimensions:
  - compliance.rules
  - compliance.observer-signals
  - compliance.unknown-handling
  - compliance.thresholds
  - compliance.enforcement-mode
activation: policies, approvals, prohibitions, quality gates, external writes, production or regulated context
blocking-dimensions:
  - compliance.rules
  - compliance.observer-signals
  - compliance.unknown-handling
outputs:
  - .agents/policies/policy-registry.json
  - .agents/policies/policy-contract.md
  - .agents/context/compliance-policy.md
---

# Compliance and Observability

Resolve how normative harness rules can be evaluated from observer or decision-model signals.

## Evidence signals

```text
approval boundaries and forbidden actions
definition of done and quality gates
security and data-handling requirements
external write and deployment policies
available task, tool, repository, CI and runtime telemetry
decision-model outputs and model-version metadata
desired observer mode: collect, advise or enforce
```

## Candidate patterns

```text
Which concrete agent actions or outcomes must be scored for compliance?
Which observer facts prove each rule true or false?
What should happen when required evidence is missing: record, escalate or block?
Which violation-score thresholds should warn, escalate or block?
Should the control plane only report recommendations or enforce them?
```

Prefer questions that expose several policy predicates or telemetry gaps at once. Do not ask the user to invent metric names when repository and runtime evidence can supply them.

## Operationalization rule

Every normative answer must be convertible to the machine-evaluable contract in `../../policies/policy-contract.md`.

If a requirement contains ambiguous terms such as "appropriate" or "sufficient", derive a finite observable rubric or mark it as an open policy-design item. Do not generate an enforceable rule whose truth still depends on unbounded prose interpretation.

## Safe defaults

```text
missing evidence is UNKNOWN, never PASS
critical UNKNOWN results escalate
critical hard-gate failures block
observer and enforcer consume the same deterministic evaluation result
enforcement mode defaults to observe unless explicitly configured
thresholds remain configurable and versioned
```

## Completion

Complete when every generated normative rule has declared signals, deterministic applicability and assertion predicates, unknown handling, weight, severity and reason codes; thresholds and enforcement mode are explicit; and unobservable requirements are listed separately.
