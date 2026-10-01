---
id: delivery-operations
version: 1
dimensions:
  - runtime.deployment
  - runtime.environments
  - delivery.ci-cd
  - operations.observability
activation-signals:
  - ci-config
  - container-files
  - infrastructure-manifests
  - production-target
outputs:
  - .agent/roles/devops-engineer.md
  - .agent/roles/observability-engineer.md
---

# Delivery and Operations

Resolve how changes are built, deployed and observed, and which actions are approval-gated.

## Evidence signals

```text
CI/CD configuration
Docker and OCI files
Kubernetes, Terraform or cloud manifests
logging, metrics and tracing configuration
```

## Candidate patterns

```text
Which environments may the agent affect?
May the agent modify pipelines or deployment manifests?
Which deployment actions require approval or are completely forbidden?
What operational evidence is required before completion?
```

## Completion

Complete when deployment boundaries, pipeline responsibilities and operational checks can be expressed safely.
