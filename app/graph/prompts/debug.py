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
        "Focus cleanly on resolving code problems:\n"
        "- Compiler errors\n"
        "- Runtime errors\n"
        "- Logical bugs\n"
        "- Do not discuss unrelated high-level algorithms.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + debug_extension)
    return [
        custom_sys,
        *state["conversation_context"],
    ]
