import os
import uvicorn
import time
import hmac
import hashlib
from fastapi import FastAPI, HTTPException, Header, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from schema import ChatbotRequestSchema
from streaming import token_stream_generator

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client_url = os.getenv("CLIENT_URL")

# Initialise your core FastAPI application container
app = FastAPI(title="Modular Langraph AI Assistant Backend")

# Enable wide cross-origin sharing rules for microservices communication flexiblilty
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        client_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Extract the secret token seed directly from Render Environment Dashboards
SHARED_SECRET_KEY = os.getenv("INTERNAL_SHARED_SECRET", "fallback_secure_key").encode(
    "utf-8"
)


async def verify_hmac_signature(
    request: Request,
    x_signature: str = Header(None, alias="X-Signature"),
    x_timestamp: str = Header(None, alias="X-Timestamp"),
):
    # 1. Enforce presence of required cryptographic headers
    if not x_signature or not x_timestamp:
        raise HTTPException(
            status_code=403, detail="Access denied: Missing signature attributes."
        )

    try:
        # 2. Check for Replay Attacks (Reject requests older than 30 seconds)
        request_time = int(x_timestamp) / 1000.0
        current_time = time.time()

        if abs(current_time - request_time) > 30.0:
            raise HTTPException(
                status_code=403, detail="Access denied: Request signature expired."
            )

        # Read the raw, unparsed request bytes body directly from the stream
        raw_body_bytes = await request.body()
        raw_body_str = raw_body_bytes.decode("utf-8")

        # Reconstruct the message signature footprint
        message_to_sign = (x_timestamp + raw_body_str).encode("utf-8")

        # Compute local HMAC-SHA256 signature
        computed_hash = hmac.new(
            SHARED_SECRET_KEY, message_to_sign, hashlib.sha256
        ).hexdigest()

        # Execute time-constant string comparison to completely mitigate Timing Attacks
        if not hmac.compare_digest(computed_hash, x_signature):
            raise HTTPException(
                status_code=403,
                detail="Invalid cryptographic hash token signature alignment.",
            )

    except ValueError:
        raise HTTPException(
            status_code=403, detail="Malformed cryptographic verification metadata."
        )
    return True


# Unlocked route allowing easy pre-warming triggers from your MERN monolith
@app.get("/health-ping")
async def health_ping():
    return {"status": "awake"}


# ----------------------------------------------------------------------
# THE ENDPOINT ROUTE ROUTER INTERFACE
# ----------------------------------------------------------------------
# Add this block at the top level
@app.get("/")
def read_root():
    return {"status": "healthy", "message": "TalentIQ AI Assistant Backend is running!"}


@app.post(
    "/api/graph/chat",
    dependencies=[Depends(verify_hmac_signature)]
)
async def handle_workspace_chat(
    payload: ChatbotRequestSchema
):

    try:

        initial_graph_state = {

            "chat_history": [
                msg.model_dump()
                for msg in payload.chat_history
            ],

            "problem_context":
                payload.problem_context.model_dump(),

            "execution_context":
                payload.execution_context.model_dump(),

            "final_response": "",
        }


        return StreamingResponse(
            token_stream_generator(
                initial_graph_state
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )


    except Exception as e:

        print(
            "Server Entry Processing Interruption:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Native Python Bootstrapper Launch Initialization settings
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
