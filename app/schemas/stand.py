from pydantic import BaseModel, EmailStr


class StandCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    comments: str | None = None


class StandResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    comments: str | None = None

    model_config = {"from_attributes": True}
