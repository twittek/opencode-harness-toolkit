---
description: "Initialize the project harness through a guided one-question-at-a-time setup assistant."
---

# Harness Init Command

## Goal

Create the initial project-specific AI-agent harness.

The purpose of the harness is fixed:

```text
To make an AI agent reliable, controlled, repeatable, and project-specific for this project.
```

Do not ask the user why a harness is needed. Ask what the project needs so the harness can be configured correctly.

## Language

- Ask interview questions in German.
- Write generated harness files in English.
- Report results in German.


## Integration & Tooling Discovery

The adaptive interview must discover external systems early, because they strongly influence the generated harness.

Use information-gain logic:

Good early question:

```text
Are there external systems or tools the agents should know about?
```

This can activate or prune large branches:

```text
- issue tracking
- code review
- documentation systems
- design systems
- quality analysis
- monitoring
- CI/CD
- cloud/deployment
- MCP planning
- wrapper scripts
```

### One-question-at-a-time flow

Do not ask for all integration details at once.

Recommended sequence:

Question 1:

```text
Are there external systems or tools the agents should know about?
```

Options:

```text
A) No external systems
B) Repository and code review only
C) Work tracking / tickets
D) Documentation / knowledge base
E) Design / UX tools
F) Quality / security / monitoring tools
G) Multiple systems
H) Other / custom
```

If the user selects a branch, ask exactly one follow-up question for that branch.

Example:

```text
Which repository and code review system do you use?
```

Options:

```text
A) GitLab
B) GitHub
C) Azure DevOps
D) Bitbucket
E) Local Git only
F) Other / custom
```

Example:

```text
Which work tracking system do you use?
```

Options:

```text
A) Jira
B) GitLab Issues
C) GitHub Issues
D) Azure Boards
E) Linear
F) Other / custom
```

Example:

```text
Which documentation or knowledge system do you use?
```

Options:

```text
A) Confluence
B) GitHub/GitLab Wiki
C) Notion
D) Markdown in repository
E) SharePoint
F) Other / custom
```

Example:

```text
Which design or UX system do you use?
```

Options:

```text
A) Figma
B) Sketch
C) Adobe XD
D) Design files in repository
E) No dedicated design system
F) Other / custom
```

Example:

```text
Which quality, security or monitoring tools are relevant?
```

Options:

```text
A) SonarQube / SonarCloud
B) Sentry
C) Grafana / Prometheus
D) Datadog
E) OWASP / dependency scanning
F) Other / custom
```

### Generated integration artifacts

When external systems are present, generate or update:

```text
.agent/context/integration-policy.md
.agent/integrations/external-systems.md
```

When a known system is selected, also generate or update the matching file:

```text
.agent/integrations/gitlab.md
.agent/integrations/github.md
.agent/integrations/jira.md
.agent/integrations/confluence.md
.agent/integrations/figma.md
.agent/integrations/sonarqube.md
```

When wrappers are useful, generate or keep scripts under:

```text
.agent/scripts/
```

Examples:

```text
.agent/scripts/gitlab-issue-comment.sh
.agent/scripts/github-issue-comment.sh
.agent/scripts/jira-issue-comment.example.sh
```

### Integration policy rules

The generated harness must document for each external system:

```text
- purpose
- access method
- read permissions
- write permissions
- approval requirements
- forbidden operations
- wrapper scripts
- credential expectations without storing secrets
```

Default:

```text
unknown system → no access
write action → explicit approval required
secret handling → never store secrets in harness files
```

### MCP planning

If the user mentions MCP servers or asks for tool automation, document MCP candidates in:

```text
.agent/mcp/mcp-policy.md
```

Do not install MCP servers during `/harness-init`.

Only create recommendations or installation plans unless the user explicitly requests an installation step.

## Guided interview mode

`/harness-init` must behave like a guided setup assistant.

### Interaction rules

- Ask exactly one question at a time.
- Do not present long grouped question blocks.
- Wait for the user's answer before asking the next question.
- Prefer OpenCode's ask/question tool for questions with predefined options.
- If the ask/question tool is available, use selectable options.
- If the ask/question tool is unavailable or fails, fall back to plain text A/B/C options.
- Always include an `Other / custom` option when predefined options may not fit.
- Let the user answer by selecting an option, typing the letter, or writing free text.
- After every answer, silently update the project understanding and decide the next most relevant question.
- Skip questions that are already answered by the user's previous responses.
- Ask follow-up questions only when the answer changes generated files, safety rules, or workflow behavior.
- Do not generate or modify files during the interview phase.
- Do not generate the harness until the user explicitly confirms the final summary.

### Strict OpenCode config contract

When generating `opencode.jsonc`, generate a valid OpenCode project configuration from the start.

Required top-level shape:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "<provider/model>",
  "instructions": ["AGENTS.md"],
  "permission": {},
  "command": {}
}
```

Allowed optional top-level keys only when explicitly needed:

```text
mcp
compaction
formatter
lsp
```

Do not invent OpenCode config keys.

Forbidden top-level keys:

```text
agents
agent
commands
permissions
providers
provider
tools
tool
rules
```

Forbidden command properties:

```text
agent
agents
model
permission
permissions
tools
```

Each command entry must contain only:

```text
description
template
```

Required lifecycle commands:

```jsonc
"command": {
  "harness-init": {
    "description": "Initialize the project harness.",
    "template": "Follow `.opencode/command/harness-init.md` exactly."
  },
  "harness-check": {
    "description": "Audit the current harness version.",
    "template": "Follow `.opencode/command/harness-check.md` exactly."
  },
  "harness-update": {
    "description": "Apply active findings for the current harness version.",
    "template": "Follow `.opencode/command/harness-update.md` exactly."
  },
  "harness-retro": {
    "description": "Collect usage feedback for the current harness version.",
    "template": "Follow `.opencode/command/harness-retro.md` exactly."
  }
}
```

Role descriptions must be stored under:

```text
.agent/roles/
```

Do not create `.opencode/agent/*.md` and do not reference role files from `opencode.jsonc`.

### Ask-tool preference

For multiple-choice questions, use OpenCode's ask/question capability with selectable options whenever possible.

Use this behavior conceptually:

```text
Question title: Project type
Question: Welche Art von Projekt ist das?
Options:
- Frontend-only application
- Backend/API service
- Fullstack application
- CLI/tooling project
- Library/package
- Monorepo
- Other / custom
```

If the ask/question tool is not available, render the same question as plain text:

```text
Frage 1: Welche Art von Projekt ist das?

A) Frontend-only Anwendung
B) Backend/API-Service
C) Fullstack-Anwendung
D) CLI-/Tooling-Projekt
E) Library/Package
F) Monorepo
G) Sonstiges / eigene Beschreibung

Bitte antworte mit A–G oder beschreibe es kurz frei.
```

### Interview state

Maintain an internal interview state with these fields:

- project_goal
- project_type
- target_result
- domain
- users
- tech_stack
- frontend_stack
- backend_stack
- persistence
- auth
- deployment
- git_hosting
- issue_workflow
- agent_responsibilities
- autonomy_level
- forbidden_actions
- quality_gates
- test_strategy
- documentation_needs
- special_tools
- open_questions
- skipped_sections

Do not print the full state after every answer unless the user asks for it.

### Initial question

Start with this exact first question in German:

```text
Lass uns die Harness Schritt für Schritt aufsetzen.

Frage 1: Welche Art von Projekt ist das?

A) Frontend-only Anwendung
B) Backend/API-Service
C) Fullstack-Anwendung
D) CLI-/Tooling-Projekt
E) Library/Package
F) Monorepo
G) Sonstiges / eigene Beschreibung

Bitte antworte mit A–G oder beschreibe es kurz frei.
```

If selectable options are available, present the same options as selectable choices.

## Adaptive interview flow

Ask questions in this order, but skip irrelevant sections based on previous answers.

### 1. Project type

Question:
Welche Art von Projekt ist das?

Options:
- Frontend-only application
- Backend/API service
- Fullstack application
- CLI/tooling project
- Library/package
- Monorepo
- Other / custom

Routing:
- Frontend-only: skip backend, database, API deployment unless mentioned.
- Backend/API: ask API, persistence, auth, deployment.
- Fullstack: ask frontend and backend.
- CLI/tooling: ask commands, inputs, outputs, test strategy.
- Library/package: ask package manager, public/private usage, API surface, release process.
- Monorepo: ask packages/apps and boundaries.

### 2. Target result

Question:
Was soll am Ende entstehen?

Options:
- Learning project / experiment
- Prototype
- MVP
- Internal tool
- Production application
- Migration/refactoring project
- Other / custom

Routing:
- Learning/prototype: use lighter governance, but keep safety rules.
- MVP/production: ask stricter questions about quality gates, tests, deployment, security.
- Migration/refactoring: ask about existing constraints and regression safety.

### 3. Domain and users

Question:
In welcher Domäne bewegt sich das Projekt und wer nutzt es?

Options:
- Consumer/web game
- Internal business application
- Customer-facing portal
- Developer tooling
- Data/AI workflow
- Energy/utilities domain
- Other / custom

Ask a short free-text follow-up only if needed:
Welche Nutzergruppen oder Rollen sind relevant?

### 4. Tech stack

Question:
Welcher Tech Stack ist geplant oder vorhanden?

Options:
- React + Vite + TypeScript
- Angular
- Vue/Nuxt
- Node/NestJS
- Java/Spring
- Python
- Other / custom
- Unknown yet

Routing:
- If frontend stack only: ask UI, tests, browser tooling.
- If backend included: ask API style, persistence, auth.
- If unknown: generate technology-neutral harness.

### 5. Persistence

Ask only if backend/fullstack/data project or user mentioned persistence.

Question:
Gibt es Persistenz oder Datenbankänderungen?

Options:
- No persistence
- Local/browser storage only
- SQL database
- NoSQL database
- Files/object storage
- Existing database
- Other / custom

### 6. Authentication and permissions

Ask only if users/accounts/security are relevant.

Question:
Gibt es Authentifizierung, Rollen oder Berechtigungen?

Options:
- No auth
- Simple local/demo auth
- OAuth/OIDC/Keycloak
- Existing enterprise auth
- Role-based permissions
- Unknown yet
- Other / custom

### 7. Git and issue workflow

Question:
Welche Git-/Issue-Umgebung soll die Harness unterstützen?

Options:
- Git only, no issue automation
- GitLab with glab
- GitHub with gh
- Local only
- Not decided yet
- Other / custom

Routing:
- GitLab: ask repository path and whether project ID is known.
- GitHub: ask owner/repo if needed.
- Local only: skip issue/MR automation.

### 8. Agent responsibilities

Question:
Welche Arbeiten soll der Agent übernehmen?

Options:
- Requirements/refinement
- Architecture planning
- Implementation
- Testing
- Review
- Documentation
- Issue/MR communication
- All of the above
- Other / custom

Allow multiple selections if the ask tool supports it. If not, ask the user to list letters.

### 9. Autonomy level

Question:
Wie autonom darf der Agent arbeiten?

Options:
- Very cautious: ask before most edits
- Balanced: edit normal project files, ask for risky actions
- Implementation-focused: make scoped changes and run tests
- Highly autonomous in sandbox only
- Custom

Default:
Balanced.

### 10. Forbidden actions

Question:
Welche Aktionen sollen grundsätzlich verboten oder genehmigungspflichtig sein?

Options:
- Merge/close/delete branches
- Deployments
- Dependency additions
- Auth/permission changes
- Database migrations
- File deletions
- Test weakening
- Production data access
- All safety defaults
- Custom

Allow multiple selections if possible. Default:
All safety defaults.

### 11. Quality gates

Question:
Welche Qualitätsprüfungen sollen als Standard gelten?

Options:
- lint
- typecheck
- unit tests
- integration tests
- e2e tests
- build
- accessibility checks
- visual regression
- manual smoke test
- Other / custom

Allow multiple selections if possible.

### 12. Special tools

Question:
Welche zusätzlichen Tools soll die Harness berücksichtigen?

Options:
- Chrome DevTools MCP
- GitLab/glab wrapper scripts
- GitHub/gh wrapper scripts
- Playwright
- Cypress
- Docker
- Local LLM/LiteLLM/OpenCode setup
- None
- Other / custom

### 13. Documentation needs

Question:
Welche Dokumentation soll der Agent pflegen oder erzeugen?

Options:
- README
- Architecture notes
- ADRs
- Refinement documents
- Test reports
- MR descriptions
- Changelog
- User documentation
- Other / custom

## Completion criteria for the interview

The interview is complete when enough information exists to safely generate:

- OpenCode config
- AGENTS.md
- lifecycle commands
- role descriptions
- context files
- playbooks
- templates
- quality gate scripts
- optional GitLab/GitHub scripts

Do not over-interview. Prefer a concise setup that can later be improved through `/harness-retro`.

## Final summary and approval

Before generating files, show a concise German summary:

```text
Zusammenfassung der geplanten Harness

- Projektart:
- Zielbild:
- Domäne/Nutzer:
- Tech Stack:
- Git-/Issue-Workflow:
- Agentenrollen:
- Autonomie-Level:
- Sicherheitsgrenzen:
- Quality Gates:
- Zusätzliche Tools:
- Zu erzeugende Dateien:

Soll ich die Harness jetzt mit diesen Annahmen erzeugen?
```

Options:
- Yes, generate the harness
- Adjust answers
- Cancel

If selectable options are available, use them.

Only generate files after explicit confirmation such as:
- "Ja"
- "Generate"
- "Erzeugen"
- selecting "Yes, generate the harness"

If the user chooses "Adjust answers", ask which section should be changed and continue the interview.

## OpenCode config hardening rules

The generated `opencode.jsonc` must be schema-safe.

Mandatory rules:

- Use `instructions` as an array:

```jsonc
"instructions": ["AGENTS.md"]
```

- Use `command`, not `commands`.
- Use `permission`, not `permissions`.
- Do not create an `agents` object/map in `opencode.jsonc`.
- Do not add `agent` fields to command definitions.
- Do not reference `.opencode/agent/*.md` from `opencode.jsonc`.
- Do not invent OpenCode config keys.
- Keep command definitions minimal: `description` and `template` only.
- Keep provider/model configuration simple and do not modify global provider files.
- Preserve existing known-good provider names unless the developer explicitly asks to change them.

Allowed `opencode.jsonc` shape:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "<provider>/<model>",
  "instructions": ["AGENTS.md"],
  "permission": {
    "edit": "ask",
    "bash": {
      "git *": "allow",
      "npm run *": "allow",
      "pnpm *": "allow",
      "npx *": "ask",
      "rm *": "deny",
      "*": "ask"
    },
    "external_directory": {
      "~/secrets/**": "deny",
      "*": "ask"
    }
  },
  "command": {
    "harness-init": {
      "description": "Initialize the project harness.",
      "template": "Follow `.opencode/command/harness-init.md` exactly."
    },
    "harness-check": {
      "description": "Audit the current harness version.",
      "template": "Follow `.opencode/command/harness-check.md` exactly."
    },
    "harness-update": {
      "description": "Apply active findings for the current harness version.",
      "template": "Follow `.opencode/command/harness-update.md` exactly."
    },
    "harness-retro": {
      "description": "Collect usage feedback for the current harness version.",
      "template": "Follow `.opencode/command/harness-retro.md` exactly."
    }
  }
}
```

Forbidden `opencode.jsonc` patterns:

```jsonc
"instructions": "AGENTS.md"
"agents": { "developer": ".opencode/agent/developer.md" }
"commands": []
"permissions": {}
"command": { "x": { "agent": "developer" } }
```

If role files are needed, create them under:

```text
.agent/roles/
```

Do not create `.opencode/agent/*.md` unless the exact OpenCode agent file schema is explicitly known and requested by the developer.

## Required generated output files

Generate at least:

- `AGENTS.md`
- `opencode.jsonc`
- `.opencode/command/harness-init.md`
- `.opencode/command/harness-check.md`
- `.opencode/command/harness-update.md`
- `.opencode/command/harness-retro.md`
- `.agent/context/project-profile.md`
- `.agent/context/harness-scope.md`
- `.agent/context/harness-version.json`
- `.agent/context/harness-changelog.md`
- `.agent/context/context-index.md`
- `.agent/context/definition-of-done.md`
- `.agent/context/autonomy-policy.md`
- `.agent/context/risk-profile.md`
- `.agent/context/context-safety-policy.md`
- `.agent/roles/architect.md`
- `.agent/roles/refinement.md`
- `.agent/roles/developer.md`
- `.agent/roles/tester.md`
- `.agent/playbooks/refinement.md`
- `.agent/playbooks/architecture.md`
- `.agent/playbooks/development-best-practices.md`
- `.agent/playbooks/testing.md`
- `.agent/playbooks/review.md`
- `.agent/playbooks/harness-check.md`
- `.agent/playbooks/harness-update.md`
- `.agent/playbooks/harness-retrospective.md`
- `.agent/templates/refinement.md`
- `.agent/templates/architecture-plan.md`
- `.agent/templates/review-report.md`
- `.agent/templates/test-report.md`
- `.agent/templates/mr-description.md`
- `.agent/scripts/quality-gates.sh`
- `.agent/scripts/load-issue.sh`
- `.agent/runs/.gitkeep`

Generate optional files only when relevant.

## Required post-generation self-check

Before reporting success, verify:

```bash
grep -R '"agents"\|"commands"\|"permissions"\|"agent":\|"provider"\|"providers"' opencode.jsonc .opencode 2>/dev/null || true
```

The result must not show invalid OpenCode config keys.

Also verify:

- `opencode.jsonc` contains `"instructions": ["AGENTS.md"]`
- `opencode.jsonc` contains `"command"`
- `opencode.jsonc` contains `"permission"`
- lifecycle command files exist
- role files exist under `.agent/roles/`
- no `.opencode/agent` directory was created
- no unknown OpenCode config keys were generated

If invalid keys are found, fix them before finishing.

## Final response after generation

Report in German:

- that the guided interview was completed
- what was created
- where the harness files are
- current harness version
- whether the OpenCode config self-check passed
- recommended next command: `/harness-check`
