import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app
from backend.models.rule_models import RuleCreate, RuleCombine, Operator

client = TestClient(app)

@pytest.fixture
def mock_rule_service():
    return AsyncMock()

class TestRuleRoutes:
    @patch("routes.rule_routes.get_rule_service")
    def test_create_rule(self, mock_get_service, mock_rule_service):
        mock_get_service.return_value = mock_rule_service
        mock_rule_service.create_rule.return_value = {
            "id": "123",
            "ast": {"type": "COMPARISON"}
        }
        
        response = client.post(
            "/api/v1/create/",
            json={
                "name": "Test Rule",
                "description": "Test Description",
                "rule_string": "age > 30"
            }
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert "ast" in response.json()

    @patch("routes.rule_routes.get_rule_service")
    def test_edit_rule(self, mock_get_service, mock_rule_service):
        mock_get_service.return_value = mock_rule_service
        mock_rule_service.edit_rule.return_value = {
            "id": "123",
            "ast": {"type": "COMPARISON"}
        }
        
        response = client.patch(
            "/api/v1/edit/123",
            json={
                "name": "Updated Rule",
                "description": "Updated Description",
                "rule_string": "age > 35"
            }
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert "ast" in response.json()

    @patch("routes.rule_routes.get_rule_service")
    def test_combine_rules(self, mock_get_service, mock_rule_service):
        mock_get_service.return_value = mock_rule_service
        mock_rule_service.combine_rules.return_value = {
            "id": "123",
            "name": "Combined Rule",
            "ast": {"type": "OPERATOR"}
        }
        
        response = client.post(
            "/api/v1/combine/",
            json={
                "rule_ids": ["123", "456"],
                "name": "Combined Rule",
                "description": "Combined Description",
                "operator": "AND"
            }
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert "ast" in response.json()

    @patch("routes.rule_routes.get_rule_service")
    def test_evaluate_rule(self, mock_get_service, mock_rule_service):
        mock_get_service.return_value = mock_rule_service
        mock_rule_service.evaluate_rule.return_value = {
            "result": True,
            "rule_name": "Test Rule",
            "rule_string": "age > 30"
        }
        
        response = client.post(
            "/api/v1/evaluate/",
            json={
                "rule_id": "123",
                "data": {"age": 35}
            }
        )
        
        assert response.status_code == 200
        assert "result" in response.json()
        assert "rule_name" in response.json()

    @patch("routes.rule_routes.get_rule_service")
    def test_get_rule(self, mock_get_service, mock_rule_service):
        mock_get_service.return_value = mock_rule_service
        mock_rule_service.get_rule.return_value = {
            "id": "123",
            "name": "Test Rule",
            "rule_string": "age > 30"
        }
        
        response = client.get("/api/v1/rule/123")
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert "name" in response.json()

    @patch("routes.rule_routes.get_rule_service")
    def test_list_rules(self, mock_get_service, mock_rule_service):
        mock_get_service.return_value = mock_rule_service
        mock_rule_service.get_rules.return_value = {
            "rules": [
                {
                    "id": "123",
                    "name": "Test Rule",
                    "rule_string": "age > 30"
                }
            ],
            "total": 1,
            "page": 1,
            "pages": 1
        }
        
        response = client.get("/api/v1/fetch/")
        
        assert response.status_code == 200
        assert "rules" in response.json()
        assert "total" in response.json()
        assert "page" in response.json()