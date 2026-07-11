# app/graph/types.py

from collections.abc import Callable

from langchain_core.messages import BaseMessage

from app.graph.intents import AssistantIntent
from app.graph.state import GraphState

PromptBuilder = Callable[
    [GraphState],
    list[BaseMessage],
]

PromptRegistry = dict[
    AssistantIntent,
    PromptBuilder,
]
