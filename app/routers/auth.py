from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.dependencies import get_db
from app.schemas.auth import AuthURLResponse, TokenResponse
from app.services.auth import (
    create_access_token,
    get_or_create_user,
    get_user_by_google_id,
    oauth,
)

router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    response_model=AuthURLResponse,
    summary="Initiate Google login",
    status_code=status.HTTP_200_OK,
)
async def login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    authorization_url = await oauth.google.create_authorization_url(redirect_uri, state="login")
    return AuthURLResponse(authorization_url=authorization_url["url"])


@router.post(
    "/signup",
    response_model=AuthURLResponse,
    summary="Initiate Google signup",
    status_code=status.HTTP_200_OK,
)
async def signup(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    authorization_url = await oauth.google.create_authorization_url(redirect_uri, state="signup")
    return AuthURLResponse(authorization_url=authorization_url["url"])


@router.get(
    "/auth/google/callback",
    response_model=TokenResponse,
    summary="Google OAuth2 callback",
    status_code=status.HTTP_200_OK,
)
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not retrieve user info from Google",
        )

    google_id = user_info["sub"]
    email = user_info["email"]
    name = user_info.get("name", email)
    state = request.query_params.get("state", "login")

    if state == "signup":
        user = get_or_create_user(db, google_id=google_id, email=email, name=name)
    else:
        user = get_user_by_google_id(db, google_id=google_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not registered. Please sign up first.",
            )

    access_token = create_access_token(user, db)
    return TokenResponse(access_token=access_token)
