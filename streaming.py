from graph import (
    llm,
    build_chat_payload,
)


async def token_stream_generator(initial_graph_state):
    """
    Streams Gemini tokens as Server-Sent Events.

    Express simply forwards these chunks to React.
    """

    try:

        messages = build_chat_payload(initial_graph_state)

        async for chunk in llm.astream(messages):

            if not chunk.content:
                continue

            print("TOKEN:", repr(chunk.content))

            yield f"data: {chunk.content}\n\n"

        yield "event: done\ndata: done\n\n"

    except Exception as e:

        print("Streaming error:", str(e))

        yield (
            "event: error\n"
            f"data: {str(e)}\n\n"
        )