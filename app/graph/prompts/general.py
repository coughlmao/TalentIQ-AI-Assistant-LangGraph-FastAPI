# app/graph/prompts/general.py

from langchain_core.messages import (
    BaseMessage,
)

from app.graph.prompts.base import build_base_prompt
from app.graph.state import GraphState


def build_general_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    return [
        base_sys,
        *state["conversation_context"],
    ]
