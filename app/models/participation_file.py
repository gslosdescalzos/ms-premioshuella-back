from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ParticipationFile(Base):
    __tablename__ = "participation_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    participation_id: Mapped[int] = mapped_column(Integer, ForeignKey("participation.id"), nullable=False)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profile.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=False)
    content_url: Mapped[str] = mapped_column(Text, nullable=False)

    participation: Mapped["Participation"] = relationship("Participation", back_populates="files")
