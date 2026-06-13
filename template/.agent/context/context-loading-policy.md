# Context Loading Policy

This policy defines which harness files should be loaded for agent work and when.

The goal is to keep the harness useful for large context windows such as 128K while avoiding unnecessary context bloat.

## Principle

Do not load the whole harness for every task.

Use the smallest useful context set.

The harness is a structured knowledge space, not one giant prompt.

## Loading tiers

### Tier 1: Always load

```text
AGENTS.md
.agent/context/project-profile.md
.agent/context/autonomy-policy.md
.agent/context/definition-of-done.md
.agent/context/risk-profile.md
.agent/context/context-loading-policy.md
```

### Tier 2: Load when relevant

```text
.agent/context/role-activation-policy.md
.agent/context/integration-policy.md
.agent/mcp/mcp-policy.md
.agent/roles/*.md
.agent/integrations/*.md
.agent/interview/*.md
.agent/playbooks/*.md
```

### Tier 3: Load only on explicit need

```text
.agent/runs/**
```

### Tier 4: Never load automatically

```text
node_modules/**
dist/**
build/**
coverage/**
.cache/**
.next/**
.nuxt/**
target/**
.DS_Store
*.bak.*
*.log
*.tmp
template/**
opencode-harness-toolkit*/**
```

## 128K context guidance

For 128K context windows, the full harness may technically fit, but that does not mean it should always be loaded.

```text
1. Start with Tier 1.
2. Determine the task type.
3. Add only the relevant Tier 2 files.
4. Add Tier 3 only when reviewing lifecycle history or findings.
5. Never load Tier 4 automatically.
```

## Output rule

When context selection matters, briefly state what was loaded and why.
