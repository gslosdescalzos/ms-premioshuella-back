from datetime import datetime

from pydantic import BaseModel, Field


class PreinscriptionCreate(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    surname: str | None = Field(default=None, max_length=255)
    categories: list[int] = Field(min_length=1)
    is_scout_group: bool


class PreinscriptionResponse(BaseModel):
    id: int
    profile_id: str
    username: str
    surname: str | None = None
    categories: list[int]
    is_scout_group: bool
    submitted_at: datetime

    model_config = {"from_attributes": True}