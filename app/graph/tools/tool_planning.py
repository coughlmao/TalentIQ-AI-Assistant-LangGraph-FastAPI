# app/graph/tools/tool_planning.py

from typing import Any

from app.graph.intents import AssistantIntent
from app.graph.state import GraphState
from app.graph.tools.tool_schema import ExecuteCodeArgs, RequestHintArgs
from app.logger import logger


async def tool_planning_node(state: GraphState) -> dict[str, Any]:
    """
    Determines whether a tool action is needed based on the unified AssistantIntent.
    """
    logger.info("Planning tool execution parameters based on structured intent")

    intent = state.get("intent")
    prob_context = state.get("problem_context") or {}
    exec_context = state.get("execution_context") or {}

    # Safely look for cross-referenced problem identifier strings
    prob_id = prob_context.get("id") or state.get("metadata", {}).get(
        "problem_id", "unknown-challenge"
    )
    user_code = exec_context.get("user_code", "")

    if not intent:
        return {"tool_plan": None}

    # Trigger Express sandbox code validation when the student explicitly needs debug operations
    if intent == AssistantIntent.DEBUG and user_code:
        validated_args = ExecuteCodeArgs(code=user_code, problem_id=prob_id)
        return {
            "tool_plan": {
                "action": "execute_code",
                "arguments": validated_args.model_dump(),
            }
        }

    # Trigger a hint validation schema when HINT mode is identified
    if intent == AssistantIntent.HINT:
        validated_args = RequestHintArgs(problem_id=prob_id, hint_level=1)
        return {
            "tool_plan": {
                "action": "request_hint",
                "arguments": validated_args.model_dump(),
            }
        }

    return {"tool_plan": None}
