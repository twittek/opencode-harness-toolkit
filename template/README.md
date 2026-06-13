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
.agent/context/harness-version.json
.agent/context/harness-changelog.md
.agent/playbooks/harness-update.md
```

Do not put project-specific secrets into this template.


Interview engine files live under:

```text
.agent/interview/
```


Integration files live under:

```text
.agent/integrations/
.agent/context/integration-policy.md
.agent/mcp/mcp-policy.md
.agent/scripts/
```


MCP discovery command:

```text
/harness-mcp
```

MCP files live under:

```text
.agent/mcp/
.agent/runs/harness-mcp/
```


Role files live under:

```text
.agent/roles/
.agent/context/role-activation-policy.md
```
