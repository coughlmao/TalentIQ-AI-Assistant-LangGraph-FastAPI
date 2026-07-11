# app/graph/prompts.py

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from app.graph.intents import AssistantIntent
from app.graph.state import GraphState
from app.graph.types import PromptRegistry


def build_base_prompt(
    state: GraphState,
) -> SystemMessage:
    """
    Builds the conre context containing system instructions,problem parameters
    and the student's workspace environment
    """
    prob = state["problem_context"]
    exec_data = state["execution_context"]

    return SystemMessage(
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


def append_chat_history(
    state: GraphState,
    initial_payload: list[BaseMessage],
) -> list[BaseMessage]:
    """
    Appends the last 4 messages of chat history to the conversation payload
    """
    chat_payload = list(initial_payload)
    recent_history = state["chat_history"][-4:]

    for msg in recent_history:
        role = msg.role if hasattr(msg, "role") else msg["role"]
        content = msg.content if hasattr(msg, "content") else msg["content"]

        if role == "user":
            chat_payload.append(HumanMessage(content=content))

        elif role == "assistant":
            chat_payload.append(AIMessage(content=content))

    return chat_payload


def build_general_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    return append_chat_history(
        state,
        [base_sys],
    )


def build_hint_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    hint_extension = (
        "\n\n"
        "## Hint Mode\n"
        "- Do NOT reveal the full solution.\n"
        "- Guide the student.\n"
        "- Ask guiding questions.\n"
        "- Give only incremental, bite-sized hints.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + hint_extension)
    return append_chat_history(
        state,
        [custom_sys],
    )


def build_debug_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    debug_extension = (
        "\n\n"
        "## Debug Mode\n"
        "Focus cleanly on resolving code problems:\n"
        "- Compiler errors\n"
        "- Runtime errors\n"
        "- Logical bugs\n"
        "- Do not discuss unrelated high-level algorithms.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + debug_extension)
    return append_chat_history(
        state,
        [custom_sys],
    )


def build_review_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    review_extension = (
        "\n\n"
        "## Review Mode\n"
        "Review the submitted implementation for:\n"
        "- Readability\n"
        "- Time and Space Complexity\n"
        "- Missing or fragile edge cases\n"
        "- Structural naming conventions\n"
        "- Maintainability\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + review_extension)
    return append_chat_history(
        state,
        [custom_sys],
    )


def build_explain_prompt(
    state: GraphState,
) -> list[BaseMessage]:
    base_sys = build_base_prompt(state)
    explain_extension = (
        "\n\n"
        "## Explain Mode\n"
        "- Focus heavily on teaching fundamental concepts.\n"
        "- Use illustrative micro-examples.\n"
        "- Avoid solving the specific problem context directly unless explicitly requested.\n"
    )
    custom_sys = SystemMessage(content=base_sys.content + explain_extension)
    return append_chat_history(
        state,
        [custom_sys],
    )


# The central, scalable Prompt Lookup Map
PROMPT_BUILDERS: PromptRegistry = {
    AssistantIntent.GENERAL: build_general_prompt,
    AssistantIntent.HINT: build_hint_prompt,
    AssistantIntent.DEBUG: build_debug_prompt,
    AssistantIntent.REVIEW: build_review_prompt,
    AssistantIntent.EXPLAIN: build_explain_prompt,
}


def build_prompt_messages(
    state: GraphState,
) -> list[BaseMessage]:
    """
    Dispatches execution to the appropriate sub-prompt builder
    based on the dynamically detected assistant intent.
    """
    intent = state.get("intent")

    # Gracefully fall back to general prompt if intent is unassigned or unknown
    builder = PROMPT_BUILDERS.get(
        intent,  # type: ignore
        build_general_prompt,
    )

    return builder(state)
