from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin_user, get_current_user, get_db
from app.exceptions import ConflictError, NotFoundError
from app.schemas.vote import VoteCountResponse, VoteResponse
from app.services.vote import create_vote, get_votes_by_category

router = APIRouter(tags=["Votes"])


@router.post(
    "/category/{category_id}/participant/{participant_id}/vote",
    response_model=VoteResponse,
    summary="Vote for a participant in a category",
    status_code=status.HTTP_201_CREATED,
)
def vote(
    category_id: int,
    participant_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        return create_vote(db, current_user["user_id"], category_id, participant_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.get(
    "/votes",
    response_model=list[VoteCountResponse],
    summary="List vote counts by category (admin only)",
    status_code=status.HTTP_200_OK,
)
def list_votes(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin_user),
):
    return get_votes_by_category(db)
