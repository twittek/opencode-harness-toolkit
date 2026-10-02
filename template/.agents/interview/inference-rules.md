# Cross-Topic Inference Rules

Topic packs contain domain-specific routing guidance. These rules apply across topics.

## Evidence before questions

Inspect safe repository evidence before asking. Treat detected technology as strong evidence, not unquestionable truth.

## Relevance propagation

```text
production relevance
→ increase security, verification, delivery and observability relevance

external systems
→ increase integration, credential and external-write governance relevance

user-facing interface
→ increase UX, accessibility and end-to-end quality relevance

sensitive data or authentication
→ make security coverage blocking before generation

migration or refactoring
→ increase regression, compatibility and architecture-boundary relevance

agent write responsibilities
→ increase autonomy, approval and self-verification relevance

normative requirements or compliance obligations
→ activate compliance observability, typed signal discovery and policy operationalization

decision-model classification
→ treat model output as a versioned signal; keep thresholding and enforcement deterministic
```

## Safe pruning

Prune a topic only when:

```text
reliable evidence makes it not applicable
its possible answers would not change harness output
an inherited policy already determines its result
```

Do not prune merely because a topic is uncommon.

## Safe defaults

Use defaults only for non-blocking uncertainty and list them in the final summary.

Default direction:

```text
unknown external write → approval required
unknown destructive action → forbidden
unknown production access → no access
unknown secret handling → no secret material in harness files
unknown verification level → standard verification
unknown role activation → smallest useful role set
```

## Conflict handling

When evidence conflicts, prefer the higher-precedence source defined in `interview-state-schema.md`. Ask one clarification question when the conflict changes permissions, safety or generated artifacts.

## No fixed flow

Inference rules activate and prune candidates. They must never impose a global question order.
