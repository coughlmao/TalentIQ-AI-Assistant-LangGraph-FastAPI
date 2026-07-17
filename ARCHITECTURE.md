# ARCHITECTURE.md: AI Agent Execution Pipeline

## Execution Lifecycle Topology

The runtime orchestrator processes inputs through a linear data-enrichment graph using LangGraph.

START ──> route_intent ──> conversation_context ──> retrieve_documents ──> tool_planning ──> tool_execution ──> build_prompt ──> generate_response ──> END

## Subsystem Responsibilities

### 1. Intent & Context Layer

- `route_intent`: Deterministic expression matching engine used to tag user input intent.
- `conversation_context`: Prunes and limits running context arrays to optimize window management.

### 2. Knowledge Retrieval Domain

- `retrieve_documents`: A runtime adapter node querying the underlying abstraction engine.
- `KnowledgeRepository`: A decoupled storage boundary. Uses local JSON structures to maintain static pedagogical teaching concepts. Swapping out JSON storage for MongoDB requires updates *only* inside this data boundaries class.

### 3. Tool Sandboxing

- `tool_planning`: Constructs structured action requests (`{action, arguments}`) or returns `None`.
- `tool_execution`: Safely interfaces outside the graph context with the Express execution backend runner via HTTP.

### 4. Generation Pipeline

- `build_prompt`: The single point of assembly. Merges history context, domain assets, and tool feedback execution data directly into a unified message structure payload.
- `generate_response`: Executes LLM processing loops. Emits token stream cycles directly down to client channels using `astream_events`.
