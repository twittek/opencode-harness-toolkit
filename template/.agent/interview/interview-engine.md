# Adaptive Scenario Discovery Interview Engine

The interview uses an information-gain-oriented approach inspired by Akinator-style questioning.

## Mandatory question tool usage

For predefined-choice questions, the agent must use OpenCode's interactive question tool first.

Plain A/B/C text is only a fallback mode.

```text
Using plain A/B/C text is a fallback mode, not the primary mode.
Do not use fallback mode unless tool usage is unavailable.
```

The fallback must not be used just because it is simpler for the model.

The preferred interaction is:

```text
question tool → selectable options → user selection → scenario update → next best question
```

## Objective

Identify the most likely development scenario with as few questions as possible.

The agent should:

1. Maintain likely scenario candidates.
2. Ask one high-value question at a time.
3. Use each answer to update scenario likelihoods.
4. Prune irrelevant branches.
5. State a hypothesis when confidence is high.
6. Ask only the next best question.
7. Generate the harness only after final confirmation.

## Field classification

The interview combines multiple disciplines:

```text
Bayesian inference
→ probability theory and Bayesian statistics
→ update scenario likelihoods after each answer

Information gain / entropy reduction
→ information theory
→ choose the next question with maximum expected uncertainty reduction

Decision trees / pruning
→ machine learning, computer science and statistics
→ remove irrelevant branches from the remaining search space

Active learning / adaptive questioning
→ machine learning
→ actively choose the next most useful question
```

Operational rule:

```text
Use Bayesian inference to update beliefs.
Use information gain to select questions.
Use pruning to skip irrelevant branches.
Use active learning to avoid static questionnaires.
```

## Mathematical framing

Use these concepts:

- Bayesian inference
- entropy reduction
- information gain
- decision-tree pruning
- active learning
- adaptive questioning

A good question partitions the remaining scenario space.

## Good vs bad question examples

Bad early question:

```text
Do you use Oracle Spatial?
```

Good early question:

```text
Are there external systems or integrations?
```

Bad early question:

```text
Do you use Vitest or Jest?
```

Good early question:

```text
Should automated tests be part of the quality gates?
```

Bad early question:

```text
Soll der Agent einen GitLab-Kommentar mit glab posten?
```

Good early question:

```text
Which system do you use for work items and code reviews?
```

## Rule

Never ask multiple dependent questions in one message.
