---
description: "Initialize a project-specific harness through an adaptive, evidence-driven interview."
---

# Harness Init Command

## Goal

Create the initial project-specific AI-agent harness.

The harness exists to make agent work reliable, controlled, repeatable and project-specific.

This command uses a genuinely adaptive interview. It must not run a fixed questionnaire or ask topic blocks in a predefined order.

## Language

```text
interview questions → German
generated harness files → English
final report → German
```

## Required interview resources

Read these files before starting discovery:

```text
.agents/interview/interview-engine.md
.agents/interview/interview-state-schema.md
.agents/interview/topic-catalog.md
.agents/interview/role-catalog.md
.agents/policies/policy-contract.md
.agents/runtime/image-contract.md
.agents/runtime/image-plan.schema.json
.agents/runtime/tektona-contract.md
.agents/runtime/tektona-deployment.schema.json
.agents/interview/question-bank.md
.agents/interview/inference-rules.md
.agents/interview/scenario-taxonomy.md
```

Load individual files under `.agents/interview/topics/` only when their catalog signals are present or their relevance remains uncertain and potentially important.

Do not load all topic packs by default.

## Non-negotiable adaptive behavior

```text
No fixed first question.
No fixed question order.
No mandatory topic sequence.
No automatic walk through every catalog question.
Exactly one user question at a time.
Every selected question must reduce harness-relevant uncertainty.
```

The current belief state determines the next question.

## Phase 0: Resolve the discovery subject

Determine what the harness is being created for before interpreting repository evidence.

The default discovery subject is the product, application, service or bounded subproject in the target repository. The harness implementation itself is control infrastructure and must not be mistaken for the product merely because its files are prominent or richly documented.

Classify evidence before using it:

```text
product evidence
→ product source, product README, domain documentation, manifests, tests, CI/CD and deployment files

harness/control evidence
→ AGENTS.md, .agents/**, .opencode/** and opencode.jsonc
→ use for inherited rules, current harness state and bootstrap constraints
→ do not use to infer the product's purpose, users, architecture or domain

toolkit/package evidence
→ template/**, toolkit installer files and toolkit maintenance documentation
→ exclude from product discovery unless the user explicitly selects the toolkit itself as the product
```

Record one discovery mode in the belief state:

```text
target-product-bootstrap          default
existing-harness-reinitialization only when explicitly requested or clearly evidenced
toolkit-self-development          only when explicitly requested or clearly confirmed
```

Infer the subject from the user's request, workspace root and product evidence when possible. If the repository is a monorepo, contains both a toolkit and a product, or the intended target remains materially ambiguous, ask exactly one focused disambiguation question before product discovery. For example:

```text
Welche fachliche oder technische Lösung soll diese Harness unterstützen:
das Produkt in diesem Repository, das Harness-Toolkit selbst oder ein bestimmtes Modul?
```

This is not a mandatory first question. Skip it whenever the subject can be established reliably from evidence.

## Phase 1: Product evidence discovery

After resolving the discovery subject, inspect evidence inside that boundary when it is safe and relevant:

```text
the user's request
README and documentation
repository and workspace structure
build and dependency manifests
test configuration
CI/CD files
deployment and infrastructure manifests
Git remotes
existing agent instructions, only as inherited constraints
existing OpenCode configuration, only as runtime configuration
existing harness or policy files, only as current control state
```

Do not make changes during evidence discovery.

Extract facts, hypotheses and uncertainty into the belief state. Record the source and confidence of each inference.

Examples:

```text
package.json shows React and Playwright
→ strong evidence for frontend and browser-test dimensions

.gitlab-ci.yml and Kubernetes manifests exist
→ strong evidence for delivery and operations relevance

the repository contains an OAuth library
→ security topic is relevant, but the intended authorization policy is not proven
```

Do not ask the user to repeat reliable repository facts. Ask for confirmation only when an inference is ambiguous, conflicts with another source or changes permissions, risk or generated artifacts.

## Phase 2: Initialize the belief state

Build the multidimensional state described in:

```text
.agents/interview/interview-state-schema.md
```

Do not force the project into a single exclusive scenario.

For unresolved dimensions, maintain coarse normalized probabilities and calculate weighted entropy as defined by the interview engine.

At minimum assess coverage for:

```text
discovery subject
project intent
runtime context
agent responsibilities
selected roles
policy evaluability and observer signals
autonomy and approval boundaries
quality expectations
integration access
risk profile
runtime image and build plan
```

## Phase 3: Generate candidates

Use `topic-catalog.md` to activate relevant topic packs.

Generate candidate questions from all active topics, not only the topic used by the previous question.

A candidate must declare internally:

```text
question id
topic id
dimensions it can resolve
plausible answer branches
estimated branch probabilities
expected posterior entropy
affected harness outputs
interaction cost
safety relevance
```

Candidate questions in topic packs are formulation patterns. Adapt them to the repository and current state. Create a project-specific candidate when it has greater expected information gain.

Discard redundant, irrelevant, dominated or premature candidates.

## Phase 4: Select the next question

For every eligible candidate, estimate:

```text
ExpectedPosteriorEntropy(q)
  = Σ P(answer | state, q) × H_weighted(state after answer)

InformationGain(q)
  = H_weighted(current state) - ExpectedPosteriorEntropy(q)

QuestionValue(q)
  = InformationGain(q) / InteractionCost(q)
```

Select the eligible question with maximum `QuestionValue`.

When command execution is available and approved, use `.agents/scripts/interview-ranker.py` to perform the entropy arithmetic deterministically. The LLM supplies the semantic belief distributions and hypothetical posteriors; the helper validates and ranks them.

The objective is weighted harness-relevant entropy reduction, not generic curiosity.

Safety constraints define eligibility. If a critical safety unknown exists, consider only candidates that can resolve a critical unknown, then choose maximum information gain among them.

Do not claim exact mathematical certainty. Use coarse probability estimates consistently and preserve uncertainty when evidence is weak.

## Phase 5: Ask one question

For questions with predefined branches, use OpenCode's interactive question tool first.

Required interaction:

```text
ask exactly one concise question
provide selectable options when useful
include Other / custom
allow free text
wait for the answer
```

Plain A/B/C text is fallback mode only when the question tool is unavailable or fails. State that fallback mode is being used.

Free-text questions are allowed when options would constrain a novel or project-specific answer.

Do not print internal probabilities, entropy tables or the full belief state unless the user asks.

## Phase 6: Update and re-plan

After every answer:

```text
record explicit facts
update every affected dimension
normalize probability distributions
recalculate weighted entropy
activate newly relevant topics
prune topics made irrelevant
remove questions made redundant
regenerate the complete candidate set
select the new maximum-value question
```

Never continue an earlier planned sequence when the answer changes candidate value.

If one answer supplies several facts, consume all of them and avoid unnecessary follow-ups.

Prefer a concise hypothesis-confirmation question when repository evidence can resolve several correlated dimensions at once.

## Safety coverage

Before generation, the final state must contain sufficient evidence for:

```text
what work the agent may perform
which normal edits may be autonomous
which external writes require approval
which destructive or irreversible actions are forbidden
whether production or sensitive data is relevant
which checks and self-verification are required
which typed observer or decision-model signals prove each normative rule
how missing evidence, low coverage and violation thresholds map to escalation
which toolchains belong in the agent image and which development resources the agent must orchestrate inside its sandbox
whether the MicroVM supplies a container daemon or supports a rootless engine
which Tektona organization, project and template scope receive the image plan
which repository, egress, proxy, registry and secret resource names are referenced without values
which Tektona sandbox resources, lifecycle and process definitions are required
which network destinations and runtime-installation privileges are available inside the sandbox
which target platforms are required and whether a local build was explicitly approved
```

An inherited organization or project policy may answer these questions without user interaction.

Use safe defaults only for non-blocking uncertainty and expose every default in the final summary.

## Stop criterion

Do not use a fixed number of questions.

Stop the interview when:

```text
criticalUnknowns is empty
required output coverage is sufficient
remaining uncertainty has safe documented defaults
the best remaining candidate has QuestionValue below the stop threshold
```

Initial default:

```text
stopThreshold = 0.15
```

The threshold is a heuristic to be calibrated from later interview outcomes.

Do not continue because unused questions remain in a topic pack.

## Final summary and approval

Before writing or modifying harness files, present a concise German summary:

```text
Zusammenfassung der geplanten Harness

Zielprodukt und Geltungsbereich
- ...

Bestätigte Fakten
- ...

Aus Repository und Antworten abgeleitete Annahmen
- ...

Verwendete sichere Defaults
- ...

Agentenaufgaben und bestätigte Rollen
- ...

Bestehende Rollen: erstellen, aktualisieren, beibehalten oder entfernen
- ...

Autonomie, Freigaben und Verbote
- ...

Maschinenprüfbare Policies, Observer-Signale und Eskalationsschwellen
- ...

Noch nicht operationalisierbare Compliance-Anforderungen
- ...

Quality Gates und Definition of Done
- ...

Integrationen und Zugriffsklassen
- ...

OCI-Agentenimage
- Ubuntu-Basis und Update-/Digest-Policy
- OpenCode-Version und Installationsmethode
- aus Evidenz abgeleitete Tool-Schichten
- innerhalb der Sandbox orchestrierte, plattformverwaltete oder ausdrücklich eingebettete Services
- Container-Runtime, Netzwerkzugriff und dynamische Installationsrechte
- Zielplattformen sowie Sandbox-/lokaler Build-Modus

Tektona-Bereitstellung
- Organisation, Projekt, Template-Scope, Name und Tag
- Repository-, Registry-, Egress-, Proxy- und Secret-Referenzen ohne Werte
- Sandbox-Ressourcen, Lifecycle und Tektona-Prozesse
- Plan-, Template-Build- oder Build-und-Sandbox-Modus
- verifizierter CLI-/SDK-/API-Adapter oder explizit ungelöster Adapter
- separate Freigabe für externe Schreiboperationen

Zu erzeugende oder anzupassende Dateien
- ...

Verbleibende nicht-blockierende Unsicherheit
- ...
```

Then ask exactly one approval question with these choices:

```text
Generate the harness
Adjust assumptions
Cancel
```

Generate files only after explicit approval.

If the user selects adjustment, ask which assumption or area should change, update the belief state and resume adaptive selection.

## Generation principles

The final belief state drives generation. The question sequence does not.

Generate only relevant roles, policies, playbooks, templates and integrations.

Prefer the smallest coherent harness that satisfies the final state. Do not copy every optional template merely because it exists.

Do not create empty optional directories or placeholder artifacts for pruned topics. The retained interview engine and catalogs are bootstrap/control resources; generated project guidance must remain separate from them.

Generated guidance must distinguish:

```text
confirmed project facts
organization or project policies
evidence-based inferences
safe defaults
open assumptions
```

## Policy and compliance generation

Use `.agents/policies/policy-contract.md` as the mandatory format for every normative harness rule.

Generate:

```text
.agents/policies/policy-registry.json
.agents/context/compliance-policy.md
```

The JSON registry is the normative source. The Markdown document is a human-readable view that explains scope, rule ownership, thresholds and operational consequences while referencing stable rule ids.

Convert every generated requirement expressed as `must`, `must not`, `required`, `forbidden` or `requires approval` into a registry rule. A prose policy may not introduce a normative requirement that is absent from the registry.

Every registry rule must have:

```text
typed and provenance-aware input signals
deterministic appliesWhen and assertion predicates
PASS, FAIL, UNKNOWN and NOT_APPLICABLE semantics
severity, weight and hard-gate setting
explicit behavior for missing evidence
stable fail and unknown reason codes
version and policy source
```

Decision-model output is an input signal, not a policy decision. Declare the model score, classification, confidence and model version as typed signals when used. The deterministic policy predicate applies configured thresholds to those signals.

If a requirement cannot be expressed without ambiguous interpretation, do not disguise it as an enforceable rule. Add it to `unobservableRequirements`, explain the missing telemetry or rubric in the final summary and resolve it through another interview question when it is safety-critical.

Generate configurable registry thresholds for warning, escalation, blocking and minimum evidence coverage. Record whether the control plane operates in `observe`, `advise` or `enforce` mode; the evaluation result stays identical across modes.

## Runtime image generation

Use `.agents/runtime/image-contract.md`, `.agents/runtime/image-plan.schema.json`, `.agents/runtime/tektona-contract.md` and `.agents/runtime/tektona-deployment.schema.json` to generate the agent runtime after the user approves the complete harness summary.

Always generate:

```text
Dockerfile
.dockerignore
.agents/runtime/image-plan.json
.agents/runtime/build-image.sh
.agents/runtime/bootstrap-sandbox.sh
.agents/runtime/tektona-deployment.json
.agents/runtime/sandbox.template.tektona.yaml
.agents/runtime/deploy-tektona.sh
.agents/context/runtime-image.md
.agents/context/tektona-deployment.md
```

Generate `.agents/runtime/compose.yaml` only when the product needs a database, queue, cache, emulator or other development resource and the selected Tektona base/template has proven container-runtime capability. Otherwise install the service in a dedicated `sandbox-service` layer and manage it as a Tektona background or autostart process.

The generated image must:

```text
use the official Ubuntu current-LTS tag through ARG UBUNTU_BASE_IMAGE=ubuntu:latest
contain OpenCode as a mandatory, versioned and verified runtime component
contain only toolchain, build, client and project-utility layers supported by evidence
contain container and Compose tooling when sandbox resources are Compose-managed
mark each optional Dockerfile layer with # harness-layer: <layer-id>
run as a non-root user whose passwd home, HOME and working directory are /workspace
exclude the project source and every secret from the build context and image
make opencode available on PATH and start it through Tektona process management rather than an interactive boot CMD
```

Classify stateful development dependencies such as databases, queues and caches as `tektona-process` services by default when their server packages can be installed reproducibly. Install the server in a distinct `sandbox-service` layer, install useful client/diagnostic tooling, and generate Tektona process plus health-check definitions. Use Compose only with recorded proof of daemon/rootless capability. Use a platform-managed service only when explicitly selected. Add a server as an `embedded-service` sharing the OpenCode lifecycle only after explicit confirmation.

Do not treat Docker or Podman CLI availability as proof that Compose can run. Record whether the target MicroVM provides a dedicated daemon/socket or supports a rootless engine, install the matching clients or runtime layer and verify the complete path during bootstrap.

Always include `tektona` in `image-plan.json.deploymentTargets`. Generate `tektona-deployment.json` as the normalized Tektona handoff and `sandbox.template.tektona.yaml` as an `apiVersion: tektona.ai/v1`, `kind: SandboxTemplate` manifest. Default to a project template, `deployment.mode = plan`, `deployment.approved = false`, `deployment.adapter = unresolved` and no automatic sandbox creation unless repository evidence or the user resolves them differently.

Prefer the Tektona-native manifest strategy. Use a verified version of `ghcr.io/tektona-ai/sandbox-base` for headless agent work or `ghcr.io/tektona-ai/desktop-x11` only when browser/computer-use evidence requires it. These official images already provide the current Ubuntu LTS, systemd, OpenCode and common developer tooling; generate named build steps only for missing project layers and still verify OpenCode. Do not copy a documentation example version without verifying that it is the intended release. Select the external-OCI-image strategy only when the committed Dockerfile must be authoritative, the image is reused outside Tektona or CI already publishes it; then require a fully qualified result image and a project registry reference for private pulls.

Reference Tektona repositories, Git credentials, registries, egress network policies, egress proxy profiles and secrets by resource name only. Never read or serialize credential values. Do not install a VNC server; Tektona provides desktop access independently of the image.

Represent bootstrap, development services and OpenCode as Tektona process definitions where appropriate. A process command may reference the cloned repository but may not contain secrets. Tektona owns process lifecycle, logs, signals and persisted autostart; the Dockerfile `CMD` remains only the portable default.

Generate `deploy-tektona.sh` with `validate`, `preview` and `apply` modes. The documented apply workflow is `tektona ctx show`, then `tektona template build run --file .agents/runtime/sandbox.template.tektona.yaml --tag <tag>`, followed—only in build-and-create-sandbox mode—by `tektona sandbox create <template-reference>:<tag> --name <sandbox-name>`. Before apply, inspect installed CLI help and version to verify those exact commands and flags, and record interface evidence in the plan. Never invent a command, SDK call, request body or additional flag. When the interface cannot be verified, the script must fail closed for `apply` with a clear adapter-required message.

Harness-generation approval does not authorize Tektona writes. Creating/updating a template, starting its asynchronous build, moving a tag, creating a sandbox or changing platform resources requires explicit approval for the resolved organization/project target. A mutating deployment must wait for a terminal successful build before tagging or sandbox creation and must record the build and template-version identifiers.

Model network access and dynamic installation as sandbox capabilities. Preinstall all known recurring toolchains and system tools. After the repository is cloned, let the sandbox bootstrap install project dependencies from authoritative lockfiles when network policy permits. If the agent needs an unforeseen tool, permit only the approved runtime-installation mode, require source and integrity evidence, record every installation and propose repeatedly installed tools as future image layers. Do not persist downloaded credentials or secrets.

The image plan is the machine-readable source for the sandbox builder. Every optional layer must include evidence references, an approved installation strategy and verification commands. The human-readable `runtime-image.md` explains the same plan without becoming a second normative source.

When image requirements are represented in the policy registry, use typed build/observer signals and deterministic rules for layer parity, OpenCode verification, non-root execution, secret-scan findings, digest resolution and local-build approval. Missing build evidence is `UNKNOWN`, never `PASS`.

Generate the local build script in all cases. Execute it only when the approved summary explicitly permits a local build and Docker, Podman or another compatible engine is available. A local build may pull images and packages and alter the local container cache, so availability alone is not approval. On success, verify OpenCode and all layer commands and record `.agents/runtime/image-lock.json` when digest data is available. Never claim a build succeeded when it was only planned.

Tektona builds the native manifest directly, or consumes a previously published OCI image when the external-image strategy is selected. It resolves an immutable template version and publishes the requested tag only after a successful build. The underlying API operation is asynchronous and must not be reported as deployed until it reaches a successful terminal state; the documented CLI build command streams and waits. Platform credentials and runtime secret/egress injection remain outside both build definitions.

## Integration generation

When external systems are relevant, generate or update:

```text
.agents/context/integration-policy.md
.agents/integrations/external-systems.md
```

Generate system-specific files only for selected systems:

```text
.agents/integrations/gitlab.md
.agents/integrations/github.md
.agents/integrations/jira.md
.agents/integrations/confluence.md
.agents/integrations/figma.md
.agents/integrations/sonarqube.md
```

For each system document:

```text
purpose
access method
read permissions
write permissions
approval requirements
forbidden operations
credential expectations without secret values
wrapper scripts when applicable
```

Do not install MCP servers during `/harness-init`. Use `/harness-mcp` for discovery, risk review and approved configuration changes.

## Role generation

Use `.agents/interview/role-catalog.md` to derive the smallest useful role set from the final belief state.

Roles are an explicit interview outcome. Do not silently install all catalog roles and do not assume that all generic "core" roles are required.

For each candidate role, track internally:

```text
role id
status: proposed | confirmed | excluded
project-specific reason
evidence ids
responsibilities covered
overlap with other roles
```

Once enough project evidence exists, confirm the proposed set with one adaptive question unless the user already selected roles explicitly. Show only the recommended roles and their project-specific reasons. Allow the user to add, remove or define a custom role. This confirmation is required before generation, but its position is determined by information gain rather than a fixed question number.

Generate exactly the confirmed roles under:

```text
.agents/roles/
```

Every generated role must follow the generated role contract in `role-catalog.md`. Tailor mission, responsibilities, triggers, context, approval boundaries and checks to the resolved product. Do not copy the generic toolkit role files verbatim.

Reconcile an existing role directory during the approved generation step:

```text
selected generated roles
→ create or update

known generic toolkit roles that are not selected
→ list for removal in the approval summary, then remove after approval
→ classify as generic only when the content still contains the known toolkit boilerplate;
  a catalog filename alone is not sufficient evidence for removal

custom or user-authored roles that are not selected
→ preserve by default and surface as retained custom roles
→ remove only when explicitly included in the approved plan
```

The final `.agents/context/role-activation-policy.md` must mention only generated or explicitly retained roles. It must not list absent catalog roles.

Do not create `.opencode/agent/*.md` unless a separately validated OpenCode agent schema is explicitly requested.

## AGENTS.md generation

When `AGENTS.md` contains `<!-- harness-bootstrap: true -->`, replace its bootstrap content during the approved generation step with a concise, project-specific instruction entry point.

When an existing `AGENTS.md` has no bootstrap marker, treat it as project evidence and preserve its valid requirements. Present material rewrites or conflict resolutions in the approval summary instead of silently replacing user-authored instructions.

The generated `AGENTS.md` must contain:

```text
resolved product identity and harness scope
instruction precedence and repository boundaries
the expected agent workflow for this project
autonomy, approval and forbidden-action summary with links to detailed policies
the confirmed role index with activation guidance
project-specific quality gates and definition-of-done references
relevant integrations and their access class
context-loading and self-verification rules
available harness lifecycle commands
```

Keep detailed rules in focused `.agents/` files and use `AGENTS.md` as the compact routing layer. Reference only files and roles that actually exist. Remove bootstrap wording, generic example roles and irrelevant integrations.

## Context-loading generation

Generate or update:

```text
.agents/context/context-loading-policy.md
```

Keep modular context loading. A large context window is not permission to load the entire harness.

## Strict OpenCode config contract

When generating `opencode.jsonc`, preserve a schema-valid OpenCode configuration.

Required shape for the supported OpenCode version:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "<provider/model>",
  "instructions": ["AGENTS.md"],
  "permission": {},
  "command": {}
}
```

Allowed optional top-level keys only when needed:

```text
mcp
compaction
formatter
lsp
```

Required lifecycle command entries:

```text
harness-init
harness-check
harness-update
harness-retro
harness-mcp
```

Each command entry must contain only:

```text
description
template
```

For this supported config contract, do not introduce:

```text
agents
agent
commands
permissions
providers
provider
rules
```

Do not silently replace a known working model or provider. When model configuration is unknown, preserve the existing value or ask only if it blocks generation.

## Required generated output

Generate or update the relevant subset of these stable artifacts:

```text
AGENTS.md
opencode.jsonc
Dockerfile
.dockerignore
.opencode/command/harness-init.md
.opencode/command/harness-check.md
.opencode/command/harness-update.md
.opencode/command/harness-retro.md
.opencode/command/harness-mcp.md
.agents/context/project-profile.md
.agents/context/harness-scope.md
.agents/context/harness-version.json
.agents/context/harness-changelog.md
.agents/context/context-index.md
.agents/context/definition-of-done.md
.agents/context/autonomy-policy.md
.agents/context/risk-profile.md
.agents/context/context-safety-policy.md
.agents/context/context-loading-policy.md
.agents/context/self-verification-policy.md
.agents/context/role-activation-policy.md
.agents/context/compliance-policy.md
.agents/policies/policy-registry.json
.agents/runtime/image-plan.json
.agents/runtime/build-image.sh
.agents/runtime/bootstrap-sandbox.sh
.agents/runtime/tektona-deployment.json
.agents/runtime/sandbox.template.tektona.yaml
.agents/runtime/deploy-tektona.sh
.agents/runtime/compose.yaml (only with proven container-runtime capability)
.agents/context/runtime-image.md
.agents/context/tektona-deployment.md
.agents/roles/<each-confirmed-role>.md
.agents/playbooks/harness-update.md
.agents/runs/.gitkeep
```

Generate additional role, playbook, integration, template and script files only when supported by the final belief state.

Do not remove the adaptive interview engine or topic packs during generation.

## Required post-generation checks

Verify:

```text
required files exist
OpenCode config shape matches the supported contract
all five lifecycle commands are registered
role files are under .agents/roles/
the generated role files exactly match the confirmed role plan plus explicitly retained custom roles
AGENTS.md is project-specific and references only files that exist
AGENTS.md contains no bootstrap marker or generic all-role inventory
no unapproved MCP server was added or enabled
generated guidance matches confirmed facts and disclosed assumptions
project-profile and harness-scope identify the resolved target product or module
harness/toolkit files were not used as product evidence unless explicitly selected as the subject
irrelevant optional artifacts were not generated
safety-critical dimensions are represented in policy files
policy-registry.json passes `.agents/scripts/policy-evaluator.py validate`
every normative Markdown requirement maps to a stable registry rule id
UNKNOWN and NOT_APPLICABLE are not treated as PASS
threshold ordering and minimum coverage are explicit
image-plan.json is valid JSON and satisfies the runtime image schema and semantic validator
Dockerfile uses the declared Ubuntu base argument and installs and verifies OpenCode
Dockerfile layer markers exactly match the image plan and every layer has repository or interview evidence
stateful development services have matching Tektona processes by default or proven Compose/platform provisioning
every Compose service has an image, health check and matching container-runtime capability
Tektona deployment plan and native manifest pass validate-tektona and contain no credential values
deploy-tektona.sh refuses external writes without separate approval and a verified CLI interface
bootstrap-sandbox.sh is idempotent, verifies the runtime and waits for service health
network and dynamic-installation permissions are explicit and runtime installations are auditable
the final image runs as non-root, does not copy the project and contains no secret material
build-image.sh passes shell syntax validation and was not executed without approval
```

Check the config for forbidden patterns and inspect every match rather than assuming all text matches are errors.

## Interview telemetry

When the approved harness enables interview telemetry, write a compact run artifact after generation containing:

```text
question ids and topics
estimated entropy before and after each answer
information-gain estimate
dimensions updated
topics activated and pruned
stop reason
```

Do not include secrets, raw credentials or unnecessary free-text content.

Telemetry is intended to calibrate the interview strategy later. It must not be used to claim model training or automatic learning in the bootstrap version.

## Final response

Report in German:

```text
that adaptive discovery completed
which evidence sources were used
how many questions were needed
why the interview stopped
what was generated or updated
which OCI layers and external services were planned and whether a local build was executed
which Tektona strategy, template reference and deployment mode were generated and whether any external write ran
which assumptions and safe defaults remain
current harness version
whether post-generation checks passed
recommended next command: /harness-check
```

## Required self-verification

Before reporting completion, use:

```text
.agents/context/self-verification-policy.md
```

Verify:

```text
the result matches the user's approved summary
only intended files were changed
the interview was adaptive rather than sequential
candidate questions were compared before selection
critical safety coverage was complete
the OpenCode configuration remains valid
available checks were run or skipped with an explicit reason
remaining risks and assumptions are reported honestly
```
