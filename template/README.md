# Harness Toolkit Template

This directory contains the files copied into a target project by `opencode-harness-toolkit-install.sh`.

Edit these files directly when changing the toolkit scaffold.

Key files:

```text
AGENTS.md
opencode.jsonc
.opencode/command/harness-init.md
.opencode/command/harness-check.md
.opencode/command/harness-update.md
.opencode/command/harness-retro.md
.agents/context/harness-version.json
.agents/context/harness-changelog.md
.agents/playbooks/harness-update.md
```

Do not put project-specific secrets into this template.


Interview engine files live under:

```text
.agents/interview/
```


Integration files live under:

```text
.agents/integrations/
.agents/context/integration-policy.md
.agents/mcp/mcp-policy.md
.agents/scripts/
```


MCP discovery command:

```text
/harness-mcp
```

MCP files live under:

```text
.agents/mcp/
.agents/runs/harness-mcp/
```


Role files live under:

```text
.agents/roles/
.agents/context/role-activation-policy.md
```


Context loading policy:

```text
.agents/context/context-loading-policy.md
```


Self-verification policy:

```text
.agents/context/self-verification-policy.md
```
