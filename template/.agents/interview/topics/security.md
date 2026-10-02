---
id: security
version: 1
dimensions:
  - security.authentication
  - security.authorization
  - security.data-sensitivity
  - security.secret-handling
activation-signals:
  - identity-library
  - user-accounts
  - production-target
  - sensitive-domain
  - external-credentials
blocking-when-relevant: true
outputs:
  - .agents/context/risk-profile.md
  - .agents/roles/security-engineer.md
---

# Security

Resolve security boundaries before generation when the project handles users, credentials, sensitive data or production access.

## Evidence signals

```text
identity and authorization configuration
secret references
security scanners
data classification documentation
deployment environment
```

## Candidate patterns

```text
Which authentication and authorization boundaries may the agent modify?
What data must be treated as sensitive or regulated?
How are secrets supplied, and which secret-related actions are forbidden?
Which security changes always require human approval?
```

## Safe defaults

```text
unknown secret values are never requested or stored
unknown production access is forbidden
auth and permission changes require approval
```

## Completion

Complete when the harness can express applicable security roles, prohibitions and approval boundaries.
