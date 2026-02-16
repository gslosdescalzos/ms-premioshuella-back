from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.colabora import ColaboraRequest, ColaboraResponse
from app.services.colabora import create_colabora

router = APIRouter(tags=["Colabora"])


@router.post(
    "/colabora",
    response_model=ColaboraResponse,
    summary="Submit a collaboration request",
    status_code=status.HTTP_201_CREATED,
)
def submit_colabora(
    body: ColaboraRequest,
    db: Session = Depends(get_db),
):
    return create_colabora(
        db,
        body.nombre,
        body.apellidos,
        body.email,
        body.telefono,
        body.comentarios,
    )
