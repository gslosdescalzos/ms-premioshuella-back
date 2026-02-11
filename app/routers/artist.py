from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.artist import ArtistCreate, ArtistResponse
from app.services.artist import create_artist, get_all_artists

router = APIRouter(prefix="/artist", tags=["Artists"])


@router.post(
    "",
    response_model=ArtistResponse,
    summary="Register a new artist",
    status_code=status.HTTP_201_CREATED,
)
def register_artist(
    data: ArtistCreate,
    db: Session = Depends(get_db),
) -> ArtistResponse:
    return create_artist(db, data)


@router.get(
    "",
    response_model=list[ArtistResponse],
    summary="List all artists",
    status_code=status.HTTP_200_OK,
)
def list_artists(db: Session = Depends(get_db)) -> list[ArtistResponse]:
    return get_all_artists(db)
