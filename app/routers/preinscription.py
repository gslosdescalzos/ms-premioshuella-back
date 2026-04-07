from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin_user, get_current_user, get_db
from app.exceptions import ConflictError, NotFoundError
from app.schemas.preinscription import PreinscriptionCreate, PreinscriptionResponse
from app.services.preinscription import (
    create_preinscription,
    get_all_preinscriptions,
    to_preinscription_response,
)

router = APIRouter(tags=["Preinscriptions"])


@router.post(
    "/preinscription",
    response_model=PreinscriptionResponse,
    summary="Submit a preinscription",
    status_code=status.HTTP_201_CREATED,
)
def create_preinscription_route(
    body: PreinscriptionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        preinscription = create_preinscription(db, current_user["user_id"], body)
        return to_preinscription_response(preinscription)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)


@router.get(
    "/preinscription",
    response_model=list[PreinscriptionResponse],
    summary="List all preinscriptions (admin only)",
    status_code=status.HTTP_200_OK,
)
def list_preinscriptions(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin_user),
):
    preinscriptions = get_all_preinscriptions(db)
    return [to_preinscription_response(preinscription) for preinscription in preinscriptions]