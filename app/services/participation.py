from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.category import Category
from app.models.participation import Participation
from app.models.profile import Profile
from app.services.storage import upload_files


def _get_or_create_profile(db: Session, user_id: str) -> Profile:
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if profile is None:
        profile = Profile(id=user_id)
        db.add(profile)
        db.flush()
    return profile


def create_participation(
    db: Session,
    user_id: str,
    category_id: int,
    comments: str | None,
    files: list[UploadFile],
    *,
    is_scout: bool,
    scout_group: str | None = None,
    phone: str,
    participant_name: str | None = None,
    participant_surname: str | None = None,
) -> Participation:
    profile = _get_or_create_profile(db, user_id)

    if not profile.can_participate:
        raise ConflictError("User is not allowed to participate")

    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise NotFoundError("Category not found")

    existing = (
        db.query(Participation)
        .filter(
            Participation.profile_id == user_id,
            Participation.category_id == category_id,
        )
        .first()
    )
    if existing is not None:
        raise ConflictError("User already has a participation in this category")

    content_url = None
    if files:
        content_url = upload_files(files, category.name, user_id)

    participation = Participation(
        profile_id=user_id,
        category_id=category_id,
        content_url=content_url,
        comments=comments,
        is_scout=is_scout,
        scout_group=scout_group,
        phone=phone,
        participant_name=participant_name,
        participant_surname=participant_surname,
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation


def get_participants_by_category(db: Session, category_id: int) -> list[Participation]:
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise NotFoundError("Category not found")

    return (
        db.query(Participation)
        .filter(Participation.category_id == category_id)
        .all()
    )


def get_all_participants(db: Session) -> list[Participation]:
    return db.query(Participation).all()
