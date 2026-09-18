import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from uuid import uuid4

@unittest.skipUnless(importlib.util.find_spec("langgraph"), "Runtime dependencies are not installed")
class ApiIntegration(unittest.TestCase):
    def test_reject_cannot_be_approved_later(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "New_Project"))
        from fastapi.testclient import TestClient
        import graph.workflow as workflow
        import api.routes as routes
        with patch.object(workflow, "get_fundamental_data", return_value={"company_name":"Test"}), \
             patch.object(workflow, "get_technical_data", return_value={"current_price":100}), \
             patch.object(workflow, "fundamental_analyst", return_value={"fundamental_analysis":"Fundamental"}), \
             patch.object(workflow, "technical_analyst", return_value={"technical_analysis":"Technical"}), \
             patch.object(workflow, "portfolio_manager", return_value={"final_memo":"Memo"}) as manager:
            routes.graph = workflow.build_graph()
            client = TestClient(routes.app)
            thread = str(uuid4())
            self.assertEqual(client.post("/api/research/start", json={"ticker":"TEST", "thread_id":thread}).status_code, 200)
            self.assertEqual(client.post("/api/research/approve", json={"thread_id":thread,"action":"reject"}).status_code, 200)
            self.assertEqual(client.post("/api/research/approve", json={"thread_id":thread,"action":"approve"}).status_code, 400)
            manager.assert_not_called()
            self.assertEqual(client.post("/api/research/approve", json={"thread_id":thread,"action":"anything"}).status_code, 422)

    def test_invalid_data_returns_error_without_llm(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "New_Project"))
        from fastapi.testclient import TestClient
        import graph.workflow as workflow
        import api.routes as routes
        with patch.object(workflow, "get_fundamental_data", return_value={"error":"Invalid ticker"}), \
             patch.object(workflow, "fundamental_analyst") as analyst:
            routes.graph = workflow.build_graph()
            response = TestClient(routes.app).post("/api/research/start", json={"ticker":"INVALID", "thread_id":str(uuid4())})
            self.assertEqual(response.status_code, 422)
            analyst.assert_not_called()
