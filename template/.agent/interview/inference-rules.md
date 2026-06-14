# Inference Rules

## Frontend-only

If the project is frontend-only, increase:

- frontend-learning-project
- browser-game-prototype
- internal-ui-tool

Decrease:

- backend-api-service
- database-migration
- integration-heavy-enterprise-project

Prune unless contradicted:

- backend deployment
- database migrations
- API contract governance
- enterprise auth

## Production

If the project is production-bound, increase:

- security-engineer role
- quality gates
- deployment policy
- observability policy
- dependency governance

## Learning or prototype

If learning/prototype, increase:

- fast feedback
- lightweight quality gates
- simple documentation

Prune:

- formal release management
- production monitoring
- enterprise governance

## External systems exist

If external systems are present, increase:

- integration-policy
- wrapper-scripts
- MCP-planning
- access-boundaries
- credential-policy

Keep:

- .agent/context/integration-policy.md
- .agent/integrations/external-systems.md
- .agent/mcp/mcp-policy.md

If GitLab is selected, keep:

- .agent/integrations/gitlab.md
- .agent/scripts/gitlab-issue-comment.sh

If GitHub is selected, keep:

- .agent/integrations/github.md
- .agent/scripts/github-issue-comment.sh

If Jira is selected, keep:

- .agent/integrations/jira.md
- .agent/scripts/jira-issue-comment.example.sh

If no external systems are present, prune:

- integration-specific wrapper scripts
- MCP discovery
- external documentation access
- issue tracker automation

## Role model inference

If authentication, authorization, secrets or sensitive data are present, keep:

```text
security-engineer
reviewer
integration-architect when external systems are involved
```

If user-facing UI is present, keep:

```text
ux-designer
accessibility-specialist
tester
```

If CI/CD, deployment or operations are present, keep:

```text
devops-engineer
observability-engineer
security-engineer for production-adjacent changes
```

If external systems or automation are present, keep:

```text
integration-architect
security-engineer
```

If data pipelines, reporting or migrations are present, keep:

```text
data-engineer
tester
performance-engineer when data size or latency matters
```

If business rules or specialized terminology are present, keep:

```text
domain-expert
requirements-engineer
product-manager
```

## Context loading inference

If the model has a large context window such as 128K, do not infer that the whole harness should always be loaded.

Prefer:

```text
128K optimized
modular loading
strong context hygiene
smallest useful context set
```

Prune from automatic context:

```text
node_modules
dist
build
coverage
template
*.bak.*
.DS_Store
```

## Self-verification inference

If the task changes files, configuration, generated artifacts, lifecycle commands, MCP settings or integration behavior, require at least standard self-verification.

Prefer strict self-verification when the task touches:

```text
- harness policies
- OpenCode configuration
- MCP configuration
- external systems
- security, secrets or permissions
- generated release artifacts
- production-adjacent workflows
```

Never infer that verification can be skipped because the task appears simple.
