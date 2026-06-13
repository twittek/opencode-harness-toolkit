# OpenCode Harness Toolkit 

This toolkit creates a small **OpenCode harness toolbox** for project-specific AI-agent workflows.

It is designed for teams or individual developers who want to make an AI coding agent:

- reliable
- controlled
- repeatable
- project-specific
- maintainable over time

The harness is not just a prompt collection. It is a lightweight operating model for AI-assisted software development.

---

## What this package gives you

After running the toolkit script, your project gets an OpenCode command set:

```text
/harness-init    → create the initial project harness
/harness-check   → audit the current harness version
/harness-update  → apply active findings and increment the harness version
/harness-retro   → collect usage feedback and create retro findings
```

This gives you a full lifecycle:

```text
Initialize → Check → Update → Retro → Check again
```

Think of it like this:

```text
/harness-init    = setup
/harness-check   = technical inspection / TÜV
/harness-update  = controlled implementation of findings
/harness-retro   = team retrospective / satisfaction-based improvement
```

---

## HTML Landing Page

This package includes one standalone HTML landing page:

```text
harness-toolkit.html
```

Open it directly in a browser. No build step is required.

## Quick start

Copy the ZIP file into the root directory of your project, unzip it there, and run the install script.

Example:

```bash
cd /path/to/your/project
cp /path/to/opencode-harness-toolkit.zip .
unzip opencode-harness-toolkit.zip
./opencode-harness-toolkit/opencode-harness-toolkit-install.sh
```

The install script already has the executable flag in the ZIP, so `chmod +x` should not be necessary.

After installation, start OpenCode from the project root:

```bash
opencode
```

Then run:

```text
/harness-init
```

The install script copies the toolkit files from:

```text
opencode-harness-toolkit/template/
```

into your project root. Existing files are backed up before being overwritten.

If your unzip tool does not preserve executable flags, run this fallback once:

```bash
chmod +x opencode-harness-toolkit/opencode-harness-toolkit-install.sh
./opencode-harness-toolkit/opencode-harness-toolkit-install.sh
```

## Package structure

```text
opencode-harness-toolkit/
├── README.md
├── harness-toolkit.html
├── opencode-harness-toolkit-install.sh
└── template/
    ├── AGENTS.md
    ├── opencode.jsonc
    ├── README.md
    ├── .opencode/
    │   └── command/
    │       ├── harness-init.md
    │       ├── harness-check.md
    │       ├── harness-update.md
    │       ├── harness-retro.md
    └── .agent/
        ├── context/
        ├── interview/
        ├── playbooks/
        ├── roles/
        ├── scripts/
        ├── skills/
        ├── templates/
        └── runs/
```

## OpenCode Config Safety

`/harness-init` is instructed to generate a valid OpenCode configuration from the start.

Required rules:

```text
- instructions must be an array: ["AGENTS.md"]
- use command, not commands
- use permission, not permissions
- do not create agents or agent mappings
- do not reference .opencode/agent/*.md
- store role descriptions under .agent/roles/
- command entries should contain only description and template
```

## Template-based toolkit

The package stores the harness scaffold as real files under `template/`.

Benefits:

```text
- easier to maintain
- easier to review
- easier for AI agents to edit safely
- no huge Markdown blocks inside Bash
- toolkit script stays small and stable
- template files can be customized directly
```

The script only performs these actions:

```text
- locate the template directory
- copy template files into the target project
- back up existing files before overwriting
- make helper shell scripts executable
- print next steps
```

## Customizing the bootstrap

To customize what gets installed, edit files directly under:

```text
template/
```

For example:

```text
template/.opencode/command/harness-init.md
template/AGENTS.md
template/opencode.jsonc
```

Then run:

```bash
./opencode-harness-toolkit-install.sh /path/to/your/project
```

## Generated files

The bootstrap creates the minimal command toolbox:

```text
AGENTS.md
opencode.jsonc
.opencode/command/harness-init.md
.opencode/command/harness-check.md
.opencode/command/harness-update.md
.opencode/command/harness-retro.md
.agent/context/harness-version.json
.agent/context/harness-changelog.md
.agent/playbooks/harness-update.md
.agent/runs/.gitkeep
.agent/runs/harness-check/.gitkeep
.agent/runs/harness-update/.gitkeep
.agent/runs/harness-retro/.gitkeep
```

After `/harness-init`, the project-specific harness should additionally contain files such as:

```text
.opencode/agent/architect.md
.opencode/agent/refinement.md
.opencode/agent/developer.md
.opencode/agent/tester.md
.agent/context/project-profile.md
.agent/context/harness-scope.md
.agent/context/context-index.md
.agent/context/definition-of-done.md
.agent/context/autonomy-policy.md
.agent/context/risk-profile.md
.agent/context/context-safety-policy.md
.agent/playbooks/refinement.md
.agent/playbooks/architecture.md
.agent/playbooks/development-best-practices.md
.agent/playbooks/testing.md
.agent/playbooks/review.md
.agent/scripts/quality-gates.sh
.agent/scripts/load-issue.sh
```

Depending on the project, `/harness-init` may also create optional files for GitLab, GitHub, monorepos, security, APIs, documentation, or dependency policies.

---

## Adaptive Scenario Discovery

Harness Toolkit does not use a static questionnaire. The interview follows an **Akinator-style adaptive discovery model**.

The core idea:

```text
Ask the next question that reduces uncertainty the most.
```

This is inspired by:

```text
- Bayesian inference
- entropy reduction
- information gain
- decision trees
- active learning
- adaptive questioning
```

The agent starts with many possible development scenarios and uses every answer to update its hypothesis.

Example scenario candidates:

```text
frontend-learning-project
browser-game-prototype
production-saas-application
internal-business-tool
backend-api-service
integration-heavy-enterprise-project
data-ai-workflow
legacy-migration
library-package
devops-automation
```

After each answer, the agent updates which scenarios are more likely and prunes irrelevant branches.

### Mathematical foundations

The interview combines several related fields:

```text
Bayesian inference
→ probability theory and Bayesian statistics
→ updates the likelihood of possible project scenarios after every answer

Information gain and entropy reduction
→ information theory
→ selects the question that reduces uncertainty the most

Decision trees and pruning
→ machine learning, computer science and statistics
→ removes irrelevant branches of the scenario space as soon as they become unlikely

Active learning and adaptive questioning
→ machine learning
→ the system actively chooses the next most useful question instead of following a static form
```

A concise description:

```text
Bayesian scenario inference meets information-gain-based questioning.
```

Or in German:

```text
Bayessche Szenario-Inferenz trifft auf informationsgewinnbasierte Fragenauswahl.
```

This distinction is important:

```text
Bayesian inference decides how beliefs change after an answer.
Information theory decides which question is worth asking next.
Decision-tree pruning decides which branches can be skipped.
Active learning turns the interview into an adaptive process.
```

Together, these ideas make the interview feel intelligent: the agent does not ask everything. It asks the question with the highest expected value for reducing uncertainty.

### Why question order matters

A weak early question is too specific:

```text
Do you use Oracle Spatial?
```

This is a bad first question because it only helps if the project is already known to be GIS- or integration-heavy.

A stronger early question is:

```text
Are there external systems or integrations?
```

This splits the project space much earlier. If the answer is "No", the agent can skip integration policies, MCP discovery, external credentials and wrapper scripts. If the answer is "Yes", those branches stay active.

Another weak early question:

```text
Do you use Vitest or Jest?
```

A better earlier question:

```text
Should automated tests be part of the quality gates?
```

Only after the answer is "Yes" does it make sense to ask about the concrete test runner.

Another weak early question:

```text
Should a GitLab issue comment be created with glab issue note?
```

A better earlier question:

```text
Which system do you use for work items and code reviews?
```

Options might be:

```text
A) GitLab
B) GitHub
C) Jira
D) Azure DevOps
E) Local only
F) Other / custom
```

### Bayesian update behavior

The agent should behave as if it maintains a probability distribution over possible project scenarios.

Example answer:

```text
Frontend-only application
```

Likely scenarios increase:

```text
frontend-learning-project
browser-game-prototype
ui-prototype
static-webapp
```

Less likely scenarios decrease:

```text
backend-api-service
database-migration
enterprise-integration-platform
devops-automation-only
```

Pruned by default:

```text
database migrations
enterprise auth
backend deployment
API contract governance
```

This is how the interview becomes short and intelligent: irrelevant branches disappear immediately.

### Decision-tree pruning

The interview should feel like a well-designed decision tree.

Good:

```text
Does the application have a backend?
```

This can remove a large number of follow-up questions.

Bad:

```text
If the application has a backend: does it use NestJS, and if yes, does it use PostgreSQL, and if yes, does it need migrations?
```

That violates the interview principle.

The rule is:

```text
One question. One answer. Update the model. Ask the next best question.
```

### Step-by-step principle

The interview must follow the Akinator principle:

```text
Is it an animal?
```

not:

```text
Is it an animal and, if yes, does it have four legs and, if yes, does it live in water?
```

For Harness Toolkit, this means:

```text
- exactly one question at a time
- selectable OpenCode multiple-choice options whenever available
- A/B/C fallback when selectable options are unavailable
- always include Other / custom
- no file generation before the final summary and explicit approval
```

### Real AI bootstrapping

This is real bootstrapping:

```text
An AI identifies its own missing context,
asks analytically optimized questions,
closes the highest-value information gaps first,
and then generates its own productive project harness.
```

The generated harness is not just a generic template. It is the first productive version of the project's agent operating system.

## Integration & Tooling Discovery

Harness Toolkit now treats external systems as first-class context.

The interview discovers which systems the agents should know about and uses the answer to activate or prune integration branches.

High-value early question:

```text
Are there external systems or tools the agents should know about?
```

This question has high information gain because it decides whether the harness needs:

```text
- issue tracking rules
- code review rules
- documentation access rules
- design-system context
- quality and security tooling
- monitoring context
- wrapper scripts
- MCP planning
- credential and write-safety policies
```

Examples of supported system categories:

```text
Repository and code review
→ GitLab, GitHub, Azure DevOps, Bitbucket

Work tracking
→ Jira, GitLab Issues, GitHub Issues, Azure Boards, Linear

Documentation and knowledge
→ Confluence, Notion, Wiki, Markdown in repository, SharePoint

Design and UX
→ Figma, Sketch, Adobe XD

Quality, security and monitoring
→ SonarQube, SonarCloud, Sentry, Grafana, Prometheus, Datadog
```

### Generated integration artifacts

When external systems are relevant, the harness can generate or update:

```text
.agent/context/integration-policy.md
.agent/integrations/external-systems.md
.agent/integrations/gitlab.md
.agent/integrations/github.md
.agent/integrations/jira.md
.agent/integrations/confluence.md
.agent/integrations/figma.md
.agent/integrations/sonarqube.md
.agent/mcp/mcp-policy.md
```

It can also provide safe wrapper scripts:

```text
.agent/scripts/gitlab-issue-comment.sh
.agent/scripts/github-issue-comment.sh
.agent/scripts/jira-issue-comment.example.sh
```

### Wrapper-first rule

If a wrapper script exists, agents should use it instead of inventing ad-hoc CLI commands.

Good:

```text
.agent/scripts/gitlab-issue-comment.sh 123 .agent/runs/comment.md
```

Riskier:

```text
glab issue note 123 -m "large generated text..."
```

The wrapper-first rule makes integrations repeatable, reviewable and safer.

### Integration safety model

Each external system should be classified by access level:

```text
read-only
write-with-approval
write-enabled
forbidden
unknown
```

Defaults:

```text
unknown system → no access
write action → explicit approval required
secrets → never store in harness files
```

This keeps the harness useful without giving agents uncontrolled access to external tools.

## Command overview

### `/harness-init`

Use this when you are starting a new project or when an existing project does not yet have a harness.

Purpose:

```text
Create the initial project-specific AI-agent harness.
```

What it does:

- conducts an adaptive interview in German
- asks only relevant follow-up questions
- creates English harness files
- creates the four core agent roles
- creates context files, playbooks, templates and scripts
- sets up harness versioning
- writes the initial changelog
- applies safe defaults

The reason for the harness is fixed and is not asked:

```text
To make an AI agent reliable, controlled, repeatable, and project-specific for this project.
```

The interview focuses on:

- what the project should achieve
- domain and users
- expected result
- application shape
- criticality
- tech stack
- test strategy
- autonomy boundaries
- Git hosting and issue workflow
- safety rules
- Definition of Done

Use cases:

```text
New frontend prototype
→ run /harness-init
→ answer that it is frontend-only and prototype
→ backend, database and migration questions are skipped

Production fullstack customer project
→ run /harness-init
→ stricter questions about security, deployment, data, API contracts and approvals are asked

GitLab project with issues and MRs
→ run /harness-init
→ choose GitLab
→ provide host, project path, project ID if known
→ GitLab/glab skill and scripts are generated
```

### Guided `/harness-init` Interview

`/harness-init` works as a step-by-step setup assistant:

```text
- one question at a time
- selectable OpenCode ask/question options when available
- A/B/C fallback when selectable options are unavailable
- adaptive skip logic
- no file generation during the interview
- final summary before generation
- explicit approval required before files are written
```

Typical first question:

```text
Welche Art von Projekt ist das?

A) Frontend-only Anwendung
B) Backend/API-Service
C) Fullstack-Anwendung
D) CLI-/Tooling-Projekt
E) Library/Package
F) Monorepo
G) Sonstiges / eigene Beschreibung
```

---

### `/harness-check`

Use this when you want to know whether the harness is still complete, consistent and maintainable.

Purpose:

```text
Audit the current harness version and write active findings.
```

What it checks:

- missing lifecycle files
- duplicated rules
- conflicting rules
- stale assumptions
- command drift
- old command names such as `/create-harness`
- unclear autonomy rules
- unsafe shell patterns
- missing GitLab/GitHub guardrails
- missing quality gates
- bloated global instructions
- poor 128K context strategy
- versioning and changelog hygiene

Output location:

```text
.agent/runs/harness-check/<current-version>/<date>/
```

Typical output files:

```text
harness-inventory.md
completeness-report.md
consistency-report.md
duplication-report.md
drift-report.md
safety-report.md
maintainability-report.md
active-findings.md
recommended-actions.md
```

Use cases:

```text
You changed AGENTS.md manually
→ run /harness-check
→ see whether the change contradicts playbooks or commands

You added GitLab scripts
→ run /harness-check
→ verify GitLab safety rules and script patterns

You suspect the harness has grown messy
→ run /harness-check
→ get duplication and maintainability findings

Before a bigger cleanup
→ run /harness-check
→ let it create structured findings for /harness-update
```

Important:

```text
/harness-check does not modify harness files.
```

It only writes reports and active findings.

---

### `/harness-update`

Use this when `/harness-check` or `/harness-retro` created active findings for the current harness version.

Purpose:

```text
Apply active findings for the current harness version, update the changelog, and increment the harness version.
```

What it reads:

```text
.agent/runs/harness-check/<current-version>/*/active-findings.md
.agent/runs/harness-check/<current-version>/*/recommended-actions.md
.agent/runs/harness-retro/<current-version>/*/active-findings.md
.agent/runs/harness-retro/<current-version>/*/proposed-changes.md
.agent/runs/harness-retro/<current-version>/*/patch-plan.md
```

What it does:

1. gathers active findings for the current version
2. deduplicates overlapping findings
3. creates an update plan
4. asks for explicit approval
5. applies only approved changes
6. updates `harness-version.json`
7. appends a detailed changelog entry
8. writes a post-update check

Output location:

```text
.agent/runs/harness-update/<current-version>/<date>/
```

Typical output files:

```text
input-findings.md
update-plan.md
approval-request.md
applied-changes.md
version-bump.md
post-update-check.md
```

If no active findings exist, it must stop and say:

```text
Für die aktuelle Harness-Version sind keine aktiven Findings vorhanden.
Führe /harness-check aus, um die Harness erneut zu prüfen,
oder /harness-retro, um nutzungsbasiertes Feedback aufzunehmen.
```

Use cases:

```text
/harness-check reports duplicate GitLab rules
→ run /harness-update
→ approve cleanup
→ version increments
→ changelog records the cleanup

/harness-retro reports that the agent asks too many questions
→ run /harness-update
→ approve autonomy/playbook adjustment
→ changelog records the behavior change

You want to apply only some findings
→ run /harness-update
→ approve selected items only
→ remaining findings stay unresolved
```

Important:

```text
/harness-update must not edit files without explicit approval.
```

---

### `/harness-retro`

Use this when you want to improve the harness based on real usage experience and developer satisfaction.

Purpose:

```text
Collect usage-based feedback and convert it into active findings for the current harness version.
```

This is not a technical audit. It is a satisfaction and practice-oriented retrospective.

It asks in German:

```text
Keep     → Was läuft gut und soll bleiben?
Problems → Was läuft schlecht?
Start    → Womit soll die Harness anfangen?
Stop     → Was soll die Harness nicht mehr tun?
Change   → Was soll angepasst oder vereinfacht werden?
Evidence → Gibt es konkrete Beispiele?
```

Output location:

```text
.agent/runs/harness-retro/<current-version>/<date>/
```

Typical output files:

```text
retro.md
satisfaction-summary.md
active-findings.md
proposed-changes.md
patch-plan.md
```

Use cases:

```text
The agent works, but feels too cautious
→ run /harness-retro
→ create findings to relax approval gates

The agent changes too much at once
→ run /harness-retro
→ create findings to tighten autonomy policy

The GitLab workflow still feels clumsy
→ run /harness-retro
→ capture concrete examples
→ /harness-update improves the GitLab skill/scripts

The initial harness is technically valid but not pleasant to use
→ run /harness-retro
→ improve practical fit
```

Important:

```text
/harness-retro does not directly modify files.
```

It creates findings. Use `/harness-update` to apply them.

---

## Versioning model

The harness is versioned independently from your application.

Version file:

```text
.agent/context/harness-version.json
```

Example:

```json
{
  "version": "0.1.0",
  "previousVersion": null,
  "status": "bootstrap",
  "lastUpdated": null,
  "lastUpdateSource": "bootstrap",
  "notes": "Initial bootstrap version. Increment after approved harness updates."
}
```

Changelog:

```text
.agent/context/harness-changelog.md
```

Every harness change must be recorded there.

### Semantic versioning

Use:

```text
patch → cleanup, documentation, consistency fixes
minor → new commands, playbooks, scripts, capabilities
major → breaking workflow, autonomy, lifecycle or command changes
```

Examples:

```text
0.1.0 → 0.1.1
Fix duplicate GitLab rules, improve script safety

0.1.1 → 0.2.0
Add /harness-update command

0.2.0 → 1.0.0
Change lifecycle model or autonomy policy in a breaking way
```

---

## Findings model

`/harness-check` and `/harness-retro` create active findings for the current version.

Finding format:

```md
## FINDING-<version>-<number>: <title>

Status: active
Severity: critical|important|minor
Source: check|retro
Detected in version: <version>
Target files:
- <path>

Problem:
...

Evidence:
...

Recommended action:
...

Risk:
...

Suggested update type: patch|minor|major
```

`/harness-update` only processes active findings for the current version.

This avoids accidentally applying outdated recommendations after the harness has already changed.

---

## GitLab support

If GitLab is selected during `/harness-init`, the harness should create:

```text
.agent/skills/gitlab-glab.md
.agent/scripts/gitlab-issue-load.sh
.agent/scripts/gitlab-issue-comment.sh
.agent/scripts/gitlab-mr-create-draft.sh
.agent/scripts/gitlab-mr-comment.sh
.agent/scripts/gitlab-api.sh
.agent/config/gitlab.env.example
```

The GitLab skill must enforce:

```text
- do not invent glab flags
- do not manually build GitLab API URLs
- prefer wrapper scripts
- use GITLAB_REPO for high-level glab issue / glab mr commands
- use GITLAB_PROJECT_ID for glab api when known
- never post long Markdown inline via glab issue note -m "..."
- always write comments to Markdown files first
- publish issue comments via .agent/scripts/gitlab-issue-comment.sh
- do not merge, close issues, delete branches or change labels without approval
```

Recommended environment variables:

```bash
export GITLAB_REPO="group/subgroup/project"
export GITLAB_PROJECT_ID="12345678"
export GITLAB_ACCESS_TOKEN="..."
```

The project ID is preferred for API calls because it avoids URL-encoding mistakes.

---

## Safety defaults

Unless the project explicitly allows otherwise:

```text
- no MR/PR merge
- no deployment
- no production data changes
- no auth/permission changes without approval
- no API contract changes without approval
- no dependency additions without approval
- no file deletion without approval
- no weakening, deleting or skipping tests
- no reading external secret directories
```

These defaults are intentionally conservative. The harness can later be tuned through `/harness-retro` and `/harness-update`.

---

## Model recommendations

Recommended model strength:

```text
/harness-init
→ strong model recommended
→ Qwen 27B Dense, Claude Sonnet, or stronger

/harness-check
→ medium to strong model
→ needs consistency and drift detection

/harness-update
→ strong model recommended
→ edits governance files and must avoid contradictions

/harness-retro
→ medium model is often enough for interview
→ strong model better for converting feedback into clean findings
```

For local setups:

```text
qwen36-27b-mtp-128k
→ architecture, implementation, harness-init, harness-update

qwen36-35b-a3b-mtp-128k
→ fast analysis, summaries, retro interview, lightweight checks

Sonnet/Opus
→ optional validation for important harness changes
```

---

## Typical workflows

### New project

```text
1. Run toolkit script
2. Start OpenCode
3. Run /harness-init
4. Review generated files
5. Run /harness-check
6. If findings exist, run /harness-update
```

### Existing project without harness

```text
1. Run toolkit script in project root
2. Run /harness-init
3. Provide project structure, stack, Git workflow and quality gates
4. Run /harness-check
5. Apply findings with /harness-update
```

### Harness starts drifting

```text
1. Run /harness-check
2. Review active findings
3. Run /harness-update
4. Approve selected changes
5. Confirm changelog and version bump
```

### Developer is unhappy with agent behavior

```text
1. Run /harness-retro
2. Provide concrete examples
3. Let it create retro findings
4. Run /harness-update
5. Approve behavior changes
```

### GitLab commands keep failing

```text
1. Run /harness-check
2. Look for GitLab/glab findings
3. Run /harness-update
4. Ensure GitLab skill/scripts are corrected
5. Run /harness-check again
```

---

## When to use what

| Situation | Command |
|---|---|
| No harness exists | `/harness-init` |
| You want a technical audit | `/harness-check` |
| Reports/findings exist and should be applied | `/harness-update` |
| You are unhappy with agent behavior | `/harness-retro` |
| You changed harness files manually | `/harness-check` |
| You want to clean up duplicates/drift | `/harness-check` then `/harness-update` |
| You want to improve autonomy rules | `/harness-retro` then `/harness-update` |
| You want to verify a previous update | `/harness-check` |

---

## Recommended cadence

```text
After initial setup:
→ run /harness-check

After manual harness edits:
→ run /harness-check

After several agent tasks:
→ run /harness-retro

Before applying changes:
→ run /harness-update only if active findings exist

After /harness-update:
→ run /harness-check again
```

For active projects:

```text
weekly or after major feature work:
→ /harness-check

every few weeks or after pain points:
→ /harness-retro
```

---

## Notes

- The bootstrap file intentionally creates only the minimal toolbox.
- The project-specific harness is generated by `/harness-init`.
- The harness should stay small and modular.
- Use playbooks for details, not huge global instructions.
- Treat the harness like code: version it, check it, update it, and document changes.
