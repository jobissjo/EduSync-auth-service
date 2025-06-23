from sqlalchemy import func, ForeignKey
from sqlalchemy import String,  DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_config import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    to_email: Mapped[str] = mapped_column(String)
    template_name: Mapped[str] = mapped_column(String)
    subject: Mapped[str| None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String)  # "success" or "failed"
    payload: Mapped[dict] = mapped_column(JSON)
    send_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="email_logs", foreign_keys=[user_id])
    send_by: Mapped["User"] = relationship("User", back_populates="sent_email_logs", foreign_keys=[send_by_id])
    


    def __repr__(self):
        return (f"EmailLog(id={self.id}, to_email={self.to_email}, template_name={self.template_name}, status={self.status}, " 
               "send_by={self.send_by}, user_id={self.user_id}, error_message={self.error_message}, timestamp={self.timestamp})")
