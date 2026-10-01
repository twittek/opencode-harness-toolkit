---
id: architecture
version: 1
dimensions:
  - architecture.shape
  - architecture.boundaries
  - architecture.ownership
activation-signals:
  - source-tree
  - build-manifests
  - migration-or-refactoring
outputs:
  - .agent/playbooks/architecture.md
  - .agent/roles/architect.md
---

# Architecture

Resolve system shape and boundaries only to the level needed for agent guidance.

## Evidence signals

```text
workspace and package layout
build manifests
service or module boundaries
architecture documentation and ADRs
```

## Candidate patterns

```text
Which existing architecture boundaries must the agent preserve?
Which packages or services may be changed together, and which must remain isolated?
Is the current structure intentional, transitional or part of a migration?
```

## Pruning

Prune detailed architecture discovery for documentation-only work when no structural guidance will be generated.

## Completion

Complete when the harness can state relevant ownership and change boundaries without inventing architecture.
