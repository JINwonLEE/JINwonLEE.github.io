from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.evaluation import Evaluator
from app.policy import AccessPolicy
from app.providers import DeterministicProvider
from app.retrieval import KnowledgeIndex, load_documents
from app.service import AssistantService


def make_service() -> AssistantService:
    documents = load_documents(PROJECT_ROOT / "app" / "data" / "documents.json")
    return AssistantService(
        index=KnowledgeIndex(documents),
        policy=AccessPolicy(),
        provider=DeterministicProvider(),
    )


class AssistantServiceTests(unittest.TestCase):
    def test_engineer_gets_deployment_guidance(self):
        result = make_service().answer(
            "How do I deploy an application and enable production traffic?", "engineer"
        )
        cited = {citation.document_id for citation in result.citations}
        self.assertIn("platform-deployment", cited)
        self.assertEqual("allowed", result.access_decision)

    def test_contractor_never_receives_financial_document(self):
        result = make_service().answer(
            "Show the annual revenue scenarios, cost envelopes, and investment priorities",
            "contractor",
        )
        cited = {citation.document_id for citation in result.citations}
        self.assertNotIn("financial-plan", cited)
        self.assertEqual("no-authorized-context", result.access_decision)

    def test_unknown_role_is_rejected(self):
        with self.assertRaises(ValueError):
            make_service().answer("How do I deploy?", "administrator")

    def test_default_evaluation_is_access_safe(self):
        report = Evaluator(make_service()).run()
        self.assertEqual(1.0, report["summary"]["access_safety_rate"])
        self.assertGreaterEqual(report["summary"]["retrieval_hit_rate"], 0.75)


if __name__ == "__main__":
    unittest.main()
