# app/graph/context.py

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
    Converts recent chat history into LangChain messages.

    This node owns conversation history preparation.

    Prompt builders should never inspect raw chat_history.
    """

    messages: list[BaseMessage] = []

    history = state["chat_history"][-4:]

    for message in history:
        if message["role"] == "user":
            messages.append(
                HumanMessage(
                    content=message["content"],
                )
            )

        else:
            messages.append(
                AIMessage(
                    content=message["content"],
                )
            )

    return messages
    