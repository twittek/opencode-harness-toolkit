# /harness-mcp

Use this command to discover, evaluate and plan MCP server usage for the project.

This command must not blindly install MCP servers.

It is a controlled MCP discovery and planning workflow.

## Objective

Identify whether MCP servers could improve the project's agent harness, then create a safe recommendation and installation plan.

The command should:

```text
1. Read the current harness context.
2. Read integration and external-system files.
3. Identify useful MCP capability gaps.
4. Ask one question at a time when information is missing.
5. Recommend candidate MCP servers or MCP categories.
6. Classify risks.
7. Create an installation plan.
8. Ask for explicit approval before modifying configuration.
```

## Input sources

Read these files when present:

```text
AGENTS.md
opencode.jsonc
.agent/context/integration-policy.md
.agent/integrations/external-systems.md
.agent/mcp/mcp-policy.md
.agent/mcp/mcp-registry.md
.agent/mcp/approved-mcp-servers.md
.agent/mcp/denied-mcp-servers.md
.agent/interview/interview-engine.md
```

Also inspect project-specific documentation if referenced by the harness.

## Adaptive MCP interview

Use the same Adaptive Scenario Discovery principle as `/harness-init`.

Ask exactly one question at a time.

Start with the highest-information question:

```text
Which MCP outcome do you want?
```

Options:

```text
A) Document existing MCP servers only
B) Recommend useful MCP servers
C) Create an installation plan
D) Review an MCP server before approval
E) Update OpenCode MCP config after approval
F) Other / custom
```

Then ask only the next best question.

Examples:

```text
Which external systems should MCP support first?
```

Options:

```text
A) GitLab / GitHub
B) Jira / work tracking
C) Confluence / documentation
D) Figma / design
E) Browser automation
F) Filesystem / local tools
G) Database / analytics
H) Other / custom
```

```text
What autonomy level should MCP tools have?
```

Options:

```text
A) Read-only
B) Write only after approval
C) Write-enabled for selected safe operations
D) Planning only, no config changes
E) Other / custom
```

## MCP categories

Classify MCP candidates into these categories:

```text
read-only
write-capable
browser-control
filesystem
secret-sensitive
production-adjacent
unknown
```

Default risk:

```text
unknown → do not install
write-capable → approval required
browser-control → approval required
filesystem → approval required
secret-sensitive → approval required
production-adjacent → approval required
```

## Recommendation model

For every MCP candidate, document:

```text
- name
- purpose
- related external system
- capability provided
- expected value
- risk category
- required permissions
- credentials needed
- installation method
- config changes
- approval status
- fallback without MCP
```

## Output files

Write findings under:

```text
.agent/runs/harness-mcp/<date>/
```

Recommended files:

```text
.agent/runs/harness-mcp/<date>/mcp-discovery-report.md
.agent/runs/harness-mcp/<date>/mcp-recommendations.md
.agent/runs/harness-mcp/<date>/mcp-risk-review.md
.agent/runs/harness-mcp/<date>/mcp-installation-plan.md
```

Update stable policy files only after the user approves:

```text
.agent/mcp/mcp-policy.md
.agent/mcp/mcp-registry.md
.agent/mcp/approved-mcp-servers.md
.agent/mcp/denied-mcp-servers.md
```

Update `opencode.jsonc` only after explicit approval.

## Approval rules

Before making config changes, show a summary:

```text
MCP installation/update plan

- MCP server:
- Purpose:
- Risk category:
- Required permissions:
- Config files to change:
- Secrets required:
- Fallback without MCP:
- Rollback plan:

Do you approve applying this MCP configuration change?
```

Options:

```text
A) Approve and apply
B) Save plan only
C) Adjust recommendation
D) Cancel
```

## Forbidden behavior

Do not:

```text
- install MCP servers without explicit approval
- modify opencode.jsonc without explicit approval
- store secrets in harness files
- print tokens or API keys
- enable write-capable MCPs silently
- enable browser-control MCPs silently
- enable filesystem MCPs silently
- enable production-adjacent MCPs silently
- use unknown MCP servers as trusted
```

## OpenCode config safety

When modifying `opencode.jsonc`, preserve the strict config contract:

Allowed top-level keys:

```text
$schema
model
instructions
permission
command
mcp
compaction
formatter
lsp
```

Forbidden top-level keys:

```text
agents
agent
commands
permissions
providers
provider
tools
tool
rules
```

Command entries may only contain:

```text
description
template
```

Do not add forbidden keys while configuring MCP.

## Final response

The final response should include:

```text
- what was discovered
- what was recommended
- what was changed, if anything
- what still needs approval
- where the run artifacts were written
```

## Required self-verification

Before reporting completion, perform a self-verification pass.

Use:

```text
.agent/context/self-verification-policy.md
```

Verify:

```text
- requirement match: the result matches the user's request
- only intended files/content were changed
- relevant harness policies were followed
- available checks/tests were run or explicitly skipped with a reason
- remaining risks or assumptions are reported honestly
```
