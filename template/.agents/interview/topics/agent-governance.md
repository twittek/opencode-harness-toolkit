---
id: agent-governance
version: 1
dimensions:
  - agent.responsibilities
  - agent.autonomy
  - agent.approval-boundaries
  - agent.forbidden-actions
  - agent.required-roles
activation: always-considered
blocking-dimensions:
  - agent.responsibilities
  - agent.approval-boundaries
  - agent.forbidden-actions
outputs:
  - .agent/context/autonomy-policy.md
  - .agent/context/risk-profile.md
  - .agent/context/role-activation-policy.md
---

# Agent Governance

Resolve what the agent may do, what requires approval and what remains forbidden.

## Evidence signals

```text
the requested agent workflow
organization policies
existing AGENTS.md or equivalent instructions
tool and runtime permissions
```

## Candidate patterns

```text
Which parts of the lifecycle should the agent perform: refinement, architecture, implementation, testing, review or communication?
Which ordinary changes may it make autonomously?
Which actions require explicit approval?
Which actions must remain forbidden even in an isolated sandbox?
```

Prefer one question that cleanly partitions responsibility and autonomy over separate questions for every tool.

## Safe defaults

```text
normal scoped workspace edits are allowed only when implementation is in scope
external writes and irreversible actions require approval
destructive, production and secret-management actions are forbidden unless explicitly governed
```

## Completion

Complete when permissions and prohibitions can be generated without relying on vague terms such as "be careful".
