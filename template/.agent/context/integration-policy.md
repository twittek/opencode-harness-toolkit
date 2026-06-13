# Integration Policy

This policy defines how agents interact with external systems.

## Principle

External systems are not assumed. They must be discovered, documented and explicitly enabled.

## Access classification

Classify every external system as one of:

```text
read-only
write-with-approval
write-enabled
forbidden
unknown
```

Default:

```text
unknown → no access
write → approval required
```

## Wrapper-first rule

If a wrapper script exists under `.agent/scripts/`, agents must use it instead of inventing ad-hoc CLI or API calls.

Examples:

```text
.agent/scripts/gitlab-issue-comment.sh
.agent/scripts/github-pr-comment.sh
.agent/scripts/jira-issue-comment.sh
```

## Credentials

Agents must never store secrets in harness files.

Allowed:

```text
- reference environment variable names
- reference local credential stores
- document expected authentication method
```

Forbidden:

```text
- writing tokens into markdown files
- printing secrets
- copying credentials into generated scripts
```

## Write safety

The following actions always require explicit user approval:

```text
- creating comments in external systems
- updating issues or tickets
- changing labels, status, sprint or assignee
- triggering CI/CD pipelines
- modifying repository settings
- changing permissions
```

## Forbidden by default

```text
- deleting remote resources
- force-pushing
- modifying secrets
- changing production configuration
- bulk operations without explicit approval
```

## MCP interaction

If an MCP server is available for an external system, document it in:

```text
.agent/mcp/mcp-policy.md
```

Do not install MCP servers automatically during `/harness-init`.
Only recommend and plan MCP usage unless the user explicitly approves installation.
