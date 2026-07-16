from langchain_core.documents import Document

from app.graph.state import GraphState


async def retrieve_relevant_docs(state:GraphState)->list[Document]:
    """
    Queries the vector store for domain knowledge matching the problem context.
    Currently returns mock documents to establish the pipeline interface.
    """
    prob=state.get("problem_context",{})
    title=prob.get("title","Unknown problem")
    
    # Simulating a vector database lookup response
    mock_doc=Document(
        page_content=f"Standard conceptual overview and edge cases for challenge:{title}",
        metadata={"source":"dsa_knowledge_base","topic":title},
    )
    
    return [mock_doc]
    