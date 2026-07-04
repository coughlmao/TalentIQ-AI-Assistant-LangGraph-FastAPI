from graph import graph_executor

async def token_stream_generator(initial_graph_state):
    """Executes the compiled graph workflow and emits word tokens in real-time."""
    try:
        # Stream messages step-by-step out of the active node channel
        async for chunk, metadata in graph_executor.astream(
            initial_graph_state, 
            stream_mode="messages"
        ):
            if chunk.content:
                # Yield raw text tokens straight through the open network link pipe
                yield chunk.content
    except Exception as e:
        yield f"\n[Streaming Connection Node Exception: {str(e)}]"