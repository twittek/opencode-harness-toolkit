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
