---
description: "Apply active findings for the current harness version."
---

# Harness Update Command

## Goal

Apply active findings for the current harness version, update the changelog, and increment the harness version.

## Inputs

Read current version from:

`.agent/context/harness-version.json`

Look for active findings in:

```text
.agent/runs/harness-check/<current-version>/*/active-findings.md
.agent/runs/harness-check/<current-version>/*/recommended-actions.md
.agent/runs/harness-retro/<current-version>/*/active-findings.md
.agent/runs/harness-retro/<current-version>/*/proposed-changes.md
.agent/runs/harness-retro/<current-version>/*/patch-plan.md
```

If no active findings exist for the current version, stop and answer in German:

"Für die aktuelle Harness-Version sind keine aktiven Findings vorhanden. Führe `/harness-check` aus, um die Harness erneut zu prüfen, oder `/harness-retro`, um nutzungsbasiertes Feedback aufzunehmen."

Do not make changes without active findings.

## Output directory

Create:

`.agent/runs/harness-update/<current-version>/<date>/`

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

## Versioning

Use semantic versioning:
- patch: cleanup, documentation, small consistency fixes
- minor: new commands, playbooks, scripts, capabilities
- major: breaking workflow/autonomy/lifecycle changes

After approved changes:
1. increment version
2. update `.agent/context/harness-version.json`
3. append detailed entry to `.agent/context/harness-changelog.md`

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
