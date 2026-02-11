from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InitialVote(Base):
    __tablename__ = "initial_vote"
    __table_args__ = (UniqueConstraint("user_id", "category_id", name="uq_initial_vote_user_category"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    participation_id: Mapped[int] = mapped_column(Integer, ForeignKey("participation.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="votes")
    participation: Mapped["Participation"] = relationship("Participation", back_populates="votes")
    category: Mapped["Category"] = relationship("Category", back_populates="votes")
