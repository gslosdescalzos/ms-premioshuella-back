from sqlalchemy.orm import Session

from app.models.stand import Stand
from app.schemas.stand import StandCreate


def create_stand(db: Session, data: StandCreate) -> Stand:
    stand = Stand(
        name=data.name,
        surname=data.surname,
        email=data.email,
        comments=data.comments,
    )
    db.add(stand)
    db.commit()
    db.refresh(stand)
    return stand


def get_all_stands(db: Session) -> list[Stand]:
    return db.query(Stand).order_by(Stand.id).all()
