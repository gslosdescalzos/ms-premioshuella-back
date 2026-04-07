from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Preinscription(Base):
    __tablename__ = "preinscription"
    __table_args__ = (
        UniqueConstraint("profile_id", name="uq_preinscription_profile"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profile.id"), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    categories: Mapped[list[int]] = mapped_column(JSON, nullable=False)
    is_scout_group: Mapped[bool] = mapped_column(Boolean, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="preinscriptions")