from datetime import datetime

from pydantic import BaseModel, EmailStr


class ColaboraRequest(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str | None = None
    comentarios: str | None = None


class ColaboraResponse(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: str
    telefono: str | None = None
    comentarios: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
