from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    google_id: str
    username: str
    email: str
    created_at: datetime
    can_participate: bool

    model_config = {"from_attributes": True}
