from datetime import datetime, timedelta

from authlib.integrations.starlette_client import OAuth
from jose import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.models.admin import Admin
from app.models.user import User

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def create_access_token(user: User, db: Session) -> str:
    is_admin = db.query(Admin).filter(Admin.user_id == user.id).first() is not None
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_admin": is_admin,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def get_or_create_user(db: Session, google_id: str, email: str, name: str) -> User:
    user = db.query(User).filter(User.google_id == google_id).first()
    if user is None:
        user = User(google_id=google_id, email=email, username=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user_by_google_id(db: Session, google_id: str) -> User | None:
    return db.query(User).filter(User.google_id == google_id).first()
