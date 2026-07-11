from collections.abc import AsyncGenerator

from app.graph.prompts import build_prompt_messages
from app.graph.services import llm
from app.graph.state import GraphState
from app.logger import logger


async def token_stream_generator(initial_graph_state:GraphState,)->AsyncGenerator[str,None]:
    """
    Streams Gemini tokens as Server-Sent Events.

    Express simply forwards these chunks to React.
    """
    logger.info("Starting token stream generator")

    try:
        messages = build_prompt_messages(initial_graph_state)

        async for chunk in llm.astream(messages):
            if not chunk.content:
                continue

            logger.debug(f"TOKEN: {chunk.content!r}")
            yield f"data: {chunk.content}\n\n"

        logger.info("Stream finished successfully")
        yield "event: done\ndata: done\n\n"

    except Exception as e:
        logger.exception("Streaming error occured while communicating with LLM")
        yield ("event: error\n" f"data: {e!s}\n\n")
