# Tektona Deployment Contract

This contract maps the generated OCI agent runtime to Tektona without making undocumented assumptions about a particular Tektona CLI, SDK or API version.

## Platform model

The image plan has two renderings: a portable Dockerfile and a Tektona-native manifest. Tektona turns the selected rendering into a sandbox-template version:

```text
image-plan.json
→ native SandboxTemplate manifest (recommended)
  or Dockerfile → externally published OCI image
→ Tektona template build (asynchronous in the API; streamed/waited by the CLI workflow)
→ immutable template version
→ tag moved to the successful version
→ optional sandbox created from project/<name>:<tag> or org/<name>:<tag>
```

Use a project template by default. Project templates are referenced as `project/<name>` (or by their bare name); organization templates are referenced as `org/<name>`. `tektona/<name>` identifies a read-only system template and must never be used as the destination for generated builds.

Template creation, builds and tag moves require the corresponding Tektona admin role. They are external writes and require explicit approval separately from approval to generate the local harness.

## Required generated artifacts

In addition to the generic image artifacts, `/harness-init` always generates:

```text
.agents/runtime/tektona-deployment.json
.agents/runtime/sandbox.template.tektona.yaml
.agents/runtime/deploy-tektona.sh
.agents/context/tektona-deployment.md
```

`tektona-deployment.json` is a normalized, versioned handoff owned by this toolkit. It is not presented as a raw Tektona API request. `sandbox.template.tektona.yaml` is the Tektona-native manifest. `deploy-tektona.sh` validates and previews the handoff and may apply it only after verifying the installed Tektona CLI command surface.

The documented CLI workflow is:

```bash
tektona ctx show
tektona template build run --file .agents/runtime/sandbox.template.tektona.yaml --tag <tag>
tektona sandbox create <template-reference>:<tag> --name <sandbox-name>
```

The build command streams its log and waits; a failed build publishes no version. Before use, verify these subcommands and flags with the installed CLI help and record its version. Never guess additional flags, SDK method signatures or HTTP request bodies. When the exact interface cannot be verified, leave deployment in `plan` mode with adapter `unresolved`; the artifacts remain ready without claiming publication.

The file-based command above is verified for the current project selected by `tektona ctx show`. An organization-scoped template requires its exact scope-selection interface to be verified separately; the generated script must fail closed instead of assuming an organization flag.

## Build strategies

Prefer `native-manifest`. Tektona's manifest is `apiVersion: tektona.ai/v1`, `kind: SandboxTemplate`; it builds on a versioned official image and runs ordered build steps. Use a verified tag of:

```text
ghcr.io/tektona-ai/sandbox-base:<version>  headless agent/CI workloads
ghcr.io/tektona-ai/desktop-x11:<version>   browser or computer-use workloads
```

The official images track the current Ubuntu LTS, boot with systemd and already include OpenCode plus common developer tooling. Generated steps therefore add only project-specific layers and still verify `opencode --version`. Use the highest verified release tag available to the target deployment; do not silently copy an example version from documentation.

Use `external-oci-image` when the committed Dockerfile is authoritative, the same image runs outside Tektona, or CI already builds it. Build and publish that image first, then let Tektona create/build the template from the fully qualified image reference. A private image requires a matching project registry credential; only its resource reference belongs in the deployment plan.

The generated native manifest must map each image-plan layer to one named build step, fail on the first error and keep build-time `user`, `workdir` and environment separate from sandbox defaults. The manifest carries no organization or project; CLI context selects the scope.

## Tektona-native responsibilities

Keep these concerns outside the OCI image and reference them by stable Tektona resource name only:

```text
repository attachment and git credential
container-registry credential
project or organization secrets
egress network policy
egress proxy profile and credential injection
sandbox CPU, memory, disk and location
auto-pause and auto-delete lifecycle
preview URLs, SSH/VNC access and sharing
```

Secret values, registry credentials and Git credentials must never appear in the deployment JSON, Dockerfile, image plan, build log or generated adapter. Egress proxy profiles are preferred for credentials that can be injected at the outbound boundary.

Do not install a VNC server in the image for Tektona. Tektona supplies desktop connectivity independently of the image.

## Repository and process lifecycle

Tektona attaches repositories to projects and can use stored Git credentials for private remotes. The sandbox platform is responsible for cloning or mounting the selected repository after the template starts. The project source is not copied into the OCI image.

Represent repeatable sandbox commands as Tektona process definitions:

```text
sandbox bootstrap → optional autostart process after the repository is available
development database/cache/queue → background or autostart process when packaged in the template
OpenCode → interactive or background process started for the assigned task
```

The Dockerfile `CMD` remains a portable default, but Tektona process management owns long-running lifecycle, logs, stop signals and autostart. A process command must not contain a secret value.

Tektona starts image `ENTRYPOINT` and `CMD` at boot. For an image intended primarily for Tektona, do not auto-start an interactive OpenCode session through `CMD`; start it through Tektona process management for the assigned task. Align the session user's passwd home, `HOME` and working directory (for the portable image, `/workspace`) so SSH, file copy and remote development tools operate in one location.

For stateful development resources, prefer `tektona-process` when the server can be installed reproducibly in a dedicated `sandbox-service` image layer. Compose remains valid only when the selected Tektona base/template explicitly proves that a usable daemon or supported rootless runtime exists. CLI presence alone is not capability evidence.

## Build and deployment gates

The safe default is:

```text
deployment.mode = plan
deployment.approved = false
deployment.adapter = unresolved
sandbox.createAfterBuild = false
```

Before a template build:

1. validate `image-plan.json`, the Dockerfile and `tektona-deployment.json`;
2. validate that the native manifest contains the declared name, official versioned base, layer steps, non-root sandbox user/workdir and no secret values;
3. resolve the target organization, project, scope and template reference;
4. verify admin permission and the exact target Tektona interface;
5. resolve repository, registry, egress and secret references without reading their values;
6. check requested CPU, memory and disk against the target deployment's sandbox limits;
7. obtain explicit approval for the template build and, separately, sandbox creation;
8. stream or poll the build to a terminal state;
9. move the requested tag only after a successful build;
10. record build id, template-version id, image/base reference and tag in the deployment result.

Never report a Tektona template as deployed while its asynchronous build is pending or failed. Never create a sandbox from an archived version. Prefer archive over destructive template/version deletion and use lifecycle/prune preview capabilities before cleanup.

## Local validation

The Dockerfile can still be built locally with Docker, Podman or BuildKit after explicit approval. A local build validates OCI portability but does not create a Tektona template version, attach platform policies or prove that a Tektona sandbox can start. Tektona remains the authoritative deployment target.
