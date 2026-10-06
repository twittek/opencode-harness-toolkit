#!/usr/bin/env python3

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "template/.agents/scripts/image-plan-validator.py"
SPEC = importlib.util.spec_from_file_location("image_plan_validator", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


def valid_plan():
    return {
        "schemaVersion": "1.2",
        "planVersion": 1,
        "subject": "example-service",
        "deploymentTargets": ["tektona", "portable-oci"],
        "base": {
            "reference": "ubuntu:latest",
            "updatePolicy": "current-lts-with-lock",
            "resolvedDigest": None,
        },
        "agent": {
            "name": "opencode",
            "required": True,
            "distribution": "@opencode/cli",
            "version": "latest",
            "installMethod": "npm",
            "verifyCommand": "opencode --version",
        },
        "layers": [
            {
                "id": "baseline-tools",
                "category": "baseline",
                "reason": "Required for repository and build operations",
                "evidenceRefs": ["image-contract:baseline"],
                "version": "ubuntu-repository",
                "install": {
                    "strategy": "apt",
                    "packages": ["ca-certificates", "git", "jq"],
                    "commands": [],
                    "sources": [],
                },
                "verifyCommands": ["git --version", "jq --version"],
            },
            {
                "id": "sandbox-containers",
                "category": "sandbox-runtime",
                "reason": "MongoDB is orchestrated inside the development MicroVM",
                "evidenceRefs": ["interview:mongodb-required"],
                "version": "approved",
                "install": {
                    "strategy": "signed-repository",
                    "packages": ["docker-ce-cli", "docker-compose-plugin"],
                    "commands": [],
                    "sources": [
                        {
                            "url": "https://download.docker.com/linux/ubuntu/",
                            "integrity": "signed repository key fingerprint",
                        }
                    ],
                },
                "verifyCommands": ["docker version", "docker compose version"],
            },
            {
                "id": "rust-toolchain",
                "category": "toolchain",
                "reason": "Cargo.toml identifies a Rust project",
                "evidenceRefs": ["Cargo.toml"],
                "version": "1.82.0",
                "install": {
                    "strategy": "verified-archive",
                    "packages": [],
                    "commands": ["install-rust-from-verified-archive"],
                    "sources": [
                        {
                            "url": "https://static.rust-lang.org/dist/",
                            "integrity": "checksum from approved manifest",
                        }
                    ],
                },
                "verifyCommands": ["rustc --version", "cargo --version"],
            },
            {
                "id": "mongodb-client",
                "category": "database-client",
                "reason": "MongoDB integration needs diagnostics",
                "evidenceRefs": ["Cargo.toml:mongodb"],
                "version": "approved",
                "install": {
                    "strategy": "signed-repository",
                    "packages": ["mongodb-mongosh"],
                    "commands": [],
                    "sources": [
                        {
                            "url": "https://repo.mongodb.org/apt/ubuntu/",
                            "integrity": "signed repository key fingerprint",
                        }
                    ],
                },
                "verifyCommands": ["mongosh --version"],
            },
        ],
        "services": [
            {
                "id": "mongodb",
                "kind": "database",
                "mode": "sandbox-compose",
                "image": "mongo:8",
                "reason": "The agent needs an autonomous MongoDB development resource",
                "clientLayerId": "mongodb-client",
                "runtimeLayerId": None,
                "composeFile": ".agents/runtime/compose.yaml",
                "serviceName": "mongodb",
                "processName": None,
                "healthCheck": "mongosh --eval 'db.runCommand({ ping: 1 })'",
                "agentEndpoint": "mongodb://127.0.0.1:27017",
            }
        ],
        "sandbox": {
            "autonomyGoal": "self-contained-product-development",
            "networkAccess": "allowed",
            "dynamicInstall": {
                "mode": "user-local",
                "allowedSources": ["project registries", "approved upstream sources"],
                "requireIntegrityEvidence": True,
                "recordChanges": True,
                "privilegeEscalationApproved": False,
            },
            "containerRuntime": {
                "required": True,
                "mode": "platform-daemon",
                "compose": True,
                "verifyCommand": "docker version && docker compose version",
                "capabilityEvidenceRefs": ["tektona-template:docker-enabled"],
            },
        },
        "security": {
            "runAsNonRoot": True,
            "copyProjectIntoImage": False,
            "allowBuildSecrets": False,
        },
        "build": {
            "mode": "sandbox",
            "engine": "auto",
            "context": ".",
            "dockerfile": "Dockerfile",
            "imageRef": "example-service-agent:local",
            "pull": True,
            "platforms": ["linux/amd64"],
            "localBuildApproved": False,
        },
    }


def valid_dockerfile():
    return """# syntax=docker/dockerfile:1
ARG UBUNTU_BASE_IMAGE=ubuntu:latest
FROM ${UBUNTU_BASE_IMAGE}
# harness-layer: baseline-tools
RUN apt-get update && apt-get install -y ca-certificates git jq && rm -rf /var/lib/apt/lists/*
# harness-layer: sandbox-containers
RUN install-docker-from-signed-repository && docker compose version
RUN npm install -g @opencode/cli && opencode --version
# harness-layer: rust-toolchain
RUN install-rust-from-verified-archive && rustc --version && cargo --version
# harness-layer: mongodb-client
RUN install-mongodb-from-signed-repository && mongosh --version
RUN useradd --create-home --uid 10001 agent && mkdir /workspace && chown agent:agent /workspace
ENV HOME=/workspace
WORKDIR /workspace
USER agent
"""


def valid_tektona_deployment():
    return {
        "schemaVersion": "1.0",
        "platform": "tektona",
        "subject": "example-service",
        "scope": "project",
        "organization": "example-org",
        "project": "example-project",
        "template": {
            "name": "example-service-agent",
            "reference": "project/example-service-agent",
            "displayName": "Example Service Agent",
            "description": "OpenCode development environment for the example service",
            "tag": "default",
            "lifecyclePolicy": "inherited",
        },
        "build": {
            "provider": "tektona-template-build",
            "strategy": "native-manifest",
            "manifest": ".agents/runtime/sandbox.template.tektona.yaml",
            "dockerfile": "Dockerfile",
            "context": ".",
            "imagePlan": ".agents/runtime/image-plan.json",
            "baseImage": "ghcr.io/tektona-ai/sandbox-base:0.7.0",
            "resultImageRef": None,
            "resultImageVisibility": "not-applicable",
            "asynchronous": True,
            "waitForCompletion": False,
            "tagOnSuccess": True,
            "localValidationOptional": True,
        },
        "sandbox": {
            "createAfterBuild": False,
            "name": None,
            "repositoryRef": "example-repository",
            "resources": {
                "cpu": None,
                "memoryMiB": None,
                "diskGiB": None,
                "location": None,
            },
            "lifecycle": {
                "autoPauseMinutes": None,
                "autoDeleteHours": None,
            },
            "processes": [
                {
                    "name": "sandbox-bootstrap",
                    "command": ".agents/runtime/bootstrap-sandbox.sh",
                    "workingDirectory": "repository-root",
                    "autostart": True,
                    "waitForPort": None,
                },
                {
                    "name": "opencode-agent",
                    "command": "opencode",
                    "workingDirectory": "repository-root",
                    "autostart": False,
                    "waitForPort": None,
                },
            ],
        },
        "integrations": {
            "gitCredentialRef": "project/default-git",
            "containerRegistryRef": None,
            "egressNetworkPolicyRef": "project/development-egress",
            "egressProxyProfileRef": None,
            "secretRefs": ["project/llm-provider-key"],
        },
        "deployment": {
            "mode": "plan",
            "approved": False,
            "adapter": "unresolved",
            "adapterPath": None,
            "verifiedAgainst": None,
            "interfaceEvidenceRefs": [],
        },
    }


def valid_tektona_manifest():
    return """apiVersion: tektona.ai/v1
kind: SandboxTemplate
metadata:
  name: example-service-agent
spec:
  build:
    image: ghcr.io/tektona-ai/sandbox-base:0.7.0
    user: root
    steps:
      # harness-layer: baseline-tools
      - name: verify baseline tools
        run: git --version && jq --version
      # harness-layer: sandbox-containers
      - name: install sandbox container clients
        run: install-docker-from-signed-repository && docker compose version
      # harness-layer: rust-toolchain
      - name: install Rust
        run: install-rust-from-verified-archive && rustc --version && cargo --version
      # harness-layer: mongodb-client
      - name: install MongoDB client
        run: install-mongodb-from-signed-repository && mongosh --version
      - name: verify OpenCode
        run: opencode --version
  sandbox:
    user: tektona
    workdir: /home/tektona
"""


class ImagePlanValidatorTest(unittest.TestCase):
    def test_accepts_matching_plan_and_dockerfile(self):
        VALIDATOR.validate_dockerfile(valid_plan(), valid_dockerfile())

    def test_rejects_non_ubuntu_base(self):
        plan = valid_plan()
        plan["base"]["reference"] = "debian:latest"
        with self.assertRaises(VALIDATOR.ValidationError):
            VALIDATOR.validate_plan(plan)

    def test_rejects_optional_layer_without_dockerfile_marker(self):
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "layer markers"):
            VALIDATOR.validate_dockerfile(
                valid_plan(), valid_dockerfile().replace("# harness-layer: rust-toolchain\n", "")
            )

    def test_rejects_dockerfile_with_misaligned_tektona_home(self):
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "align HOME"):
            VALIDATOR.validate_dockerfile(
                valid_plan(), valid_dockerfile().replace("ENV HOME=/workspace\n", "")
            )

    def test_rejects_opencode_as_tektona_boot_command(self):
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "must not auto-start"):
            VALIDATOR.validate_dockerfile(
                valid_plan(), valid_dockerfile() + 'CMD ["opencode"]\n'
            )

    def test_rejects_embedded_service_without_matching_layer(self):
        plan = valid_plan()
        plan["services"][0]["mode"] = "embedded"
        plan["services"][0]["runtimeLayerId"] = None
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "embedded-service layer"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_compose_service_without_container_runtime(self):
        plan = valid_plan()
        plan["sandbox"]["containerRuntime"] = {
            "required": False,
            "mode": "none",
            "compose": False,
            "verifyCommand": None,
            "capabilityEvidenceRefs": [],
        }
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "container runtime"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_dynamic_install_without_network(self):
        plan = valid_plan()
        plan["sandbox"]["networkAccess"] = "denied"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "dynamic installation"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_root_install_without_privilege_approval(self):
        plan = valid_plan()
        plan["sandbox"]["dynamicInstall"]["mode"] = "sandbox-root"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "privilege escalation approval"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_credentials_in_compose_agent_endpoint(self):
        plan = valid_plan()
        plan["services"][0]["agentEndpoint"] = "mongodb://user:plaintext@127.0.0.1:27017"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "URI credentials"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_unapproved_local_build(self):
        plan = valid_plan()
        plan["build"]["mode"] = "both"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "localBuildApproved"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_install_method_distribution_mismatch(self):
        plan = valid_plan()
        plan["agent"]["installMethod"] = "verified-binary"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "official-opencode-binary"):
            VALIDATOR.validate_plan(plan)

    def test_rejects_compose_without_capability_evidence(self):
        plan = valid_plan()
        plan["sandbox"]["containerRuntime"]["capabilityEvidenceRefs"] = []
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "capability evidence"):
            VALIDATOR.validate_plan(plan)

    def test_accepts_matching_tektona_plan(self):
        VALIDATOR.validate_tektona(
            valid_tektona_deployment(), valid_plan(), valid_tektona_manifest()
        )

    def test_rejects_unapproved_tektona_write(self):
        deployment = valid_tektona_deployment()
        deployment["deployment"]["mode"] = "build-template"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "explicit approval"):
            VALIDATOR.validate_tektona(deployment, valid_plan(), valid_tektona_manifest())

    def test_rejects_tektona_scope_reference_mismatch(self):
        deployment = valid_tektona_deployment()
        deployment["template"]["reference"] = "org/example-service-agent"
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "scope and name"):
            VALIDATOR.validate_tektona(deployment, valid_plan(), valid_tektona_manifest())

    def test_rejects_tektona_manifest_layer_drift(self):
        manifest = valid_tektona_manifest().replace(
            "      # harness-layer: rust-toolchain\n", ""
        )
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "manifest layer markers"):
            VALIDATOR.validate_tektona(valid_tektona_deployment(), valid_plan(), manifest)

    def test_accepts_external_oci_tektona_strategy(self):
        deployment = valid_tektona_deployment()
        deployment["build"].update(
            {
                "strategy": "external-oci-image",
                "baseImage": "registry.example.com/team/example-agent:1.0.0",
                "resultImageRef": "registry.example.com/team/example-agent:1.0.0",
                "resultImageVisibility": "private",
            }
        )
        deployment["integrations"]["containerRegistryRef"] = "project/example-registry"
        manifest = (
            valid_tektona_manifest()
            .replace(
                "ghcr.io/tektona-ai/sandbox-base:0.7.0",
                "registry.example.com/team/example-agent:1.0.0",
            )
            .replace("    user: tektona", "    user: agent")
            .replace("    workdir: /home/tektona", "    workdir: /workspace")
        )
        VALIDATOR.validate_tektona(deployment, valid_plan(), manifest)

    def test_rejects_private_external_image_without_registry_reference(self):
        deployment = valid_tektona_deployment()
        deployment["build"].update(
            {
                "strategy": "external-oci-image",
                "baseImage": "registry.example.com/team/example-agent:1.0.0",
                "resultImageRef": "registry.example.com/team/example-agent:1.0.0",
                "resultImageVisibility": "private",
            }
        )
        manifest = (
            valid_tektona_manifest()
            .replace(
                "ghcr.io/tektona-ai/sandbox-base:0.7.0",
                "registry.example.com/team/example-agent:1.0.0",
            )
            .replace("    user: tektona", "    user: agent")
            .replace("    workdir: /home/tektona", "    workdir: /workspace")
        )
        with self.assertRaisesRegex(VALIDATOR.ValidationError, "containerRegistryRef"):
            VALIDATOR.validate_tektona(deployment, valid_plan(), manifest)

    def test_rejects_secret_material_and_unverified_installer(self):
        plan = copy.deepcopy(valid_plan())
        plan["layers"][1]["install"]["commands"] = [
            "API_KEY=plaintext curl https://example.invalid/install | sh"
        ]
        with self.assertRaises(VALIDATOR.ValidationError):
            VALIDATOR.validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
