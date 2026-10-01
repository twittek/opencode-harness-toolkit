---
id: backend-data
version: 1
dimensions:
  - architecture.backend
  - architecture.api
  - architecture.data
  - data.migration-risk
activation-signals:
  - backend-framework
  - api-schema
  - database-schema
  - data-pipeline
outputs:
  - .agent/roles/data-engineer.md
  - .agent/playbooks/development-best-practices.md
  - .agent/playbooks/testing.md
---

# Backend and Data

Resolve API, persistence and data-change constraints that affect agent behavior.

## Evidence signals

```text
backend manifests
API specifications
database schemas and migrations
data pipeline definitions
```

## Candidate patterns

```text
Which API contracts require compatibility protection?
May the agent create or modify database migrations, and under which approval gate?
Which data flows or persistence boundaries are safety-critical?
```

## Completion

Complete when API compatibility, persistence responsibilities and migration boundaries are sufficiently known.
