from pydantic import BaseModel,Field
from typing import List, Literal

class ProblemContextSchema(BaseModel):
    title:str=Field(...,description="Title of the challenge")
    description:str=Field(...,description="The text description layout of the problem")
    constraints:List[str]=Field(default=[],description="List of constraints")
    
class ExecutionContextSchema(BaseModel):
    input:str=Field(...,description="Active language selected in the editor dropdown")
    user_code:str=Field(...,description="The live script content inside Monaco Editor")
    compiler_output:str=Field(...,description="Text from the compiler output terminal panel")
    
class ChatHistoryMessageSchema(BaseModel):
    role:Literal["user", "assistant"]=Field(...,description="Role of the message sender")
    content:str=Field(...,description="Content of the message")
    
# Your core payload schema validating the incoming stream body
class ChatbotRequestSchema(BaseModel):
    problem_id:str
    problem_context:ProblemContextSchema
    execution_context:ExecutionContextSchema
    chat_history:List[ChatHistoryMessageSchema]