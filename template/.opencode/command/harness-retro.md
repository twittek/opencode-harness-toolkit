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
