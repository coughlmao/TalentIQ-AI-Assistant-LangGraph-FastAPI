# app/graph/context/context.py

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
)

from app.graph.state import GraphState


def build_conversation_context(
    state: GraphState,
) -> list[BaseMessage]:
    """
    Converts historical data context into native LangChain Message lists.
    Guarantees the absolute final element evaluates explicitly to the latest
    user statement to stabilize downstream model execution.
    """
    messages: list[BaseMessage] = []
    raw_history = state.get("chat_history") or []

    # Safeguard: If the incoming chat history already includes the fresh prompt
    # at the tail end, drop it temporarily to avoid duplicate entries.
    latest_msg = state.get("latest_user_message", "").strip()
    if (
        raw_history
        and raw_history[-1].get("role") == "user"
        and raw_history[-1].get("content", "").strip() == latest_msg
    ):
        history_pool = raw_history[:-1]
    else:
        history_pool = raw_history

    # Take trailing conversation contexts (up to 4 frames of history)
    recent_history = history_pool[-4:]

    for message in recent_history:
        if message["role"] == "user":
            messages.append(HumanMessage(content=message["content"]))
        else:
            messages.append(AIMessage(content=message["content"]))

    # Always append the fresh operational question at the end
    if latest_msg:
        messages.append(HumanMessage(content=latest_msg))

    return messages
