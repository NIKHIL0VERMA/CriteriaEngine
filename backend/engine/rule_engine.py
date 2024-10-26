from typing import List, Dict, Any
from models.rule_models import Node, NodeType, Operator

class RuleEngine:
    def __init__(self):
        """Initialize the rule engine with comparison operators"""
        self.comparison_ops = {
            '>': lambda x, y: float(x) > float(y),
            '<': lambda x, y: float(x) < float(y),
            '=': lambda x, y: str(x) == str(y),
            '>=': lambda x, y: float(x) >= float(y),
            '<=': lambda x, y: float(x) <= float(y),
            '!=': lambda x, y: str(x) != str(y)
        }

    def create_rule(self, rule_string: str) -> Node:
        """
        Create an AST from a rule string
        Example: "age > 30 AND department = 'Sales'"
        """
        rule_string = rule_string.strip()
        tokens = self._tokenize(rule_string)
        return self._parse_expression(tokens)

    def _tokenize(self, rule_string: str) -> List[str]:
        """Convert rule string into tokens"""
        # Handle parentheses
        rule_string = rule_string.replace('(', ' ( ').replace(')', ' ) ')
        
        # Handle quotes
        tokens = []
        in_quotes = False
        current_token = ''
        
        for char in rule_string:
            if char in ["'", '"']:
                if in_quotes:
                    current_token += char
                    tokens.append(current_token)
                    current_token = ''
                    in_quotes = False
                else:
                    current_token = char
                    in_quotes = True
            elif in_quotes:
                current_token += char
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            else:
                current_token += char
        
        if current_token:
            tokens.append(current_token)
            
        return [t for t in tokens if t.strip()]

    def _parse_expression(self, tokens: List[str]) -> Node:
        """Empty error"""
        if not tokens:
            raise ValueError("Empty rule string")
            
        """Parse tokens into an AST"""
        def precedence(op: str) -> int:
            if op in ['AND']:
                return 2
            if op in ['OR']:
                return 1
            return 0

        output = []
        operators = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(output, operators.pop())
                operators.pop()  # Remove '('
            elif token in ['AND', 'OR']:
                while (operators and operators[-1] != '(' and 
                       precedence(operators[-1]) >= precedence(token)):
                    self._apply_operator(output, operators.pop())
                operators.append(token)
            else:
                # Handle comparison
                if i + 2 < len(tokens):
                    field = token
                    op = tokens[i + 1]
                    value = tokens[i + 2]
                    
                    if op in self.comparison_ops:
                        node = Node(
                            type=NodeType.COMPARISON,
                            operator=Operator(op),
                            left=Node(type=NodeType.OPERAND, value=field),
                            right=Node(type=NodeType.OPERAND, value=self._convert_value(value))
                        )
                        output.append(node)
                        i += 2
                    else:
                        raise ValueError(f"Invalid operator: {op}")
            i += 1

        while operators:
            self._apply_operator(output, operators.pop())

        return output[0]

    def _apply_operator(self, output: List[Node], operator: str) -> None:
        """Apply operator to the output stack"""
        right = output.pop()
        left = output.pop()
        output.append(Node(
            type=NodeType.OPERATOR,
            operator=Operator(operator),
            left=left,
            right=right
        ))

    def _convert_value(self, value: str) -> Any:
        """Convert string value to appropriate type"""
        if value.startswith(("'", '"')):
            return value.strip("'\"")
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def combine_rules(self, nodes: Node, operator: NodeType.OPERATOR) -> Node:
        """
        Combine multiple rules into a single optimized AST
        """
        if not nodes:
            raise ValueError("No rules provided")
        
        if len(nodes) == 1:
            raise AttributeError("Can't combine only one rule")
        
        # Combine with OR
        combined = nodes[0]
        for node in nodes[1:]:
            combined = Node(
                type=NodeType.OPERATOR,
                operator=operator,
                left=combined,
                right=node
            )

        return self._optimize_ast(combined)

    def _optimize_ast(self, node: Node) -> Node:
        """Optimize the AST by removing redundant nodes and combining similar conditions"""
        if not node:
            return node

        # Recursively optimize children
        if node.left:
            node.left = self._optimize_ast(node.left)
        if node.right:
            node.right = self._optimize_ast(node.right)

        # Combine similar conditions
        if node.type == NodeType.OPERATOR:
            if (node.left and node.right and 
                node.left.type == NodeType.COMPARISON and 
                node.right.type == NodeType.COMPARISON):
                # If same field and operator, combine values
                if (node.left.left.value == node.right.left.value and 
                    node.left.operator == node.right.operator):
                    # Combine the conditions based on operator type
                    if node.operator == Operator.OR:
                        return self._combine_conditions(node.left, node.right)

        return node

    def _combine_conditions(self, node1: Node, node2: Node) -> Node:
        """Combine similar conditions when possible"""
        # This is a simple example - can be expanded based on needs
        if node1.operator == Operator.GT:
            return Node(
                type=NodeType.COMPARISON,
                operator=node1.operator,
                left=node1.left,
                right=Node(
                    type=NodeType.OPERAND,
                    value=max(node1.right.value, node2.right.value)
                )
            )
        return node1

    def evaluate_rule(self, node: Node, data: Dict[str, Any]) -> bool:
        """Evaluate a rule against provided data"""
        if not node:
            return False

        if node.type == NodeType.COMPARISON:
            left_val = data.get(node.left.value)
            right_val = node.right.value
            
            if left_val is None:
                return False
                
            return self.comparison_ops[node.operator.value](left_val, right_val)
            
        elif node.type == NodeType.OPERATOR:
            left_result = self.evaluate_rule(node.left, data)
            right_result = self.evaluate_rule(node.right, data)
            
            if node.operator == Operator.AND:
                return left_result and right_result
            elif node.operator == Operator.OR:
                return left_result or right_result
                
        return False

