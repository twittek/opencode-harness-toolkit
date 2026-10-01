---
id: quality-verification
version: 1
dimensions:
  - quality.gates
  - quality.test-strategy
  - quality.definition-of-done
  - quality.self-verification
activation: always-considered
outputs:
  - .agent/context/definition-of-done.md
  - .agent/context/self-verification-policy.md
  - .agent/scripts/quality-gates.sh
---

# Quality and Verification

Resolve the smallest meaningful set of checks required for the actual project and task types.

## Evidence signals

```text
test scripts and configuration
lint and typecheck configuration
build system
CI required checks
existing definition of done
```

## Candidate patterns

```text
Which existing checks are mandatory before an agent reports completion?
Which critical behavior lacks automated coverage and needs a manual check?
How strict must final self-verification be for risky changes?
```

Do not ask the user to enumerate tools already visible in project manifests. Ask about policy and missing expectations.

## Safe default

Use standard self-verification and existing project checks when no stronger requirement is indicated.

## Completion

Complete when definition of done, executable checks and evidence expectations can be generated.
