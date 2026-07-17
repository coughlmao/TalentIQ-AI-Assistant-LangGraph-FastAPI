# app/graph/builder.py

from langgraph.graph import END, START, StateGraph

from app.graph.nodes.node import (
    build_prompt_node,
    conversation_context_node,
    generate_response_node,
    retrieve_documents_node,
    route_intent_node,
)
from app.graph.state import GraphState
from app.graph.tools.tool_execution import tool_execution_node
from app.graph.tools.tool_planning import tool_planning_node

builder = StateGraph(GraphState)

# Register Processing Nodes
builder.add_node("route_intent", route_intent_node)
builder.add_node("conversation_context", conversation_context_node)
builder.add_node("retrieve_documents", retrieve_documents_node)
builder.add_node("tool_planning", tool_planning_node)
builder.add_node("tool_execution", tool_execution_node)
builder.add_node("build_prompt", build_prompt_node)
builder.add_node("generate_response", generate_response_node)

# Orchestration Flow Topology (Edges)
builder.add_edge(START, "route_intent")
builder.add_edge("route_intent", "conversation_context")
builder.add_edge("conversation_context", "retrieve_documents")
builder.add_edge("retrieve_documents", "tool_planning")
builder.add_edge("tool_planning", "tool_execution")
builder.add_edge("tool_execution", "build_prompt")
builder.add_edge("build_prompt", "generate_response")
builder.add_edge("generate_response", END)

graph_executor = builder.compile()
