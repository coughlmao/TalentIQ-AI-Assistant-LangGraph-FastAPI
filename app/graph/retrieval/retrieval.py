# app/graph/retrieval/retrieval.py

from langchain_core.documents import Document

from app.graph.retrieval.repository import KnowledgeRepository
from app.graph.state import GraphState
from app.logger import logger

# Global singleton repository instance to prevent recurrent file I/O operations
_repo = KnowledgeRepository()


async def retrieve_relevant_docs(state: GraphState) -> list[Document]:
    """
    Business rules translation engine. Inspects the incoming GraphState
    problem metadata context tags and fetches matching items from the Repository.
    """
    prob_context = state.get("problem_context") or {}

    # Safely gather tags from problem metadata structure
    search_tags: list[str] = prob_context.get("tags", [])

    # Fallback: add the problem title or id as a tag if explicit tags are empty
    if not search_tags and "title" in prob_context:
        search_tags.append(prob_context["title"])
    if not search_tags and "id" in prob_context:
        search_tags.append(prob_context["id"])

    logger.info("Retrieval service querying repository with tags: %s", search_tags)

    return await _repo.find_by_tags(search_tags)
