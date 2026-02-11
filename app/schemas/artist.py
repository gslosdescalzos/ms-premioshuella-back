from pydantic import BaseModel, EmailStr


class ArtistCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    comments: str | None = None


class ArtistResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    comments: str | None = None

    model_config = {"from_attributes": True}
