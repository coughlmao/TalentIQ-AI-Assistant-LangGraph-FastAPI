# app/graph/retrieval/repository.py

import json
from pathlib import Path
from typing import Any

from langchain_core.documents import Document

from app.logger import logger


class KnowledgeRepository:
    def __init__(self, data_dir: str | None = None):
        if data_dir is None:
            # Resolves cleanly to app/knowledge/data
            base_dir = Path(__file__).resolve().parents[2]
            self.data_dir = base_dir / "knowledge" / "data"
        else:
            self.data_dir = Path(data_dir)

        self._cached_documents: list[dict[str, Any]] = []
        self._load_local_repository()

    def _load_local_repository(self) -> None:
        """Loads and caches JSON domain assets during initialization."""
        if not self.data_dir.exists():
            logger.warning(
                "Knowledge repository data directory not found at %s", self.data_dir
            )
            return

        json_files = list(self.data_dir.glob("*.json"))
        for file_path in json_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    self._cached_documents.append(data)
            except Exception as e:
                logger.error(
                    "Failed to parse knowledge document %s: %s", file_path.name, e
                )

        logger.info(
            "KnowledgeRepository successfully indexed %d concepts.",
            len(self._cached_documents),
        )

    async def find_by_tags(self, tags: list[str]) -> list[Document]:
        """
        Scans cached concepts for any tag intersections.
        Returns native LangChain Document instances.
        """
        if not tags:
            return []

        normalized_query_tags = {tag.lower().strip() for tag in tags}
        matched_docs = []

        for doc_data in self._cached_documents:
            doc_tags = {t.lower().strip() for t in doc_data.get("tags", [])}
            # If there is any semantic overlap between problem tags and repository entries
            if normalized_query_tags.intersection(doc_tags):
                matched_docs.append(
                    Document(
                        page_content=doc_data.get("content", ""),
                        metadata={
                            "topic": doc_data.get("topic", "General"),
                            "source": "knowledge_base_repository",
                        },
                    )
                )
        return matched_docs
