# Candidate Question Guidance

Questions are generated from active topic packs and current project evidence. This file does not define an interview sequence.

## Candidate quality

A strong candidate question:

```text
resolves one or more high-impact unknowns
causes different answers to produce meaningfully different harness output
can prune multiple downstream branches
is answerable without unnecessary research
does not repeat reliable evidence
is concise enough to ask alone
```

Weak candidates ask for implementation details before their topic is relevant or collect preferences that do not change the harness.

## Candidate comparison

Before asking a question, compare candidates from all active topics.

For each candidate estimate:

```text
answer branches and their probabilities
affected belief dimensions
expected posterior entropy
generated artifacts affected
risk relevance
interaction cost
```

Select the eligible candidate with maximum weighted information gain per unit of interaction cost.

## Dynamic formulation

Topic-pack questions are starting points. Adapt wording and options to the observed project.

Prefer:

```text
I found GitLab CI and Kubernetes manifests. Are deployments managed by this
repository, and should deployment changes always require approval?
```

over:

```text
Do you use CI/CD?
```

The first form confirms evidence and resolves governance impact in one answer.

## Multi-fact answers

When an answer resolves several dimensions, update all of them. Do not ask follow-up questions for facts the user already supplied.

## Required interaction behavior

```text
ask exactly one question at a time
use the question tool for predefined choices
include Other / custom
allow free-text answers
do not reveal internal scoring unless requested
```
