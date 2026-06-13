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
