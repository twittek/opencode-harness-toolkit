# Interview Topic Catalog

Load this index before selecting interview topics. Load a full topic pack only when its signals are present or its relevance is uncertain and potentially high-impact.

| Topic | File | Primary uncertainty | Typical activation signals |
|---|---|---|---|
| Discovery subject | `topics/discovery-subject.md` | product or module the harness supports; evidence boundary | always first evaluated; ambiguous roots, monorepos, existing harness or toolkit files |
| Project intent | `topics/project-intent.md` | purpose, change type, delivery stage, users | always considered; repository state and initial request |
| Architecture | `topics/architecture.md` | system shape, boundaries, ownership | source tree, manifests, migration or implementation work |
| Frontend and UX | `topics/frontend-ux.md` | UI stack, UX, accessibility, browser checks | UI framework, browser assets, user-facing product |
| Backend and data | `topics/backend-data.md` | API, persistence, migrations, data flows | backend framework, schema, database or pipeline evidence |
| Security | `topics/security.md` | auth, permissions, secrets, sensitive data | accounts, identity libraries, production or regulated context |
| Integrations | `topics/integrations.md` | external systems, access methods, writes | Git remotes, tickets, docs, MCPs, third-party APIs |
| Delivery and operations | `topics/delivery-operations.md` | CI/CD, environments, deployment, observability | pipeline and infrastructure manifests |
| Quality and verification | `topics/quality-verification.md` | tests, checks, definition of done | always considered; test and build evidence |
| Agent governance | `topics/agent-governance.md` | responsibilities, autonomy, approvals, prohibitions | always considered; requested agent work |
| Documentation | `topics/documentation.md` | maintained artifacts and audiences | docs tree, ADRs, release or compliance needs |

## Routing rule

Topic presence does not require asking a question. Evidence may resolve a topic without user interaction.

## Extension rule

New topic packs may be added without editing the interview engine. Add one row here and follow the topic contract documented in `topics/README.md`.
