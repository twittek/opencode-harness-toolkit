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

## OpenCode Config Safety

When generating or editing `opencode.jsonc`:

- `instructions` must be an array, for example `["AGENTS.md"]`
- use `command`, not `commands`
- use `permission`, not `permissions`
- do not create `agents` or `agent` mappings
- do not reference `.opencode/agent/*.md`
- store role descriptions under `.agent/roles/`
- command entries should contain only `description` and `template`
- generate the OpenCode config correctly from the start
