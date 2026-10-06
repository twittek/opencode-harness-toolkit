# Agent Runtime Image Contract

This contract defines how `/harness-init` turns discovered project requirements into a buildable OCI agent image.

## Required generated artifacts

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

When the project needs databases, queues, caches, emulators or similar development resources, also generate:

```text
.agents/runtime/compose.yaml
```

Generate `compose.yaml` only when the target sandbox has proven container-runtime capability. On Tektona, prefer a dedicated `sandbox-service` layer plus Tektona process management when the service can be installed reproducibly. The Tektona mapping is defined in `.agents/runtime/tektona-contract.md`.

After a successful local or sandbox build, the builder should additionally produce:

```text
.agents/runtime/image-lock.json
```

The Dockerfile is the portable build source. `image-plan.json` is the machine-readable explanation and sandbox handoff. `image-lock.json` records the resolved base digest, final image digest and installed tool versions.

Generate `.dockerignore` as a deny-by-default build context. Admit only the Dockerfile and the machine-readable image plan when the selected builder needs that plan. The project repository is cloned or mounted later by the sandbox runtime, not sent to or copied into the image build.

## Layer model

Generate layers in this stable order:

```text
1. official Ubuntu base
2. baseline operating-system utilities
3. sandbox orchestration tools when required
4. OpenCode agent
5. detected language toolchains and build tools
6. detected database and integration clients
7. project-specific utilities
8. sandbox-service binaries managed by Tektona processes when required
9. explicitly embedded services when approved
10. non-root runtime user and final metadata
```

Every optional layer must map to interview or repository evidence and have a stable id in `image-plan.json`.

Use comments in the generated Dockerfile:

```dockerfile
# harness-layer: rust-toolchain
# harness-layer: mongodb-client
```

This makes the Dockerfile auditable against the image plan.

## Ubuntu base policy

Default to the official `ubuntu:latest` image, which tracks the current Ubuntu LTS. The build must use `--pull` and record the resolved immutable base digest.

For reproducible or regulated projects, replace the moving tag through the build argument with an approved version-and-digest reference such as:

```text
ubuntu:<lts-version>@sha256:<digest>
```

The Dockerfile must expose the base as a build argument:

```dockerfile
ARG UBUNTU_BASE_IMAGE=ubuntu:latest
FROM ${UBUNTU_BASE_IMAGE}
```

Do not use an arbitrary Ubuntu mirror or unofficial base image without explicit approval.

## Mandatory OpenCode layer

OpenCode is always present in the image, independently of the detected project stack.

Use a supported official installation method. The default contract uses the official npm package:

```text
@opencode/cli
```

For the npm installation method, install an approved Node.js/npm runtime in the mandatory OpenCode step even when Node.js is not part of the project stack. Expose and use:

```dockerfile
ARG OPENCODE_VERSION=latest
RUN npm install --global "@opencode/cli@${OPENCODE_VERSION}" \
    && opencode --version
```

The image plan declares the requested OpenCode version and update policy. The build lock records the concrete installed version. The Dockerfile must verify:

```text
opencode --version
```

Do not inject provider keys, API tokens or OpenCode credentials during image build.

## Tool discovery and mapping

Derive tool layers from strong evidence before asking the user:

```text
Cargo.toml, Cargo.lock, rust-toolchain.toml
→ Rust compiler, Cargo and required native build dependencies

package.json and lockfiles
→ Node.js runtime and the selected package manager

pyproject.toml, requirements files or uv.lock
→ Python runtime and the selected environment/package tool

go.mod
→ Go toolchain

pom.xml, build.gradle or gradle wrapper
→ JDK and matching build tool requirements

database configuration or drivers
→ database client and diagnostic tools

CI files and development-container definitions
→ additional evidence for versions and system packages
```

Prefer versions from repository manifests, lockfiles and toolchain files. Ask one focused question only when different versions or installation modes would materially change the image.

Do not add a tool merely because it appeared in a generic topic catalog.

## Autonomous development sandbox

The image exists to give the agent everything required to develop, build, test and diagnose the product inside its isolated MicroVM. Known recurring requirements belong in the image or declared sandbox resources; internet access and runtime installation are fallbacks, not substitutes for a complete plan.

Classify every discovered dependency:

```text
toolchain
→ installed in the agent image

client or diagnostic utility
→ installed in the agent image when useful for the assigned work

stateful development resource on Tektona
→ installed in a dedicated sandbox-service image layer when reproducible
→ started and monitored through a Tektona background/autostart process

stateful resource through Compose
→ use only when the selected Tektona template proves a usable daemon or supported rootless runtime
→ declare in `.agents/runtime/compose.yaml` and start inside the sandbox MicroVM

platform-managed service
→ use only when sandbox policy or infrastructure explicitly selects it

embedded service
→ installed in the agent image only after explicit confirmation
```

Example for MongoDB:

```text
MongoDB is used by the project
→ install the approved MongoDB client/diagnostic tooling in the agent image
→ prefer a versioned sandbox-service layer for the server
→ declare a Tektona background/autostart process with a health check

Tektona template proves a compatible container runtime
→ alternatively add an approved MongoDB image to `.agents/runtime/compose.yaml`
→ record that concrete capability as evidence and let `bootstrap-sandbox.sh` start it
```

Do not start a database daemon from the Dockerfile or image `CMD`. Keep its binaries in a distinct layer and its lifecycle explicit through Tektona processes or, with proven capability, Compose. An `embedded-service` shares the OpenCode process lifecycle and still requires explicit confirmation.

When one or more Compose resources are required, the agent image must contain compatible container and Compose clients. The image plan must also declare how the sandbox supplies execution:

```text
platform-daemon
→ the MicroVM platform exposes a dedicated container daemon/socket to the agent

rootless-in-microvm
→ the image contains a rootless engine and the MicroVM permits user namespaces and cgroups
```

Do not assume that installing only the Docker CLI creates a usable daemon. `/harness-init` must select a mode supported by the target sandbox. The generated bootstrap script must fail clearly when the declared runtime is unavailable.

For every non-`none` container-runtime mode, record `capabilityEvidenceRefs` in the image plan. Tektona documentation for template builds and sandbox processes does not by itself prove Docker-in-Docker or socket availability.

## Network and runtime installation

Model sandbox internet access and dynamic installation explicitly in `image-plan.json`.

Known tools needed for normal development must be preinstalled in the image. When network access is allowed, the agent may download sources, dependencies or an unforeseen tool into the disposable sandbox according to the configured installation mode:

```text
user-local
→ install below the agent home or workspace without privilege escalation

sandbox-root
→ permit OS-level installation only when the isolated-sandbox policy explicitly grants it

disabled
→ no runtime installation
```

Every runtime installation must record the source, requested version, integrity or signature evidence, task id and installed path in sandbox telemetry or `.agents/runs/<task-id>/runtime-installations.jsonl`. It must not persist credentials in shell history, logs, the repository or resulting image. Repeated runtime installations are drift signals: `/harness-retro` or `/harness-check` should propose promoting them into the next image plan.

`sandbox-root` requires a separate explicit privilege-escalation approval in the plan. Network access alone never authorizes root installation.

## Dockerfile requirements

The generated Dockerfile must:

```text
use syntax compatible with Docker BuildKit and OCI builders
use the official Ubuntu base argument
set noninteractive package installation only for build steps
combine apt update/install/cleanup in the same layer
install ca-certificates, curl, git, jq and required archive/build utilities
install and verify OpenCode
install every required image-plan layer and verify its tools
install container/Compose tooling whenever sandbox-compose resources are declared
create and use a non-root agent user
use /workspace as the agent's passwd home, HOME and default working directory
avoid copying the project source into the runtime image
contain no credentials, secret values or environment-specific endpoints
provide OCI labels for subject, plan version and source repository when known
keep OpenCode on PATH and start it through Tektona process management for Tektona workloads
```

Tektona starts Dockerfile `ENTRYPOINT` and `CMD` at sandbox boot. Do not use an interactive `opencode` command as the Tektona image's automatic boot workload. For a portable non-Tektona variant, a command may be supplied by the caller.

Remote installers require an approved source and integrity strategy. Prefer signed package repositories or checksum-verified archives. A raw `curl | sh` pipeline is not acceptable in the generated final Dockerfile.

Validate the generated contract before any build:

```bash
python3 .agents/scripts/image-plan-validator.py validate-plan .agents/runtime/image-plan.json
python3 .agents/scripts/image-plan-validator.py validate-dockerfile .agents/runtime/image-plan.json Dockerfile
python3 .agents/scripts/image-plan-validator.py validate-tektona .agents/runtime/tektona-deployment.json .agents/runtime/image-plan.json .agents/runtime/sandbox.template.tektona.yaml
bash -n .agents/runtime/build-image.sh
bash -n .agents/runtime/deploy-tektona.sh
```

## Observer and policy evidence

The builder or sandbox observer should emit typed facts for the resulting image and runtime, including the resolved base digest, output digest, OpenCode version, installed layer ids, verification results, runtime user, scan result, build mode, Compose health and runtime installations. The generated policy registry may use those facts for deterministic rules such as:

```text
declared layer ids == verified installed layer ids
OpenCode verification exit code == 0
runtime user != root
secret scan finding count == 0
local build executed implies local build approved
moving base reference implies resolved digest is present
```

Missing build or scan evidence is `UNKNOWN`, never `PASS`. A scanner or decision model supplies facts; configured policy predicates and thresholds determine escalation.

## Sandbox build handoff

The platform handoff contains:

```text
Dockerfile
.dockerignore
.agents/runtime/image-plan.json
.agents/runtime/tektona-deployment.json
.agents/runtime/sandbox.template.tektona.yaml
.agents/runtime/compose.yaml when declared
```

Tektona builds the native manifest by default. It uses the Dockerfile path only after an external OCI build has published the declared result image to a registry.

The platform builder should:

```text
build with --pull
target all declared platforms
resolve and record base and output digests
run every declared verification command
run opencode --version
produce an SBOM and build-provenance reference when supported
scan the final image according to organization policy
write or return image-lock.json
publish only after the configured approval gate
provide the declared container-runtime capability to each created MicroVM when Compose is selected
```

Network access and registry credentials are platform concerns. Do not store them in the repository or Dockerfile.

After the repository is cloned, the sandbox should run:

```text
.agents/runtime/bootstrap-sandbox.sh
```

The script verifies the declared runtime, coordinates any Compose resources, verifies Tektona-managed service endpoints, installs project dependencies from repository lockfiles when the network policy permits and then verifies the development environment. It must be idempotent and provide a cleanup command for resources it owns. Runtime secrets are referenced through Tektona secret or egress-proxy resources; values are never committed to scripts, JSON or `compose.yaml`.

The image contains reusable compilers, package managers and system tools. Project source and project-specific dependency trees are acquired after the repository is cloned so that the same image remains reusable and lockfiles remain authoritative.

Generated Compose resources must use approved versioned images, an isolated project network, explicit health checks, an explicit agent-facing endpoint and ephemeral volumes by default. Do not mount host paths, a host-wide container socket or unrelated platform resources into service containers. Bind published development ports only when the agent needs host-style access inside the MicroVM; never expose them outside the sandbox unless the sandbox policy explicitly allows it.

## Local build

The same image may be built locally before sandbox submission when Docker, Podman or a compatible BuildKit frontend is available.

`build-image.sh` must support:

```text
CONTAINER_ENGINE=docker|podman
IMAGE_REF=<local or registry reference>
UBUNTU_BASE_IMAGE=<optional immutable override>
OPENCODE_VERSION=<approved version override>
```

The script must select only an available approved engine, call its build command with `--pull`, pass the declared build arguments, tag `IMAGE_REF`, then start disposable verification containers for `opencode --version` and every declared layer verification command. It must use neither registry login nor secret build arguments.

Local execution is optional and requires explicit approval because it pulls images, downloads packages and changes the local container cache. A successful local build validates portability but does not replace the sandbox platform's digest, policy scan or provenance record.

## Update and drift behavior

`/harness-check` compares repository evidence, `image-plan.json`, Dockerfile layer markers and `image-lock.json`.

Examples of drift:

```text
Rust was added to the project but no Rust layer exists
a database was removed but its client layer remains
compose declares a database but the image lacks working container/Compose tooling
the sandbox runtime cannot provide the daemon mode declared by the plan
the agent repeatedly installs the same undeclared tool at runtime
OpenCode is missing or cannot report its version
the moving Ubuntu tag resolved to a new digest without a recorded rebuild
the Dockerfile contains a layer absent from the image plan
the lock references a tool version that no longer matches the Dockerfile arguments
```

Image changes follow the normal proposal, approval and versioning lifecycle.
