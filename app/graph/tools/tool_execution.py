# app/graph/tools/tool_execution.py

from typing import Any

from app.graph.state import GraphState
from app.graph.tools.tool_executor import call_express_execution_sandbox
from app.logger import logger


async def tool_execution_node(state: GraphState) -> dict[str, Any]:
    """
    Orchestration node responsible for execution routing logic.
    Decoupled directly from LangGraph through specialized function abstractions.
    """
    tool_plan = state.get("tool_plan")

    # Check if a tool execution requirement was declared by the planning node
    if not tool_plan or tool_plan.get("action") != "execute_code":
        logger.info(
            "Tool execution skipped: No plan present or tool requires no sandboxed execution loop."
        )
        return {"tool_results": []}

    arguments = tool_plan.get("arguments", {})
    code = arguments.get("code", "")

    # Extract operational runner metadata fields from state payload
    exec_context = state.get("execution_context") or {}
    language = exec_context.get("language", "python")

    logger.info("Tool execution node executing action: %s", tool_plan["action"])

    # Dispatch execution out to the Express sandboxed service runner utilities
    sandbox_result = await call_express_execution_sandbox(language=language, code=code)

    return {"tool_results": [sandbox_result]}
