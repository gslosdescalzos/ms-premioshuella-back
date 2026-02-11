from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.participation import Participation
from app.models.user import User
from app.services.file import save_files


def create_participation(
    db: Session,
    user_id: int,
    category_id: int,
    comments: str | None,
    files: list[UploadFile],
) -> Participation:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    existing = (
        db.query(Participation)
        .filter(
            Participation.user_id == user_id,
            Participation.category_id == category_id,
        )
        .first()
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has a participation in this category",
        )

    content_url = None
    if files:
        content_url = save_files(files, category.name, user.username)

    participation = Participation(
        user_id=user_id,
        category_id=category_id,
        content_url=content_url,
        comments=comments,
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation


def get_participants_by_category(db: Session, category_id: int) -> list[User]:
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return (
        db.query(User)
        .join(Participation, Participation.user_id == User.id)
        .filter(Participation.category_id == category_id)
        .all()
    )


def get_all_participants(db: Session) -> list[User]:
    return (
        db.query(User)
        .join(Participation, Participation.user_id == User.id)
        .distinct()
        .all()
    )
