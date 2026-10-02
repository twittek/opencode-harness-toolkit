# Adaptive Harness Discovery Engine

This engine controls `/harness-init`.

Its purpose is to discover the smallest sufficient set of project facts needed to generate a safe, useful and project-specific agent harness.

The interview is not a questionnaire and has no fixed question order.

## Core loop

```text
inspect available evidence
→ update the belief state
→ activate relevant topic packs
→ generate candidate questions
→ estimate the expected posterior for each candidate
→ select the eligible question with maximum weighted information gain
→ ask exactly one question
→ update beliefs and prune branches
→ evaluate generation readiness
→ repeat or summarize
```

Every question must earn its place by reducing harness-relevant uncertainty.

## Discovery subject boundary

Resolve the subject before interpreting repository evidence. By default, discover the product, application, service or selected subproject that the harness will support—not the harness machinery itself.

Use three evidence classes:

```text
product evidence
→ may establish purpose, users, domain, architecture, runtime and delivery expectations

harness/control evidence
→ AGENTS.md, .agents/**, .opencode/** and opencode.jsonc
→ may establish inherited rules, bootstrap state and runtime constraints
→ must not establish product identity or product architecture by itself

toolkit/package evidence
→ template/**, installer files and toolkit maintenance documentation
→ ignore for product inference unless toolkit-self-development is the confirmed subject
```

The default mode is `target-product-bootstrap`. Use `existing-harness-reinitialization` or `toolkit-self-development` only when explicitly requested or confirmed by strong evidence.

If the target remains ambiguous after the initial scan, ask one focused subject question. This question is conditional, not a fixed first question. Do not continue into project-intent discovery until the subject boundary is inferred with high confidence or confirmed.

## Sources of evidence

After resolving the subject, inspect available evidence inside that boundary when it can be read safely:

```text
README and project documentation
repository layout
package and build manifests
test configuration
CI/CD configuration
deployment manifests
Git remotes
existing agent or harness files
existing policies and architecture documentation
the user's initial request
```

Do not ask for a fact that reliable evidence already establishes.

Record the source and confidence for inferred facts. Repository evidence is not automatically authoritative; ask for confirmation when it conflicts with user input or materially changes safety behavior.

## Belief state

Maintain the state described in `interview-state-schema.md`.

The state models independent harness-relevant dimensions rather than forcing the project into one scenario label.

Examples:

```text
project intent
delivery stage
architecture boundaries
runtime and deployment
users and domain
data sensitivity
authentication and authorization
external integrations
agent responsibilities
autonomy and approval boundaries
quality gates
documentation expectations
```

Each dimension has:

```text
candidate values or hypotheses
normalized probabilities
confidence
evidence source
harness impact weight
risk weight
status: unknown | inferred | confirmed | not-applicable
```

## Entropy

For a dimension `d` with hypotheses `i`, use Shannon entropy:

```text
H(d) = -Σ p(i) × log2(p(i))
```

Use normalized probabilities. A confirmed or not-applicable dimension has zero remaining entropy.

Total harness-relevant uncertainty is weighted:

```text
H_weighted(state) = Σ H(d) × impact(d) × risk(d)
```

`impact(d)` estimates how strongly the dimension changes generated harness artifacts.

`risk(d)` gives additional weight to uncertainty that affects security, permissions, external writes, production behavior or irreversible actions.

Do not maximize generic curiosity. Reduce uncertainty that changes the generated harness.

## Candidate questions

Create candidates from all currently relevant topic packs under:

```text
.agents/interview/topics/
```

Topic-pack questions are examples and reusable candidates, not mandatory blocks. The LLM may formulate a better project-specific question when it resolves the same dimensions more efficiently.

Each candidate should identify:

```text
id
source topic
dimensions resolved
possible answer branches
estimated probability of each branch
expected posterior beliefs for affected dimensions
harness artifacts affected
interaction cost
whether it resolves a blocking safety unknown
```

Discard a candidate when:

```text
the answer is already known with sufficient confidence
the dimension is not relevant
all possible answers lead to the same harness output
another candidate dominates it by resolving the same uncertainty at lower cost
it depends on an unanswered prerequisite
it asks for implementation detail before the relevant branch is active
```

## Expected information gain

For a candidate question `q` with possible answers `a`:

```text
ExpectedPosteriorEntropy(q)
  = Σ P(a | state, q) × H_weighted(state after a)

InformationGain(q)
  = H_weighted(current state) - ExpectedPosteriorEntropy(q)
```

Rank eligible candidates by:

```text
QuestionValue(q) = InformationGain(q) / InteractionCost(q)
```

Use an interaction cost of `1.0` by default. Increase it for questions that are difficult, sensitive, require research or contain many independent choices.

Ask the eligible candidate with the highest `QuestionValue`.

The probability estimates are beliefs, not facts. Keep them coarse and honest. Their purpose is consistent comparison between candidates, not fake precision.

For exact entropy arithmetic, use the optional standard-library helper when execution is available and approved:

```text
.agents/scripts/interview-ranker.py
```

It accepts a JSON belief state and candidate-answer posteriors through a file or standard input. The LLM remains responsible for semantic hypotheses and probability estimates; the helper only performs deterministic entropy calculation and ranking.

When candidates are close, prefer the question that:

```text
affects more generated artifacts
resolves higher-risk uncertainty
can prune more topic branches
is easier for the user to answer
confirms or rejects a high-impact repository inference
```

## Safety constraints

Maximum information gain is the selection objective inside the eligible candidate set. Safety constraints define eligibility.

Before generation, the engine must have enough evidence about:

```text
agent responsibilities
autonomy and approval boundaries
external write behavior
production or sensitive-data relevance
required completion checks
forbidden or irreversible actions
the project-specific role set
machine-evaluable policy rules and their required evidence
```

A safety fact may come from an inherited organization policy, repository policy or user answer. Do not ask again when an authoritative source already supplies it.

If a critical safety dimension is unresolved, restrict candidate selection to questions that can resolve a critical unknown. Among those candidates, still choose maximum weighted information gain.

## Question construction

Ask exactly one question at a time.

For predefined answer branches, use OpenCode's question tool first.

Required behavior:

```text
1. Ask one concise question.
2. Provide mutually understandable options when useful.
3. Include `Other / custom`.
4. Allow free text even when options are present.
5. Do not expose probability calculations unless the user asks.
6. Do not mechanically announce topic activation.
```

Plain A/B/C text is fallback mode only when the question tool is unavailable or fails.

Free-text questions are appropriate when predefined choices would constrain the answer or when the project is novel.

## Answer processing

After each answer:

```text
normalize explicit facts
preserve ambiguity instead of silently resolving it
update affected probability distributions
record the user's answer as the strongest source
activate newly relevant topic packs
deactivate or prune irrelevant topics
recalculate weighted entropy
generate a fresh candidate set
```

Do not follow a previously planned sequence when the new answer changes which question has the highest expected value.

If an answer contains several facts, update all affected dimensions and skip questions made redundant by those facts.

If an answer contradicts repository evidence, surface the conflict in one focused clarification question only when it affects the harness.

## Hypothesis confirmation

Prefer confirming a compact evidence-based hypothesis over asking several low-value questions.

Example:

```text
I found a Spring backend, an Angular frontend, GitLab CI and Kubernetes manifests.
Should I treat this as an existing production system where the harness must
prioritize regression safety and approval-gated deployment changes?
```

One confirmation may resolve multiple correlated dimensions.

## Topic loading

Start with `topic-catalog.md`, which contains summaries and routing signals.

Load `role-catalog.md` when agent responsibilities are being resolved. Treat it as a candidate library, never as an installation manifest.

Load full topic packs only when their activation signals are present or their relevance remains uncertain and potentially high-impact.

Do not load every topic pack merely because context is available.

Topic packs may be added without changing the core engine. Unknown custom topics may be created from project evidence during the interview, but their assumptions must be visible in the final summary.

## Generation readiness and stopping

Stop asking questions when all of the following are true:

```text
no blocking safety unknown remains
the project-specific role set is confirmed
required harness outputs can be generated
remaining uncertainty has a safe documented default
the best remaining candidate has low expected information gain
the final summary can distinguish facts, inferences and defaults
```

Suggested decision rule:

```text
ready = criticalUnknowns is empty
        AND discoverySubject is sufficient
        AND roleSelection is sufficient
        AND policyEvaluability is sufficient
        AND requiredOutputCoverage is complete
        AND maxRemainingQuestionValue < stopThreshold
```

Use `0.15` as an initial stop threshold for question value unless the project policy specifies another threshold. This is a starting heuristic that should later be calibrated from interview outcomes.

Do not stop merely because a fixed number of questions was asked.

Do not continue merely because a topic pack contains unused questions.

## Interview trace

Keep a compact internal trace for later evaluation:

```text
question id and topic
entropy before
estimated information gain
reason selected
answer summary
entropy after
dimensions updated
topics activated or pruned
```

During bootstrap this trace remains internal and must not contain secrets. After the user approves generation, it may be written as a run artifact when the harness configuration enables interview telemetry.

## Generation contract

The final belief state, not the sequence of questions, drives generation.

Before writing files, present a concise summary that separates:

```text
confirmed facts
evidence-based inferences
defaults and assumptions
active safety boundaries
selected roles and policies
files to create or update
remaining non-blocking uncertainty
```

Generate files only after explicit approval.

## Prohibited behavior

Do not:

```text
run a fixed interview sequence
start with an exact hard-coded question regardless of context
ask every question in a topic pack
claim Bayesian inference without maintaining probability distributions
claim maximum information gain without comparing candidates
ask for facts already established by reliable evidence
optimize entropy unrelated to harness output
skip safety-critical coverage because another question has higher generic entropy
hide assumptions in generated files
```
