from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    can_participate: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    participations: Mapped[list["Participation"]] = relationship(
        "Participation", back_populates="profile"
    )
    votes: Mapped[list["InitialVote"]] = relationship(
        "InitialVote", back_populates="profile"
    )
