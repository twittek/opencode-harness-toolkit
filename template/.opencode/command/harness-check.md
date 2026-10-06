---
description: "Audit the current harness version and write active findings."
---

# Harness Check Command

## Goal

Audit the current harness version for completeness, consistency, duplication, drift, safety and maintainability.

Do not modify harness files.

## Version scope

Read current version from:

`.agents/context/harness-version.json`

Write reports under:

`.agents/runs/harness-check/<current-version>/<date>/`

If version is missing, use `unknown` and create a critical finding.

## Output files

Create:
- `harness-inventory.md`
- `completeness-report.md`
- `consistency-report.md`
- `duplication-report.md`
- `drift-report.md`
- `safety-report.md`
- `maintainability-report.md`
- `active-findings.md`
- `recommended-actions.md`

## Finding format

```md
## FINDING-<version>-<number>: <title>

Status: active
Severity: critical|important|minor
Source: check
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

## Checks

Inspect harness files:
- `AGENTS.md`
- `opencode.jsonc` or `opencode.json`
- `.opencode/command/*.md`
- `.opencode/agent/*.md`
- `.agents/context/*.md`
- `.agents/interview/*.md`
- `.agents/interview/topics/*.md`
- `.agents/roles/*.md`
- `.agents/integrations/*.md`
- `.agents/mcp/*.md`
- `.agents/playbooks/*.md`
- `.agents/templates/*.md`
- `.agents/skills/*.md`
- `.agents/scripts/*.sh`
- `.agents/scripts/*.py`
- `.agents/runtime/*`
- `Dockerfile`
- `.dockerignore`

Check:
- missing lifecycle files
- duplicate rules
- contradictions
- stale command names like `/create-harness`
- unclear autonomy boundaries
- unsafe shell patterns
- GitLab/GitHub guardrail gaps
- context strategy not 128K-friendly
- version/changelog hygiene

Check adaptive interview integrity:

```text
- no fixed first question or global question order
- the belief state models independent dimensions and probabilities
- weighted entropy and expected information gain are defined
- candidate questions are compared across active topics
- safety-critical unknowns constrain candidate eligibility
- topic packs are modular and do not behave as mandatory blocks
- repository evidence is used before asking redundant questions
- generation readiness and a stop criterion are defined
- all topic-catalog references resolve to existing files
```

Final response in German:
- current version
- health rating: green/yellow/red
- number of active findings
- recommended next step

## Generated structure checks

Verify that initialization produced a project-specific structure rather than a copied toolkit scaffold:

```text
- AGENTS.md does not contain <!-- harness-bootstrap: true --> after initialization
- AGENTS.md identifies the target product and references only files that exist
- every role named by AGENTS.md and role-activation-policy.md has a matching file
- every generated role is confirmed by the recorded role plan or explicitly retained as custom
- absent catalog roles are not listed as active
- generated roles contain project-specific responsibilities, boundaries and checks
- generic toolkit boilerplate was not copied as final role guidance
- optional integrations, policies and playbooks exist only when supported by the harness state
```

Treat stale bootstrap instructions, an all-role dump or references to absent files as active findings.

## Policy evaluability checks

Verify that policies can be scored by an observer and deterministic policy engine:

```text
- .agents/policies/policy-registry.json exists and passes policy-evaluator.py validate
- policy registry, task evidence and evaluation result schemas are present and valid JSON
- registry and rule versions are present
- every signal has a type, source and required provenance
- every rule has deterministic applicability and assertion predicates
- every rule defines severity, weight, unknown handling and reason codes
- warnAt <= escalateAt <= blockAt and minimumCoverage is explicit
- PASS, FAIL, UNKNOWN and NOT_APPLICABLE remain distinct
- missing or invalid evidence never becomes PASS
- hard-gate behavior is explicit
- decision-model outputs are typed input signals rather than enforcement decisions
- normative Markdown statements reference matching registry rule ids
- unobservable or ambiguous requirements are tracked as policy-design gaps
```

Search normative prose for terms such as `appropriate`, `reasonable`, `sufficient`, `adequate`, `best effort` and `when necessary`. Flag each occurrence unless the text references a finite measurable rubric or explicitly marks the item as non-normative guidance.

Treat schema errors, undeclared signals, missing-evidence-as-pass behavior and ambiguous critical rules as high-severity findings.

## OCI runtime image checks

Verify that the generated agent image is reproducible, evidence-based and safe:

```text
- Dockerfile, .dockerignore, runtime-image.md, image-plan.json, build-image.sh and bootstrap-sandbox.sh exist
- tektona-deployment.json, deploy-tektona.sh and tektona-deployment.md exist
- image-plan.json is valid JSON and passes image-plan-validator.py validate-plan
- the Dockerfile passes image-plan-validator.py validate-dockerfile
- tektona-deployment.json and sandbox.template.tektona.yaml pass image-plan-validator.py validate-tektona against image-plan.json
- the base is the declared official Ubuntu reference and moving tags have a recorded digest after a build
- OpenCode is installed through the declared method and opencode --version is executed
- every # harness-layer marker has exactly one matching image-plan layer and vice versa
- every optional layer has repository or approved interview evidence
- service client layers point to declared layers
- required databases, queues, caches and emulators have a matching tektona-process, proven sandbox-compose or explicitly selected platform provisioning
- every tektona-process service points to a sandbox-service layer and matching Tektona process definition
- every sandbox-compose service has a pinned/approved image, health check and matching compose.yaml entry
- the declared platform daemon or rootless engine has recorded capability evidence sufficient to run Compose inside the MicroVM
- known recurring tools are image layers rather than repeated runtime downloads
- allowed runtime installations record source, version, integrity evidence, task and installed path
- the image runs as non-root from /workspace and does not copy the project source
- no credentials, secret values or environment-specific endpoints are present
- build-image.sh passes shell syntax checking and honors the approved build mode
- bootstrap-sandbox.sh passes shell syntax checking, is idempotent and has an explicit cleanup path
- deploy-tektona.sh validates/previews in plan mode and refuses writes without approval plus a version-verified adapter
- Tektona repository, credential, registry, egress, proxy and secret fields contain references only, never values
- Tektona scope/reference, resource requests, lifecycle, asynchronous build wait and process definitions are internally consistent
- every image-plan layer has one matching ordered marker/build step in the Tektona manifest and OpenCode is verified
- compose.yaml passes container-engine Compose validation when an engine is available
- image-lock.json, when present, matches base, OpenCode, layer versions and the last image digest
```

Compare current manifests, lockfiles, CI configuration, development-container files, Tektona target resources and recorded runtime installations with the image/deployment plans. Treat a newly required tool, a repeatedly downloaded tool, a removed dependency that remains installed, an unexplained layer, an unresolved moving base, a broken process/Compose resource, a stale Tektona reference or an unverified OpenCode installation as drift.

## Context Loading Policy checks

Check whether the harness uses the smallest useful context set.

Verify:

```text
- .agents/context/context-loading-policy.md exists
- Tier 1 baseline files are defined
- role-aware loading rules exist
- integration-aware loading rules exist
- run artifacts are not treated as always-loaded context
- generated/dependency folders are excluded
- the policy supports large context windows without encouraging context bloat
```

## Required self-verification

Before reporting completion, perform a self-verification pass.

Use:

```text
.agents/context/self-verification-policy.md
```

Verify:

```text
- requirement match: the result matches the user's request
- only intended files/content were changed
- relevant harness policies were followed
- available checks/tests were run or explicitly skipped with a reason
- remaining risks or assumptions are reported honestly
```
