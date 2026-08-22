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
