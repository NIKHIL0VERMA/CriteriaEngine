import pytest
from backend.models.rule_models import Node, NodeType, Operator, RuleCreate, RuleCombine, RuleResponse
from pydantic import ValidationError

class TestRuleModels:
    def test_node_creation(self):
        node = Node(
            type=NodeType.COMPARISON,
            operator=Operator.GT,
            left=Node(type=NodeType.OPERAND, value="age"),
            right=Node(type=NodeType.OPERAND, value=30)
        )
        
        assert node.type == NodeType.COMPARISON
        assert node.operator == Operator.GT
        assert node.left.value == "age"
        assert node.right.value == 30

    def test_node_to_dict(self):
        node = Node(
            type=NodeType.COMPARISON,
            operator=Operator.GT,
            left=Node(type=NodeType.OPERAND, value="age"),
            right=Node(type=NodeType.OPERAND, value=30)
        )
        
        node_dict = node.to_dict()
        assert node_dict["type"] == NodeType.COMPARISON.value
        assert node_dict["operator"] == Operator.GT.value
        assert node_dict["left"]["value"] == "age"
        assert node_dict["right"]["value"] == 30

    def test_node_from_dict(self):
        node_dict = {
            "type": "COMPARISON",
            "operator": ">",
            "value": None,
            "attribute": None,
            "left": {
                "type": "OPERAND",
                "operator": None,
                "value": "age",
                "attribute": None,
                "left": None,
                "right": None
            },
            "right": {
                "type": "OPERAND",
                "operator": None,
                "value": 30,
                "attribute": None,
                "left": None,
                "right": None
            }
        }
        
        node = Node.from_dict(node_dict)
        assert node.type == NodeType.COMPARISON
        assert node.operator == Operator.GT
        assert node.left.value == "age"
        assert node.right.value == 30

    def test_rule_create_validation(self):
        # Valid rule creation
        rule = RuleCreate(
            name="Test Rule",
            description="Test Description",
            rule_string="age > 30"
        )
        assert rule.name == "Test Rule"
        assert rule.description == "Test Description"
        assert rule.rule_string == "age > 30"

        # Invalid rule creation - missing required field
        with pytest.raises(ValidationError):
            RuleCreate(
                description="Test Description",
                rule_string="age > 30"
            )

    def test_rule_combine_validation(self):
        # Valid rule combination
        rule_combine = RuleCombine(
            rule_ids=["123", "456"],
            name="Combined Rule",
            description="Combined Description",
            operator=Operator.AND
        )
        assert len(rule_combine.rule_ids) == 2
        assert rule_combine.operator == Operator.AND

        # Invalid rule combination - empty rule_ids
        with pytest.raises(ValidationError):
            RuleCombine(
                rule_ids=[],
                name="Combined Rule",
                operator=Operator.AND
            )

    def test_rule_response_model(self):
        # Valid rule response
        response = RuleResponse(
            id="123",
            name="Test Rule",
            description="Test Description",
            rule_string="age > 30",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
            parent_rules=["456", "789"]
        )
        assert response.id == "123"
        assert len(response.parent_rules) == 2

        # Optional fields
        response = RuleResponse(
            id="123",
            name="Test Rule",
            rule_string="age > 30",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00"
        )
        assert response.description is None
        assert response.parent_rules == []