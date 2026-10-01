# Jira Integration

Use this file when the project uses Jira for work items, epics, stories, bugs or project planning.

## Recommended access

Preferred access path:

```text
Jira MCP server, Jira CLI or approved API wrapper scripts
```

## Allowed read operations

```text
- read issues
- read epics
- read acceptance criteria
- read comments
- read status and labels
```

## Write operations requiring approval

```text
- create comments
- transition issues
- update descriptions
- update acceptance criteria
- change assignees
- change sprint or priority
```

## Forbidden by default

```text
- deleting issues
- bulk transitions
- modifying workflows
- changing permissions
- reading or printing secrets
```

## Required wrapper scripts

Prefer wrappers under:

```text
.agent/scripts/jira-*.sh
```
