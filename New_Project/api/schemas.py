from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=24, pattern=r"^[A-Z0-9.^=\-]+$")
    thread_id: UUID


class ApprovalRequest(BaseModel):
    thread_id: UUID
    action: Literal["approve", "reject"]
