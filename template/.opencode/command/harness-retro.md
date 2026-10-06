---
description: "Collect usage feedback and write retro findings for the current harness version."
---

# Harness Retro Command

## Goal

Collect usage-based feedback and convert it into active findings for the current harness version.

Do not directly modify harness files. Use `/harness-update` to apply findings.

## Version scope

Read current version from:

`.agents/context/harness-version.json`

Write to:

`.agents/runs/harness-retro/<current-version>/<date>/`

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

## Required self-verification

Before reporting completion, perform a self-verification pass.

Use:

```text
.agents/context/self-verification-policy.md
```

Policy-evaluation history may support improvement proposals, but must not silently change rules or thresholds. Retrospective findings should identify the affected rule ids, observed false positives or false negatives, coverage gaps and a versioned proposed change for later approval through `/harness-update`.

Runtime-image feedback may include missing tools, repeated runtime installations, unnecessary layers, excessive image size, build failures, architecture mismatches, slow startup, stale Tektona resource references, failed Tektona processes, unavailable container daemons, failed Compose health checks or service-placement problems. Record the affected layer, service or Tektona resource id and concrete build/task evidence; do not directly rewrite, rebuild or redeploy the image during the retrospective.

Verify:

```text
- requirement match: the result matches the user's request
- only intended files/content were changed
- relevant harness policies were followed
- available checks/tests were run or explicitly skipped with a reason
- remaining risks or assumptions are reported honestly
```
