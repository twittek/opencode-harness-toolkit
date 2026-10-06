---
description: "Apply active findings for the current harness version."
---

# Harness Update Command

## Goal

Apply active findings for the current harness version, update the changelog, and increment the harness version.

## Inputs

Read current version from:

`.agents/context/harness-version.json`

Look for active findings in:

```text
.agents/runs/harness-check/<current-version>/*/active-findings.md
.agents/runs/harness-check/<current-version>/*/recommended-actions.md
.agents/runs/harness-retro/<current-version>/*/active-findings.md
.agents/runs/harness-retro/<current-version>/*/proposed-changes.md
.agents/runs/harness-retro/<current-version>/*/patch-plan.md
```

If no active findings exist for the current version, stop and answer in German:

"Für die aktuelle Harness-Version sind keine aktiven Findings vorhanden. Führe `/harness-check` aus, um die Harness erneut zu prüfen, oder `/harness-retro`, um nutzungsbasiertes Feedback aufzunehmen."

Do not make changes without active findings.

## Output directory

Create:

`.agents/runs/harness-update/<current-version>/<date>/`

Write:
- `input-findings.md`
- `update-plan.md`
- `approval-request.md`
- `applied-changes.md`
- `version-bump.md`
- `post-update-check.md`

## Approval gate

Create the update plan first.

Then ask in German:

"Ich habe einen Update-Plan für die aktuelle Harness-Version erstellt. Soll ich alle Änderungen anwenden, nur bestimmte Punkte anwenden oder abbrechen?"

Do not edit harness files without explicit approval.

When an approved update changes normative behavior:

```text
- update the canonical rule in .agents/policies/policy-registry.json
- increment the changed rule version and registry version
- update human-readable policy views to reference the rule id
- validate the registry with .agents/scripts/policy-evaluator.py validate
- preserve explicit UNKNOWN and threshold behavior
- record the policy change in the harness changelog
```

Do not change enforcement thresholds, hard gates or missing-evidence behavior through prose-only edits.

When an approved finding changes the agent runtime image:

```text
- update image-plan.json, Dockerfile, tektona-deployment.json and their human-readable views together
- update Tektona process definitions, compose.yaml and bootstrap-sandbox.sh when sandbox resources or capabilities change
- increment planVersion
- preserve evidence references for every added or retained layer
- validate the plan, Dockerfile and Tektona deployment with image-plan-validator.py
- invalidate or refresh image-lock.json instead of leaving a stale lock
- rebuild locally only when the update approval explicitly includes it
- preserve separate explicit approval for Tektona template builds, tag moves and sandbox creation
- leave credential values and provenance to Tektona; keep only stable resource references in the plan
- promote repeatedly observed runtime installations into evidence-backed image layers when approved
```

## Versioning

Use semantic versioning:
- patch: cleanup, documentation, small consistency fixes
- minor: new commands, playbooks, scripts, capabilities
- major: breaking workflow/autonomy/lifecycle changes

After approved changes:
1. increment version
2. update `.agents/context/harness-version.json`
3. append detailed entry to `.agents/context/harness-changelog.md`

Every changed harness file must be mentioned in the changelog.

## Changelog format

```md
## [<new-version>] - <YYYY-MM-DD>

### Source

- Command: `/harness-update`
- Previous version: `<old-version>`
- Applied findings:
  - FINDING-...

### Changed
- ...

### Fixed
- ...

### Removed
- ...

### Safety / Governance
- ...

### Follow-up
- ...
```

Final response in German:
- old version
- new version
- applied changes
- changelog location
- remaining findings
- recommended next command

## Required self-verification

Before reporting completion, perform a self-verification pass.

Use:

```text
.agents/context/self-verification-policy.md
```

Verify:

```text
- requirement match: the result matches the user's request
- only intended files/content were changed
- relevant harness policies were followed
- available checks/tests were run or explicitly skipped with a reason
- remaining risks or assumptions are reported honestly
```
