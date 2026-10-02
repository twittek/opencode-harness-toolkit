# Topic Pack Contract

Each topic pack is a modular source of discovery knowledge, not a questionnaire.

A topic pack should contain:

```text
YAML frontmatter with id, version, dimensions, activation signals and outputs
the uncertainty the topic resolves
repository signals that may answer it
candidate questions or formulation patterns
pruning conditions
completion conditions
safe defaults when applicable
```

Candidate questions are optional templates. The interview engine may adapt or replace them when a project-specific question has greater expected information gain.

Do not encode a mandatory internal order. Use prerequisites only when one fact is genuinely required to interpret another.

Safety topics may declare blocking dimensions that must be resolved from evidence, policy or a user answer before generation.

Topics that produce normative requirements must also activate `compliance-observability.md`. Their rules must be expressible through the machine-evaluable policy contract with typed signals, deterministic predicates and explicit unknown handling. Ambiguous prose is not an enforceable policy.
