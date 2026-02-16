from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Participation(Base):
    __tablename__ = "participation"
    __table_args__ = (
        UniqueConstraint("profile_id", "category_id", name="uq_participation_profile_category"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profile.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=False)
    content_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_scout: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None)
    scout_group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    participant_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    participant_surname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_finalist: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="participations")
    category: Mapped["Category"] = relationship("Category", back_populates="participations")
    votes: Mapped[list["InitialVote"]] = relationship("InitialVote", back_populates="participation")
