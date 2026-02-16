from sqlalchemy.orm import Session

from app.exceptions import ConflictError
from app.models.newsletter import Newsletter


def subscribe(db: Session, email: str) -> Newsletter:
    existing = db.query(Newsletter).filter(Newsletter.email == email).first()
    if existing is not None:
        raise ConflictError("Email already subscribed")

    entry = Newsletter(email=email)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
