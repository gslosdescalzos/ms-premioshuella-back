from datetime import datetime

from pydantic import BaseModel, EmailStr


class ContactRequest(BaseModel):
    nombre: str
    email: EmailStr
    mensaje: str


class ContactResponse(BaseModel):
    id: int
    nombre: str
    email: str
    mensaje: str
    created_at: datetime

    model_config = {"from_attributes": True}
