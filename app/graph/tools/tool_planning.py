# app/graph/tool_planning.py

from typing import Any

from app.graph.state import GraphState
from app.graph.tools.tool_schema import ExecuteCodeArgs, RequestHintArgs
from app.logger import logger


async def tool_planning_node(state: GraphState) -> dict[str, Any]:
    """
    Analyzes the structured intent from the state graph to build tool arguments.
    Uses Pydantic classes to validate arguments and resolve linter warnings.
    """
    logger.info("Planning tool execution parameters based on structured intent")
    
    intent = state.get("intent")
    prob_context = state.get("problem_context", {})
    prob_id = prob_context.get("id", "unknown-challenge")
    
    tool_plan = {
        "tool_name": None,
        "tool_args": {},
        "requires_execution": False
    }
    
    if not intent:
        return {"tool_plan": tool_plan}

    # Intent routing checks (adjust to match your exact intent enum/string structure)
    if intent.value == "execute_code":
        # Validate arguments using the Pydantic schema
        validated_args = ExecuteCodeArgs(
            code=state.get("latest_user_message", ""),
            problem_id=prob_id
        )
        tool_plan["tool_name"] = "execute_code"
        tool_plan["tool_args"] = validated_args.model_dump()
        tool_plan["requires_execution"] = True
        
    elif intent.value == "request_hint":
        # Validate arguments using the Pydantic schema
        validated_args = RequestHintArgs(
            problem_id=prob_id,
            hint_level=1
        )
        tool_plan["tool_name"] = "request_hint"
        tool_plan["tool_args"] = validated_args.model_dump()
        tool_plan["requires_execution"] = True
        
    return {
        "tool_plan": tool_plan
    }