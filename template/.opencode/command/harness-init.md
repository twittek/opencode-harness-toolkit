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
.agent/interview/interview-engine.md
.agent/interview/interview-state-schema.md
.agent/interview/topic-catalog.md
.agent/interview/question-bank.md
.agent/interview/inference-rules.md
.agent/interview/scenario-taxonomy.md
```

Load individual files under `.agent/interview/topics/` only when their catalog signals are present or their relevance remains uncertain and potentially important.

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
→ AGENTS.md, .agent/**, .opencode/** and opencode.jsonc
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
.agent/interview/interview-state-schema.md
```

Do not force the project into a single exclusive scenario.

For unresolved dimensions, maintain coarse normalized probabilities and calculate weighted entropy as defined by the interview engine.

At minimum assess coverage for:

```text
discovery subject
project intent
runtime context
agent responsibilities
autonomy and approval boundaries
quality expectations
integration access
risk profile
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

When command execution is available and approved, use `.agent/scripts/interview-ranker.py` to perform the entropy arithmetic deterministically. The LLM supplies the semantic belief distributions and hypothetical posteriors; the helper validates and ranks them.

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

Agentenaufgaben und Rollen
- ...

Autonomie, Freigaben und Verbote
- ...

Quality Gates und Definition of Done
- ...

Integrationen und Zugriffsklassen
- ...

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

Generated guidance must distinguish:

```text
confirmed project facts
organization or project policies
evidence-based inferences
safe defaults
open assumptions
```

## Integration generation

When external systems are relevant, generate or update:

```text
.agent/context/integration-policy.md
.agent/integrations/external-systems.md
```

Generate system-specific files only for selected systems:

```text
.agent/integrations/gitlab.md
.agent/integrations/github.md
.agent/integrations/jira.md
.agent/integrations/confluence.md
.agent/integrations/figma.md
.agent/integrations/sonarqube.md
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

Select the smallest useful role set from the final belief state.

Store role descriptions under:

```text
.agent/roles/
```

Do not create `.opencode/agent/*.md` unless a separately validated OpenCode agent schema is explicitly requested.

## Context-loading generation

Generate or update:

```text
.agent/context/context-loading-policy.md
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
.opencode/command/harness-init.md
.opencode/command/harness-check.md
.opencode/command/harness-update.md
.opencode/command/harness-retro.md
.opencode/command/harness-mcp.md
.agent/context/project-profile.md
.agent/context/harness-scope.md
.agent/context/harness-version.json
.agent/context/harness-changelog.md
.agent/context/context-index.md
.agent/context/definition-of-done.md
.agent/context/autonomy-policy.md
.agent/context/risk-profile.md
.agent/context/context-safety-policy.md
.agent/context/context-loading-policy.md
.agent/context/self-verification-policy.md
.agent/context/role-activation-policy.md
.agent/playbooks/harness-update.md
.agent/runs/.gitkeep
```

Generate additional role, playbook, integration, template and script files only when supported by the final belief state.

Do not remove the adaptive interview engine or topic packs during generation.

## Required post-generation checks

Verify:

```text
required files exist
OpenCode config shape matches the supported contract
all five lifecycle commands are registered
role files are under .agent/roles/
no unapproved MCP server was added or enabled
generated guidance matches confirmed facts and disclosed assumptions
project-profile and harness-scope identify the resolved target product or module
harness/toolkit files were not used as product evidence unless explicitly selected as the subject
irrelevant optional artifacts were not generated
safety-critical dimensions are represented in policy files
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
which assumptions and safe defaults remain
current harness version
whether post-generation checks passed
recommended next command: /harness-check
```

## Required self-verification

Before reporting completion, use:

```text
.agent/context/self-verification-policy.md
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
