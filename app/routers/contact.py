from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.contact import ContactRequest, ContactResponse
from app.services.contact import create_contact

router = APIRouter(tags=["Contact"])


@router.post(
    "/contact",
    response_model=ContactResponse,
    summary="Submit a contact message",
    status_code=status.HTTP_201_CREATED,
)
def submit_contact(
    body: ContactRequest,
    db: Session = Depends(get_db),
):
    return create_contact(db, body.nombre, body.email, body.mensaje)
