# app/graph/prompts/explain.py

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)

from app.graph.prompts.base import build_base_prompt
from app.graph.state import GraphState


def build_explain_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    explain_extension = (
        "\n\n"
        "## Explain Mode\n"
        "- Teach the underlying concept first, then connect it back to the problem.\n"
        "- Use illustrative micro-examples and compact comparisons.\n"
        "- Avoid jumping straight to the final answer unless explicitly requested.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + explain_extension)
    return [
        custom_sys,
        *state["conversation_context"],
    ]
