from sqlalchemy.orm import Session

from app.models.colabora import Colabora


def create_colabora(
    db: Session,
    nombre: str,
    apellidos: str,
    email: str,
    telefono: str | None,
    comentarios: str | None,
) -> Colabora:
    entry = Colabora(
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        telefono=telefono,
        comentarios=comentarios,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
