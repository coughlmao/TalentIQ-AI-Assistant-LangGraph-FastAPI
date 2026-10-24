# ARCHITECTURE.md: AI Agent Execution Pipeline

## Execution Lifecycle Topology

The runtime orchestrator processes inputs through a linear data-enrichment graph using LangGraph.

START ──> route_intent ──> conversation_context ──> retrieve_documents ──> tool_planning ──> tool_execution ──> build_prompt ──> generate_response ──> END

## Subsystem Responsibilities

### 1. Intent & Context Layer

- `route_intent`: Deterministic expression matching engine used to tag user input intent.
- `conversation_context`: Prunes and limits running context arrays to optimize window management.

### State Flow

`GraphState` is the shared typed state passed through the graph. The API initializes
the request fields (`chat_history`, `latest_user_message`, `problem_context`, and
`execution_context`) plus empty workflow fields. The principal state fields are
populated or consumed as follows:

- `route_intent` populates `intent`.
- `conversation_context` populates `conversation_context`.
- `retrieve_documents` populates `retrieved_documents`.
- `tool_planning` populates `tool_plan`.
- `tool_execution` populates `tool_results` for executable code plans.
- `build_prompt` populates `llm_messages`.
- `generate_response` populates `final_response`.

### 2. Knowledge Retrieval Domain

- `retrieve_documents`: A runtime adapter node querying the underlying abstraction engine.
- `KnowledgeRepository`: A decoupled storage boundary. It currently loads local JSON structures and performs tag-intersection matching for static pedagogical concepts. A different store can be introduced behind this boundary if it preserves the repository interface.

### 3. Tool Execution Boundary

- `tool_planning`: Constructs structured action requests (`{action, arguments}`) or returns `None`. It currently plans `execute_code` for debug requests and `request_hint` for hint requests.
- `tool_execution`: Executes only `execute_code` plans by calling the external Express code-execution service over HTTP. Planned `request_hint` actions are currently skipped; hint behavior is supplied by the prompt layer. This backend does not by itself establish the external service's isolation, resource limits, or execution restrictions.

### 4. Generation Pipeline

- `build_prompt`: Assembles the final message payload from conversation context, problem and execution context, retrieved knowledge, and available tool results.
- `generate_response`: Invokes the configured Gemini model inside the graph. The outer SSE adapter observes LangChain events with `astream_events` and forwards emitted chat-model chunks to the client. Progressive delivery depends on events emitted by the provider and the deployment path.

### Failure and Boundary Notes

- HMAC verification runs at the API boundary before the chat graph starts.
- Retrieval failures and model failures occur inside the streamed graph execution path.
- Express request failures are converted into unsuccessful tool results for prompt context.
- The API emits an SSE `error` event when graph execution raises an exception; it does not provide a separate retry or recovery loop.
