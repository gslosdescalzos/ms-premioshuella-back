from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import category, colabora, contact, newsletter, participation, vote

app = FastAPI(
    title="Premios Huella API",
    description="API for managing the Premios Huella awards platform",
    version="1.0.0",
    openapi_tags=[
        {"name": "Categories", "description": "Category management"},
        {"name": "Participations", "description": "Participation and participant management"},
        {"name": "Votes", "description": "Voting management"},
        {"name": "Newsletter", "description": "Newsletter subscription"},
        {"name": "Contact", "description": "Contact form"},
        {"name": "Colabora", "description": "Collaboration requests"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category.router, prefix=settings.API_V1_PREFIX)
app.include_router(participation.router, prefix=settings.API_V1_PREFIX)
app.include_router(vote.router, prefix=settings.API_V1_PREFIX)
app.include_router(newsletter.router, prefix=settings.API_V1_PREFIX)
app.include_router(contact.router, prefix=settings.API_V1_PREFIX)
app.include_router(colabora.router, prefix=settings.API_V1_PREFIX)
