# TalentIQ AI Assistant Backend

A modular AI assistant backend built with **FastAPI**, **LangGraph**, and **Google Gemini** that provides intelligent coding assistance inside the TalentIQ coding workspace.

The backend powers an AI coding instructor capable of:

- Understanding user coding questions
- Detecting user intent
- Building contextual prompts
- Retrieving relevant programming knowledge
- Executing code through an external sandbox service
- Streaming AI responses in real time

The system is designed around a **LangGraph workflow architecture**, allowing future expansion into more advanced agentic capabilities such as dynamic tool selection, multi-step reasoning, and long-term memory.

---

# Features

## AI Conversation Pipeline

The assistant processes every request through a structured LangGraph workflow:

```
User Request
     |
     v
Intent Detection
     |
     v
Conversation Context Builder
     |
     v
Knowledge Retrieval
     |
     v
Tool Planning
     |
     v
Tool Execution
     |
     v
Prompt Assembly
     |
     v
LLM Generation
     |
     v
Streaming Response
```

Each stage has a dedicated responsibility, making the system easier to maintain and extend.

---

# Core Capabilities

## Intent-Based Assistance

The assistant classifies incoming messages into supported interaction modes:

### General

General programming conversations and explanations.

### Hint

Provides incremental guidance without revealing complete solutions.

### Debug

Analyzes compiler errors, runtime failures, and incorrect behavior.

### Review

Reviews implementations for:

- Code quality
- Complexity
- Maintainability
- Edge cases

### Explain

Focuses on teaching programming concepts and fundamentals.

---

# Architecture

## Technology Stack

### Backend

- FastAPI
- Python
- LangGraph
- LangChain
- Pydantic
- SSE (Server Sent Events)

### AI Model

- Google Gemini
- `gemini-2.5-flash`

### External Services

- Express.js execution sandbox
- Frontend coding workspace

---

# Project Structure

```
app
│
├── main.py
│
├── config.py
├── logger.py
│
├── schemas
│   └── request.py
│
├── security
│   └── hmac.py
│
├── streaming
│   └── sse.py
│
└── graph
    │
    ├── builder.py
    ├── state.py
    ├── intents.py
    │
    ├── nodes
    │   ├── node.py
    │   └── routing.py
    │
    ├── prompts
    │   ├── base.py
    │   ├── registry.py
    │   ├── general.py
    │   ├── hint.py
    │   ├── debug.py
    │   ├── review.py
    │   └── explain.py
    │
    ├── context
    │   ├── context.py
    │   └── context_formatter.py
    │
    ├── retrieval
    │   └── retrieval.py
    │
    ├── tools
    │   ├── tool_planning.py
    │   ├── tool_execution.py
    │   └── tool_schema.py
    │
    └── llm
        └── llm.py
```

---

# LangGraph Workflow

The assistant uses LangGraph to model the AI reasoning pipeline.

The graph state contains:

```python
GraphState
```

which stores:

- User conversation history
- Problem context
- Execution context
- Detected intent
- Retrieved knowledge
- Tool plans
- Tool outputs
- Prompt messages
- Final response

Each graph node modifies only the part of the state it owns.

---

# Request Flow

## 1. Client Request

The frontend sends:

```json
{
  "problem_context": {},
  "execution_context": {},
  "chat_history": []
}
```

The request contains:

### Problem Context

Information about the coding challenge:

- Title
- Description
- Constraints

### Execution Context

Current workspace state:

- Programming language
- User code
- Compiler output

### Chat History

Previous conversation messages.

---

# 2. Intent Detection

The router analyzes the latest user message.

Example:

```
"Why am I getting this runtime error?"
```

becomes:

```
DEBUG
```

Example:

```
"Can you explain binary search?"
```

becomes:

```
EXPLAIN
```

---

# 3. Context Preparation

Conversation history is converted into LangChain message objects.

The assistant currently uses recent conversation history to keep prompts efficient.

---

# 4. Retrieval Layer

The retrieval pipeline provides additional knowledge context.

Currently it supports:

- Problem-related references
- Programming concepts
- Execution context enrichment

The retrieval layer is isolated so it can later be replaced with:

- MongoDB vector search
- Chroma
- Pinecone
- Weaviate
- Other vector databases

without affecting the graph architecture.

---

# 5. Tool Execution

The assistant integrates with the existing Express execution service.

Supported languages:

- Python
- JavaScript

(Java support depends on Java runtime availability.)

The execution pipeline provides:

- Program output
- Runtime errors
- Compiler failures

which are injected back into the AI reasoning context.

---

# 6. Prompt Construction

Prompts are dynamically selected based on intent.

Example:

```
DEBUG
 |
 v
debug.py prompt builder
```

```
HINT
 |
 v
hint.py prompt builder
```

Each prompt extends a shared base coding instructor prompt.

---

# 7. LLM Generation

The final structured message payload is sent to Gemini.

The model receives:

- System instructions
- Problem information
- User workspace
- Conversation context
- Retrieved knowledge
- Tool execution results

---

# Streaming Responses

The backend uses Server Sent Events (SSE).

The response flow:

```
Gemini Token
      |
      v
LangGraph Event Stream
      |
      v
FastAPI StreamingResponse
      |
      v
Frontend Chat Interface
```

This allows users to see responses appear progressively.

---

# API Reference

## Health Check

```
GET /health
```

Response:

```json
{
  "status": "awake"
}
```

---

## Chat Endpoint

```
POST /api/graph/chat
```

Headers:

```
X-Signature
X-Timestamp
```

Request:

```json
{
  "problem_context": {
    "title": "Two Sum",
    "description": "Find two numbers",
    "constraints": []
  },

  "execution_context": {
    "language": "python",
    "user_code": "",
    "compiler_output": ""
  },

  "chat_history": [
    {
      "role": "user",
      "content": "Help debug this"
    }
  ]
}
```

Response:

```
text/event-stream
```

Example:

```
data: The issue is caused by...

data: because your loop condition...

event: done
data: done
```

---

# Environment Setup

## Requirements

- Python 3.11+
- Google Gemini API Key

---

## Installation

Clone repository:

```bash
git clone <repository-url>

cd TalentIQ-AI-Assistant-LangGraph-FastAPI
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create:

```
.env
```

Example:

```env
GOOGLE_API_KEY=your_google_api_key

CLIENT_URL=http://localhost:5173

EXPRESS_API_URL=http://localhost:3000/api

INTERNAL_SHARED_SECRET=your_shared_secret
```

---

# Running the Backend

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Server:

```
http://localhost:8000
```

---

# Security

The chat endpoint uses HMAC request verification.

The middleware validates:

- Request signature
- Timestamp freshness
- Shared secret integrity

Protection includes:

- Replay attack prevention
- Timing attack resistant comparison

---

# Design Principles

## Separation of Concerns

The project separates:

### API Layer

Responsible for:

- HTTP requests
- Authentication
- Streaming responses


### Graph Layer

Responsible for:

- AI workflow orchestration


### Prompt Layer

Responsible for:

- Assistant behavior


### Tool Layer

Responsible for:

- External actions


### Retrieval Layer

Responsible for:

- Knowledge enrichment


### Model Layer

Responsible for:

- LLM provider interaction

---

# Future Improvements

The architecture supports future additions:

## Advanced Agent Loop

Move from:

```
Plan -> Execute -> Respond
```

towards:

```
Observe
   |
Reason
   |
Act
   |
Observe
   |
Refine
```

---

## Persistent Memory

Possible additions:

- User learning history
- Previous solutions
- Coding patterns
- Personalized teaching

---

## Production Retrieval

Replace current retrieval implementation with:

- MongoDB Atlas Vector Search
- Dedicated knowledge database
- Embedding pipeline

---

## Observability

Future monitoring:

- LangSmith tracing
- Request latency tracking
- Token usage analytics
- Failure monitoring

---

# Current Status

The backend currently provides:

✅ FastAPI API layer  
✅ LangGraph orchestration  
✅ Gemini integration  
✅ Intent-based routing  
✅ Context management  
✅ Retrieval pipeline  
✅ Tool execution integration  
✅ SSE streaming responses  
✅ Secure request validation  

The architecture is prepared for future expansion into a more advanced autonomous coding assistant system.

---

# Author

TalentIQ AI Assistant Backend

Built using FastAPI + LangGraph + Gemini
