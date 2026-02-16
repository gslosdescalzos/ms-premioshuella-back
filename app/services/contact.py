from sqlalchemy.orm import Session

from app.models.contact import Contact


def create_contact(db: Session, nombre: str, email: str, mensaje: str) -> Contact:
    entry = Contact(nombre=nombre, email=email, mensaje=mensaje)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
