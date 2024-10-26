from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

class NodeType(Enum):
    OPERATOR = "OPERATOR"   
    COMPARISON = "COMPARISON"  
    OPERAND = "OPERAND"    

class Operator(Enum):
    AND = "AND"
    OR = "OR"
    GT = ">"
    LT = "<"
    EQ = "="
    GTE = ">="
    LTE = "<="
    NEQ = "!="

class RuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rule_string: str

class RuleCombine(BaseModel):
    rule_ids: List[str]
    name: str
    description: Optional[str] = None
    operator: Operator

class RuleEvaluate(BaseModel):
    rule_id: str
    data: Dict

class RuleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    rule_string: str
    created_at: str
    updated_at: str
    parent_rules: Optional[List[str]] = []


@dataclass
class Node:
    """AST node representation"""
    type: NodeType
    operator: Optional[Operator] = None
    value: Any = None
    attribute: Optional[str] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "value": self.value,
            "operator": self.operator.value if self.operator else None,
            "attribute": self.attribute,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Node':
        node = cls(
            type=NodeType(data["type"]),
            value=data["value"],
            attribute=data["attribute"]
        )
        if data["operator"]:
            node.operator = Operator(data["operator"])
        if data["left"]:
            node.left = cls.from_dict(data["left"])
        if data["right"]:
            node.right = cls.from_dict(data["right"])
        return node



