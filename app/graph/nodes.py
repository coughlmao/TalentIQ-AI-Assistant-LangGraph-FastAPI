# app/graph/nodes.py

from __future__ import annotations

from typing import Any

from langchain_core.messages import BaseMessage

from app.graph.context import build_conversation_context
from app.graph.prompts import build_prompt_messages
from app.graph.routing import detect_intent
from app.graph.state import GraphState
from app.logger import logger


def conversation_context_node(
    state: GraphState,
) -> dict[str, Any]:
    """
    Builds reusable conversation context.
    """

    return {
        "conversation_context": build_conversation_context(state),
    }


def route_intent_node(
    state: GraphState,
) -> dict[str, Any]:
    """
    Determines the user's intent using deterministic pattern matching.
    """
    logger.info("Routing assistant intent")

    intent = detect_intent(
        state["latest_user_message"],
    )

    logger.info("Detected intent: %s", intent.value)

    return {
        "intent": intent,
    }


def build_prompt_node(
    state: GraphState,
) -> dict[str, Any]:
    """
    Builds the target LangChain message payload based on the matched intent.
    """
    logger.info("Building prompt payload structure")

    messages = build_prompt_messages(
        state,
    )

    return {
        "prompt_messages": messages,
    }


def prepare_response_node(
    state: GraphState,
) -> dict[str, list[BaseMessage]]:
    """
    Final preparation node.

    Future PRs will inject:

    - retrieved documents
    - tool outputs
    - memory
    - planning

    before reaching the model.
    """

    logger.info("Preparing final LLM payload")

    return {
        "llm_messages": state["prompt_messages"],
    }
