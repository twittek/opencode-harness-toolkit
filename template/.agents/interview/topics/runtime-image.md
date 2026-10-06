---
id: runtime-image
version: 1
dimensions:
  - runtime.oci-base
  - runtime.toolchains
  - runtime.database-clients
  - runtime.service-dependencies
  - runtime.container-orchestration
  - runtime.network-access
  - runtime.dynamic-install
  - runtime.target-platforms
  - runtime.build-mode
  - runtime.version-policy
  - runtime.tektona-scope
  - runtime.tektona-template
  - runtime.tektona-integrations
  - runtime.tektona-resources
  - runtime.tektona-deployment-mode
activation-signals:
  - always-evaluate-for-image-generation
  - language-manifest
  - database-driver
  - ci-runtime
  - development-container
outputs:
  - Dockerfile
  - .dockerignore
  - .agents/runtime/image-plan.json
  - .agents/runtime/build-image.sh
  - .agents/runtime/bootstrap-sandbox.sh
  - .agents/runtime/tektona-deployment.json
  - .agents/runtime/sandbox.template.tektona.yaml
  - .agents/runtime/deploy-tektona.sh
  - .agents/runtime/compose.yaml
  - .agents/context/runtime-image.md
  - .agents/context/tektona-deployment.md
---

# Agent Runtime Image

Resolve the smallest reproducible OCI image that can run OpenCode and the tools required by the confirmed project work.

## Evidence signals

```text
language and package manifests
lockfiles and toolchain-version files
database drivers and connection configuration
CI images and build jobs
development-container configuration
deployment manifests and target CPU architecture
```

## Inference direction

```text
language or build manifest
→ matching toolchain layer

database evidence
→ client or diagnostic layer when useful
→ dedicated sandbox-service layer plus Tektona process by default

confirmed Docker-in-sandbox capability
→ Compose remains an optional service lifecycle

stateful server inside the agent image
→ embedded only after explicit confirmation
```

OpenCode is mandatory and does not require an interview question. Do not ask the user to repeat versions that are reliably declared by the repository.

## Candidate patterns

Ask only when the answer changes the generated image materially:

```text
The repository supports two incompatible runtime versions. Which one must the agent image use?
Does the sandbox provide a container daemon, or must the MicroVM run a rootless engine itself?
Which Tektona organization/project and project- or organization-scoped template should receive the build?
Which existing Tektona repository, egress policy, proxy profile, registry and secret references belong to the sandbox?
Should initialization stop at a validated plan, build the template after separate approval, or also create a sandbox after a successful build?
Which CPU, memory, disk, location, auto-pause and auto-delete settings are required?
Which internet destinations and runtime-installation privileges may the agent use inside its disposable sandbox?
Which target platforms are required when repository and delivery evidence do not resolve amd64 versus arm64?
Should the generated image only be built by the sandbox, or is an explicitly approved local validation build also wanted?
```

## Safe defaults

```text
base → official ubuntu:latest, resolved and locked by the builder
runtime user → non-root
OpenCode → mandatory, versioned and verified
Tektona scope → project template
Tektona deployment → validated plan only; no external write
Tektona adapter → unresolved until exact installed CLI, SDK or OpenAPI interface is verified
Tektona build strategy → native SandboxTemplate on a verified official sandbox-base release
stateful dependency → sandbox-service layer plus Tektona background/autostart process
container execution → none unless platform-daemon or rootless capability is evidenced
known recurring tool → preinstalled in the image
unforeseen tool → user-local runtime installation when network policy permits
local build → not executed without explicit approval
target platform → infer from delivery evidence; otherwise linux/amd64
secrets → Tektona resource references only; values never baked into the image or plan
```

## Completion

Complete when the image and Tektona deployment plans can be rendered without inventing tools or platform interfaces, each optional layer has evidence, every development service has a Tektona process or proven Compose lifecycle, repository/egress/secret references contain no values, sandbox resources are explicit and build/deployment permissions are known.
