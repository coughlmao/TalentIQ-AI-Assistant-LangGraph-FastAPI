# app/graph/tools/tool_schema.py

from pydantic import BaseModel, Field


class ExecuteCodeArgs(BaseModel):
    """
    Schema for executing a student's Python code inside an isolated sandbox environment
    """

    code: str = Field(
        ...,
        description="The complex Python code snippet submitted by the student that needs execution or syntax validation.",
    )
    problem_id: str = Field(
        ...,
        description="The unique identification string of the current coding problem (e.g., 'two-sum').",
    )


class RequestHintArgs(BaseModel):
    """
    Schema for requesting an incremental pedagogical hint without running any code
    """

    problem_id: str = Field(
        ...,
        description="The unique identification string of the current coding problem",
    )
    hint_level: int = Field(
        default=1,
        description="The progressive depth of the hint requested (1=conceptual direction, 2=strategy setup)",
    )
