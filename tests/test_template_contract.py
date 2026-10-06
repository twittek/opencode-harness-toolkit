#!/usr/bin/env python3

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template"


class TemplateContractTest(unittest.TestCase):
    def test_harness_init_is_not_a_fixed_questionnaire(self):
        command = (TEMPLATE / ".opencode/command/harness-init.md").read_text()
        self.assertIn("maximum `QuestionValue`", command)
        self.assertIn("No fixed first question", command)
        self.assertIn("## Phase 0: Resolve the discovery subject", command)
        self.assertIn("This is not a mandatory first question", command)
        self.assertNotIn("Ask questions in this order", command)
        self.assertNotIn("Start with this exact first question", command)
        self.assertNotIn("## Adaptive interview flow", command)

    def test_topic_catalog_is_modular(self):
        topics = sorted((TEMPLATE / ".agents/interview/topics").glob("*.md"))
        content_topics = [path for path in topics if path.name != "README.md"]
        self.assertGreaterEqual(len(content_topics), 13)
        self.assertIn(
            "discovery-subject.md", {path.name for path in content_topics}
        )
        self.assertIn(
            "compliance-observability.md", {path.name for path in content_topics}
        )
        self.assertIn("runtime-image.md", {path.name for path in content_topics})
        ids = []
        for topic in content_topics:
            content = topic.read_text()
            self.assertTrue(content.startswith("---\n"), topic.name)
            self.assertIn("\nid:", content, topic.name)
            self.assertIn("\ndimensions:", content, topic.name)
            ids.append(
                next(
                    line.split(":", 1)[1].strip()
                    for line in content.splitlines()
                    if line.startswith("id:")
                )
            )
        self.assertEqual(len(ids), len(set(ids)))

        catalog = (TEMPLATE / ".agents/interview/topic-catalog.md").read_text()
        references = set(re.findall(r"`(topics/[^`]+\.md)`", catalog))
        self.assertEqual(len(references), len(topics))
        for reference in references:
            self.assertTrue((TEMPLATE / ".agents/interview" / reference).is_file(), reference)

    def test_all_lifecycle_commands_remain_registered(self):
        config = json.loads((TEMPLATE / "opencode.jsonc").read_text())
        commands = config["command"]
        self.assertEqual(
            set(commands),
            {
                "harness-init",
                "harness-check",
                "harness-update",
                "harness-retro",
                "harness-mcp",
            },
        )

    def test_interview_resources_exist(self):
        required = [
            ".agents/interview/interview-engine.md",
            ".agents/interview/interview-state-schema.md",
            ".agents/interview/topic-catalog.md",
            ".agents/interview/role-catalog.md",
            ".agents/interview/question-bank.md",
            ".agents/interview/inference-rules.md",
            ".agents/interview/scenario-taxonomy.md",
            ".agents/scripts/interview-ranker.py",
            ".agents/policies/policy-contract.md",
            ".agents/policies/policy-registry.schema.json",
            ".agents/policies/task-evidence.schema.json",
            ".agents/policies/evaluation-result.schema.json",
            ".agents/scripts/policy-evaluator.py",
            ".agents/runtime/image-contract.md",
            ".agents/runtime/image-plan.schema.json",
            ".agents/runtime/tektona-contract.md",
            ".agents/runtime/tektona-deployment.schema.json",
            ".agents/scripts/image-plan-validator.py",
        ]
        for relative in required:
            self.assertTrue((TEMPLATE / relative).is_file(), relative)

    def test_discovery_subject_separates_product_and_harness_evidence(self):
        engine = (TEMPLATE / ".agents/interview/interview-engine.md").read_text()
        state = (TEMPLATE / ".agents/interview/interview-state-schema.md").read_text()
        self.assertIn("## Discovery subject boundary", engine)
        self.assertIn("harness/control evidence", engine)
        self.assertIn("toolkit/package evidence", engine)
        self.assertIn('"discoverySubject": "missing|partial|sufficient"', state)

    def test_role_selection_is_confirmed_and_generated_selectively(self):
        command = (TEMPLATE / ".opencode/command/harness-init.md").read_text()
        state = (TEMPLATE / ".agents/interview/interview-state-schema.md").read_text()
        catalog = (TEMPLATE / ".agents/interview/role-catalog.md").read_text()
        bootstrap_agents = (TEMPLATE / "AGENTS.md").read_text()
        check = (TEMPLATE / ".opencode/command/harness-check.md").read_text()

        self.assertIn("Generate exactly the confirmed roles", command)
        self.assertIn("Do not copy the generic toolkit role files verbatim", command)
        self.assertIn("## AGENTS.md generation", command)
        self.assertIn('"roleSelection": {', state)
        self.assertIn('"status": "unknown|proposed|confirmed"', state)
        self.assertIn("It is not a list of roles that must all be installed", catalog)
        self.assertTrue(bootstrap_agents.startswith("<!-- harness-bootstrap: true -->"))
        self.assertIn("Treat stale bootstrap instructions", check)

    def test_policy_generation_is_machine_evaluable(self):
        command = (TEMPLATE / ".opencode/command/harness-init.md").read_text()
        contract = (TEMPLATE / ".agents/policies/policy-contract.md").read_text()
        check = (TEMPLATE / ".opencode/command/harness-check.md").read_text()

        self.assertIn("## Policy and compliance generation", command)
        self.assertIn("The JSON registry is the normative source", command)
        self.assertIn("UNKNOWN", contract)
        self.assertIn("NOT_APPLICABLE", contract)
        self.assertIn("violationScore", contract)
        self.assertIn("minimumCoverage", contract)
        self.assertIn("## Policy evaluability checks", check)

        json.loads(
            (TEMPLATE / ".agents/policies/policy-registry.schema.json").read_text()
        )
        json.loads(
            (TEMPLATE / ".agents/policies/task-evidence.schema.json").read_text()
        )
        json.loads(
            (TEMPLATE / ".agents/policies/evaluation-result.schema.json").read_text()
        )

    def test_runtime_image_generation_is_evidence_driven_and_safe(self):
        command = (TEMPLATE / ".opencode/command/harness-init.md").read_text()
        contract = (TEMPLATE / ".agents/runtime/image-contract.md").read_text()
        check = (TEMPLATE / ".opencode/command/harness-check.md").read_text()

        self.assertIn("## Runtime image generation", command)
        self.assertIn("ARG UBUNTU_BASE_IMAGE=ubuntu:latest", command)
        self.assertIn("OpenCode as a mandatory", command)
        self.assertIn("only when the approved summary explicitly permits", command)
        self.assertIn("# harness-layer: rust-toolchain", contract)
        self.assertIn("stateful development resource", contract)
        self.assertIn(".agents/runtime/compose.yaml", contract)
        self.assertIn("rootless-in-microvm", contract)
        self.assertIn("Every runtime installation must record", contract)
        self.assertIn("Tektona process management", contract)
        self.assertIn("capabilityEvidenceRefs", contract)
        self.assertIn("tektona-deployment.json", command)
        self.assertIn("sandbox.template.tektona.yaml", command)
        self.assertIn("Never invent a command", command)
        self.assertIn("## OCI runtime image checks", check)
        json.loads(
            (TEMPLATE / ".agents/runtime/image-plan.schema.json").read_text()
        )
        json.loads(
            (TEMPLATE / ".agents/runtime/tektona-deployment.schema.json").read_text()
        )

    def test_documentation_explains_post_init_runtime_modes(self):
        readme = (ROOT / "README.md").read_text()
        template_readme = (TEMPLATE / "README.md").read_text()
        website = (ROOT / "harness-toolkit.html").read_text()

        for content in (readme, template_readme, website):
            self.assertIn("build-template", content)
            self.assertIn("build-and-create-sandbox", content)
            self.assertIn("Local OCI build", content)
        self.assertIn("What can happen directly after `/harness-init`", readme)
        self.assertIn("deploy-tektona.sh apply", readme)
        self.assertIn("What can happen directly after", website)

    def test_public_documentation_matches_current_command_and_mcp_contract(self):
        readme = (ROOT / "README.md").read_text()
        template_readme = (TEMPLATE / "README.md").read_text()
        bootstrap_agents = (TEMPLATE / "AGENTS.md").read_text()
        website = (ROOT / "harness-toolkit.html").read_text()
        commands = (
            "/harness-init",
            "/harness-check",
            "/harness-update",
            "/harness-retro",
            "/harness-mcp",
        )

        for command in commands:
            self.assertIn(command, readme)
            self.assertIn(command, website)
        for content in (readme, template_readme, bootstrap_agents, website):
            self.assertIn("chrome-devtools", content)
            self.assertNotIn(".agents/skills/gitlab-glab.md", content)
        self.assertIn("Five focused commands", website)
        self.assertIn("compliance observability", readme)
        self.assertIn("Tektona is an optional execution target", website)

    def test_installer_preserves_target_readme(self):
        installer = ROOT / "opencode-harness-toolkit-install.sh"
        original = "# Existing Product\n\nProduct-specific evidence.\n"

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            readme = target / "README.md"
            agents = target / "AGENTS.md"
            existing_agents = "# Existing Agent Rules\n\nKeep this requirement.\n"
            readme.write_text(original)
            agents.write_text(existing_agents)

            subprocess.run(
                [str(installer), str(target)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(readme.read_text(), original)
            self.assertEqual(list(target.glob("README.md.bak.*")), [])
            self.assertEqual(agents.read_text(), existing_agents)
            self.assertEqual(list(target.glob("AGENTS.md.bak.*")), [])

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            subprocess.run(
                [str(installer), str(target)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse((target / "README.md").exists())
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue(
                (target / ".agents/interview/role-catalog.md").is_file()
            )
            self.assertTrue(
                (target / ".agents/context/self-verification-policy.md").is_file()
            )
            self.assertTrue(
                (target / ".agents/policies/policy-contract.md").is_file()
            )
            self.assertTrue(
                (target / ".agents/policies/task-evidence.schema.json").is_file()
            )
            self.assertTrue(
                (target / ".agents/scripts/policy-evaluator.py").is_file()
            )
            self.assertTrue(
                (target / ".agents/runtime/image-contract.md").is_file()
            )
            self.assertTrue(
                (target / ".agents/runtime/image-plan.schema.json").is_file()
            )
            self.assertTrue(
                (target / ".agents/runtime/tektona-contract.md").is_file()
            )
            self.assertTrue(
                (target / ".agents/runtime/tektona-deployment.schema.json").is_file()
            )
            self.assertTrue(
                (target / ".agents/scripts/image-plan-validator.py").is_file()
            )
            self.assertFalse((target / "Dockerfile").exists())
            self.assertFalse(
                (target / ".agents/runtime/image-plan.json").exists()
            )
            self.assertFalse(
                (target / ".agents/runtime/tektona-deployment.json").exists()
            )
            self.assertFalse(
                (target / ".agents/runtime/sandbox.template.tektona.yaml").exists()
            )
            self.assertFalse(
                (target / ".agents/policies/policy-registry.json").exists()
            )
            self.assertEqual(
                list((target / ".agents/roles").glob("*.md")), []
            )
            self.assertFalse(
                (target / ".agents/context/role-activation-policy.md").exists()
            )
            self.assertFalse((target / ".agents/integrations").exists())


if __name__ == "__main__":
    unittest.main()
