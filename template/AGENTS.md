<!-- harness-bootstrap: true -->

# Bootstrap Agent Instructions

This file exists only to run `/harness-init` safely. The approved initialization replaces it with project-specific instructions.

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
.agents/context/harness-version.json
```

All harness changes must be documented in:

```text
.agents/context/harness-changelog.md
```

## General rules

- Keep global instructions compact.
- Prefer focused playbooks over huge prompts.
- Use `.agents/runs/<task-id>/` for reports and handoffs.
- Do not post long Markdown inline into shell commands.
- If GitLab is used, read `.agents/skills/gitlab-glab.md` first.
- If GitLab is used, do not invent `glab` commands or flags.
- If GitLab is used, comments must be written to Markdown files first and posted via `.agents/scripts/gitlab-issue-comment.sh`.
- After completing a task, explicitly verify the result against the requirements.

## OpenCode Config Safety

When generating or editing `opencode.jsonc`:

- `instructions` must be an array, for example `["AGENTS.md"]`
- use `command`, not `commands`
- use `permission`, not `permissions`
- do not create `agents` or `agent` mappings
- do not reference `.opencode/agent/*.md`
- store role descriptions under `.agents/roles/`
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
- write run artifacts under .agents/runs/harness-mcp/
```

## Self-verification policy

Use `.agents/context/self-verification-policy.md` before reporting completion.

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

Use `.agents/context/context-loading-policy.md` to decide which harness files to load.

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

For `/harness-init`, load `.agents/interview/topic-catalog.md` first and load individual `.agents/interview/topics/*.md` files only when their routing signals make them relevant.

## Role model

During `/harness-init`, derive and confirm the smallest project-specific role set using:

```text
.agents/interview/role-catalog.md
```

Generate only confirmed roles under `.agents/roles/` and describe their routing in:

```text
.agents/context/role-activation-policy.md
```

Do not copy or generate the entire role catalog. The final `AGENTS.md` must reference only roles that actually exist in the initialized project.

## Machine-evaluable policies

Use `.agents/policies/policy-contract.md` when `/harness-init` generates policies or compliance requirements.

Normative prose is not sufficient. Every mandatory, forbidden or approval-gated behavior must map to a versioned rule in `.agents/policies/policy-registry.json` with typed signals, deterministic predicates, explicit unknown handling and reason codes.

Missing evidence is `UNKNOWN`, never compliant by default. Decision-model output may be a declared signal, but the policy evaluator and configured thresholds determine the result and recommended action.

## Interactive question tool policy

For any harness interview question with predefined options, use OpenCode's question tool first.

Plain A/B/C text is fallback mode only.

```text
Using plain A/B/C text is a fallback mode, not the primary mode.
Do not use fallback mode unless tool usage is unavailable.
```

Always ask exactly one question at a time and include `Other / custom`.

## Adaptive interview policy

`/harness-init` must use `.agents/interview/interview-engine.md` and the modular topic packs under `.agents/interview/topics/`.

Required behavior:

```text
- inspect available project evidence before asking
- maintain a multidimensional belief state
- compare candidate questions across all active topics
- select the eligible question with maximum weighted information gain
- recalculate candidates after every answer
- stop based on generation readiness, not a fixed question count
```

Forbidden behavior:

```text
- fixed first question
- fixed topic or question order
- walking through every topic pack
- asking for facts already established by reliable evidence
- claiming Bayesian selection without comparing candidate questions
```
