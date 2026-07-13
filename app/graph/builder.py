# app/graph/builder.py

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.graph.nodes import (
    build_prompt_node,
    conversation_context_node,
    prepare_response_node,
    route_intent_node,
)
from app.graph.state import GraphState

builder = StateGraph(GraphState)

# 1. Register the processing nodes
builder.add_node(
    "route_intent",
    route_intent_node,
)

builder.add_node(
    "conversation_context",
    conversation_context_node,
)

builder.add_node(
    "build_prompt",
    build_prompt_node,
)

builder.add_node(
    "prepare_response",
    prepare_response_node,
)

# 2. Build the orchestration flow topology
builder.add_edge(
    START,
    "route_intent",
)

builder.add_edge(
    "route_intent",
    "build_prompt",
)

builder.add_edge(
    "build_prompt",
    "prepare_response",
)

# Route to END right after building the prompt payload
builder.add_edge(
    "prepare_response",
    END,
)

# The compiled runner execution instance
graph_executor = builder.compile()
