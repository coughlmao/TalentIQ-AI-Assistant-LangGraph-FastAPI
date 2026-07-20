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
        "Return findings in a review-style order:\n"
        "1. Severity-ranked issues first.\n"
        "2. Why each issue matters.\n"
        "3. Concrete improvement suggestions.\n"
        "4. Edge cases or risks to test.\n"
        "Focus on readability, complexity, fragile edge cases, naming, and maintainability.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + review_extension)
    return [
        custom_sys,
        *state["conversation_context"],
    ]
