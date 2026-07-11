# app/graph/nodes.py

from __future__ import annotations

from langchain_core.messages import BaseMessage

from app.graph.intents import AssistantIntent
from app.graph.prompts import build_prompt_messages
from app.graph.routing import detect_intent
from app.graph.state import GraphState
from app.logger import logger


def route_intent_node(
    state: GraphState,
) -> dict[str, AssistantIntent | None]:
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
) -> dict[str, list[BaseMessage]]:
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
