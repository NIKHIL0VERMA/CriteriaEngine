from fastapi import APIRouter, Depends
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection

from models.rule_models import RuleCreate, RuleCombine, RuleEvaluate
from services.rule_service import RuleService
from database import get_rules_collection

router = APIRouter(prefix="/api/v1")

async def get_rule_service(
    collection: AsyncIOMotorCollection = Depends(get_rules_collection)
) -> RuleService:
    return RuleService(collection)

@router.post("/create/")
async def create_rule(
    rule: RuleCreate,
    service: RuleService = Depends(get_rule_service)
) -> Dict[str, Any]:
    return await service.create_rule(rule)

@router.put("/update/{rule_id}")
async def edit_rule(
    rule_id: str,
    rule: RuleCreate,
    service: RuleService = Depends(get_rule_service)
) -> Dict[str, Any]:
    return await service.edit_rule(rule_id, rule)

@router.post("/combine/")
async def combine_rules(
    rules: RuleCombine,
    service: RuleService = Depends(get_rule_service)
) -> Dict[str, Any]:
    return await service.combine_rules(rules)

@router.post("/evaluate/")
async def evaluate_rule(
    evaluation: RuleEvaluate,
    service: RuleService = Depends(get_rule_service)
) -> Dict[str, Any]:
    return await service.evaluate_rule(evaluation.rule_id, evaluation.data)

@router.get("/rule/{rule_id}")
async def get_rule(
    rule_id: str,
    service: RuleService = Depends(get_rule_service)
) -> Dict[str, Any]:
    return await service.get_rule(rule_id)

@router.get("/fetch/")
async def list_rules(
    page: int = 1,
    limit: int = 10,
    service: RuleService = Depends(get_rule_service)
) -> Dict[str, Any]:
    return await service.get_rules(page, limit)