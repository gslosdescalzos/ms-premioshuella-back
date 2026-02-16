from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.category import CategoryResponse
from app.services.category import get_all_categories, get_category_by_name

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="List all categories",
    status_code=status.HTTP_200_OK,
)
def list_categories(db: Session = Depends(get_db), name: str | None = None):
    if name is not None:
        category = get_category_by_name(db, name)
        return [category] if category else []
    return get_all_categories(db)
