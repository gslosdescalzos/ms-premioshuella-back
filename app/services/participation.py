from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.category import Category
from app.models.participation import Participation
from app.models.participation_file import ParticipationFile
from app.models.profile import Profile
from app.schemas.participation import ParticipationFileResponse, ParticipationResponse
from app.services.storage import extract_storage_key, generate_presigned_download


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
    *,
    content_urls: list[str] | None = None,
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

    participation = Participation(
        profile_id=user_id,
        category_id=category_id,
        comments=comments,
        is_scout=is_scout,
        scout_group=scout_group,
        phone=phone,
        participant_name=participant_name,
        participant_surname=participant_surname,
    )
    db.add(participation)
    db.flush()

    if content_urls:
        for url_or_key in content_urls:
            storage_key = extract_storage_key(url_or_key)
            pf = ParticipationFile(
                participation_id=participation.id,
                profile_id=user_id,
                category_id=category_id,
                content_url=storage_key,
            )
            db.add(pf)

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


def to_participation_response(participation: Participation) -> ParticipationResponse:
    files_resp: list[ParticipationFileResponse] = []
    for f in participation.files:
        try:
            key = extract_storage_key(f.content_url)
            download_url = generate_presigned_download(key)
            files_resp.append(ParticipationFileResponse(id=f.id, content_url=download_url))
        except Exception:
            files_resp.append(ParticipationFileResponse(id=f.id, content_url=""))
    return ParticipationResponse(
        id=participation.id,
        profile_id=participation.profile_id,
        category_id=participation.category_id,
        comments=participation.comments,
        is_scout=participation.is_scout,
        scout_group=participation.scout_group,
        phone=participation.phone,
        participant_name=participation.participant_name,
        participant_surname=participation.participant_surname,
        is_finalist=participation.is_finalist,
        submitted_at=participation.submitted_at,
        files=files_resp,
    )
