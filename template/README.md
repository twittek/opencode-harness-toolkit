# Harness Toolkit Template

This directory contains bootstrap resources and generation references used by `opencode-harness-toolkit-install.sh` and `/harness-init`.

This maintenance README is package documentation and is deliberately not copied to the target project. A target project's existing `README.md` must remain product evidence for adaptive discovery.

Edit these files directly when changing the toolkit scaffold.

Key files:

```text
AGENTS.md
opencode.jsonc
.opencode/command/harness-init.md
.opencode/command/harness-check.md
.opencode/command/harness-update.md
.opencode/command/harness-retro.md
.opencode/command/harness-mcp.md
.agents/interview/topic-catalog.md
.agents/interview/role-catalog.md
.agents/interview/topics/
.agents/scripts/interview-ranker.py
.agents/policies/policy-contract.md
.agents/policies/policy-registry.schema.json
.agents/policies/task-evidence.schema.json
.agents/policies/evaluation-result.schema.json
.agents/scripts/policy-evaluator.py
.agents/runtime/image-contract.md
.agents/runtime/image-plan.schema.json
.agents/runtime/tektona-contract.md
.agents/runtime/tektona-deployment.schema.json
.agents/scripts/image-plan-validator.py
```

The installer copies only the bootstrap allowlist: commands, interview resources, entropy, policy and image-plan validators, policy and runtime schemas, bootstrap `AGENTS.md`, OpenCode configuration, and the context-loading and self-verification policies. Project-specific roles, integrations, policy rules, image plans, Dockerfiles, playbooks and run structures are deferred to `/harness-init`.

The bootstrap `opencode.jsonc` currently includes `litellm-local/qwen36-27b-mtp-128k` as an editable default model and an enabled local `chrome-devtools` MCP entry invoked through `npx`. These are current distribution defaults, not project requirements. Review them before first use; project-specific MCP additions or changes belong in `/harness-mcp` and remain approval-gated.

If the target already contains `AGENTS.md`, the installer preserves it. During initialization it is treated as project evidence and reconciled through the approval summary instead of being overwritten silently.

Do not put project-specific secrets into this template.


Interview engine files live under:

```text
.agents/interview/interview-engine.md
.agents/interview/interview-state-schema.md
.agents/interview/topic-catalog.md
.agents/interview/topics/
```

The topic packs are modular sources of discovery knowledge. They do not define a fixed questionnaire or global question order.

The current catalog covers discovery subject, project intent, architecture, frontend/UX, backend/data, security, integrations, delivery/operations, quality, agent governance, documentation, compliance observability and OCI/Tektona runtime generation.


Integration files live under:

```text
.agents/integrations/
.agents/context/integration-policy.md
.agents/mcp/mcp-policy.md
.agents/scripts/
```


MCP discovery command:

```text
/harness-mcp
```

MCP files live under:

```text
.agents/mcp/
.agents/runs/harness-mcp/
```


Generic role references maintained by the toolkit live under:

```text
.agents/roles/
```

They are not copied into target projects. `/harness-init` uses `.agents/interview/role-catalog.md`, confirms a project-specific role set and generates only those role files plus a matching activation policy.


Context loading policy:

```text
.agents/context/context-loading-policy.md
```


Self-verification policy:

```text
.agents/context/self-verification-policy.md
```

Machine-evaluable policy resources:

```text
.agents/policies/policy-contract.md
.agents/policies/policy-registry.schema.json
.agents/policies/task-evidence.schema.json
.agents/policies/evaluation-result.schema.json
.agents/scripts/policy-evaluator.py
```

`/harness-init` generates the project-specific `.agents/policies/policy-registry.json`; it is not copied from the toolkit.

OCI agent-image generation resources:

```text
.agents/interview/topics/runtime-image.md
.agents/runtime/image-contract.md
.agents/runtime/image-plan.schema.json
.agents/runtime/tektona-contract.md
.agents/runtime/tektona-deployment.schema.json
.agents/scripts/image-plan-validator.py
```

After approval, `/harness-init` generates `Dockerfile`, `.dockerignore`, the OCI image plan and scripts, plus `.agents/runtime/tektona-deployment.json`, `.agents/runtime/sandbox.template.tektona.yaml`, `.agents/runtime/deploy-tektona.sh` and `.agents/context/tektona-deployment.md`. The native manifest uses a verified official Tektona Ubuntu/OpenCode base by default; an externally published Dockerfile image remains supported when required. Stateful resources use Tektona processes by default; `compose.yaml` is generated only with proven container-runtime capability. Deployment defaults to a non-mutating plan and requires separate approval plus a version-verified Tektona adapter before template build, tag move or sandbox creation.

Post-init execution modes:

| Mode | Outcome | Required approval |
|---|---|---|
| `plan` | Generate and validate OCI/Tektona artifacts; perform no external write | Harness generation |
| Local OCI build | Build and verify the Dockerfile with Docker, Podman or BuildKit | Separate local-build approval |
| `build-template` | Build an immutable Tektona template version and move its tag after success | Separate Tektona deployment approval |
| `build-and-create-sandbox` | Build the template, wait for success and create a named sandbox | Template-build and sandbox-creation approval |

The recommended Tektona path builds `.agents/runtime/sandbox.template.tektona.yaml` directly on a verified `sandbox-base` release, so it needs no separately published project image. The external OCI path is used when the Dockerfile is authoritative or shared outside Tektona; that image must be published first and private pulls require a Tektona project registry reference.

Generated controls:

```bash
.agents/runtime/build-image.sh                 # approved local OCI build
.agents/runtime/deploy-tektona.sh validate     # no platform write
.agents/runtime/deploy-tektona.sh preview      # resolved deployment summary
.agents/runtime/deploy-tektona.sh apply        # approved template/sandbox writes
```

Approving harness generation never authorizes a local build or Tektona write. `apply` requires a resolved organization/project context, an authenticated and version-verified Tektona CLI, the necessary platform role and an approved deployment plan.
