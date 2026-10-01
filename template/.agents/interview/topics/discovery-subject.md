---
id: discovery-subject
version: 1
dimensions:
  - discovery.subject
  - discovery.target-root
  - discovery.mode
activation: always-evaluated-before-product-discovery
outputs:
  - .agent/context/project-profile.md
  - .agent/context/harness-scope.md
---

# Discovery Subject

Resolve which product, application, service or bounded subproject the harness is meant to support. This establishes the evidence boundary for every later topic.

## Evidence signals

```text
the user's current request
workspace and repository roots
product source and product documentation outside harness-control paths
monorepo workspace definitions
existing harness metadata indicating—but not defining—the target
toolkit or template files that may otherwise be mistaken for product files
```

## Evidence classes

```text
product evidence
→ eligible to describe purpose, domain, users and architecture

harness/control evidence
→ AGENTS.md, .agent/**, .opencode/** and opencode.jsonc
→ eligible only for inherited constraints and current harness state

toolkit/package evidence
→ template/**, installers and toolkit maintenance documentation
→ excluded unless toolkit-self-development is confirmed
```

## Candidate patterns

Use a subject question only when evidence cannot resolve the boundary with high confidence:

```text
Welche fachliche oder technische Lösung soll diese Harness unterstützen:
das Produkt in diesem Repository, das Harness-Toolkit selbst oder ein bestimmtes Modul?

Ich sehe mehrere mögliche Produktgrenzen im Monorepo. Für welchen Pfad oder welches Modul soll die Harness gelten?
```

Adapt the choices to the actual repository. Include the inferred default when one exists.

## Pruning

Do not ask this topic's question when the user's request and product evidence identify one target unambiguously.

## Completion

Complete when discovery mode, target root and subject identity are confirmed or strongly inferred, and harness/toolkit paths have been classified separately from product evidence.

This topic must complete before project-intent and architecture evidence is interpreted.
