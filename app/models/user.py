from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    google_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    can_participate: Mapped[bool] = mapped_column(Boolean, default=True)

    admin: Mapped["Admin"] = relationship("Admin", back_populates="user", uselist=False)
    participations: Mapped[list["Participation"]] = relationship("Participation", back_populates="user")
    votes: Mapped[list["InitialVote"]] = relationship("InitialVote", back_populates="user")
