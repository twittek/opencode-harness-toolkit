# MCP Policy

This file documents MCP usage boundaries for the project.

## Current status

MCP discovery is not automatic during `/harness-init`.

The harness may document:

```text
- existing MCP servers
- candidate MCP servers
- recommended MCP usage
- security concerns
- installation plans requiring explicit approval
```

## Default rule

Do not install or enable MCP servers automatically.

## MCP categories

Classify MCP servers as:

```text
read-only
write-capable
browser-control
filesystem
secret-sensitive
production-adjacent
```

Write-capable, browser-control, filesystem, secret-sensitive and production-adjacent MCP servers require explicit approval before installation or use.



## Discovery command

Use:

```text
/harness-mcp
```

for MCP discovery, recommendations, risk reviews and installation planning.

## MCP workflow

```text
1. Discover capability gaps.
2. Map gaps to MCP candidate categories.
3. Assess value.
4. Assess risk.
5. Create a recommendation.
6. Create an installation plan.
7. Ask for explicit approval.
8. Apply config only after approval.
```

## Risk matrix

| Category | Default decision | Approval required | Notes |
|---|---:|---:|---|
| read-only | candidate | recommended | Still verify data exposure |
| write-capable | blocked | yes | Can mutate external systems |
| browser-control | blocked | yes | Can operate web sessions |
| filesystem | blocked | yes | Can read/write local files |
| secret-sensitive | blocked | yes | May expose credentials |
| production-adjacent | blocked | yes | May affect production systems |
| unknown | blocked | yes | Must be classified first |

## Recommendation template

```text
MCP server:
Purpose:
Related system:
Capability:
Expected value:
Risk category:
Required permissions:
Credential source:
Config changes:
Fallback without MCP:
Rollback plan:
Recommendation:
```

## Installation policy

Do not install or configure MCP servers automatically during `/harness-init`.

`/harness-mcp` may modify configuration only after explicit user approval.

The recommended default is:

```text
recommend and plan first
apply later
```
