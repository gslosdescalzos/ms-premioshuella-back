from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.category import Category
from app.models.preinscription import Preinscription
from app.models.profile import Profile
from app.schemas.preinscription import PreinscriptionCreate, PreinscriptionResponse


def _get_or_create_profile(db: Session, user_id: str) -> Profile:
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if profile is None:
        profile = Profile(id=user_id)
        db.add(profile)
        db.flush()
    return profile


def create_preinscription(
    db: Session,
    user_id: str,
    payload: PreinscriptionCreate,
) -> Preinscription:
    _get_or_create_profile(db, user_id)

    existing = (
        db.query(Preinscription)
        .filter(Preinscription.profile_id == user_id)
        .first()
    )
    if existing is not None:
        raise ConflictError("User already has a preinscription")

    category_ids = sorted(set(payload.categories))
    found_categories = (
        db.query(Category.id)
        .filter(Category.id.in_(category_ids))
        .all()
    )
    found_category_ids = {category_id for (category_id,) in found_categories}
    missing_category_ids = [category_id for category_id in category_ids if category_id not in found_category_ids]
    if missing_category_ids:
        raise NotFoundError(f"Categories not found: {', '.join(str(category_id) for category_id in missing_category_ids)}")

    preinscription = Preinscription(
        profile_id=user_id,
        username=payload.username,
        surname=payload.surname,
        categories=category_ids,
        is_scout_group=payload.is_scout_group,
    )
    db.add(preinscription)
    db.commit()
    db.refresh(preinscription)
    return preinscription


def get_all_preinscriptions(db: Session) -> list[Preinscription]:
    return db.query(Preinscription).order_by(Preinscription.submitted_at.desc()).all()


def to_preinscription_response(preinscription: Preinscription) -> PreinscriptionResponse:
    return PreinscriptionResponse(
        id=preinscription.id,
        profile_id=preinscription.profile_id,
        username=preinscription.username,
        surname=preinscription.surname,
        categories=preinscription.categories,
        is_scout_group=preinscription.is_scout_group,
        submitted_at=preinscription.submitted_at,
    )