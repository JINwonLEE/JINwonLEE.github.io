"""Guard the verified claims shared by the website and public PDFs."""

import json
import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_TOOLS = ("Terraform", "Ansible")
STABLE_CVS = (
    "CV-Eng.pdf",
    "CV-Platform-SRE.pdf",
    "CV-Applied-AI.pdf",
    "CV-Kor.pdf",
)
DATED_CVS = (
    "output/pdf/Jinwon-Lee-CV-Master-2026-09.pdf",
    "output/pdf/Jinwon-Lee-CV-Platform-SRE-2026-09.pdf",
    "output/pdf/Jinwon-Lee-CV-Applied-AI-2026-09.pdf",
    "output/pdf/Jinwon-Lee-CV-Kor-2026-09.pdf",
)


def pdf_text(path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


class PublicClaimsTest(unittest.TestCase):
    def test_project_configs_use_bash_for_cluster_provisioning(self):
        for filename in ("portfolio-config.json", "portfolio-config-ko.json"):
            data = json.loads((ROOT / filename).read_text(encoding="utf-8"))
            project = next(
                project
                for project in data["projects"]
                if project["image"].endswith("thumb-k8s-automation.svg")
            )
            self.assertEqual(["Kubernetes", "Bash"], project["technologies"])
            serialized = json.dumps(project)
            self.assertNotIn("Python", serialized)
            for tool in EXCLUDED_TOOLS:
                self.assertNotIn(tool, serialized)

    def test_stable_and_dated_cvs_are_two_page_ats_readable_documents(self):
        for relative_path in (*STABLE_CVS, *DATED_CVS):
            path = ROOT / relative_path
            with self.subTest(pdf=relative_path):
                reader = PdfReader(path)
                self.assertEqual(2, len(reader.pages))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                self.assertIn("Convergence Aware CNN Training", text)
                self.assertIn("Bash", text)
                self.assertNotIn("Target Fit", text)
                for tool in EXCLUDED_TOOLS:
                    self.assertNotIn(tool, text)

    def test_public_portfolio_pdfs_use_current_claims(self):
        for filename in ("Portfolio-Eng.pdf", "Portfolio-Kor.pdf"):
            text = pdf_text(ROOT / filename)
            with self.subTest(pdf=filename):
                self.assertIn("130,000", text)
                self.assertIn("Bash", text)
                self.assertIn("Enterprise AI Assistant", text)
                for tool in EXCLUDED_TOOLS:
                    self.assertNotIn(tool, text)

    def test_public_html_uses_stable_cv_links_and_no_removed_tool_claims(self):
        combined = "\n".join(
            (ROOT / filename).read_text(encoding="utf-8")
            for filename in ("index.html", "index-ko.html")
        )
        for filename in STABLE_CVS:
            self.assertIn(filename, combined)
        for tool in EXCLUDED_TOOLS:
            self.assertNotIn(tool, combined)
        self.assertIn("Bash-based one-click Kubernetes", combined)
        self.assertIn("Bash 기반 원클릭 Kubernetes", combined)


if __name__ == "__main__":
    unittest.main()
