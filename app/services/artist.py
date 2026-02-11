from sqlalchemy.orm import Session

from app.models.artist import Artist
from app.schemas.artist import ArtistCreate


def create_artist(db: Session, data: ArtistCreate) -> Artist:
    artist = Artist(
        name=data.name,
        surname=data.surname,
        email=data.email,
        comments=data.comments,
    )
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


def get_all_artists(db: Session) -> list[Artist]:
    return db.query(Artist).order_by(Artist.id).all()
