# app/graph/nodes/node.py

from __future__ import annotations

from typing import Any

from langchain_core.messages import BaseMessage

from app.graph.context.context import build_conversation_context
from app.graph.context.context_formatter import build_enrichment_directive
from app.graph.llm.llm import llm
from app.graph.nodes.routing import detect_intent
from app.graph.prompts import build_prompt_messages
from app.graph.retrieval.retrieval import retrieve_relevant_docs
from app.graph.state import GraphState
from app.logger import logger


def conversation_context_node(state: GraphState) -> dict[str, Any]:
    """
    Builds reusable conversation context.
    """
    return {"conversation_context": build_conversation_context(state)}


def route_intent_node(state: GraphState) -> dict[str, Any]:
    """
    Determines the user's intent using deterministic pattern matching.
    """
    logger.info("Routing assistant intent")
    intent = detect_intent(state["latest_user_message"])
    logger.info("Detected intent: %s", intent.value)
    return {"intent": intent}


async def retrieve_documents_node(state: GraphState) -> dict[str, Any]:
    """
    Fetches relevant code documentation, conceptual references,
    or hint scaffolds to aid generation.
    """
    logger.info("Executing retrieval pipeline step")
    docs = await retrieve_relevant_docs(state)
    return {"retrieved_documents": docs}


def build_prompt_node(state: GraphState) -> dict[str, Any]:
    """
    Consolidates base system prompt rules, context timelines, tool verification states,
    and user messages into the absolute final execution structure.
    """
    logger.info("Building consolidated target message payload matrix")

    # 1. Fetch the base message setup (e.g., system instructions + user questions)
    base_messages = build_prompt_messages(state)

    # 2. Build enrichment system frames using current state parameters
    enrichment_directive = build_enrichment_directive(
        retrieved_docs=state.get("retrieved_documents") or [],
        tool_results=state.get("tool_results") or [],
    )

    # 3. Inject enrichment instructions right behind the main System Message frame
    if enrichment_directive and base_messages:
        first_msg, *rest_msgs = base_messages
        assembled_messages = [first_msg, enrichment_directive, *rest_msgs]
    else:
        assembled_messages = base_messages

    return {"llm_messages": assembled_messages}


async def generate_response_node(state: GraphState) -> dict[str, Any]:
    """
    Natively runs model inference inside the LanGraph topology
    Using astream_events will capture token chunks emitted right here.
    """
    logger.info("Invoking LLM provider within graph topology")
    messages: list[BaseMessage] = state["llm_messages"]
    # We await the complete call here; astream_events will intercept the stream chunks under the hood
    response = await llm.ainvoke(messages)
    return {"final_response": str(response.content)}
