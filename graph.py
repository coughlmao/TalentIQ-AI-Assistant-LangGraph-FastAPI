from typing_extensions import TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
)


class GraphState(TypedDict):
    chat_history: list
    problem_context: dict
    execution_context: dict
    final_response: str


def build_chat_payload(state: GraphState):
    """
    Builds the conversation payload for Gemini.
    """

    prob = state["problem_context"]
    exec_data = state["execution_context"]

    system_prompt = SystemMessage(
        content=(
            "You are an expert DSA programming instructor helping a student solve coding challenges.\n\n"
            "Rules:\n"
            "Every response MUST be valid GitHub-Flavored Markdown.\n"
            "Formatting rules:\n"
            "- Start with a heading when appropriate.\n"
            "- Use bullet lists instead of long paragraphs.\n"
            "- Use numbered steps for explanations.\n"
            "- Use **bold** for key ideas.\n"
            "- Use `inline code` for variables, functions and algorithms.\n"
            "- Wrap all multi-line code in fenced code blocks with the language.\n"
            "- Never output HTML.\n"
            "- Leave blank lines between sections.\n"
            "- Keep paragraphs short.\n"
            "- Prefer readable formatting over dense text.\n"
            "If answering about code:\n"
            "1. Explain the issue.\n"
            "2. Explain why it happens.\n"
            "3. Give a hint.\n"
            "4. Show only small code snippets if necessary.\n"
            "Never provide a full copy-paste solution.\n\n"
            f"## Current Problem\n"
            f"Title: {prob['title']}\n\n"
            f"Description:\n"
            f"{prob['description']}\n\n"
            f"Constraints:\n"
            f"{', '.join(prob['constraints'])}\n\n"
            "## Student Workspace\n"
            f"Language: {exec_data['language']}\n\n"
            f"Current Code:\n"
            f"```{exec_data['language']}\n"
            f"{exec_data['user_code']}\n"
            f"```\n\n"
            "Compiler Output:\n"
            "```\n"
            f"{exec_data['compiler_output']}\n"
            "```"
        )
    )

    chat_payload = [system_prompt]

    recent_history = state["chat_history"][-4:]

    for msg in recent_history:
        role = msg.role if hasattr(msg, "role") else msg["role"]
        content = msg.content if hasattr(msg, "content") else msg["content"]

        if role == "user":
            chat_payload.append(HumanMessage(content=content))

        elif role == "assistant":
            chat_payload.append(AIMessage(content=content))

    return chat_payload


def coding_instructor_node(state: GraphState):

    messages = build_chat_payload(state)

    response = llm.invoke(messages)

    return {
        "final_response": response.content,
    }


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
