# External Systems

This file documents the external systems used by the project and how agents may interact with them.

## System inventory

| System | Purpose | Access mode | Read allowed | Write allowed | Wrapper required | Notes |
|---|---|---:|---:|---:|---:|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Access modes

Use these categories:

```text
none
manual-only
cli
api
mcp
browser
```

## Interaction boundaries

For every external system, document:

```text
- what the system is used for
- which CLI, API or MCP server may be used
- which actions are read-only
- which actions require explicit approval
- which actions are forbidden
- which wrapper scripts must be used
- where credentials are expected, without storing secrets
```

## Discovery notes

The harness should treat unknown systems as unavailable until explicitly documented.
