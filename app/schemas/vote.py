from datetime import datetime

from pydantic import BaseModel


class VoteResponse(BaseModel):
    id: int
    profile_id: str
    participation_id: int
    category_id: int
    creation_date: datetime

    model_config = {"from_attributes": True}


class VoteCountResponse(BaseModel):
    category_id: int
    category_name: str
    participation_id: int
    vote_count: int
