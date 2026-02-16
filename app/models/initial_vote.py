from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InitialVote(Base):
    __tablename__ = "initial_vote"
    __table_args__ = (
        UniqueConstraint("profile_id", "category_id", name="uq_initial_vote_profile_category"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profile.id"), nullable=False)
    participation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("participation.id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="votes")
    participation: Mapped["Participation"] = relationship("Participation", back_populates="votes")
    category: Mapped["Category"] = relationship("Category", back_populates="votes")
