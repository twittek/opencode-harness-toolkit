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

## MCP discovery command

Use `/harness-mcp` for controlled MCP discovery, recommendations, risk review and installation planning.

Rules:

```text
- do not install MCP servers without explicit approval
- do not modify opencode.jsonc without explicit approval
- do not store secrets in harness files
- classify MCP candidates by risk category
- write run artifacts under .agent/runs/harness-mcp/
```

## Self-verification policy

Use `.agent/context/self-verification-policy.md` before reporting completion.

Every task must end with a self-verification pass before the final response.

Minimum verification:

```text
- check the result against the user's original request
- check that only intended files/content were changed
- run available tests/checks or explain why not
- report remaining risks or assumptions honestly
```

Do not claim completion without verification.

For implementation or artifact changes, include a concise final verification summary:

```text
Verification:
- Requirement match: ...
- Files changed: ...
- Checks run: ...
- Open risks: ...
```

## Context Loading Policy

Use `.agent/context/context-loading-policy.md` to decide which harness files to load.

Default behavior:

```text
- load Tier 1 baseline files
- load Tier 2 files only when relevant
- load Tier 3 run artifacts only when explicitly needed
- never load Tier 4 paths automatically
```

The harness is a structured knowledge space, not one giant prompt.

For 128K context windows, do not load everything just because it fits.
Use the smallest useful context set.

## Role model

The harness uses role files under:

```text
.agent/roles/
```

and activation rules under:

```text
.agent/context/role-activation-policy.md
```

Roles are not always active. Activate the smallest useful role set for the task.

Core roles:

```text
architect
requirements-engineer
developer
tester
reviewer
```

Specialist roles:

```text
security-engineer
ux-designer
accessibility-specialist
devops-engineer
integration-architect
data-engineer
domain-expert
technical-writer
performance-engineer
observability-engineer
product-manager
```

## Interactive question tool policy

For any harness interview question with predefined options, use OpenCode's question tool first.

Plain A/B/C text is fallback mode only.

```text
Using plain A/B/C text is a fallback mode, not the primary mode.
Do not use fallback mode unless tool usage is unavailable.
```

Always ask exactly one question at a time and include `Other / custom`.
