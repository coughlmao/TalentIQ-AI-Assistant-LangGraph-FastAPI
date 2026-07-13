# app/graph/llm.py


from collections.abc import AsyncGenerator

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    api_key=settings.GOOGLE_API_KEY,
)


async def stream_response(
    messages: list[BaseMessage],
) -> AsyncGenerator[str, None]:
    """
    Streams response tokens from the configured LLM.
    """

    async for chunk in llm.astream(messages):
        if not chunk.content:
            continue

        yield chunk.content


async def invoke_response(
    messages: list[BaseMessage],
) -> str:
    """
    Executes a complete non-streaming inference.
    """

    response = await llm.ainvoke(messages)

    return str(response.content)
