from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Newsletter(Base):
    __tablename__ = "newsletter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    subscribed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
