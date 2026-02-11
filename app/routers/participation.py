from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin_user, get_current_user, get_db
from app.schemas.participation import ParticipantResponse, ParticipationResponse
from app.services.participation import (
    create_participation,
    get_all_participants,
    get_participants_by_category,
)

router = APIRouter(tags=["Participations"])


@router.post(
    "/category/{category_id}/participate",
    response_model=ParticipationResponse,
    summary="Submit a participation for a category",
    status_code=status.HTTP_201_CREATED,
)
def participate(
    category_id: int,
    user_id: int = Form(...),
    comments: str | None = Form(None),
    files: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    return create_participation(db, user_id, category_id, comments, files)


@router.get(
    "/category/{category_id}/participant",
    response_model=list[ParticipantResponse],
    summary="List participants by category (admin only)",
    status_code=status.HTTP_200_OK,
)
def list_participants_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin_user),
):
    return get_participants_by_category(db, category_id)


@router.get(
    "/participant",
    response_model=list[ParticipantResponse],
    summary="List all participants (admin only)",
    status_code=status.HTTP_200_OK,
)
def list_all_participants(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin_user),
):
    return get_all_participants(db)
