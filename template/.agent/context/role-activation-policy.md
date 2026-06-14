# Role Activation Policy

This file defines when the agent should activate specialist perspectives.

The harness does not require separate runtime subagents. It can use these roles as explicit thinking lenses inside the same context.

## Principle

Activate only the roles relevant to the current task.

Do not load every role into every response.

Use the smallest useful role set.

## Core roles

```text
architect
requirements-engineer
developer
tester
reviewer
```

## Specialist roles

```text
security-engineer
ux-designer
accessibility-specialist
devops-engineer
integration-architect
data-engineer
domain-expert
technical-writer
performance-engineer
observability-engineer
product-manager
```

## Activation matrix

| Trigger | Activate roles |
|---|---|
| New feature or unclear request | requirements-engineer, product-manager |
| Architecture or system boundaries | architect |
| Implementation or refactoring | developer, reviewer |
| Tests or quality gates | tester, reviewer |
| Authentication, authorization, secrets, MCP permissions | security-engineer |
| External systems, APIs, GitLab/GitHub/Jira/Confluence automation | integration-architect, security-engineer |
| User flows, forms, navigation, UX copy | ux-designer |
| UI components, keyboard, contrast, WCAG | accessibility-specialist |
| CI/CD, Docker, Kubernetes, deployment | devops-engineer |
| Data models, imports, reporting, migrations | data-engineer |
| Business rules, domain terminology, user roles | domain-expert |
| README, runbooks, user/developer docs | technical-writer |
| Latency, rendering, throughput, caching | performance-engineer |
| Logging, metrics, tracing, incident diagnosis | observability-engineer |

## Conflict handling

When roles conflict:

```text
security > correctness > maintainability > speed > convenience
```

## Output rule

Do not mention role activation mechanically in every answer.

Mention roles only when it helps the user understand trade-offs or risk.

## Self-verification role behavior

All roles must participate in final self-verification for their area.

Examples:

```text
developer
→ verifies implementation matches the requirement and checks/tests were run

tester
→ verifies acceptance criteria, edge cases and regression risk

security-engineer
→ verifies permissions, secrets and unsafe side effects

integration-architect
→ verifies external-system behavior, write boundaries and fallback paths

technical-writer
→ verifies documentation matches the actual implemented behavior
```

If multiple roles are active, the final response should summarize the combined verification outcome.
