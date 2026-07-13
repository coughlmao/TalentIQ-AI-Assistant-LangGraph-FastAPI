# app/streaming/sse.py

from collections.abc import AsyncGenerator

from app.graph.builder import graph_executor
from app.graph.llm import (
    llm,
    stream_response,
)
from app.graph.state import GraphState
from app.logger import logger


async def token_stream_generator(
    initial_graph_state: GraphState,
) -> AsyncGenerator[str, None]:
    """
    Executes the LangGraph pipeline to route and build context,
    then streams Gemini tokens directly as Server-Sent Events (SSE).
    """
    logger.info("Starting token stream generator workflow")

    try:
        logger.info("Invoking LangGraph intent routing & prompt pipeline...")
        final_graph_state = await graph_executor.ainvoke(initial_graph_state)

        # Crash loudly right here if the orchestration graph failed to deliver
        messages = final_graph_state["llm_messages"]

        logger.info("Initiating Gemini token stream...")
        async for token in stream_response(messages):
            yield f"data: {token}\n\n"
            if not token.content:
                continue

            logger.debug("Streaming token received")
            yield f"data: {token.content}\n\n"

        logger.info("Stream finished successfully")
        yield "event: done\ndata: done\n\n"

    except Exception as err:
        logger.exception(
            "Streaming error occurred while orchestrating or communicating with LLM"
        )
        yield f"event: error\ndata: {err!s}\n\n"
