
from __future__ import annotations

from typing import Any

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from app.graph.intents import AssistantIntent


class GraphState(TypedDict):
    """
    Shared mutable state flowing through every LangGraph node.

    Every node owns only a subset of these fields.
    """

    # ------------------------------------------------------------------
    # Incoming request
    # ------------------------------------------------------------------

    chat_history: list[dict[str, str]]

    latest_user_message: str

    problem_context: dict[str, Any]

    execution_context: dict[str, Any]

    retrieved_documents: list[Document]
    
    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    intent: AssistantIntent | None

    # ------------------------------------------------------------------
    # Conversation
    # ------------------------------------------------------------------

    conversation_context: list[BaseMessage]

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    retrieved_documents: list[Document]

    # ------------------------------------------------------------------
    # Planning
    # ------------------------------------------------------------------

    tool_calls: list[dict[str, Any]]

    # ------------------------------------------------------------------
    # Tool Execution
    # ------------------------------------------------------------------

    tool_plan: dict[str,Any]
    
    tool_results:list[dict[str,Any]]

    # ------------------------------------------------------------------
    # Prompt
    # ------------------------------------------------------------------

    prompt_messages: list[BaseMessage]
    
    llm_messages: list[BaseMessage]

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    final_response: str

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    metadata: dict[str, Any]
