from app.graph.prompts import build_prompt_messages
from app.graph.services import llm


async def token_stream_generator(initial_graph_state):
    """
    Streams Gemini tokens as Server-Sent Events.

    Express simply forwards these chunks to React.
    """

    try:
        messages = build_prompt_messages(initial_graph_state)

        async for chunk in llm.astream(messages):
            if not chunk.content:
                continue

            print("TOKEN:", repr(chunk.content))
            yield f"data: {chunk.content}\n\n"

        yield "event: done\ndata: done\n\n"

    except Exception as e:
        print("Streaming error:", str(e))
        yield ("event: error\n" f"data: {e!s}\n\n")
