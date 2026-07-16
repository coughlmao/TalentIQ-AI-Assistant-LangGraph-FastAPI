from collections.abc import AsyncGenerator

from app.graph.builder import graph_executor
from app.graph.state import GraphState
from app.logger import logger


async def token_stream_generator(
    initial_graph_state: GraphState,
) -> AsyncGenerator[str, None]:
    """
    Executes the LangGraph topology and streams internal events and token chunks
    in real time back to the client via Server-Sent Events (SSE).
    """
    logger.info("Initializing graph-native event stream workflow")

    try:
        # Stream graph lifecycle events using the production v2 engine specifications
        async for event in graph_executor.astream_events(initial_graph_state, version="v2"):
            kind = event.get("event")
            
            # Catch token stream chunks directly from the chat model provider inside the graph
            if kind == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and chunk.content:
                    # Stream tokens out immediately to client as an SSE data frame
                    yield f"data: {chunk.content}\n\n"

            # Hook point for monitoring graph node transitions
            elif kind == "on_chain_start" and event.get("name") == "LangGraph":
                logger.info("Graph processing chain started execution lifecycle loop")

        logger.info("Stream finished successfully")
        yield "event: done\ndata: done\n\n"

    except Exception as err:
        logger.exception("Streaming error occurred during native graph execution")
        yield f"event: error\ndata: {err!s}\n\n"