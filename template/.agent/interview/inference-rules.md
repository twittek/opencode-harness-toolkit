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
