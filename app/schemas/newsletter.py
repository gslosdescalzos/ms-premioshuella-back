from datetime import datetime

from pydantic import BaseModel, EmailStr


class NewsletterRequest(BaseModel):
    email: EmailStr


class NewsletterResponse(BaseModel):
    id: int
    email: str
    subscribed_at: datetime

    model_config = {"from_attributes": True}
