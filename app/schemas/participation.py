from datetime import datetime

from pydantic import BaseModel


class ParticipationResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    content_url: str | None = None
    comments: str | None = None
    is_finalist: bool
    submitted_at: datetime

    model_config = {"from_attributes": True}


class ParticipantResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}
