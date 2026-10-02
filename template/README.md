# Harness Toolkit Template

This directory contains bootstrap resources and generation references used by `opencode-harness-toolkit-install.sh` and `/harness-init`.

This maintenance README is package documentation and is deliberately not copied to the target project. A target project's existing `README.md` must remain product evidence for adaptive discovery.

Edit these files directly when changing the toolkit scaffold.

Key files:

```text
AGENTS.md
opencode.jsonc
.opencode/command/harness-init.md
.opencode/command/harness-check.md
.opencode/command/harness-update.md
.opencode/command/harness-retro.md
.opencode/command/harness-mcp.md
.agents/interview/topic-catalog.md
.agents/interview/role-catalog.md
.agents/interview/topics/
.agents/scripts/interview-ranker.py
.agents/policies/policy-contract.md
.agents/policies/policy-registry.schema.json
.agents/policies/task-evidence.schema.json
.agents/policies/evaluation-result.schema.json
.agents/scripts/policy-evaluator.py
```

The installer copies only the bootstrap allowlist: commands, interview resources, entropy and policy evaluators, policy schemas, bootstrap `AGENTS.md`, OpenCode configuration, and the context-loading and self-verification policies. Project-specific roles, integrations, policy rules, playbooks and run structures are deferred to `/harness-init`.

If the target already contains `AGENTS.md`, the installer preserves it. During initialization it is treated as project evidence and reconciled through the approval summary instead of being overwritten silently.

Do not put project-specific secrets into this template.


Interview engine files live under:

```text
.agents/interview/interview-engine.md
.agents/interview/interview-state-schema.md
.agents/interview/topic-catalog.md
.agents/interview/topics/
```

The topic packs are modular sources of discovery knowledge. They do not define a fixed questionnaire or global question order.


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


Generic role references maintained by the toolkit live under:

```text
.agents/roles/
```

They are not copied into target projects. `/harness-init` uses `.agents/interview/role-catalog.md`, confirms a project-specific role set and generates only those role files plus a matching activation policy.


Context loading policy:

```text
.agents/context/context-loading-policy.md
```


Self-verification policy:

```text
.agents/context/self-verification-policy.md
```

Machine-evaluable policy resources:

```text
.agents/policies/policy-contract.md
.agents/policies/policy-registry.schema.json
.agents/policies/task-evidence.schema.json
.agents/policies/evaluation-result.schema.json
.agents/scripts/policy-evaluator.py
```

`/harness-init` generates the project-specific `.agents/policies/policy-registry.json`; it is not copied from the toolkit.
