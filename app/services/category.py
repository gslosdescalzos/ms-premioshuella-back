from sqlalchemy.orm import Session

from app.models.category import Category


def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()
