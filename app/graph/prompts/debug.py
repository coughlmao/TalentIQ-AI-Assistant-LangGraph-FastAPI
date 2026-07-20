# app/graph/prompts/debug.py

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)

from app.graph.prompts.base import build_base_prompt
from app.graph.state import GraphState


def build_debug_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    debug_extension = (
        "\n\n"
        "## Debug Mode\n"
        "- Focus on the root cause before proposing a fix.\n"
        "- Prioritize compiler errors, runtime errors, and logical bugs.\n"
        "- State the likely failing line or condition when possible.\n"
        "- Keep unrelated algorithm discussion out unless it is necessary to fix the bug.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + debug_extension)
    return [
        custom_sys,
        *state["conversation_context"],
    ]
