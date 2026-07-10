from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import settings
from app.schemas.request import ChatbotRequestSchema
from app.security.hmac import verify_hmac_signature
from app.streaming.sse import token_stream_generator

app = FastAPI(
    title="Modular LangGraph AI Assistant Backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.CLIENT_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def check_health() -> dict[str, str]:
    return {"status": "awake"}


@app.get("/")
def read_root():
    return {"status": "healthy", "message": "TalentIQ AI Assistant Backend is running!"}


@app.post("/api/graph/chat", dependencies=[Depends(verify_hmac_signature)])
async def handle_workspace_chat(payload: ChatbotRequestSchema):

    try:

        initial_graph_state = {
            "chat_history": [msg.model_dump() for msg in payload.chat_history],
            "problem_context": payload.problem_context.model_dump(),
            "execution_context": payload.execution_context.model_dump(),
            "final_response": "",
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

        print("Server Entry Processing Interruption:", str(err))

        raise HTTPException(status_code=500, detail=str(err)) from err
