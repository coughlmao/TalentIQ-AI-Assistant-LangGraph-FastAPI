# app/graph/intents.py

from __future__ import annotations

from enum import StrEnum


class AssistantIntent(StrEnum):
    """
    Supported assistant capabilities

    This enum is intentionally small for now.
    More intents can be introduced incrementally
    without affecting the graph architecture
    """

    GENERAL = "general"

    HINT = "hint"

    DEBUG = "debug"

    REVIEW = "review"

    EXPLAIN = "explain"
