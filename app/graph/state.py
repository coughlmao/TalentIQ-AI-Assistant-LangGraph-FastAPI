from __future__ import annotations

from typing import Any

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class GraphState(TypedDict):
    chat_history: list[dict[str, str]]
    latest_user_message: str
    problem_context: dict[str, Any]
    execution_context: dict[str, Any]
    prompt_messages: list[BaseMessage]
    final_response: str
