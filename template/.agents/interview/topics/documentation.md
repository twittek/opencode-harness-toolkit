---
id: documentation
version: 1
dimensions:
  - documentation.audiences
  - documentation.required-artifacts
  - documentation.maintenance
activation-signals:
  - docs-tree
  - adr-records
  - release-process
  - refinement-workflow
outputs:
  - .agent/roles/technical-writer.md
  - .agent/templates
---

# Documentation

Resolve which documentation is part of completion and who consumes it.

## Evidence signals

```text
README and docs structure
ADRs and architecture notes
release and changelog process
issue and refinement templates
```

## Candidate patterns

```text
Which documentation must change together with code or architecture changes?
Which audiences need generated artifacts?
Are refinement, review, test or release documents required?
```

## Pruning

Do not ask when repository policy already defines documentation obligations and no conflict exists.

## Completion

Complete when required documentation artifacts and maintenance triggers are known.
