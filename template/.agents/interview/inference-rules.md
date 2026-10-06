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

language or build manifest
→ activate the matching OCI toolchain layer and prefer repository-declared versions

database evidence
→ add client tooling when useful and prefer a sandbox-service layer managed as a Tektona process

Compose-managed development resources
→ require documented capability evidence, a declared container daemon mode, Compose tooling, health checks and sandbox bootstrap

Tektona target
→ generate a project-scoped template plan by default and keep external writes unapproved
→ reference repositories, credentials, egress policies, proxy profiles, registries and secrets by name only

available Tektona CLI, SDK or OpenAPI description
→ inspect the exact version/interface before generating an apply-capable deployment adapter

allowed sandbox internet access
→ enable recorded user-local runtime installation as a fallback, not as a replacement for known image layers

CI image, toolchain file or development container
→ treat declared runtime versions as strong image-plan evidence
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
unknown stateful service placement → Tektona process backed by a distinct sandbox-service image layer
unknown container daemon availability → mode none; do not generate Compose without capability evidence
unknown Tektona scope → project template
unknown Tektona deployment permission → validated plan only; no template build, tag move or sandbox creation
unknown Tektona interface → unresolved adapter; never invent CLI, SDK or API syntax
unknown runtime-install privilege → user-local only; no privilege escalation
unknown image base version → official current Ubuntu LTS tag with digest recorded by the builder
unknown local image-build permission → generate the build script but do not execute it
```

Never put credentials into an image build plan. A local build is eligible only after explicit approval because it downloads artifacts and changes the local container cache.

## Conflict handling

When evidence conflicts, prefer the higher-precedence source defined in `interview-state-schema.md`. Ask one clarification question when the conflict changes permissions, safety or generated artifacts.

## No fixed flow

Inference rules activate and prune candidates. They must never impose a global question order.
