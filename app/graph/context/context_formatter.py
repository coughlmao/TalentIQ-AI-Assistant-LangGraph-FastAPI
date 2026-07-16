from typing import Any

from langchain_core.documents import Document
from langchain_core.messages import SystemMessage


def format_context_segments(
    retrieved_docs: list[Document],
    tool_results: list[dict[str, Any]],
) -> list[str]:
    """
    Transforms raw retrieved documents and sandbox tool output maps into
    clean Markdown segment blocks for LLM injection.
    """
    segments: list[str] = []

    # 1. Format Retrieval Knowledge Base Hits
    if retrieved_docs:
        segments.append("## Supplemental Domain Documentation")
        for idx, doc in enumerate(retrieved_docs, 1):
            source = doc.metadata.get("source", "unknown")
            segments.append(f"### Reference [{idx}] (Source: {source})")
            segments.append(doc.page_content)

    # 2. Format Execution Sandbox Run Outputs
    if tool_results:
        segments.append("## Execution Sandbox Tool Outputs")
        for idx, res in enumerate(tool_results, 1):
            status = "Success" if res.get("success") else "Failed"
            segments.append(f"### Tool Execution Action [{idx}] Status: {status}")
            if res.get("stdout"):
                segments.append(f"Standard Output:\n```\n{res['stdout']}\n```")
            if res.get("stderr"):
                segments.append(f"Standard Error:\n```\n{res['stderr']}\n```")

    return segments


def build_enrichment_directive(
    retrieved_docs: list[Document],
    tool_results: list[dict[str, Any]],
) -> SystemMessage | None:
    """
    Assembles formatted segments into a single isolated SystemMessage directive.
    Returns None if there is no context to inject, avoiding wasted tokens.
    """
    segments = format_context_segments(retrieved_docs, tool_results)
    if not segments:
        return None

    return SystemMessage(
        content=(
            "INJECTED REAL-TIME CONTEXT:\n"
            "Use the following real-time data to ground your suggestions. "
            "Prioritize verification code outputs or core document strategies if present.\n\n"
            f"{'\n\n'.join(segments)}"
        )
    )