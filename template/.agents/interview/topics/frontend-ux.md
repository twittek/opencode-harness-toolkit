---
id: frontend-ux
version: 1
dimensions:
  - architecture.frontend
  - quality.browser
  - quality.accessibility
  - product.user-experience
activation-signals:
  - frontend-framework
  - browser-assets
  - user-facing-interface
outputs:
  - .agents/roles/ux-designer.md
  - .agents/roles/accessibility-specialist.md
  - .agents/playbooks/testing.md
---

# Frontend and UX

Resolve UI-specific development and verification expectations.

## Evidence signals

```text
frontend manifests and framework configuration
component and route structure
browser or end-to-end tests
design-system dependencies
```

## Candidate patterns

```text
Which user journeys are critical enough to require browser-level verification?
Which accessibility or design-system requirements must every UI change satisfy?
Does a design source such as Figma define expected behavior or only visual guidance?
```

Avoid asking for a framework already established by reliable manifests unless migration is plausible.

## Completion

Complete when UI roles, required checks and design/accessibility constraints can be generated.
