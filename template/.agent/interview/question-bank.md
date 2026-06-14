# Question Bank

Questions should be selected by expected information gain, not by fixed order.

## High-value early questions

```text
Soll das Ergebnis produktiv betrieben werden?
```

```text
Does the application have a backend?
```

```text
Gibt es echte Nutzer, Rollen oder Berechtigungen?
```

```text
Are there external systems or integrations?
```

```text
Ist es ein Neubau, eine Erweiterung, eine Migration oder ein Refactoring?
```

```text
Soll der Agent Code ändern oder primär planen/dokumentieren?
```

## Lower-value detail questions

Ask later only if the branch is active:

```text
Welche konkrete Testlibrary nutzt ihr?
```

```text
Welche konkrete Datenbank?
```

```text
Welcher konkrete MCP-Server?
```

```text
Welcher konkrete GitLab-Befehl?
```

## Integration discovery questions

High-value early question:

```text
Are there external systems or tools the agents should know about?
```

Repository and review branch:

```text
Which repository and code review system do you use?
```

Work tracking branch:

```text
Which work tracking system do you use?
```

Documentation branch:

```text
Which documentation or knowledge system do you use?
```

Design branch:

```text
Which design or UX system do you use?
```

Quality branch:

```text
Which quality, security or monitoring tools are relevant?
```

Avoid asking for CLI commands before the system itself is known.

## MCP discovery questions

Use these questions in `/harness-mcp`.

```text
Which MCP outcome do you want?
```

Options:

```text
A) Document existing MCP servers only
B) Recommend useful MCP servers
C) Create an installation plan
D) Review an MCP server before approval
E) Update OpenCode MCP config after approval
F) Other / custom
```

```text
Which external systems should MCP support first?
```

Options:

```text
A) GitLab / GitHub
B) Jira / work tracking
C) Confluence / documentation
D) Figma / design
E) Browser automation
F) Filesystem / local tools
G) Database / analytics
H) Other / custom
```

## Role model discovery questions

High-value early question:

```text
Which specialist perspectives should the harness include?
```

Options:

```text
A) Keep it minimal: architect, requirements, developer, tester, reviewer
B) Security and compliance
C) UX and accessibility
D) DevOps and operations
E) Integrations and external systems
F) Data, analytics or reporting
G) Domain expertise and business rules
H) Multiple specialist roles
I) Other / custom
```

Follow-up questions:

```text
Does the project handle authentication, authorization, secrets or sensitive data?
Does the project include user-facing interfaces?
Does the project require deployment or operational support?
Does the project require domain-specific business knowledge?
```

## Context loading questions

```text
How should the harness manage context loading?
```

Options:

```text
A) Compact: load only baseline files and explicit task files
B) Balanced: baseline plus relevant roles, integrations and policies
C) Rich: use more harness context when the model has a large context window
D) 128K optimized: modular loading with strong context hygiene
E) Other / custom
```

## Self-verification questions

High-value verification question:

```text
How strict should final self-verification be?
```

Options:

```text
A) Lightweight: short requirement check before final response
B) Standard: requirement match, changed files and checks run
C) Strict: requirement traceability, tests/checks, risks and assumptions
D) Regulated: evidence-based verification and explicit approval points
E) Other / custom
```

Default recommendation:

```text
Standard for normal projects.
Strict for harness changes, integrations, MCP, security-sensitive work or production-adjacent systems.
```
