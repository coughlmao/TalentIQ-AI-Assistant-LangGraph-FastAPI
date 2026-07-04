from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langgraph.graph import StateGraph,START,END

load_dotenv()

# Define your langGraph model tracker core
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class GraphState(TypedDict):
    chat_history:list
    problem_context:dict
    execution_context:dict
    final_response:str
    
def coding_instructor_node(state:GraphState):
    prob=state["problem_context"]
    exec_data=state["execution_context"]
    
    # System prompting configuration stays the same
    system_prompt=SystemMessage(content=(
         f"You are an expert DSA programming instructor helping a student solve a challenge.\n"
        f"Do not supply direct copy-paste code solutions or full code text blocks.\n\n"
        f"### Active Problem: {prob['title']}\n"
        f"Description Layout: {prob['description']}\n"
        f"Algorithmic Constraints: {', '.join(prob['constraints'])}\n\n"
        f"### Student Active Workspace Status:\n"
        f"Language Environment: {exec_data['language']}\n"
        f"Active Code in Monaco Editor:\n```\n{exec_data['user_code']}\n```\n"
        f"Compiler Terminal Execution Logs:\n```\n{exec_data['compiler_output']}\n```\n\n"
        f"CRITICAL INSTRUCTION: Analyze the code and terminal bugs. Use Socratic hinting methods "
        f"to clear up logical misunderstandings or edge-case oversights. Guide them to correct their own lines."
    ))
    
    # Enforce your sliding context window using the correct aligned key
    CONTEXT_WINDOW=4
    recent_history=state["chat_history"][-CONTEXT_WINDOW:]
    
    # Assemble your LangChain chat payload stack
    chat_payload=[system_prompt]
    for msg in recent_history:
        # Note:If your ChatHistoryMessages uses Pydantic Objects,
        # handling them as dictionary lookups is smooth
        role=msg.role if hasattr(msg,'role') else msg["role"]
        content=msg.content if hasattr(msg,'content') else msg["content"]
        
        if role == "user":
            chat_payload.append(HumanMessage(content=content))
        elif role == "assistant":
            chat_payload.append(AIMessage(content=content))
    return {"final_response":llm.astream(chat_payload)}

# Stitch and compile the LangGraph workflow structure
builder = StateGraph(GraphState)
builder.add_node("instructor", coding_instructor_node)
builder.add_edge(START, "instructor")
builder.add_edge("instructor", END)

# Export the compiled executable graph blueprint
graph_executor = builder.compile()