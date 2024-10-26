from typing import List, Dict, Optional, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException

from models.rule_models import RuleCreate, RuleCombine, Node, Operator
from engine.rule_engine import RuleEngine

class RuleService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
        self.rule_engine = RuleEngine()

    async def create_rule(self, rule: RuleCreate) -> Dict[str, Any]:
        """Create a new rule"""
        try:
            # Validate and create AST
            ast = self.rule_engine.create_rule(rule.rule_string)
            
            # Prepare document
            rule_doc = {
                "name": rule.name,
                "description": rule.description,
                "rule_string": rule.rule_string,
                "ast": ast.to_dict(),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await self.collection.insert_one(rule_doc)
            return {
                "id": str(result.inserted_id),
                "ast": ast.to_dict()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def edit_rule(self, rule_id: str, rule: RuleCreate) -> Dict[str, Any]:
        """Edit an existing rule"""
        try:
            ast = self.rule_engine.create_rule(rule.rule_string)
            
            rule_doc = {
                "name": rule.name,
                "description": rule.description,
                "rule_string": rule.rule_string,
                "ast": ast.to_dict(),
                "updated_at": datetime.utcnow()
            }
            
            result = await self.collection.update_one(
                {"_id": ObjectId(rule_id)}, 
                {"$set": rule_doc}
            )
            
            if result.modified_count == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="Rule not found or no changes made"
                )
            
            return {"id": rule_id, "ast": ast.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def combine_rules(self, rules_data: RuleCombine) -> Dict[str, Any]:
        """Combine multiple rules into one"""
        try:
            # Validate rule count
            if len(rules_data.rule_ids) < 2:
                raise HTTPException(
                    status_code=400,
                    detail="At least 2 rules are required for combination"
                )

            # Fetch rules from database
            rules = await self._find_multiple_rules(rules_data.rule_ids)
            if not rules or len(rules) != len(rules_data.rule_ids):
                raise HTTPException(
                    status_code=404,
                    detail="One or more rules not found"
                )

            # Create nodes from stored ASTs
            nodes = [Node.from_dict(rule["ast"]) for rule in rules]
            
            # Create the combined rule string
            original_rules = [rule["rule_string"] for rule in rules]
            combined_rule_string = f" {rules_data.operator} ".join(
                f"({rule})" for rule in original_rules
            )

            # Combine rules
            try:
                combined_ast = self.rule_engine.combine_rules(
                    nodes, 
                    Operator(rules_data.operator)
                )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error combining rules: {str(e)}"
                )

            # Save combined rule
            rule_doc = {
                "name": rules_data.name,
                "description": rules_data.description,
                "rule_string": combined_rule_string,
                "ast": combined_ast.to_dict(),
                "parent_rules": [str(rule["_id"]) for rule in rules],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await self.collection.insert_one(rule_doc)
            return {
                "id": str(result.inserted_id),
                "name": rules_data.name,
                "description": rules_data.description,
                "rule_string": combined_rule_string,
                "ast": combined_ast.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def evaluate_rule(
        self, 
        rule_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate a rule against provided data"""
        try:
            rule = await self.collection.find_one({"_id": ObjectId(rule_id)})
            if not rule:
                raise HTTPException(status_code=404, detail="Rule not found")
            
            node = Node.from_dict(rule["ast"])
            result = self.rule_engine.evaluate_rule(node, data)
            
            return {
                "result": result,
                "rule_name": rule["name"],
                "rule_string": rule["rule_string"]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_rules(
        self, 
        page: int = 1, 
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get paginated list of rules"""
        skip = (page - 1) * limit
        total = await self.collection.count_documents({})
        
        rules = await self.collection.find() \
            .skip(skip) \
            .limit(limit) \
            .to_list(length=limit)
        
        return {
            "rules": [self._format_rule_response(rule) for rule in rules],
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }

    async def get_rule(self, rule_id: str) -> Dict[str, Any]:
        """Get a single rule by ID"""
        rule = await self.collection.find_one({"_id": ObjectId(rule_id)})
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        return self._format_rule_response(rule)

    async def _find_multiple_rules(self, rule_ids: List[str]) -> List[Dict]:
        """Helper method to find multiple rules by IDs"""
        try:
            object_ids = [ObjectId(id) for id in rule_ids]
            rules = await self.collection.find(
                {"_id": {"$in": object_ids}}
            ).to_list(length=None)
            return rules
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def _format_rule_response(self, rule: Dict) -> Dict:
        """Helper method to format rule response"""
        return {
            "id": str(rule["_id"]),
            "name": rule["name"],
            "description": rule.get("description"),
            "rule_string": rule["rule_string"],
            "created_at": rule["created_at"],
            "updated_at": rule["updated_at"],
            "parent_rules": rule.get("parent_rules", [])
        }