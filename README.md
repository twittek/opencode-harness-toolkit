# OpenCode Harness Toolkit

This toolkit creates a small **OpenCode harness toolbox** for project-specific AI-agent workflows.

It is designed for teams or individual developers who want to make an AI coding agent:

- reliable
- controlled
- repeatable
- project-specific
- maintainable over time

The harness is not just a prompt collection. It is a lightweight operating model for AI-assisted software development.

The current toolkit combines:

```text
adaptive evidence-driven discovery
selective project-specific roles
machine-evaluable policy and compliance rules
observer/decision-model-ready evidence contracts
OCI agent-runtime generation
native Tektona template and sandbox deployment planning
controlled MCP discovery
versioned checks, updates and retrospectives
```

---

## What this package gives you

After running the toolkit script, your project gets an OpenCode command set:

```text
/harness-init    → create the initial project harness
/harness-check   → audit the current harness version
/harness-update  → apply active findings and increment the harness version
/harness-retro   → collect usage feedback and create retro findings
/harness-mcp     → discover and plan MCP usage with approval gates
```

This gives you a full lifecycle with optional capability and runtime branches:

```text
Initialize → Check → Update → Retro → Check again
     ├────→ MCP discovery and approved configuration
     └────→ OCI/Tektona plan → separately approved build or sandbox
```

MCP discovery is an optional approval-first branch of this lifecycle.

Think of it like this:

```text
/harness-init    = setup
/harness-check   = technical inspection / TÜV
/harness-update  = controlled implementation of findings
/harness-retro   = team retrospective / satisfaction-based improvement
/harness-mcp     = controlled MCP discovery and installation planning
```

---

## HTML Landing Page

This package includes one standalone HTML landing page:

```text
harness-toolkit.html
```

Open it directly in a browser. No build step is required.

The page documents the same current lifecycle, policy, OCI and Tektona behavior as this README.

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

Review the installed `opencode.jsonc` before starting. The distributed bootstrap currently contains a local `chrome-devtools` MCP entry backed by `npx`; `/harness-mcp` governs project-specific MCP additions, removals and permission changes.

Then run:

```text
/harness-init
```

The install script copies the harness scaffold from:

```text
opencode-harness-toolkit/template/
```

`template/README.md` is toolkit maintenance documentation and is not installed. The target project's existing `README.md` remains untouched so `/harness-init` can use it as product evidence.

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
    │       ├── harness-mcp.md
    │       └── harness-retro.md
    └── .agents/
        ├── context/
        ├── interview/
        │   ├── interview-engine.md
        │   ├── interview-state-schema.md
        │   ├── topic-catalog.md
        │   └── topics/
        ├── playbooks/
        ├── roles/
        ├── policies/
        ├── runtime/
        ├── scripts/
        ├── integrations/
        ├── mcp/
        └── runs/
```

Many files below `template/.agents/` are maintenance references or optional generation sources. The installer uses an explicit bootstrap allowlist; it does not copy the complete tree into a target project.

## OpenCode Config Safety

`/harness-init` is instructed to generate a valid OpenCode configuration from the start.

Required rules:

```text
- instructions must be an array: ["AGENTS.md"]
- use command, not commands
- use permission, not permissions
- do not create agents or agent mappings
- do not reference .opencode/agent/*.md
- store role descriptions under .agents/roles/
- command entries should contain only description and template
```

## Bootstrap and generation model

The package stores bootstrap resources and generation references as real files under `template/`.

Benefits:

```text
- easier to maintain
- easier to review
- easier for AI agents to edit safely
- no huge Markdown blocks inside Bash
- toolkit script stays small and stable
- template files can be customized directly
```

The script performs these actions:

```text
- locate the template directory
- copy only bootstrap commands, interview resources and baseline safety policies
- defer project-specific roles, integrations, playbooks and policies to /harness-init
- back up existing files before overwriting
- preserve the product README
- preserve an existing project-authored AGENTS.md
- print next steps
```

## Development checks

Run the standard-library test suite from the toolkit directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The tests verify the entropy ranker, deterministic policy evaluator, OCI/Tektona plan validator, approval and secret-safety restrictions, modular topic contract, selective generation rules, lifecycle-command registration, documentation coverage and absence of the former fixed interview flow.

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
.opencode/command/harness-mcp.md
.agents/interview/interview-engine.md
.agents/interview/interview-state-schema.md
.agents/interview/topic-catalog.md
.agents/interview/role-catalog.md
.agents/interview/topics/*.md
.agents/scripts/interview-ranker.py
.agents/policies/policy-contract.md
.agents/policies/policy-registry.schema.json
.agents/policies/task-evidence.schema.json
.agents/policies/evaluation-result.schema.json
.agents/scripts/policy-evaluator.py
.agents/runtime/image-contract.md
.agents/runtime/image-plan.schema.json
.agents/runtime/tektona-contract.md
.agents/runtime/tektona-deployment.schema.json
.agents/scripts/image-plan-validator.py
.agents/context/context-loading-policy.md
.agents/context/self-verification-policy.md
```

The installer deliberately does not populate `.agents/roles/`, integrations, project policies, playbooks or run directories. After `/harness-init`, the project-specific harness contains only the artifacts supported by the approved interview state, such as:

```text
.agents/roles/<confirmed-role>.md
.agents/context/project-profile.md
.agents/context/harness-scope.md
.agents/context/context-index.md
.agents/context/definition-of-done.md
.agents/context/autonomy-policy.md
.agents/context/risk-profile.md
.agents/context/context-safety-policy.md
.agents/context/compliance-policy.md
.agents/context/harness-version.json
.agents/context/harness-changelog.md
.agents/policies/policy-registry.json
.agents/playbooks/refinement.md
.agents/playbooks/architecture.md
.agents/playbooks/development-best-practices.md
.agents/playbooks/testing.md
.agents/playbooks/review.md
.agents/scripts/quality-gates.sh
.agents/scripts/load-issue.sh
Dockerfile
.dockerignore
.agents/context/runtime-image.md
.agents/runtime/image-plan.json
.agents/runtime/build-image.sh
.agents/runtime/bootstrap-sandbox.sh
.agents/runtime/tektona-deployment.json
.agents/runtime/sandbox.template.tektona.yaml
.agents/runtime/deploy-tektona.sh
.agents/runtime/compose.yaml                   (only with proven container-runtime capability)
.agents/context/tektona-deployment.md
```

Depending on the project, `/harness-init` may also create optional files for GitLab, GitHub, monorepos, security, APIs, documentation, or dependency policies.

---

## Adaptive Harness Discovery

`/harness-init` does not run a predefined questionnaire. It maintains a multidimensional belief state, uses repository evidence before asking questions and selects the next question by expected weighted information gain.

Before product discovery starts, the engine resolves the discovery subject: the product, service or bounded module the harness is intended to support. By default, `AGENTS.md`, `.agents/**`, `.opencode/**`, `opencode.jsonc`, toolkit templates and installer documentation are treated as control evidence—not as evidence for the product's purpose or architecture. If a monorepo or mixed toolkit/product repository leaves the target ambiguous, the engine asks one focused target question; otherwise it proceeds without it.

```text
inspect evidence
→ update beliefs
→ activate relevant topic packs
→ compare candidate questions
→ ask the maximum-value question
→ update entropy and prune topics
→ stop when generation readiness is sufficient
```

### Multidimensional beliefs

Projects are not forced into one exclusive scenario such as "frontend project" or "enterprise application". The engine maintains uncertainty over independent dimensions:

```text
project intent and delivery stage
architecture and runtime
users, domain and data sensitivity
authentication and permissions
external integrations
agent responsibilities and autonomy
quality gates and documentation
selected expert roles
policy observability and deterministic escalation
agent runtime image and development services
Tektona template, resources and deployment mode
```

Repository evidence may resolve dimensions before the first question. A detected framework, CI pipeline or deployment manifest is recorded with its source and confidence instead of being asked again.

### Weighted entropy reduction

For a dimension with hypotheses `i`, the engine uses Shannon entropy:

```text
H(d) = -Σ p(i) × log2(p(i))
```

Total uncertainty is weighted by harness impact and risk:

```text
H_weighted(state) = Σ H(d) × impact(d) × risk(d)
```

For every eligible candidate question:

```text
InformationGain(q)
  = H_weighted(current state)
    - Σ P(answer | q) × H_weighted(state after answer)

QuestionValue(q)
  = InformationGain(q) / InteractionCost(q)
```

The optional `.agents/scripts/interview-ranker.py` helper performs this entropy arithmetic deterministically from LLM-supplied belief distributions and hypothetical posteriors. It uses only the Python standard library.

The engine asks the eligible question with maximum value. Safety-critical unknowns constrain which candidates are eligible.

This is not generic curiosity optimization. A question is valuable only when different answers change generated policies, roles, permissions, playbooks, quality gates, runtime layers, Tektona resources or other harness artifacts.

### Modular topic packs

Discovery knowledge lives under:

```text
.agents/interview/topics/
```

The initial catalog includes:

```text
discovery subject and evidence boundary
project intent
architecture
frontend and UX
backend and data
security
integrations
delivery and operations
quality and verification
agent governance
documentation
compliance observability
agent runtime image
```

Topic packs provide activation signals, uncertainty dimensions, evidence sources, candidate-question patterns, completion conditions and safe defaults. They are not interview blocks and define no global order.

New topic packs can be added without changing the core engine.

### Dynamic first question

There is no hard-coded first question.

For an existing repository, the first question may confirm a high-impact hypothesis:

```text
I found a Spring backend, an Angular frontend, GitLab CI and Kubernetes
manifests. Should I treat this as an existing production system where the
harness must prioritize regression safety and approval-gated deployments?
```

For an empty project, the highest-value first question may instead ask which outcome should be built.

### Stop criterion

The interview stops when:

```text
no critical safety unknown remains
required harness outputs can be generated
remaining uncertainty has documented safe defaults
the best remaining question has low expected information gain
```

It does not stop after a fixed number of questions and does not continue merely because unused catalog questions remain.

### Interaction contract

```text
one question at a time
OpenCode question tool for predefined choices
free text when choices would constrain the answer
Other / custom remains available
no harness generation before final summary and explicit approval
```

The final belief state drives generation. The path of questions does not.

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
.agents/context/integration-policy.md
.agents/integrations/external-systems.md
.agents/integrations/gitlab.md
.agents/integrations/github.md
.agents/integrations/jira.md
.agents/integrations/confluence.md
.agents/integrations/figma.md
.agents/integrations/sonarqube.md
```

`/harness-init` records MCP capability needs but does not install project-specific MCP servers. Stable MCP registry and approval files are created or updated through `/harness-mcp` when that workflow is selected.

When supported by the selected system and approved access model, it can also generate focused wrapper scripts such as:

```text
.agents/scripts/gitlab-issue-comment.sh
.agents/scripts/github-issue-comment.sh
.agents/scripts/jira-issue-comment.example.sh
```

### Wrapper-first rule

If a wrapper script exists, agents should use it instead of inventing ad-hoc CLI commands.

Good:

```text
.agents/scripts/gitlab-issue-comment.sh 123 .agents/runs/comment.md
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

## Adaptive Role Model

Harness Toolkit generates a small, project-specific and policy-driven role model.

The goal is not to create noisy subagents for every task. The goal is to give the agent explicit expert lenses and clear activation rules.

The catalog contains reusable candidates such as:

```text
architect
requirements-engineer
developer
tester
reviewer
```

Specialist roles:

```text
security-engineer
ux-designer
accessibility-specialist
devops-engineer
integration-architect
data-engineer
domain-expert
technical-writer
performance-engineer
observability-engineer
product-manager
```

### Adaptive role confirmation

The interview first derives a proposed role set from project evidence, expected agent responsibilities and risk. Once the proposal is concrete enough, it asks for confirmation, for example:

```text
Für dieses Projekt schlage ich Developer, Tester und Security Engineer vor.
Developer und Tester decken Implementierung und Regressionen ab; Security
Engineer ist wegen Authentifizierung und externen Schreibzugriffen relevant.
Welche Rollen möchtest du übernehmen, ergänzen oder entfernen?
```

The position and wording of this question remain adaptive. It is not a fixed checklist. The user can add, remove or define custom roles.

The confirmed selection determines whether the harness should include guidance for:

```text
- security and secrets
- UX and accessibility
- DevOps and operations
- external integrations
- data and reporting
- domain expertise
- documentation quality
- performance and observability
```

### Role activation policy

Generated role guidance lives under:

```text
.agents/roles/
```

The activation policy lives under:

```text
.agents/context/role-activation-policy.md
```

Examples:

```text
Authentication, authorization, secrets or MCP permissions
→ security-engineer

External systems, APIs, GitLab/GitHub/Jira automation
→ integration-architect, security-engineer

User flows, forms, navigation or UX copy
→ ux-designer

UI components, keyboard behavior, contrast or WCAG
→ accessibility-specialist

CI/CD, Docker, Kubernetes or deployment
→ devops-engineer

Business rules, terminology or domain-specific validation
→ domain-expert
```

Default:

```text
generate only confirmed roles
tailor every role to the product and its policies
do not copy generic toolkit role files
activate only relevant roles
avoid role noise
prefer the smallest useful role set
```

## Machine-Evaluable Policy & Compliance

Harness policies are generated as executable contracts, not as normative prose that an observer must reinterpret.

```text
Observer / Telemetry Sidecar
→ typed facts with provenance

Decision Model
→ optional typed score or classification with model version and confidence

Policy Registry
→ versioned applicability and assertion predicates

Deterministic Policy Evaluator
→ PASS | FAIL | UNKNOWN | NOT_APPLICABLE
→ compliance score, violation score and evidence coverage

Control Plane
→ continue | warn | escalate | block
```

The canonical source is:

```text
.agents/policies/policy-registry.json
```

Human-readable policy documents reference stable rule ids, but cannot override the registry. Every mandatory, forbidden or approval-gated behavior must declare:

```text
typed observer or decision-model signals
required provenance
deterministic applicability and assertion predicates
severity and weight
hard-gate behavior
missing-evidence behavior
stable fail and unknown reason codes
rule and registry versions
```

The evaluator uses five distinct outcomes:

| Status | Result | Meaning |
|---|---:|---|
| `PASS` | `true` | The applicable rule is proven satisfied. |
| `FAIL` | `false` | The applicable rule is proven violated. |
| `UNKNOWN` | `null` | Required evidence is absent or invalid. |
| `NOT_APPLICABLE` | `null` | The rule definitively does not apply. |
| `ERROR` | `null` | Registry or evaluator execution is invalid. |

Missing evidence never becomes `PASS`.

Aggregate scoring is deterministic:

```text
violationScore = weighted FAIL / weighted (PASS + FAIL)
complianceScore = 1 - violationScore
coverage = weighted (PASS + FAIL) / weighted (PASS + FAIL + UNKNOWN)
```

The registry configures `warnAt`, `escalateAt`, `blockAt` and `minimumCoverage`. Critical hard-gate failures can block immediately; critical unknowns can escalate even before an aggregate threshold is reached.

A decision model remains upstream of the policy engine. It may emit a probability, classification or confidence as a versioned signal, but it does not decide whether to warn, escalate or block. This keeps enforcement reproducible across observer-only and enforcer deployments.

Requirements that cannot yet be expressed as observable predicates are recorded as policy-design gaps rather than being presented as enforceable rules.

## Adaptive OCI Agent Image

After the approved interview, `/harness-init` now produces a portable OCI build contract in addition to the project harness:

```text
Dockerfile                         → executable image definition
.dockerignore                      → excludes source, secrets and local state
.agents/runtime/image-plan.json    → machine-readable layers, evidence and services
.agents/runtime/build-image.sh     → optional local Docker/Podman validation
.agents/runtime/bootstrap-sandbox.sh → starts and verifies sandbox resources
.agents/runtime/tektona-deployment.json → validated template/sandbox handoff
.agents/runtime/sandbox.template.tektona.yaml → recommended native Tektona build
.agents/runtime/deploy-tektona.sh  → validates, previews and uses a verified adapter
.agents/runtime/compose.yaml       → optional, only with proven container capability
.agents/context/runtime-image.md   → human-readable explanation
.agents/context/tektona-deployment.md → Tektona scope, references and approval state
```

The portable image starts from the official current Ubuntu LTS tag, installs OpenCode as a mandatory component and then adds only the tool layers supported by repository or interview evidence. The Tektona-native rendering starts from a verified release of `ghcr.io/tektona-ai/sandbox-base`, which itself tracks the current Ubuntu LTS and already contains OpenCode, then adds only missing project layers.

```text
Cargo.toml or rust-toolchain.toml
→ Rust compiler, Cargo and required native build tools in the agent image

MongoDB driver or configuration
→ MongoDB client/diagnostic tooling in the agent image
→ MongoDB server in a distinct sandbox-service layer
→ lifecycle through a Tektona background/autostart process
```

The autonomy goal is a self-contained development sandbox. For required databases, queues, caches and emulators, the Tektona default is a dedicated service layer plus a health-checked Tektona process. Compose remains available only when the chosen Tektona template provides documented daemon/socket or rootless-runtime capability. A daemon is never assumed merely because a CLI is installed; the plan must record capability evidence.

Known recurring tools are preinstalled. When sandbox internet access is permitted, the agent may install an unforeseen tool in user-local or explicitly approved sandbox-root mode. The source, version, integrity evidence, task and installed path are recorded. Repeated downloads become drift evidence and should be promoted into the next image version.

The repository is attached through the Tektona project and cloned at sandbox startup. The bootstrap then installs project dependencies from its lockfiles and verifies Tektona-managed or Compose-managed resources. This keeps source code and fast-changing dependency trees out of the reusable base image without reducing agent autonomy.

Stateful servers are installed directly into the OpenCode image only after explicit confirmation. The image runs as a non-root user, does not contain a copy of the project repository and must not contain credentials. Every optional Dockerfile layer has a stable `# harness-layer` marker that is checked against the evidence-bearing image plan.

Tektona can build the native `SandboxTemplate` manifest directly (recommended) or consume an OCI image published from the Dockerfile when the same image must run outside Tektona. A build publishes an immutable version and moves a requested tag only after success. The deployment plan references repositories, Git credentials, registries, egress policies, proxy profiles and secrets by name—never by value—and captures sandbox resources, lifecycle and processes. Applying it requires separate approval and verification of the installed Tektona CLI command surface. The same Dockerfile can be built locally with Docker or Podman after explicit approval, but local success does not create a Tektona template or sandbox.

### What can happen directly after `/harness-init`

`/harness-init` always generates and validates the build and deployment artifacts. What it executes afterward is an explicit interview outcome:

| Mode | Result | Prerequisites | External effect |
|---|---|---|---|
| `plan` | Dockerfile, native Tektona manifest, image plan, deployment plan and scripts | Approved harness generation | None |
| Local OCI build | A tagged OCI image in the local Docker, Podman or BuildKit cache | Available engine and explicit local-build approval | Pulls packages/images and changes the local container cache |
| `build-template` | A new immutable Tektona template version; the requested tag moves only after success | Resolved org/project context, authenticated and verified Tektona CLI, template-admin permission and separate deployment approval | Writes a template version and tag in Tektona |
| `build-and-create-sandbox` | Successful template build followed by a new Tektona sandbox | All template-build prerequisites plus a resolved sandbox name, resources, lifecycle and sandbox-creation approval | Writes a template version/tag and creates a sandbox |

No external write is implied by approving harness generation. The default is `plan`, with `deployment.approved = false`. Local build, Tektona template build and sandbox creation are separately visible and approval-gated actions.

The generated scripts expose the intended control points:

```bash
# Build and verify a conventional local OCI image, when approved.
.agents/runtime/build-image.sh

# Validate the Tektona handoff without writing to the platform.
.agents/runtime/deploy-tektona.sh validate

# Show the resolved scope, template, tag, resources and pending actions.
.agents/runtime/deploy-tektona.sh preview

# Build the template and optionally create the sandbox, only when the
# approved deployment plan and verified CLI adapter permit it.
.agents/runtime/deploy-tektona.sh apply
```

### Two Tektona delivery paths

The deployment plan chooses one of two strategies:

```text
native-manifest (recommended)
→ sandbox.template.tektona.yaml
→ verified ghcr.io/tektona-ai/sandbox-base:<version>
→ Tektona installs only the missing project tools
→ no separate OCI registry publication is required

external-oci-image
→ build Dockerfile locally or in CI
→ publish the fully qualified image to a registry
→ reference a project registry credential when the image is private
→ Tektona builds the template from that published image
```

A local OCI build and a Tektona template build are therefore different outcomes. A local build proves portable image construction; only a successful Tektona template build creates the immutable version from which Tektona can start a sandbox.

### Direct Tektona sandbox flow

When `build-and-create-sandbox` is selected and separately approved, the generated deployment script performs the guarded sequence:

```text
validate image plan + Dockerfile + Tektona manifest + deployment plan
→ verify `tektona` CLI version and required command surface
→ verify active organization/project context
→ start the template build and stream/wait for completion
→ stop on failed or incomplete build; publish no success claim
→ use the requested tag only after the version was published successfully
→ create the named sandbox from <template-reference>:<tag>
→ record build id, template-version id and sandbox result
```

Repository, Git credential, registry, secret, egress-policy and proxy-profile fields contain Tektona resource references only. Credential values never enter the Dockerfile, manifest, deployment JSON or build logs.

## MCP Discovery & Planning

Harness Toolkit includes a dedicated MCP command:

```text
/harness-mcp
```

This command performs controlled MCP inventory, discovery, recommendation and installation planning.

It does **not** blindly install additional MCP servers or mutate MCP configuration.

The distributed bootstrap `opencode.jsonc` currently contains one explicit default: the local `chrome-devtools` MCP server invoked through `npx`. Treat it as existing configuration during discovery. Review or remove it before first use when browser tooling or runtime package download is not acceptable for the target project.

### Why MCP discovery is separate

MCP servers can be powerful. Some are read-only, but others can:

```text
- write to external systems
- control a browser session
- access the filesystem
- interact with secret-sensitive systems
- affect production-adjacent environments
```

Therefore MCP handling is intentionally separated from `/harness-init`.

`/harness-init` may document MCP needs.

`/harness-mcp` inventories existing entries, evaluates new or changed candidates and creates a plan.

Configuration changes happen only after explicit approval.

### MCP workflow

```text
1. Discover capability gaps.
2. Map gaps to MCP candidate categories.
3. Assess value.
4. Assess risk.
5. Create recommendations.
6. Create an installation plan.
7. Ask for approval.
8. Apply config only after approval.
```

### MCP risk categories

```text
read-only
write-capable
browser-control
filesystem
secret-sensitive
production-adjacent
unknown
```

Default rules:

```text
unknown → do not install
write-capable → approval required
browser-control → approval required
filesystem → approval required
secret-sensitive → approval required
production-adjacent → approval required
```

### MCP artifacts

The command writes run-specific findings under:

```text
.agents/runs/harness-mcp/<date>/
```

Typical outputs:

```text
mcp-discovery-report.md
mcp-recommendations.md
mcp-risk-review.md
mcp-installation-plan.md
```

Stable MCP policy files live under:

```text
.agents/mcp/mcp-policy.md
.agents/mcp/mcp-registry.md
.agents/mcp/approved-mcp-servers.md
.agents/mcp/denied-mcp-servers.md
```

### Approval-first configuration

Before changing `opencode.jsonc`, `/harness-mcp` must show:

```text
MCP installation/update plan

- MCP server:
- Purpose:
- Risk category:
- Required permissions:
- Config files to change:
- Secrets required:
- Fallback without MCP:
- Rollback plan:
```

Then ask for explicit approval.

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
- confirms a project-specific role set and creates only those roles
- replaces the bootstrap AGENTS.md with a concise project-specific routing document
- generates a deterministic policy registry with typed evidence and explicit unknown handling
- creates only relevant context files, playbooks, integrations and scripts
- generates the evidence-backed OCI runtime and Tektona deployment contract
- can separately build a local OCI image, a Tektona template or a Tektona template plus sandbox after explicit approval
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
- observer signals, policy thresholds and enforcement mode
- required agent-image toolchains and sandbox services
- Tektona scope, template strategy, resource references and deployment mode

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
→ a GitLab integration policy and only the required reviewed wrappers are generated
```

### Guided `/harness-init` Interview

`/harness-init` works as a step-by-step setup assistant:

```text
- one question at a time
- selectable OpenCode ask/question options when available
- A/B/C fallback when selectable options are unavailable
- repository evidence before questions
- candidate comparison across modular topic packs
- maximum weighted information gain per question
- no fixed first question or topic order
- no file generation during the interview
- final summary before generation
- explicit approval required before files are written
- separate approval required before a local image build or Tektona write
```

The first question depends on available evidence. For an empty project it may be:

```text
Was soll entstehen oder verändert werden, und welches Ergebnis soll am Ende erreicht sein?
```

For an existing project it may instead confirm a repository-derived hypothesis that resolves several high-impact dimensions at once.

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
- stale bootstrap instructions, unconfirmed roles or references to absent role files
- policy-registry schema, predicate, signal, threshold and missing-evidence errors
- Dockerfile/image-plan layer drift and unverified OpenCode installation
- Tektona manifest/deployment-plan drift, unsafe credential material and unapproved write modes
- broken Tektona-process or capability-unproven Compose service definitions

Output location:

```text
.agents/runs/harness-check/<current-version>/<date>/
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

After changing toolchains, services or Tektona settings
→ run /harness-check
→ verify image-plan, manifest, deployment references and runtime capabilities
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
.agents/runs/harness-check/<current-version>/*/active-findings.md
.agents/runs/harness-check/<current-version>/*/recommended-actions.md
.agents/runs/harness-retro/<current-version>/*/active-findings.md
.agents/runs/harness-retro/<current-version>/*/proposed-changes.md
.agents/runs/harness-retro/<current-version>/*/patch-plan.md
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

For approved policy changes, it keeps the JSON registry, typed signals, thresholds and human-readable rule references synchronized. For runtime changes, it updates the image plan, Dockerfile, Tektona manifest/deployment plan and related scripts together, invalidates stale locks and preserves separate build/deployment approvals.

Output location:

```text
.agents/runs/harness-update/<current-version>/<date>/
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

It may also capture evidence-backed runtime feedback such as missing tools, repeated dynamic installations, slow image startup, failed Tektona processes, stale platform references or unnecessary image layers. It records findings only; it does not rebuild or redeploy the runtime.

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
.agents/runs/harness-retro/<current-version>/<date>/
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
→ /harness-update improves the integration policy or reviewed wrappers

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

### `/harness-mcp`

Use this to inventory existing MCP configuration, identify capability gaps, assess candidate risk and prepare an approval-gated configuration change.

It writes discovery, recommendation, risk-review and installation-plan artifacts under `.agents/runs/harness-mcp/<date>/`. Existing MCP entries are documented; new installations, enablement, permission changes and `opencode.jsonc` edits occur only after explicit approval. Secret values never belong in the plan or configuration.

---

## Versioning model

The harness is versioned independently from your application.

Version file:

```text
.agents/context/harness-version.json
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
.agents/context/harness-changelog.md
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

If GitLab is relevant and confirmed during `/harness-init`, the generated project harness should contain the relevant subset of:

```text
.agents/context/integration-policy.md
.agents/integrations/external-systems.md
.agents/integrations/gitlab.md
.agents/scripts/gitlab-issue-comment.sh
additional focused wrappers only when the approved workflow needs them
```

The integration guidance and wrappers must enforce:

```text
- do not invent glab flags
- do not manually build GitLab API URLs
- use an existing reviewed wrapper when one covers the operation
- use GITLAB_REPO for high-level glab issue / glab mr commands
- use GITLAB_PROJECT_ID for glab api when known
- never post long Markdown inline via glab issue note -m "..."
- always write comments to Markdown files first
- publish issue comments via .agents/scripts/gitlab-issue-comment.sh
- classify reads and writes explicitly
- require approval for posting, merge, close, label, branch deletion and other external mutations unless the generated policy grants a narrower action
```

Recommended environment variables:

```bash
export GITLAB_REPO="group/subgroup/project"
export GITLAB_PROJECT_ID="12345678"
export GITLAB_ACCESS_TOKEN="..."
```

The project ID is preferred for API calls because it avoids URL-encoding mistakes. These environment-variable names are references only; values must not be committed to the harness.

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

## Self-Verification Policy

The toolkit includes a self-verification policy so agents do not report completion prematurely.

Bootstrap policy file, retained or tailored by initialization:

```text
.agents/context/self-verification-policy.md
```

Core rule:

```text
Every task must end with a self-verification pass before the final response.
```

The agent must verify:

```text
- whether the result matches the original user request
- whether only intended files/content were changed
- whether relevant harness policies were followed
- whether available checks/tests were run or explicitly skipped with a reason
- whether remaining risks or assumptions need to be reported
```

Recommended final response format:

```text
Verification:
- Requirement match: ...
- Files changed: ...
- Checks run: ...
- Open risks: ...
```

For harness changes, integrations, MCP, security-sensitive work or production-adjacent systems, use stricter verification with requirement traceability and explicit risk reporting.

## Context Loading Policy

Harness Toolkit now includes a context loading policy for large-context models.

This is especially useful for 128K context windows.

A large context window does not mean the whole harness should be loaded for every task.

Principle:

```text
The harness is a structured knowledge space, not one giant prompt.
Use the smallest useful context set.
```

Bootstrap policy file, retained or tailored by initialization:

```text
.agents/context/context-loading-policy.md
```

### Loading tiers

| Tier | When to load | Examples |
|---|---|---|
| Tier 1 | Always load | `AGENTS.md`, project profile, autonomy policy, definition of done, risk profile, context loading policy |
| Tier 2 | Load when relevant | role activation policy, specialist roles, integration policies, MCP policy, playbooks |
| Tier 3 | Load only on explicit need | run artifacts, previous findings, historical reports |
| Tier 4 | Never load automatically | `node_modules`, `dist`, `build`, `coverage`, `template`, `.DS_Store`, `*.bak.*`, logs |

### 128K recommendation

```text
1. Start with Tier 1.
2. Determine the task type.
3. Add only relevant Tier 2 files.
4. Add Tier 3 only when reviewing lifecycle history or findings.
5. Never load Tier 4 automatically.
```

### Drift detection

`/harness-check` should detect context drift, such as generated folders being included or AGENTS.md encouraging loading everything.

## Model selection guidance

Model names and relative rankings age quickly, so the toolkit documents capability requirements rather than a permanent vendor/model benchmark.

| Command | Recommended strength | Reason |
|---|---|---|
| `/harness-init` | highest available reasoning quality | Requires repository interpretation, multidimensional belief updates, candidate comparison, policy operationalization, role selection and coherent OCI/Tektona generation. |
| `/harness-check` | medium to high reasoning quality | Requires consistency, schema, drift, safety and evidence analysis without changing the harness. |
| `/harness-update` | high reasoning quality | Changes governance and runtime contracts while preserving rule, schema and version consistency. |
| `/harness-retro` | medium for interview; higher for consolidation | Collecting feedback is simple; turning it into non-duplicated, evidence-backed findings is harder. |
| `/harness-mcp` | high reasoning quality | Requires inventory, capability matching, risk classification and safe configuration planning. |

The distributed `opencode.jsonc` currently names `litellm-local/qwen36-27b-mtp-128k` as its bootstrap default. Treat this as an editable local configuration choice, not a quality guarantee or a requirement. `/harness-init` preserves a known working model/provider unless the user chooses a change.

Evaluate a candidate model against the actual contracts:

```text
can it inspect repository evidence before asking questions?
can it compare candidate questions instead of following a fixed list?
can it preserve JSON/YAML/schema and OpenCode config correctness?
can it generate deterministic policies without ambiguous normative prose?
can it keep approval boundaries and Tektona resource references intact?
can it run and interpret the provided validators and tests?
```

Optional validation pattern:

```text
1. Generate a representative harness.
2. Run /harness-check and the repository test suite.
3. Compare missing questions, false assumptions, policy ambiguity and runtime-plan validity.
4. Use stronger review for critical findings or major harness updates.
```

---

## Typical workflows

### New project

```text
1. Run toolkit script
2. Start OpenCode
3. Run /harness-init
4. Review the approved harness, policy and runtime/Tektona plans
5. Optionally run a separately approved local OCI or Tektona deployment action
6. Run /harness-check
7. If findings exist, run /harness-update
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
4. Ensure the GitLab integration policy and reviewed wrappers are corrected
5. Run /harness-check again
```

### A new MCP capability is needed

```text
1. Run /harness-mcp
2. Inventory the existing MCP configuration
3. Review candidate value, permissions, secrets and rollback
4. Approve only the selected configuration change
5. Run /harness-check after configuration changes
```

### Build the agent runtime or create a Tektona sandbox

```text
1. Run /harness-init or /harness-check to resolve the current runtime plan
2. Preview the generated local-build or Tektona deployment action
3. Approve the exact local or platform write separately
4. Build the OCI image, Tektona template, or template plus sandbox
5. Record outputs and run /harness-check for drift
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
| You need or want to review MCP capabilities | `/harness-mcp` |
| Toolchains, services or Tektona settings changed | `/harness-check`, then `/harness-update` if findings are approved |
| You want an OCI image or Tektona sandbox | `/harness-init` runtime plan, then the separately approved generated script |

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

After an OCI/Tektona build or sandbox change:
→ record build/version evidence and run /harness-check

Before adding or changing MCP configuration:
→ run /harness-mcp
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
