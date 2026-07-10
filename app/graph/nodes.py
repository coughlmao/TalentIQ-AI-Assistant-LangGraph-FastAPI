from app.graph.prompts import build_prompt_messages
from app.graph.services import llm
from app.graph.state import GraphState


def coding_instructor_node(
    state: GraphState,
):

    messages = build_prompt_messages(state)

    response = llm.invoke(messages)

    return {
        "final_response": response.content,
    }
