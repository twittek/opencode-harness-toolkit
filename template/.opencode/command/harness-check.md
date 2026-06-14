---
description: "Audit the current harness version and write active findings."
---

# Harness Check Command

## Goal

Audit the current harness version for completeness, consistency, duplication, drift, safety and maintainability.

Do not modify harness files.

## Version scope

Read current version from:

`.agent/context/harness-version.json`

Write reports under:

`.agent/runs/harness-check/<current-version>/<date>/`

If version is missing, use `unknown` and create a critical finding.

## Output files

Create:
- `harness-inventory.md`
- `completeness-report.md`
- `consistency-report.md`
- `duplication-report.md`
- `drift-report.md`
- `safety-report.md`
- `maintainability-report.md`
- `active-findings.md`
- `recommended-actions.md`

## Finding format

```md
## FINDING-<version>-<number>: <title>

Status: active
Severity: critical|important|minor
Source: check
Detected in version: <version>
Target files:
- <path>

Problem:
...

Evidence:
...

Recommended action:
...

Risk:
...

Suggested update type: patch|minor|major
```

## Checks

Inspect harness files:
- `AGENTS.md`
- `opencode.jsonc` or `opencode.json`
- `.opencode/command/*.md`
- `.opencode/agent/*.md`
- `.agent/context/*.md`
- `.agent/playbooks/*.md`
- `.agent/templates/*.md`
- `.agent/skills/*.md`
- `.agent/scripts/*.sh`

Check:
- missing lifecycle files
- duplicate rules
- contradictions
- stale command names like `/create-harness`
- unclear autonomy boundaries
- unsafe shell patterns
- GitLab/GitHub guardrail gaps
- context strategy not 128K-friendly
- version/changelog hygiene

Final response in German:
- current version
- health rating: green/yellow/red
- number of active findings
- recommended next step

## Context Loading Policy checks

Check whether the harness uses the smallest useful context set.

Verify:

```text
- .agent/context/context-loading-policy.md exists
- Tier 1 baseline files are defined
- role-aware loading rules exist
- integration-aware loading rules exist
- run artifacts are not treated as always-loaded context
- generated/dependency folders are excluded
- the policy supports large context windows without encouraging context bloat
```

## Required self-verification

Before reporting completion, perform a self-verification pass.

Use:

```text
.agent/context/self-verification-policy.md
```

Verify:

```text
- requirement match: the result matches the user's request
- only intended files/content were changed
- relevant harness policies were followed
- available checks/tests were run or explicitly skipped with a reason
- remaining risks or assumptions are reported honestly
```
