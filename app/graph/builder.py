from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.graph.nodes import coding_instructor_node
from app.graph.state import GraphState

builder = StateGraph(GraphState)

builder.add_node(
    "instructor",
    coding_instructor_node,
)

builder.add_edge(
    START,
    "instructor",
)

builder.add_edge(
    "instructor",
    END,
)

graph_executor = builder.compile()
