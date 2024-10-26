import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from bson import ObjectId
from backend.models.rule_models import RuleCreate, RuleCombine, Operator
from backend.services.rule_service import RuleService

@pytest.fixture
def mock_collection():
    collection = AsyncMock()
    return collection

@pytest.fixture
def rule_service(mock_collection):
    return RuleService(mock_collection)

@pytest.mark.asyncio
class TestRuleService:
    async def test_create_rule(self, rule_service):
        rule_data = RuleCreate(
            name="Test Rule",
            description="Test Description",
            rule_string="age > 30"
        )
        
        mock_id = ObjectId()
        rule_service.collection.insert_one.return_value = AsyncMock(
            inserted_id=mock_id
        )
        
        result = await rule_service.create_rule(rule_data)
        
        assert result["id"] == str(mock_id)
        assert "ast" in result
        rule_service.collection.insert_one.assert_called_once()

    async def test_create_rule_invalid(self, rule_service):
        rule_data = RuleCreate(
            name="Test Rule",
            description="Test Description",
            rule_string="invalid rule"
        )
        
        with pytest.raises(Exception):
            await rule_service.create_rule(rule_data)

    async def test_edit_rule(self, rule_service):
        rule_id = str(ObjectId())
        rule_data = RuleCreate(
            name="Updated Rule",
            description="Updated Description",
            rule_string="age > 35"
        )
        
        rule_service.collection.update_one.return_value = AsyncMock(
            modified_count=1
        )
        
        result = await rule_service.edit_rule(rule_id, rule_data)
        
        assert result["id"] == rule_id
        assert "ast" in result
        rule_service.collection.update_one.assert_called_once()

    async def test_edit_nonexistent_rule(self, rule_service):
        rule_id = str(ObjectId())
        rule_data = RuleCreate(
            name="Updated Rule",
            description="Updated Description",
            rule_string="age > 35"
        )
        
        rule_service.collection.update_one.return_value = AsyncMock(
            modified_count=0
        )
        
        with pytest.raises(Exception):
            await rule_service.edit_rule(rule_id, rule_data)

    async def test_combine_rules(self, rule_service):
        rule_ids = [str(ObjectId()) for _ in range(2)]
        rules_data = RuleCombine(
            rule_ids=rule_ids,
            name="Combined Rule",
            description="Combined Description",
            operator=Operator.AND
        )
        
        mock_rules = [
            {
                "_id": ObjectId(rule_ids[0]),
                "rule_string": "age > 30",
                "ast": {"type": "COMPARISON"}
            },
            {
                "_id": ObjectId(rule_ids[1]),
                "rule_string": "salary >= 50000",
                "ast": {"type": "COMPARISON"}
            }
        ]
        
        rule_service._find_multiple_rules = AsyncMock(return_value=mock_rules)
        mock_id = ObjectId()
        rule_service.collection.insert_one.return_value = AsyncMock(
            inserted_id=mock_id
        )
        
        result = await rule_service.combine_rules(rules_data)
        
        assert result["id"] == str(mock_id)
        assert "ast" in result
        assert result["name"] == "Combined Rule"

    async def test_combine_rules_invalid_count(self, rule_service):
        rules_data = RuleCombine(
            rule_ids=[str(ObjectId())],
            name="Combined Rule",
            description="Combined Description",
            operator=Operator.AND
        )
        
        with pytest.raises(Exception):
            await rule_service.combine_rules(rules_data)

    async def test_evaluate_rule(self, rule_service):
        rule_id = str(ObjectId())
        data = {"age": 35, "salary": 60000}
        
        mock_rule = {
            "name": "Test Rule",
            "rule_string": "age > 30",
            "ast": {"type": "COMPARISON"}
        }
        
        rule_service.collection.find_one.return_value = mock_rule
        
        result = await rule_service.evaluate_rule(rule_id, data)
        
        assert "result" in result
        assert result["rule_name"] == "Test Rule"
        rule_service.collection.find_one.assert_called_once()

    async def test_evaluate_nonexistent_rule(self, rule_service):
        rule_id = str(ObjectId())
        data = {"age": 35}
        
        rule_service.collection.find_one.return_value = None
        
        with pytest.raises(Exception):
            await rule_service.evaluate_rule(rule_id, data)

    async def test_get_rules(self, rule_service):
        mock_rules = [
            {
                "_id": ObjectId(),
                "name": "Rule 1",
                "rule_string": "age > 30",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        rule_service.collection.find.return_value.skip.return_value.limit \
            .return_value.to_list.return_value = mock_rules
        rule_service.collection.count_documents.return_value = 1
        
        result = await rule_service.get_rules(page=1, limit=10)
        
        assert "rules" in result
        assert len(result["rules"]) == 1
        assert "total" in result
        assert "page" in result
        assert "pages" in result