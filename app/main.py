import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, artist, category, participation, stand, vote


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield


app = FastAPI(
    title="Premios Huella API",
    description="API for managing the Premios Huella awards platform",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Auth", "description": "Authentication via Google SSO"},
        {"name": "Categories", "description": "Category management"},
        {"name": "Participations", "description": "Participation and participant management"},
        {"name": "Votes", "description": "Voting management"},
        {"name": "Artists", "description": "Artist registration and listing"},
        {"name": "Stands", "description": "Stand registration and listing"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(category.router, prefix=settings.API_V1_PREFIX)
app.include_router(participation.router, prefix=settings.API_V1_PREFIX)
app.include_router(vote.router, prefix=settings.API_V1_PREFIX)
app.include_router(artist.router, prefix=settings.API_V1_PREFIX)
app.include_router(stand.router, prefix=settings.API_V1_PREFIX)
