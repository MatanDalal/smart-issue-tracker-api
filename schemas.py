from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Define the structure of an Issue received from the user
class Issue(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"

    # Prevent empty values or values containing only spaces
    @field_validator("title", "description")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value


# Define the structure of an Issue returned by the API
class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved", "closed"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)