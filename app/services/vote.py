from sqlalchemy import func
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.category import Category
from app.models.initial_vote import InitialVote
from app.models.participation import Participation


def create_vote(
    db: Session, user_id: str, category_id: int, participant_id: int
) -> InitialVote:
    participation = (
        db.query(Participation)
        .filter(
            Participation.id == participant_id,
            Participation.category_id == category_id,
        )
        .first()
    )
    if participation is None:
        raise NotFoundError("Participation not found for this participant in this category")

    existing_vote = (
        db.query(InitialVote)
        .filter(
            InitialVote.profile_id == user_id,
            InitialVote.category_id == category_id,
        )
        .first()
    )
    if existing_vote is not None:
        raise ConflictError("User has already voted in this category")

    vote = InitialVote(
        profile_id=user_id,
        participation_id=participation.id,
        category_id=category_id,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote


def get_votes_by_category(db: Session) -> list[dict]:
    results = (
        db.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            Participation.id.label("participation_id"),
            func.count(InitialVote.id).label("vote_count"),
        )
        .join(Participation, Participation.category_id == Category.id)
        .outerjoin(InitialVote, InitialVote.participation_id == Participation.id)
        .group_by(
            Category.id,
            Category.name,
            Participation.id,
        )
        .all()
    )

    return [
        {
            "category_id": row.category_id,
            "category_name": row.category_name,
            "participation_id": row.participation_id,
            "vote_count": row.vote_count,
        }
        for row in results
    ]
