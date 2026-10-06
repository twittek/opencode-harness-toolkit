#!/usr/bin/env python3
"""Validate an agent image plan and its generated Dockerfile.

This standard-library validator complements image-plan.schema.json with semantic
checks that are awkward to express in JSON Schema, especially cross-references
between services, layers and Dockerfile markers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


LAYER_ID = re.compile(r"^[a-z0-9][a-z0-9-]+$")
DIGEST = re.compile(r"^sha256:[a-f0-9]{64}$")
PLATFORMS = {"linux/amd64", "linux/arm64"}
CATEGORIES = {
    "baseline",
    "sandbox-runtime",
    "toolchain",
    "build-tool",
    "database-client",
    "integration-client",
    "project-utility",
    "sandbox-service",
    "embedded-service",
}
SECRET_PATTERN = re.compile(
    r"(?i)(password|passwd|api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[^\s$<{]+"
)
CURL_PIPE_SHELL = re.compile(r"(?i)\bcurl\b[^\n|]*\|\s*(?:ba)?sh\b")
CREDENTIAL_URI = re.compile(r"://[^/@:\s]+:[^/@\s]+@")
LAYER_MARKER = re.compile(r"^\s*#\s*harness-layer:\s*([a-z0-9][a-z0-9-]+)\s*$", re.MULTILINE)


class ValidationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def _object(value: Any, name: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{name} must be an object")
    return value


def _array(value: Any, name: str) -> list[Any]:
    _require(isinstance(value, list), f"{name} must be an array")
    return value


def _string(value: Any, name: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{name} must be a non-empty string")
    return value


def _exact_keys(value: dict[str, Any], required: set[str], name: str) -> None:
    missing = required - value.keys()
    extra = value.keys() - required
    _require(not missing, f"{name} is missing keys: {', '.join(sorted(missing))}")
    _require(not extra, f"{name} has unsupported keys: {', '.join(sorted(extra))}")


def validate_plan(plan: Any) -> None:
    root = _object(plan, "plan")
    _exact_keys(
        root,
        {"schemaVersion", "planVersion", "subject", "deploymentTargets", "base", "agent", "layers", "services", "sandbox", "security", "build"},
        "plan",
    )
    _require(root["schemaVersion"] == "1.2", "schemaVersion must be 1.2")
    _require(isinstance(root["planVersion"], int) and root["planVersion"] >= 1, "planVersion must be an integer >= 1")
    _string(root["subject"], "subject")
    deployment_targets = _array(root["deploymentTargets"], "deploymentTargets")
    _require(bool(deployment_targets), "deploymentTargets must not be empty")
    _require(set(deployment_targets) <= {"tektona", "portable-oci"}, "deploymentTargets contains an unsupported target")
    _require(len(deployment_targets) == len(set(deployment_targets)), "deploymentTargets must be unique")
    _require("tektona" in deployment_targets, "deploymentTargets must include tektona")

    base = _object(root["base"], "base")
    _exact_keys(base, {"reference", "updatePolicy", "resolvedDigest"}, "base")
    reference = _string(base["reference"], "base.reference")
    _require(bool(re.fullmatch(r"ubuntu:[A-Za-z0-9._-]+(?:@sha256:[a-f0-9]{64})?", reference)), "base.reference must use an official ubuntu tag")
    _require(base["updatePolicy"] in {"current-lts-with-lock", "pinned-digest"}, "base.updatePolicy is invalid")
    if base["resolvedDigest"] is not None:
        _require(isinstance(base["resolvedDigest"], str) and bool(DIGEST.fullmatch(base["resolvedDigest"])), "base.resolvedDigest is invalid")

    agent = _object(root["agent"], "agent")
    _exact_keys(agent, {"name", "required", "distribution", "version", "installMethod", "verifyCommand"}, "agent")
    _require(agent["name"] == "opencode", "agent.name must be opencode")
    _require(agent["required"] is True, "OpenCode must be required")
    _string(agent["version"], "agent.version")
    _require(agent["installMethod"] in {"npm", "verified-binary"}, "agent.installMethod is invalid")
    expected_distribution = "@opencode/cli" if agent["installMethod"] == "npm" else "official-opencode-binary"
    _require(agent["distribution"] == expected_distribution, f"agent.distribution must be {expected_distribution} for {agent['installMethod']}")
    _require(agent["verifyCommand"] == "opencode --version", "agent.verifyCommand must be opencode --version")

    layers = _array(root["layers"], "layers")
    layer_ids: set[str] = set()
    for index, raw_layer in enumerate(layers):
        name = f"layers[{index}]"
        layer = _object(raw_layer, name)
        _exact_keys(layer, {"id", "category", "reason", "evidenceRefs", "version", "install", "verifyCommands"}, name)
        layer_id = _string(layer["id"], f"{name}.id")
        _require(bool(LAYER_ID.fullmatch(layer_id)), f"{name}.id is invalid")
        _require(layer_id not in layer_ids, f"duplicate layer id: {layer_id}")
        layer_ids.add(layer_id)
        _require(layer["category"] in CATEGORIES, f"{name}.category is invalid")
        _string(layer["reason"], f"{name}.reason")
        evidence = _array(layer["evidenceRefs"], f"{name}.evidenceRefs")
        _require(bool(evidence) and all(isinstance(item, str) and item.strip() for item in evidence), f"{name}.evidenceRefs must contain evidence")
        _require(len(evidence) == len(set(evidence)), f"{name}.evidenceRefs must be unique")
        _string(layer["version"], f"{name}.version")
        install = _object(layer["install"], f"{name}.install")
        _exact_keys(install, {"strategy", "packages", "commands", "sources"}, f"{name}.install")
        _require(install["strategy"] in {"apt", "signed-repository", "verified-archive", "language-manager", "custom-approved"}, f"{name}.install.strategy is invalid")
        packages = _array(install["packages"], f"{name}.install.packages")
        commands = _array(install["commands"], f"{name}.install.commands")
        _array(install["sources"], f"{name}.install.sources")
        _require(all(isinstance(item, str) and item.strip() for item in packages + commands), f"{name} install entries must be non-empty strings")
        for command in commands:
            _require(not CURL_PIPE_SHELL.search(command), f"{name} contains an unverified curl-to-shell installer")
            _require(not SECRET_PATTERN.search(command), f"{name} appears to contain secret material")
        verify = _array(layer["verifyCommands"], f"{name}.verifyCommands")
        _require(bool(verify) and all(isinstance(item, str) and item.strip() for item in verify), f"{name}.verifyCommands must not be empty")

        for source_index, raw_source in enumerate(install["sources"]):
            source_name = f"{name}.install.sources[{source_index}]"
            source = _object(raw_source, source_name)
            _exact_keys(source, {"url", "integrity"}, source_name)
            _require(_string(source["url"], f"{source_name}.url").startswith("https://"), f"{source_name}.url must use HTTPS")
            _string(source["integrity"], f"{source_name}.integrity")

    baseline_layers = [layer for layer in layers if layer["category"] == "baseline"]
    _require(len(baseline_layers) == 1, "the image plan must contain exactly one baseline layer")
    _require(layers and layers[0]["category"] == "baseline", "the baseline layer must be first")
    category_order = {
        "baseline": 0,
        "sandbox-runtime": 1,
        "toolchain": 2,
        "build-tool": 2,
        "database-client": 3,
        "integration-client": 3,
        "project-utility": 4,
        "sandbox-service": 5,
        "embedded-service": 6,
    }
    orders = [category_order[layer["category"]] for layer in layers]
    _require(orders == sorted(orders), "image-plan layers are not in stable category order")

    services = _array(root["services"], "services")
    service_ids: set[str] = set()
    for index, raw_service in enumerate(services):
        name = f"services[{index}]"
        service = _object(raw_service, name)
        _exact_keys(service, {"id", "kind", "mode", "image", "reason", "clientLayerId", "runtimeLayerId", "composeFile", "serviceName", "processName", "healthCheck", "agentEndpoint"}, name)
        service_id = _string(service["id"], f"{name}.id")
        _require(bool(LAYER_ID.fullmatch(service_id)), f"{name}.id is invalid")
        _require(service_id not in service_ids, f"duplicate service id: {service_id}")
        service_ids.add(service_id)
        _require(service["kind"] in {"database", "cache", "queue", "search", "object-storage", "other"}, f"{name}.kind is invalid")
        _require(service["mode"] in {"tektona-process", "sandbox-compose", "platform-service", "embedded"}, f"{name}.mode is invalid")
        _require(service["image"] is None or isinstance(service["image"], str), f"{name}.image must be a string or null")
        _string(service["reason"], f"{name}.reason")
        client_layer = service["clientLayerId"]
        _require(client_layer is None or client_layer in layer_ids, f"{name}.clientLayerId does not reference a declared layer")
        runtime_layer = service["runtimeLayerId"]
        _require(runtime_layer is None or runtime_layer in layer_ids, f"{name}.runtimeLayerId does not reference a declared layer")
        compose_file = service["composeFile"]
        service_name = service["serviceName"]
        process_name = service["processName"]
        health_check = service["healthCheck"]
        agent_endpoint = service["agentEndpoint"]
        _require(compose_file is None or isinstance(compose_file, str), f"{name}.composeFile must be a string or null")
        _require(service_name is None or isinstance(service_name, str), f"{name}.serviceName must be a string or null")
        _require(process_name is None or isinstance(process_name, str), f"{name}.processName must be a string or null")
        _require(health_check is None or isinstance(health_check, str), f"{name}.healthCheck must be a string or null")
        _require(agent_endpoint is None or isinstance(agent_endpoint, str), f"{name}.agentEndpoint must be a string or null")
        if service["mode"] == "embedded":
            _require(runtime_layer is not None, f"embedded service {service_id} requires runtimeLayerId referencing an embedded-service layer")
            _require(any(layer["id"] == runtime_layer and layer["category"] == "embedded-service" for layer in layers), f"embedded service {service_id} requires a referenced embedded-service layer")
            _require(compose_file is None and service_name is None and process_name is None, f"embedded service {service_id} must not declare external lifecycle routing")
        elif service["mode"] == "tektona-process":
            _require(runtime_layer is not None, f"tektona-process service {service_id} requires runtimeLayerId")
            _require(any(layer["id"] == runtime_layer and layer["category"] == "sandbox-service" for layer in layers), f"tektona-process service {service_id} requires a referenced sandbox-service layer")
            _require(compose_file is None and service_name is None and service["image"] is None, f"tektona-process service {service_id} must not declare container routing")
            _string(process_name, f"{name}.processName")
            _string(health_check, f"{name}.healthCheck")
            _string(agent_endpoint, f"{name}.agentEndpoint")
            _require(not SECRET_PATTERN.search(agent_endpoint), f"{name}.agentEndpoint must not contain credentials")
            _require(not CREDENTIAL_URI.search(agent_endpoint), f"{name}.agentEndpoint must not contain URI credentials")
        elif service["mode"] == "sandbox-compose":
            _require(runtime_layer is None, f"sandbox-compose service {service_id} must not have runtimeLayerId")
            _require(compose_file == ".agents/runtime/compose.yaml", f"sandbox-compose service {service_id} must use .agents/runtime/compose.yaml")
            _string(service_name, f"{name}.serviceName")
            _require(process_name is None, f"sandbox-compose service {service_id} must not declare a Tektona process")
            _string(health_check, f"{name}.healthCheck")
            _string(service["image"], f"{name}.image")
            _string(agent_endpoint, f"{name}.agentEndpoint")
            _require(not SECRET_PATTERN.search(agent_endpoint), f"{name}.agentEndpoint must not contain credentials")
            _require(not CREDENTIAL_URI.search(agent_endpoint), f"{name}.agentEndpoint must not contain URI credentials")
        else:
            _require(runtime_layer is None, f"platform service {service_id} must not have runtimeLayerId")
            _require(compose_file is None and service_name is None and process_name is None, f"platform service {service_id} must not declare local lifecycle routing")

    sandbox = _object(root["sandbox"], "sandbox")
    _exact_keys(sandbox, {"autonomyGoal", "networkAccess", "dynamicInstall", "containerRuntime"}, "sandbox")
    _require(sandbox["autonomyGoal"] == "self-contained-product-development", "sandbox.autonomyGoal is invalid")
    _require(sandbox["networkAccess"] in {"allowed", "restricted", "denied"}, "sandbox.networkAccess is invalid")
    dynamic_install = _object(sandbox["dynamicInstall"], "sandbox.dynamicInstall")
    _exact_keys(dynamic_install, {"mode", "allowedSources", "requireIntegrityEvidence", "recordChanges", "privilegeEscalationApproved"}, "sandbox.dynamicInstall")
    _require(dynamic_install["mode"] in {"disabled", "user-local", "sandbox-root"}, "sandbox.dynamicInstall.mode is invalid")
    sources = _array(dynamic_install["allowedSources"], "sandbox.dynamicInstall.allowedSources")
    _require(all(isinstance(source, str) and source.strip() for source in sources), "sandbox.dynamicInstall.allowedSources contains an invalid value")
    _require(len(sources) == len(set(sources)), "sandbox.dynamicInstall.allowedSources must be unique")
    _require(dynamic_install["requireIntegrityEvidence"] is True, "runtime installation must require integrity evidence")
    _require(dynamic_install["recordChanges"] is True, "runtime installations must be recorded")
    _require(isinstance(dynamic_install["privilegeEscalationApproved"], bool), "sandbox.dynamicInstall.privilegeEscalationApproved must be boolean")
    if dynamic_install["mode"] == "sandbox-root":
        _require(dynamic_install["privilegeEscalationApproved"] is True, "sandbox-root installation requires explicit privilege escalation approval")
    else:
        _require(dynamic_install["privilegeEscalationApproved"] is False, "privilege escalation approval must be false unless sandbox-root mode is selected")
    if sandbox["networkAccess"] == "denied":
        _require(dynamic_install["mode"] == "disabled", "dynamic installation must be disabled when network access is denied")
    container_runtime = _object(sandbox["containerRuntime"], "sandbox.containerRuntime")
    _exact_keys(container_runtime, {"required", "mode", "compose", "verifyCommand", "capabilityEvidenceRefs"}, "sandbox.containerRuntime")
    _require(isinstance(container_runtime["required"], bool), "sandbox.containerRuntime.required must be boolean")
    _require(container_runtime["mode"] in {"platform-daemon", "rootless-in-microvm", "none"}, "sandbox.containerRuntime.mode is invalid")
    _require(isinstance(container_runtime["compose"], bool), "sandbox.containerRuntime.compose must be boolean")
    _require(container_runtime["verifyCommand"] is None or isinstance(container_runtime["verifyCommand"], str), "sandbox.containerRuntime.verifyCommand must be a string or null")
    capability_evidence = _array(container_runtime["capabilityEvidenceRefs"], "sandbox.containerRuntime.capabilityEvidenceRefs")
    _require(all(isinstance(item, str) and item.strip() for item in capability_evidence), "sandbox.containerRuntime.capabilityEvidenceRefs contains an invalid value")
    _require(len(capability_evidence) == len(set(capability_evidence)), "sandbox.containerRuntime.capabilityEvidenceRefs must be unique")
    compose_services = [service for service in services if service["mode"] == "sandbox-compose"]
    if compose_services:
        _require(container_runtime["required"] is True, "sandbox-compose services require a container runtime")
        _require(container_runtime["mode"] != "none", "sandbox-compose services require an executable container runtime mode")
        _require(container_runtime["compose"] is True, "sandbox-compose services require Compose")
        _string(container_runtime["verifyCommand"], "sandbox.containerRuntime.verifyCommand")
        _require(bool(capability_evidence), "sandbox-compose services require container-runtime capability evidence")
        _require(any(layer["category"] == "sandbox-runtime" for layer in layers), "sandbox-compose services require a sandbox-runtime layer")
    elif container_runtime["mode"] == "none":
        _require(container_runtime["required"] is False and container_runtime["compose"] is False, "container runtime mode none must not be required or enable Compose")
        _require(not capability_evidence, "container runtime mode none must not claim capability evidence")

    security = _object(root["security"], "security")
    _exact_keys(security, {"runAsNonRoot", "copyProjectIntoImage", "allowBuildSecrets"}, "security")
    _require(security == {"runAsNonRoot": True, "copyProjectIntoImage": False, "allowBuildSecrets": False}, "security settings must enforce non-root, no project copy and no build secrets")

    build = _object(root["build"], "build")
    _exact_keys(build, {"mode", "engine", "context", "dockerfile", "imageRef", "pull", "platforms", "localBuildApproved"}, "build")
    _require(build["mode"] in {"sandbox", "local", "both"}, "build.mode is invalid")
    _require(build["engine"] in {"auto", "docker", "podman", "buildkit"}, "build.engine is invalid")
    _require(build["context"] == "." and build["dockerfile"] == "Dockerfile", "build paths must use the repository root")
    _string(build["imageRef"], "build.imageRef")
    _require(build["pull"] is True, "build.pull must be true")
    platforms = _array(build["platforms"], "build.platforms")
    _require(bool(platforms) and set(platforms) <= PLATFORMS and len(platforms) == len(set(platforms)), "build.platforms is empty, duplicated or unsupported")
    _require(isinstance(build["localBuildApproved"], bool), "build.localBuildApproved must be boolean")
    if build["mode"] in {"local", "both"}:
        _require(build["localBuildApproved"] is True, "local or both build mode requires explicit localBuildApproved")


def validate_dockerfile(plan: Any, dockerfile: str) -> None:
    validate_plan(plan)
    _require(bool(re.search(r"^ARG\s+UBUNTU_BASE_IMAGE=ubuntu:[^\s]+\s*$", dockerfile, re.MULTILINE)), "Dockerfile must declare the Ubuntu base argument")
    _require(bool(re.search(r"^FROM\s+\$\{UBUNTU_BASE_IMAGE\}(?:\s|$)", dockerfile, re.MULTILINE)), "Dockerfile must use UBUNTU_BASE_IMAGE in FROM")
    _require("opencode --version" in dockerfile, "Dockerfile must verify OpenCode")
    if plan["agent"]["installMethod"] == "npm":
        _require("@opencode/cli" in dockerfile, "Dockerfile must install the declared OpenCode npm distribution")
    else:
        _require("official-opencode-binary" in dockerfile or "OPENCODE_" in dockerfile, "Dockerfile must document the verified official OpenCode binary installation")
    _require(bool(re.search(r"^USER\s+agent\s*$", dockerfile, re.MULTILINE)), "Dockerfile must end in the non-root agent user")
    _require(bool(re.search(r"^WORKDIR\s+/workspace\s*$", dockerfile, re.MULTILINE)), "Dockerfile must use /workspace")
    _require(bool(re.search(r"^ENV\s+HOME=/workspace\s*$", dockerfile, re.MULTILINE)), "Dockerfile must align HOME with /workspace for Tektona sessions")
    _require(not re.search(r"^\s*(?:COPY|ADD)\s+\.\s", dockerfile, re.MULTILINE), "Dockerfile must not copy the project into the image")
    _require(not re.search(r"^\s*(?:CMD|ENTRYPOINT)\s+.*\bopencode\b", dockerfile, re.MULTILINE | re.IGNORECASE), "Dockerfile must not auto-start interactive OpenCode at Tektona sandbox boot")
    _require(not CURL_PIPE_SHELL.search(dockerfile), "Dockerfile contains an unverified curl-to-shell installer")
    _require(not SECRET_PATTERN.search(dockerfile), "Dockerfile appears to contain secret material")
    markers = LAYER_MARKER.findall(dockerfile)
    declared = [layer["id"] for layer in plan["layers"]]
    _require(len(markers) == len(set(markers)), "Dockerfile contains duplicate harness-layer markers")
    _require(markers == declared, f"Dockerfile layer markers do not match image-plan order: declared={declared}, markers={markers}")


def _nullable_reference(value: Any, name: str) -> None:
    _require(value is None or (isinstance(value, str) and bool(value.strip())), f"{name} must be a non-empty string or null")
    if isinstance(value, str):
        _require(not SECRET_PATTERN.search(value), f"{name} appears to contain secret material")
        _require(not CREDENTIAL_URI.search(value), f"{name} must not contain URI credentials")


def validate_tektona_manifest(deployment: Any, image_plan: Any, manifest: str) -> None:
    """Apply conservative structural checks without depending on a YAML package."""
    _require(bool(re.search(r"^apiVersion:\s*tektona\.ai/v1\s*$", manifest, re.MULTILINE)), "Tektona manifest apiVersion must be tektona.ai/v1")
    _require(bool(re.search(r"^kind:\s*SandboxTemplate\s*$", manifest, re.MULTILINE)), "Tektona manifest kind must be SandboxTemplate")
    template_name = re.escape(deployment["template"]["name"])
    _require(bool(re.search(rf"^\s{{2}}name:\s*{template_name}\s*$", manifest, re.MULTILINE)), "Tektona manifest metadata.name must match the deployment plan")
    base_image = re.escape(deployment["build"]["baseImage"])
    _require(bool(re.search(rf"^\s{{4}}image:\s*{base_image}\s*$", manifest, re.MULTILINE)), "Tektona manifest build image must match the deployment plan")
    _require(bool(re.search(r"^\s{4}user:\s*root\s*$", manifest, re.MULTILINE)), "Tektona manifest build steps must use root for package installation")
    _require(bool(re.search(r"^\s{2}sandbox:\s*$", manifest, re.MULTILINE)), "Tektona manifest must declare sandbox defaults")
    if deployment["build"]["strategy"] == "native-manifest":
        _require(bool(re.search(r"^\s{4}user:\s*tektona\s*$", manifest, re.MULTILINE)), "Tektona official base must use the tektona sandbox user")
        _require(bool(re.search(r"^\s{4}workdir:\s*/home/tektona\s*$", manifest, re.MULTILINE)), "Tektona official base must align sandbox workdir with the tektona home")
    else:
        _require(bool(re.search(r"^\s{4}user:\s*agent\s*$", manifest, re.MULTILINE)), "external OCI image must use its declared non-root agent user")
        _require(bool(re.search(r"^\s{4}workdir:\s*/workspace\s*$", manifest, re.MULTILINE)), "external OCI image must align sandbox workdir with /workspace")
    _require("opencode --version" in manifest, "Tektona manifest must verify OpenCode")
    _require(not CURL_PIPE_SHELL.search(manifest), "Tektona manifest contains an unverified curl-to-shell installer")
    _require(not SECRET_PATTERN.search(manifest), "Tektona manifest appears to contain secret material")
    markers = LAYER_MARKER.findall(manifest)
    declared = [layer["id"] for layer in image_plan["layers"]]
    _require(len(markers) == len(set(markers)), "Tektona manifest contains duplicate harness-layer markers")
    _require(markers == declared, f"Tektona manifest layer markers do not match image-plan order: declared={declared}, markers={markers}")


def validate_tektona(deployment: Any, image_plan: Any, manifest: str) -> None:
    """Validate the normalized Tektona handoff and its image-plan relationship."""
    validate_plan(image_plan)
    root = _object(deployment, "tektona deployment")
    _exact_keys(
        root,
        {"schemaVersion", "platform", "subject", "scope", "organization", "project", "template", "build", "sandbox", "integrations", "deployment"},
        "tektona deployment",
    )
    _require(root["schemaVersion"] == "1.0", "Tektona schemaVersion must be 1.0")
    _require(root["platform"] == "tektona", "platform must be tektona")
    _require(_string(root["subject"], "subject") == image_plan["subject"], "Tektona subject must match image-plan subject")
    _require(root["scope"] in {"project", "organization"}, "scope must be project or organization")
    _string(root["organization"], "organization")
    if root["scope"] == "project":
        _string(root["project"], "project")
    else:
        _require(root["project"] is None, "organization-scoped deployment must set project to null")

    template = _object(root["template"], "template")
    _exact_keys(template, {"name", "reference", "displayName", "description", "tag", "lifecyclePolicy"}, "template")
    name = _string(template["name"], "template.name")
    _require(bool(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", name)), "template.name is invalid")
    expected_prefix = "project/" if root["scope"] == "project" else "org/"
    _require(template["reference"] == f"{expected_prefix}{name}", "template.reference does not match scope and name")
    _string(template["displayName"], "template.displayName")
    _string(template["description"], "template.description")
    _require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", _string(template["tag"], "template.tag"))), "template.tag is invalid")
    _require(template["lifecyclePolicy"] in {"inherited", "project", "organization"}, "template.lifecyclePolicy is invalid")

    build = _object(root["build"], "build")
    _exact_keys(build, {"provider", "strategy", "manifest", "dockerfile", "context", "imagePlan", "baseImage", "resultImageRef", "resultImageVisibility", "asynchronous", "waitForCompletion", "tagOnSuccess", "localValidationOptional"}, "build")
    _require(build["provider"] == "tektona-template-build", "build.provider must be tektona-template-build")
    _require(build["strategy"] in {"native-manifest", "external-oci-image"}, "build.strategy is invalid")
    _require(build["manifest"] == ".agents/runtime/sandbox.template.tektona.yaml", "build.manifest is invalid")
    _require(build["dockerfile"] == "Dockerfile" and build["context"] == ".", "Tektona build paths must use the repository root")
    _require(build["imagePlan"] == ".agents/runtime/image-plan.json", "build.imagePlan is invalid")
    base_image = _string(build["baseImage"], "build.baseImage")
    _require(not CREDENTIAL_URI.search(base_image), "build.baseImage must not contain registry credentials")
    _nullable_reference(build["resultImageRef"], "build.resultImageRef")
    if build["strategy"] == "native-manifest":
        _require(bool(re.fullmatch(r"ghcr\.io/tektona-ai/(?:sandbox-base|desktop-x11):[0-9]+\.[0-9]+\.[0-9]+", base_image)), "native-manifest must use a verified X.Y.Z official Tektona base image")
        _require(build["resultImageRef"] is None, "native-manifest does not require an externally published result image")
        _require(build["resultImageVisibility"] == "not-applicable", "native-manifest result image visibility must be not-applicable")
    else:
        _string(build["resultImageRef"], "build.resultImageRef")
        _require(":" in build["resultImageRef"] or "@sha256:" in build["resultImageRef"], "external-oci-image requires a tagged or digested result image reference")
        _require(base_image == build["resultImageRef"], "external-oci-image manifest base must equal resultImageRef")
        _require(build["resultImageVisibility"] in {"public", "private"}, "external-oci-image visibility must be public or private")
    _require(build["asynchronous"] is True and build["tagOnSuccess"] is True and build["localValidationOptional"] is True, "Tektona build invariants are invalid")
    _require(isinstance(build["waitForCompletion"], bool), "build.waitForCompletion must be boolean")

    sandbox = _object(root["sandbox"], "sandbox")
    _exact_keys(sandbox, {"createAfterBuild", "name", "repositoryRef", "resources", "lifecycle", "processes"}, "sandbox")
    _require(isinstance(sandbox["createAfterBuild"], bool), "sandbox.createAfterBuild must be boolean")
    _nullable_reference(sandbox["name"], "sandbox.name")
    if sandbox["name"] is not None:
        _require(bool(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", sandbox["name"])), "sandbox.name is invalid")
    _nullable_reference(sandbox["repositoryRef"], "sandbox.repositoryRef")
    resources = _object(sandbox["resources"], "sandbox.resources")
    _exact_keys(resources, {"cpu", "memoryMiB", "diskGiB", "location"}, "sandbox.resources")
    _require(resources["cpu"] is None or (isinstance(resources["cpu"], (int, float)) and not isinstance(resources["cpu"], bool) and resources["cpu"] > 0), "sandbox.resources.cpu must be positive or null")
    _require(resources["memoryMiB"] is None or (isinstance(resources["memoryMiB"], int) and resources["memoryMiB"] >= 256), "sandbox.resources.memoryMiB must be >= 256 or null")
    _require(resources["diskGiB"] is None or (isinstance(resources["diskGiB"], int) and resources["diskGiB"] >= 1), "sandbox.resources.diskGiB must be >= 1 or null")
    _nullable_reference(resources["location"], "sandbox.resources.location")
    lifecycle = _object(sandbox["lifecycle"], "sandbox.lifecycle")
    _exact_keys(lifecycle, {"autoPauseMinutes", "autoDeleteHours"}, "sandbox.lifecycle")
    _require(lifecycle["autoPauseMinutes"] is None or (isinstance(lifecycle["autoPauseMinutes"], int) and lifecycle["autoPauseMinutes"] >= 0), "sandbox.lifecycle.autoPauseMinutes is invalid")
    _require(lifecycle["autoDeleteHours"] is None or (isinstance(lifecycle["autoDeleteHours"], int) and lifecycle["autoDeleteHours"] >= 1), "sandbox.lifecycle.autoDeleteHours is invalid")
    process_names: set[str] = set()
    for index, raw_process in enumerate(_array(sandbox["processes"], "sandbox.processes")):
        process_name = f"sandbox.processes[{index}]"
        process = _object(raw_process, process_name)
        _exact_keys(process, {"name", "command", "workingDirectory", "autostart", "waitForPort"}, process_name)
        name_value = _string(process["name"], f"{process_name}.name")
        _require(bool(LAYER_ID.fullmatch(name_value)), f"{process_name}.name is invalid")
        _require(name_value not in process_names, f"duplicate Tektona process name: {name_value}")
        process_names.add(name_value)
        command = _string(process["command"], f"{process_name}.command")
        _require(not SECRET_PATTERN.search(command), f"{process_name}.command appears to contain secret material")
        _require(process["workingDirectory"] == "repository-root", f"{process_name}.workingDirectory must be repository-root")
        _require(isinstance(process["autostart"], bool), f"{process_name}.autostart must be boolean")
        _require(process["waitForPort"] is None or (isinstance(process["waitForPort"], int) and 1 <= process["waitForPort"] <= 65535), f"{process_name}.waitForPort is invalid")

    expected_processes = {service["processName"] for service in image_plan["services"] if service["mode"] == "tektona-process"}
    _require(expected_processes <= process_names, "every tektona-process service must have a matching Tektona process definition")

    integrations = _object(root["integrations"], "integrations")
    _exact_keys(integrations, {"gitCredentialRef", "containerRegistryRef", "egressNetworkPolicyRef", "egressProxyProfileRef", "secretRefs"}, "integrations")
    for key in {"gitCredentialRef", "containerRegistryRef", "egressNetworkPolicyRef", "egressProxyProfileRef"}:
        _nullable_reference(integrations[key], f"integrations.{key}")
    if build["strategy"] == "external-oci-image" and build["resultImageVisibility"] == "private":
        _string(integrations["containerRegistryRef"], "integrations.containerRegistryRef")
    secret_refs = _array(integrations["secretRefs"], "integrations.secretRefs")
    _require(all(isinstance(item, str) and item.strip() for item in secret_refs), "integrations.secretRefs contains an invalid value")
    _require(len(secret_refs) == len(set(secret_refs)), "integrations.secretRefs must be unique")
    _require(all(not SECRET_PATTERN.search(item) and not CREDENTIAL_URI.search(item) for item in secret_refs), "integrations.secretRefs must contain references, never values")

    deployment_state = _object(root["deployment"], "deployment")
    _exact_keys(deployment_state, {"mode", "approved", "adapter", "adapterPath", "verifiedAgainst", "interfaceEvidenceRefs"}, "deployment")
    _require(deployment_state["mode"] in {"plan", "build-template", "build-and-create-sandbox"}, "deployment.mode is invalid")
    _require(isinstance(deployment_state["approved"], bool), "deployment.approved must be boolean")
    _require(deployment_state["adapter"] in {"unresolved", "cli", "sdk", "api"}, "deployment.adapter is invalid")
    _nullable_reference(deployment_state["adapterPath"], "deployment.adapterPath")
    _nullable_reference(deployment_state["verifiedAgainst"], "deployment.verifiedAgainst")
    evidence = _array(deployment_state["interfaceEvidenceRefs"], "deployment.interfaceEvidenceRefs")
    _require(all(isinstance(item, str) and item.strip() for item in evidence), "deployment.interfaceEvidenceRefs contains an invalid value")
    _require(len(evidence) == len(set(evidence)), "deployment.interfaceEvidenceRefs must be unique")

    if deployment_state["mode"] == "plan":
        _require(deployment_state["approved"] is False, "plan mode must not claim deployment approval")
        _require(sandbox["createAfterBuild"] is False, "plan mode must not create a sandbox")
    else:
        _require(deployment_state["approved"] is True, "mutating Tektona deployment requires explicit approval")
        _require(deployment_state["adapter"] != "unresolved", "mutating Tektona deployment requires a resolved adapter")
        _string(deployment_state["adapterPath"], "deployment.adapterPath")
        _string(deployment_state["verifiedAgainst"], "deployment.verifiedAgainst")
        _require(bool(evidence), "mutating Tektona deployment requires interface evidence")
        _require(build["waitForCompletion"] is True, "mutating Tektona deployment must wait for the asynchronous build")
    if deployment_state["mode"] == "build-and-create-sandbox":
        _require(sandbox["createAfterBuild"] is True, "build-and-create-sandbox mode must enable sandbox creation")
        _string(sandbox["name"], "sandbox.name")
    else:
        _require(sandbox["createAfterBuild"] is False, "sandbox creation is only valid in build-and-create-sandbox mode")
    validate_tektona_manifest(root, image_plan, manifest)


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"cannot read valid JSON from {path}: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan_parser = subparsers.add_parser("validate-plan")
    plan_parser.add_argument("plan", type=Path)
    docker_parser = subparsers.add_parser("validate-dockerfile")
    docker_parser.add_argument("plan", type=Path)
    docker_parser.add_argument("dockerfile", type=Path)
    tektona_parser = subparsers.add_parser("validate-tektona")
    tektona_parser.add_argument("deployment", type=Path)
    tektona_parser.add_argument("plan", type=Path)
    tektona_parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        plan = _load_json(args.plan)
        if args.command == "validate-plan":
            validate_plan(plan)
        elif args.command == "validate-dockerfile":
            validate_dockerfile(plan, args.dockerfile.read_text())
        else:
            validate_tektona(_load_json(args.deployment), plan, args.manifest.read_text())
    except (OSError, ValidationError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
