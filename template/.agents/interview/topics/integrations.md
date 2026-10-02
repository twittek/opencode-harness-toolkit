---
id: integrations
version: 1
dimensions:
  - integrations.repository
  - integrations.work-tracking
  - integrations.documentation
  - integrations.external-systems
  - integrations.write-boundaries
activation-signals:
  - git-remote
  - issue-reference
  - external-api
  - mcp-config
outputs:
  - .agents/context/integration-policy.md
  - .agents/integrations/external-systems.md
  - .agents/mcp/mcp-policy.md
---

# Integrations

Resolve which external systems matter, how they are accessed and which writes require approval.

## Evidence signals

```text
Git remotes and repository metadata
issue references
CI variables without values
existing integration wrappers
MCP configuration
```

## Candidate patterns

```text
Which external systems must the agent read or update?
Which system is authoritative for work items and code review?
Which external writes require approval or are forbidden?
Are approved wrappers or MCP servers already available?
```

Do not ask for specific CLI commands before the system and access mode are known.

## Completion

Complete when each relevant system has an access classification and credential expectation without secret material.
