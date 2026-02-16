from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin_user, get_current_user, get_db
from app.exceptions import ConflictError, NotFoundError
from app.schemas.participation import ParticipationResponse
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
    comments: str | None = Form(None),
    is_scout: bool = Form(...),
    scout_group: str | None = Form(None),
    phone: str = Form(...),
    participant_name: str | None = Form(None),
    participant_surname: str | None = Form(None),
    files: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        return create_participation(
            db,
            current_user["user_id"],
            category_id,
            comments,
            files,
            is_scout=is_scout,
            scout_group=scout_group,
            phone=phone,
            participant_name=participant_name,
            participant_surname=participant_surname,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.get(
    "/category/{category_id}/participant",
    response_model=list[ParticipationResponse],
    summary="List participants by category (admin only)",
    status_code=status.HTTP_200_OK,
)
def list_participants_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin_user),
):
    try:
        return get_participants_by_category(db, category_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get(
    "/participant",
    response_model=list[ParticipationResponse],
    summary="List all participants (admin only)",
    status_code=status.HTTP_200_OK,
)
def list_all_participants(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin_user),
):
    return get_all_participants(db)
