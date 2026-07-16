# app/graph/prompts/hint.py

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)

from app.graph.prompts.base import build_base_prompt
from app.graph.state import GraphState


def build_hint_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    hint_extension = (
        "\n\n"
        "## Hint Mode\n"
        "- Do NOT reveal the full solution.\n"
        "- Guide the student.\n"
        "- Ask guiding questions.\n"
        "- Give only incremental, bite-sized hints.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + hint_extension)
    return [
        custom_sys,
        *state["conversation_context"],
    ]
