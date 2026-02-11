from pydantic import BaseModel


class AuthURLResponse(BaseModel):
    authorization_url: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
