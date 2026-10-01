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
        self.assertGreaterEqual(len(content_topics), 11)
        self.assertIn(
            "discovery-subject.md", {path.name for path in content_topics}
        )
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
            ".agents/interview/question-bank.md",
            ".agents/interview/inference-rules.md",
            ".agents/interview/scenario-taxonomy.md",
            ".agents/scripts/interview-ranker.py",
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

    def test_installer_preserves_target_readme(self):
        installer = ROOT / "opencode-harness-toolkit-install.sh"
        original = "# Existing Product\n\nProduct-specific evidence.\n"

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            readme = target / "README.md"
            readme.write_text(original)

            subprocess.run(
                [str(installer), str(target)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(readme.read_text(), original)
            self.assertEqual(list(target.glob("README.md.bak.*")), [])

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            subprocess.run(
                [str(installer), str(target)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse((target / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
