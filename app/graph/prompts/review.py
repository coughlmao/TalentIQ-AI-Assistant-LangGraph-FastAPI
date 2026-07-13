# app/graph/prompts/review.py

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
)

from app.graph.prompts.base import build_base_prompt
from app.graph.state import GraphState


def build_review_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    review_extension = (
        "\n\n"
        "## Review Mode\n"
        "Review the submitted implementation for:\n"
        "- Readability\n"
        "- Time and Space Complexity\n"
        "- Missing or fragile edge cases\n"
        "- Structural naming conventions\n"
        "- Maintainability\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + review_extension)
    return [
        custom_sys,
        *state["conversation_context"],
    ]
