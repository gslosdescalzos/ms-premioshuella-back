from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.stand import StandCreate, StandResponse
from app.services.stand import create_stand, get_all_stands

router = APIRouter(prefix="/stand", tags=["Stands"])


@router.post(
    "",
    response_model=StandResponse,
    summary="Register a new stand",
    status_code=status.HTTP_201_CREATED,
)
def register_stand(
    data: StandCreate,
    db: Session = Depends(get_db),
) -> StandResponse:
    return create_stand(db, data)


@router.get(
    "",
    response_model=list[StandResponse],
    summary="List all stands",
    status_code=status.HTTP_200_OK,
)
def list_stands(db: Session = Depends(get_db)) -> list[StandResponse]:
    return get_all_stands(db)
