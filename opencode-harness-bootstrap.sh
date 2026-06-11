#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"

mkdir -p "$ROOT/.opencode/command"
mkdir -p "$ROOT/.opencode/agent"
mkdir -p "$ROOT/.agent/context"
mkdir -p "$ROOT/.agent/playbooks"
mkdir -p "$ROOT/.agent/templates"
mkdir -p "$ROOT/.agent/scripts"
mkdir -p "$ROOT/.agent/skills"
mkdir -p "$ROOT/.agent/roles"
mkdir -p "$ROOT/.agent/config"
mkdir -p "$ROOT/.agent/runs/harness-check"
mkdir -p "$ROOT/.agent/runs/harness-update"
mkdir -p "$ROOT/.agent/runs/harness-retro"
touch "$ROOT/.agent/runs/.gitkeep"
touch "$ROOT/.agent/runs/harness-check/.gitkeep"
touch "$ROOT/.agent/runs/harness-update/.gitkeep"
touch "$ROOT/.agent/runs/harness-retro/.gitkeep"

if [ -f "$ROOT/.opencode/command/create-harness.md" ] && [ ! -f "$ROOT/.opencode/command/harness-init.md" ]; then
  mv "$ROOT/.opencode/command/create-harness.md" "$ROOT/.opencode/command/harness-init.md"
fi

if [ ! -f "$ROOT/.agent/context/harness-version.json" ]; then
cat > "$ROOT/.agent/context/harness-version.json" <<'EOF'
{
  "version": "0.1.0",
  "previousVersion": null,
  "status": "bootstrap",
  "lastUpdated": null,
  "lastUpdateSource": "bootstrap",
  "notes": "Initial bootstrap version. Increment after approved harness updates."
}
EOF
fi

if [ ! -f "$ROOT/.agent/context/harness-changelog.md" ]; then
cat > "$ROOT/.agent/context/harness-changelog.md" <<'EOF'
# Harness Changelog

All harness changes must be recorded here.

## [0.1.0] - Bootstrap

### Added

- Initial bootstrap structure.
- Lifecycle commands:
  - `/harness-init`
  - `/harness-check`
  - `/harness-update`
  - `/harness-retro`

### Governance

- Harness changes must be versioned.
- Findings are scoped to the current harness version.
- `/harness-update` must update this changelog and increment the version.
EOF
fi

cat > "$ROOT/AGENTS.md" <<'EOF'
# Project Agent Instructions

This project uses OpenCode with a project-local harness.

## Fixed harness purpose

The harness exists to make an AI agent reliable, controlled, repeatable, and project-specific for this project.

## Harness lifecycle

```text
/harness-init    = create initial harness
/harness-check   = audit current harness version and write findings
/harness-update  = apply active findings for current version, update changelog, increment version
/harness-retro   = collect usage feedback and write retro findings
```

## Versioning

Current version is tracked in:

```text
.agent/context/harness-version.json
```

All harness changes must be documented in:

```text
.agent/context/harness-changelog.md
```

## General rules

- Keep global instructions compact.
- Prefer focused playbooks over huge prompts.
- Use `.agent/runs/<task-id>/` for reports and handoffs.
- Do not post long Markdown inline into shell commands.
- If GitLab is used, read `.agent/skills/gitlab-glab.md` first.
- If GitLab is used, do not invent `glab` commands or flags.
- If GitLab is used, comments must be written to Markdown files first and posted via `.agent/scripts/gitlab-issue-comment.sh`.
- After completing a task, explicitly verify the result against the requirements.
EOF

if [ ! -f "$ROOT/opencode.jsonc" ] && [ ! -f "$ROOT/opencode.json" ]; then
cat > "$ROOT/opencode.jsonc" <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "litellm-local/qwen36-27b-mtp-128k",
  "instructions": ["AGENTS.md"],
  "permission": {
    "edit": "ask",
    "bash": {
      "git *": "allow",
      "glab *": "ask",
      "gh *": "ask",
      "npm run *": "allow",
      "pnpm *": "allow",
      "npx *": "ask",
      "mkdir *": "allow",
      "cat *": "allow",
      "touch *": "allow",
      "chmod *": "allow",
      "rm *": "deny",
      "*": "ask"
    },
    "external_directory": {
      "~/secrets/**": "deny",
      "*": "ask"
    }
  },
  "command": {
    "harness-init": {
      "description": "Create an OpenCode agent harness after an adaptive German project interview.",
      "template": "Run the adaptive project harness initialization interview. Follow `.opencode/command/harness-init.md` exactly."
    },
    "harness-check": {
      "description": "Audit the current harness version and write active findings.",
      "template": "Audit the current harness version. Follow `.opencode/command/harness-check.md` exactly."
    },
    "harness-update": {
      "description": "Apply active findings for the current harness version.",
      "template": "Apply active findings for the current harness version. Follow `.opencode/command/harness-update.md` exactly."
    },
    "harness-retro": {
      "description": "Collect usage feedback and write retro findings for the current harness version.",
      "template": "Run the harness retrospective. Follow `.opencode/command/harness-retro.md` exactly."
    }
  },
  "mcp": {
    "chrome-devtools": {
      "type": "local",
      "command": ["npx", "-y", "chrome-devtools-mcp@latest"],
      "enabled": true
    }
  },
  "compaction": {
    "auto": true,
    "tail_turns": 15
  },
  "formatter": false,
  "lsp": false
}
EOF
fi

cat > "$ROOT/.opencode/command/harness-init.md" <<'EOF'
---
description: "Initialize an OpenCode harness by conducting an adaptive German project interview."
---

# Harness Init Command

## Fixed purpose

Do not ask why the developer wants a harness. The purpose is fixed:

"To make an AI agent reliable, controlled, repeatable, and project-specific for this project."

## Task

Conduct an adaptive German interview. Generate English harness files.

Create:
- `AGENTS.md`
- `opencode.jsonc`
- `.opencode/command/harness-init.md`
- `.opencode/command/harness-check.md`
- `.opencode/command/harness-update.md`
- `.opencode/command/harness-retro.md`
- `.agent/roles/architect.md`
- `.agent/roles/refinement.md`
- `.agent/roles/developer.md`
- `.agent/roles/tester.md`
- `.agent/context/project-profile.md`
- `.agent/context/harness-scope.md`
- `.agent/context/harness-version.json`
- `.agent/context/harness-changelog.md`
- `.agent/context/context-index.md`
- `.agent/context/definition-of-done.md`
- `.agent/context/autonomy-policy.md`
- `.agent/context/risk-profile.md`
- `.agent/context/context-safety-policy.md`
- `.agent/playbooks/refinement.md`
- `.agent/playbooks/architecture.md`
- `.agent/playbooks/development-best-practices.md`
- `.agent/playbooks/testing.md`
- `.agent/playbooks/review.md`
- `.agent/playbooks/harness-check.md`
- `.agent/playbooks/harness-update.md`
- `.agent/playbooks/harness-retrospective.md`
- `.agent/scripts/quality-gates.sh`
- `.agent/scripts/load-issue.sh`

If GitLab is selected, also create:
- `.agent/skills/gitlab-glab.md`
- `.agent/scripts/gitlab-issue-load.sh`
- `.agent/scripts/gitlab-issue-comment.sh`
- `.agent/scripts/gitlab-mr-create-draft.sh`
- `.agent/scripts/gitlab-mr-comment.sh`
- `.agent/scripts/gitlab-api.sh`
- `.agent/config/gitlab.env.example`

## Adaptive interview

Ask in German. Start broad, then branch.

First ask:
- Was soll mit dem Projekt fachlich oder technisch erreicht werden?
- Was ist das erwartete Ergebnis: Prototyp, MVP, produktive Anwendung, internes Tool, Kundenprojekt, Lernprojekt, Library, CLI/Automation, anderes?
- Für welche Branche oder Domäne wird das Projekt gebaut?
- Welche Art Anwendung ist es: Frontend-only, Backend-only, Fullstack, Library, CLI, Mobile, Data Pipeline, anderes?
- Wer nutzt das Ergebnis?
- Was sind die wichtigsten Workflows?
- Gibt es mehrere Apps/Packages?
- Gibt es mandanten-/kundenindividuelle Varianten?
- Welche Art Arbeit soll der Agent übernehmen?
- Wie kritisch ist das Projekt?
- Was soll der Agent nie tun?

Skip irrelevant branches:
- no backend → no backend guardrails
- no persistence → no database/migration questions
- frontend-only prototype → keep governance lightweight
- no GitLab/GitHub → skip issue/MR automation
- no browser UI → skip Chrome DevTools unless requested

Always include:
- autonomy boundaries
- Definition of Done
- testing/quality gates
- context safety
- versioning/changelog rules
EOF

cat > "$ROOT/.opencode/command/harness-check.md" <<'EOF'
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
EOF

cat > "$ROOT/.opencode/command/harness-update.md" <<'EOF'
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
EOF

cat > "$ROOT/.opencode/command/harness-retro.md" <<'EOF'
---
description: "Collect usage feedback and write retro findings for the current harness version."
---

# Harness Retro Command

## Goal

Collect usage-based feedback and convert it into active findings for the current harness version.

Do not directly modify harness files. Use `/harness-update` to apply findings.

## Version scope

Read current version from:

`.agent/context/harness-version.json`

Write to:

`.agent/runs/harness-retro/<current-version>/<date>/`

Create:
- `retro.md`
- `satisfaction-summary.md`
- `active-findings.md`
- `proposed-changes.md`
- `patch-plan.md`

## German interview

Ask:

### Keep
- Was läuft gut und soll bleiben?

### Problems
- Was läuft schlecht?
- Wo fragt der Agent zu viel oder zu wenig?
- Wo lädt er falschen oder zu viel Kontext?
- Wo sind Kommandos, Scripts oder Skills unklar?

### Start
- Womit soll die Harness anfangen?

### Stop
- Was soll die Harness nicht mehr tun?

### Change
- Was soll angepasst, zusammengeführt, aufgeräumt oder vereinfacht werden?

### Evidence
- Gibt es konkrete Beispiele: Issue, MR, Command, Datei, Agentenantwort, Fehlverhalten oder guter Output?

Use the same finding format as `/harness-check`, with `Source: retro`.

Final response in German:
- current version
- feedback summary
- number of active retro findings
- recommended next command: `/harness-update`
EOF

cat > "$ROOT/.agent/playbooks/harness-update.md" <<'EOF'
# Harness Update Playbook

Use this playbook for `/harness-update`.

Rules:
- Only process findings for the current harness version.
- Do not apply findings from older versions unless explicitly approved.
- Never change application source code.
- Create an update plan before editing.
- Ask for approval before editing.
- Update `harness-version.json`.
- Append a detailed changelog entry.
- Every changed harness file must be mentioned in the changelog.
EOF


cat > "$ROOT/.opencode/command/harness-repair-opencode-config.md" <<'EOF'
---
description: "Repair common invalid OpenCode project config patterns."
---

# Harness Repair OpenCode Config Command

## Goal

Repair common invalid OpenCode project configuration patterns that prevent OpenCode from starting.

## Language

Reply to the user in German.
Write config files in valid JSONC.

## Rules

Do not invent OpenCode config keys.

Use this safe schema:

- `instructions` must be an array, for example `["AGENTS.md"]`
- use `command`, not `commands`
- use `permission`, not `permissions`
- do not create an `agents` map
- do not add `agent` fields to command definitions
- keep commands with `description` and `template` only
- keep role descriptions under `.agent/roles/`

## Steps

1. Backup existing config:
   - `opencode.jsonc.bak`
   - `opencode.json.bak`

2. If both `opencode.json` and `opencode.jsonc` exist, prefer `opencode.jsonc` and rename `opencode.json` to `opencode.json.disabled`.

3. Rewrite `opencode.jsonc` to a safe minimal configuration while preserving the existing `model` value if possible.

4. Ensure lifecycle commands exist:
   - `harness-init`
   - `harness-check`
   - `harness-update`
   - `harness-retro`
   - `harness-repair-opencode-config`

5. Remove invalid keys:
   - `agents`
   - `commands`
   - `permissions`
   - any `agent` field inside command definitions

6. Final check:

```bash
grep -R '"agents"\|"commands"\|"permissions"\|"agent":' opencode.jsonc .opencode 2>/dev/null || true
```

If matches remain in config files, fix them.

## Safe minimal config template

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "<preserve-existing-model-or-provider/model>",
  "instructions": ["AGENTS.md"],
  "permission": {
    "edit": "ask",
    "bash": {
      "git *": "allow",
      "glab *": "ask",
      "gh *": "ask",
      "npm run *": "allow",
      "pnpm *": "allow",
      "npx *": "ask",
      "mkdir *": "allow",
      "cat *": "allow",
      "touch *": "allow",
      "chmod *": "allow",
      "rm *": "deny",
      "*": "ask"
    },
    "external_directory": {
      "~/secrets/**": "deny",
      "*": "ask"
    }
  },
  "command": {
    "harness-init": {
      "description": "Initialize the project harness.",
      "template": "Follow `.opencode/command/harness-init.md` exactly."
    },
    "harness-check": {
      "description": "Audit the current harness version.",
      "template": "Follow `.opencode/command/harness-check.md` exactly."
    },
    "harness-update": {
      "description": "Apply active findings for the current harness version.",
      "template": "Follow `.opencode/command/harness-update.md` exactly."
    },
    "harness-retro": {
      "description": "Collect usage feedback for the current harness version.",
      "template": "Follow `.opencode/command/harness-retro.md` exactly."
    },
    "harness-repair-opencode-config": {
      "description": "Repair common invalid OpenCode project config patterns.",
      "template": "Follow `.opencode/command/harness-repair-opencode-config.md` exactly."
    }
  },
  "compaction": {
    "auto": true,
    "tail_turns": 15
  },
  "formatter": false,
  "lsp": false
}
```

## Final response

Report in German:
- which files were backed up
- which invalid keys were removed
- current model value
- whether the final grep check is clean
EOF

echo "OpenCode harness bootstrap v15 installed."
echo
echo "Next steps:"
echo "  1. Review opencode.jsonc and set your model/provider if needed."
echo "  2. Start: opencode"
echo "  3. Run: /harness-init"
echo "  4. Audit with: /harness-check"
echo "  5. Apply findings with: /harness-update"
echo "  6. Reflect with: /harness-retro"
echo "  7. Repair config if needed: /harness-repair-opencode-config"
