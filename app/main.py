# app/main.py

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import settings
from app.logger import logger
from app.schemas.request import ChatbotRequestSchema
from app.security.hmac import verify_hmac_signature
from app.streaming.sse import token_stream_generator

app = FastAPI(
    title="Modular LangGraph AI Assistant Backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(settings.CLIENT_URL).rstrip("/"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def check_health() -> dict[str, str]:
    return {
        "status": "awake",
    }


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "TalentIQ AI Assistant Backend is running!",
    }


@app.post(
    "/api/graph/chat",
    dependencies=[Depends(verify_hmac_signature)],
)
async def handle_workspace_chat(
    payload: ChatbotRequestSchema,
) -> StreamingResponse:

    try:
        latest_user_message = ""
        if payload.chat_history:
            latest_user_message = payload.chat_history[-1].content

        # Map complete payload matrix accurately into runtime GraphState variables
        initial_graph_state = {
            "chat_history": [msg.model_dump() for msg in payload.chat_history],
            "latest_user_message": latest_user_message,
            "problem_context": payload.problem_context.model_dump(),
            "execution_context": payload.execution_context.model_dump(),
            "intent": None,
            "conversation_context": [],
            "retrieved_documents": [],
            "tool_plan": None,
            "tool_results": [],
            "llm_messages": [],
            "final_response": "",
            "metadata": {"problem_id": payload.problem_id},
        }

        return StreamingResponse(
            token_stream_generator(initial_graph_state),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as err:
        logger.exception("Server entry processing interruption discovered")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from err
