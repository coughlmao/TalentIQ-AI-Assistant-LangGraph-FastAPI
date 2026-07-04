import os
import uvicorn
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from schema import ChatbotRequestSchema
from streaming import token_stream_generator

load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")

#Initialise your core FastAPI application container
app=FastAPI(title="Modular Langraph AI Assistant Backend")

# Enable wide cross-origin sharing rules for microservices communication flexiblilty
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# THE ENDPOINT ROUTE ROUTER INTERFACE
# ----------------------------------------------------------------------
# Add this block at the top level
@app.get("/")
def read_root():
    return {"status": "healthy", "message": "TalentIQ AI Assistant Backend is running!"}

@app.post("/api/graph/chat")
async def handle_workspace_chat(payload:ChatbotRequestSchema):
     try:
        # Convert Pydantic object instances into pure dict structures via .model_dump()
        initial_graph_state = {
            "chat_history": [msg.model_dump() for msg in payload.chat_history],
            "problem_context": payload.problem_context.model_dump(),
            "execution_context": payload.execution_context.model_dump(),
            "final_response": ""
        }
        
        # Dispatch the asynchronous token event loop streaming container straight to Express
        return StreamingResponse(
            token_stream_generator(initial_graph_state), 
            media_type="text/event-stream"
            )
        
     except Exception as e:
        print(f"Server Entry Processing Interruption: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Microservice Internal Failure: {str(e)}")
    
# Native Python Bootstrapper Launch Initialization settings
if __name__ == "__main__":
    # Remember to execute: export GEMINI_API_KEY="your-key" inside your terminal before booting
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)