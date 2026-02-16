from datetime import datetime

from pydantic import BaseModel


class ParticipationResponse(BaseModel):
    id: int
    profile_id: str
    category_id: int
    content_url: str | None = None
    comments: str | None = None
    is_scout: bool | None = None
    scout_group: str | None = None
    phone: str | None = None
    participant_name: str | None = None
    participant_surname: str | None = None
    is_finalist: bool
    submitted_at: datetime

    model_config = {"from_attributes": True}
