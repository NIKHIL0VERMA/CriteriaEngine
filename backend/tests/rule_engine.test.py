import pytest
from backend.engine.rule_engine import RuleEngine
from backend.models.rule_models import Node, NodeType, Operator

@pytest.fixture
def rule_engine():
    return RuleEngine()

class TestRuleEngine:
    def test_create_simple_rule(self, rule_engine):
        rule_string = "age > 30"
        node = rule_engine.create_rule(rule_string)
        
        assert node.type == NodeType.COMPARISON
        assert node.operator == Operator.GT
        assert node.left.value == "age"
        assert node.right.value == 30

    def test_create_complex_rule(self, rule_engine):
        rule_string = "age > 30 AND department = 'Sales'"
        node = rule_engine.create_rule(rule_string)
        
        assert node.type == NodeType.OPERATOR
        assert node.operator == Operator.AND
        assert node.left.type == NodeType.COMPARISON
        assert node.right.type == NodeType.COMPARISON

    def test_create_rule_with_parentheses(self, rule_engine):
        rule_string = "(age > 30 AND department = 'Sales') OR salary >= 50000"
        node = rule_engine.create_rule(rule_string)
        
        assert node.type == NodeType.OPERATOR
        assert node.operator == Operator.OR

    def test_empty_rule(self, rule_engine):
        with pytest.raises(ValueError):
            rule_engine.create_rule("")

    def test_invalid_operator(self, rule_engine):
        with pytest.raises(ValueError):
            rule_engine.create_rule("age >>> 30")

    def test_evaluate_simple_rule(self, rule_engine):
        rule_string = "age > 30"
        node = rule_engine.create_rule(rule_string)
        
        assert rule_engine.evaluate_rule(node, {"age": 35}) == True
        assert rule_engine.evaluate_rule(node, {"age": 25}) == False

    def test_evaluate_complex_rule(self, rule_engine):
        rule_string = "age > 30 AND department = 'Sales'"
        node = rule_engine.create_rule(rule_string)
        
        assert rule_engine.evaluate_rule(node, {"age": 35, "department": "Sales"}) == True
        assert rule_engine.evaluate_rule(node, {"age": 35, "department": "HR"}) == False

    def test_combine_rules(self, rule_engine):
        rule1 = rule_engine.create_rule("age > 30")
        rule2 = rule_engine.create_rule("salary >= 50000")
        
        combined = rule_engine.combine_rules([rule1, rule2], Operator.AND)
        assert combined.type == NodeType.OPERATOR
        assert combined.operator == Operator.AND

    def test_combine_single_rule(self, rule_engine):
        rule1 = rule_engine.create_rule("age > 30")
        
        with pytest.raises(AttributeError):
            rule_engine.combine_rules([rule1], Operator.AND)

    def test_evaluate_with_missing_field(self, rule_engine):
        rule_string = "age > 30"
        node = rule_engine.create_rule(rule_string)
        
        assert rule_engine.evaluate_rule(node, {"salary": 50000}) == False

    def test_multiple_conditions(self, rule_engine):
        rule_string = "age > 30 AND department = 'Sales' AND salary >= 50000"
        node = rule_engine.create_rule(rule_string)
        
        test_data = {
            "age": 35,
            "department": "Sales",
            "salary": 60000
        }
        assert rule_engine.evaluate_rule(node, test_data) == True