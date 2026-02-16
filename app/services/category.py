from sqlalchemy.orm import Session

from app.models.category import Category


def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def get_category_by_name(db: Session, name: str) -> Category | None:
    name = name.lower().strip()
    return db.query(Category).filter(Category.name == name).first()
