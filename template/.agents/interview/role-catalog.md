# Role Catalog

This catalog is discovery input for `/harness-init`. It is not a list of roles that must all be installed.

The interview derives role candidates from the confirmed project scope, agent responsibilities, risk profile and expected work. The user confirms the final role set before generation.

## Selection principles

```text
select the smallest role set that covers expected work and material risks
do not install every core role by default
combine responsibilities when separate roles would add no useful guidance
add a custom role when the project's domain requires one
record why every selected role exists
record why plausible but unnecessary roles were excluded
```

## Catalog

| Role id | Primary responsibility | Typical evidence |
|---|---|---|
| `requirements-engineer` | turn ambiguous needs into testable requirements | refinement, issue discovery, acceptance criteria, stakeholder ambiguity |
| `product-manager` | product outcomes, scope and prioritization | MVP decisions, roadmap, user value, competing priorities |
| `domain-expert` | domain language, rules and business correctness | specialized domain, regulated processes, complex business rules |
| `architect` | system boundaries and durable technical decisions | multiple components, architecture work, migrations, scalability |
| `developer` | implement and refactor product changes | implementation, maintenance, bug fixing |
| `tester` | verification strategy and regression protection | tests, quality gates, release confidence |
| `reviewer` | independent review against policy and quality criteria | pull requests, release gates, high-impact changes |
| `security-engineer` | security, permissions and sensitive operations | auth, secrets, sensitive data, external writes, production access |
| `integration-architect` | external-system contracts and failure behavior | APIs, webhooks, GitLab, GitHub, Jira, MCP or third-party services |
| `ux-designer` | user flows, interaction clarity and UX behavior | user-facing UI, forms, onboarding, dashboards |
| `accessibility-specialist` | inclusive interaction and accessibility | WCAG obligations, public UI, keyboard or assistive-technology use |
| `data-engineer` | data models, movement and traceability | databases, migrations, ETL, reporting, analytics |
| `devops-engineer` | build, release, deployment and runtime operations | CI/CD, containers, infrastructure, environments |
| `observability-engineer` | diagnosability and operational signals | logs, metrics, traces, alerts, incident response |
| `performance-engineer` | performance risks and budgets | latency, throughput, large data, rendering, concurrency |
| `technical-writer` | maintained documentation for defined audiences | developer docs, user docs, runbooks, compliance documentation |

## Confirmation contract

When role selection is not already explicit, ask one adaptive confirmation question after enough project evidence exists to make a concrete recommendation.

The question must:

```text
show the proposed roles and a one-line project-specific reason for each
allow roles to be added, removed or replaced with a custom role
support multiple selection when the question tool allows it
avoid presenting every catalog role as a checklist
```

## Generated role contract

Every selected role becomes one file under `.agents/roles/<role-id>.md` and must be tailored to the resolved discovery subject.

Each generated role contains:

```text
YAML frontmatter with role id, generated-by: harness-init and harness version
project-specific mission
responsibilities and explicit non-responsibilities
activation and deactivation triggers
required context and applicable policies
approval and escalation boundaries
project-specific checks and expected outputs
handoff or collaboration rules when other selected roles are involved
```

Do not copy generic catalog prose unchanged into a generated role file.
