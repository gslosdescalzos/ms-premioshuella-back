from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.category import CategoryResponse
from app.services.category import get_all_categories

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="List all categories",
    status_code=status.HTTP_200_OK,
)
def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)
