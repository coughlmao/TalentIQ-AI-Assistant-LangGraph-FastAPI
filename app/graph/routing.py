# app/graph/routing.py

from __future__ import annotations

import re

from app.graph.intents import AssistantIntent

HINT_PATTERNS = (
    r"\bhint\b",
    r"\bstuck\b",
    r"\bnext step\b",
    r"\bnudge\b",
)

DEBUG_PATTERNS = (
    r"\berror\b",
    r"\bbug\b",
    r"\bdebug\b",
    r"\bfailing\b",
    r"\bexception\b",
    r"\bcompile\b",
    r"\bruntime\b",
    r"\bwrong answer\b",
    r"\btle\b",
    r"\bmle\b",
)

REVIEW_PATTERNS = (
    r"\breview\b",
    r"\boptimi[sz]e\b",
    r"\bcomplexity\b",
    r"\btime complexity\b",
    r"\bspace complexity\b",
    r"\bimprove\b",
)

EXPLAIN_PATTERNS = (
    r"\bexplain\b",
    r"\bwhat is\b",
    r"\bhow does\b",
    r"\bwhy\b",
)


def _matches(
    message: str,
    patterns: tuple[str, ...],
) -> bool:

    return any(re.search(pattern, message) for pattern in patterns)


def detect_intent(
    message: str,
) -> AssistantIntent:

    normalized = message.lower()

    if _matches(
        normalized,
        HINT_PATTERNS,
    ):
        return AssistantIntent.HINT

    if _matches(
        normalized,
        DEBUG_PATTERNS,
    ):
        return AssistantIntent.DEBUG

    if _matches(
        normalized,
        REVIEW_PATTERNS,
    ):
        return AssistantIntent.REVIEW

    if _matches(
        normalized,
        EXPLAIN_PATTERNS,
    ):
        return AssistantIntent.EXPLAIN

    return AssistantIntent.GENERAL
