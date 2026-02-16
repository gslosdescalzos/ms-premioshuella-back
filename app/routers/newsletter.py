from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.exceptions import ConflictError
from app.schemas.newsletter import NewsletterRequest, NewsletterResponse
from app.services.newsletter import subscribe

router = APIRouter(tags=["Newsletter"])


@router.post(
    "/newsletter",
    response_model=NewsletterResponse,
    summary="Subscribe to the newsletter",
    status_code=status.HTTP_201_CREATED,
)
def subscribe_newsletter(
    body: NewsletterRequest,
    db: Session = Depends(get_db),
):
    try:
        return subscribe(db, body.email)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
