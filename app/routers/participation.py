import json

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin_user, get_current_user, get_db
from app.exceptions import ConflictError, NotFoundError
from app.models.category import Category
from app.schemas.participation import (
    ParticipationResponse,
    PresignUploadRequest,
    PresignUploadResponse,
)
from app.services.participation import (
    create_participation,
    get_all_participants,
    get_participants_by_category,
    to_participation_response,
)
from app.services.storage import generate_presigned_upload

router = APIRouter(tags=["Participations"])


@router.post(
    "/category/{category_id}/presign-upload",
    response_model=PresignUploadResponse,
    summary="Generate presigned URLs for S3 upload",
    status_code=status.HTTP_200_OK,
)
def presign_upload(
    category_id: int,
    body: PresignUploadRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    uploads = generate_presigned_upload(
        filenames=[f.filename for f in body.files],
        content_types=[f.content_type for f in body.files],
        category_name=category.name,
        user_id=current_user["user_id"],
    )
    return PresignUploadResponse(uploads=uploads)


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
    content_urls: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    content_urls_list: list[str] = []
    if content_urls:
        try:
            content_urls_list = json.loads(content_urls)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="content_urls must be a valid JSON array",
            )

    try:
        participation = create_participation(
            db,
            current_user["user_id"],
            category_id,
            comments,
            content_urls=content_urls_list or None,
            is_scout=is_scout,
            scout_group=scout_group,
            phone=phone,
            participant_name=participant_name,
            participant_surname=participant_surname,
        )
        return to_participation_response(participation)
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
        participations = get_participants_by_category(db, category_id)
        return [to_participation_response(p) for p in participations]
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
    participations = get_all_participants(db)
    return [to_participation_response(p) for p in participations]
