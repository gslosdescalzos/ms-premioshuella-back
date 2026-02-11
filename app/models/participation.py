from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Participation(Base):
    __tablename__ = "participation"
    __table_args__ = (UniqueConstraint("user_id", "category_id", name="uq_participation_user_category"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=False)
    content_url: Mapped[str] = mapped_column(String(500), nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    is_finalist: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="participations")
    category: Mapped["Category"] = relationship("Category", back_populates="participations")
    votes: Mapped[list["InitialVote"]] = relationship("InitialVote", back_populates="participation")
