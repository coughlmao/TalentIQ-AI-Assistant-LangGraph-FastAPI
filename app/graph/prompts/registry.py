# app/graph/prompts/registry.py

from langchain_core.messages import (
    BaseMessage,
)

from app.graph.intents import AssistantIntent
from app.graph.prompts.debug import build_debug_prompt
from app.graph.prompts.explain import build_explain_prompt
from app.graph.prompts.general import build_general_prompt
from app.graph.prompts.hint import build_hint_prompt
from app.graph.prompts.review import build_review_prompt
from app.graph.state import GraphState
from app.graph.types import PromptRegistry

# The central, scalable Prompt Lookup Map
PROMPT_BUILDERS: PromptRegistry = {
    AssistantIntent.GENERAL: build_general_prompt,
    AssistantIntent.HINT: build_hint_prompt,
    AssistantIntent.DEBUG: build_debug_prompt,
    AssistantIntent.REVIEW: build_review_prompt,
    AssistantIntent.EXPLAIN: build_explain_prompt,
}


def build_prompt_messages(
    state: GraphState,
) -> list[BaseMessage]:
    """
    Dispatches execution to the appropriate sub-prompt builder
    based on the dynamically detected assistant intent.
    """
    intent = state.get("intent")

    # Gracefully fall back to general prompt if intent is unassigned or unknown
    builder = PROMPT_BUILDERS.get(
        intent,  # type: ignore
        build_general_prompt,
    )

    return builder(state)
