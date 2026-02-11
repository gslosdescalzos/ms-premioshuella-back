from datetime import datetime

from pydantic import BaseModel


class VoteCreate(BaseModel):
    user_id: int


class VoteResponse(BaseModel):
    id: int
    user_id: int
    participation_id: int
    category_id: int
    creation_date: datetime

    model_config = {"from_attributes": True}


class VoteCountResponse(BaseModel):
    category_id: int
    category_name: str
    participation_id: int
    participant_username: str
    vote_count: int
