---
id: project-intent
version: 1
dimensions:
  - project.intent
  - project.delivery-stage
  - project.domain
  - project.user-groups
activation: always-considered
prerequisites:
  - discovery.subject
outputs:
  - .agents/context/project-profile.md
  - .agents/context/harness-scope.md
---

# Project Intent

Resolve what should be built or changed, why it matters, who uses it and how mature the intended result must be.

Evaluate this topic only inside the resolved discovery-subject boundary. Do not infer product intent from `AGENTS.md`, `.agents/**`, `.opencode/**`, `opencode.jsonc`, toolkit templates or installer documentation. Those sources describe the control system unless the toolkit itself is the confirmed product.

## Evidence signals

```text
user request
the target product's README and product documentation
existing source and release structure
issue or refinement input
```

## Candidate patterns

```text
What outcome should this project or change produce?
Is this a new build, extension, migration, refactoring or documentation effort?
Should the result be treated as an experiment, internal tool or production system?
Who uses it and which domain constraints materially affect development?
```

Combine these only when one concise hypothesis confirmation resolves several dimensions.

## Completion

Complete when purpose, delivery expectations and relevant users are sufficient to choose governance depth and generated artifacts.
