from sqlalchemy import func
from sqlalchemy import String,  DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db_config import Base


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    to_email: Mapped[str] = mapped_column(String)
    template_name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)  # "success" or "failed"
    payload: Mapped[dict] = mapped_column(JSON)
    send_by: Mapped[str | None] = mapped_column(String, nullable=True)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (f"EmailLog(id={self.id}, to_email={self.to_email}, template_name={self.template_name}, status={self.status}, " 
               "send_by={self.send_by}, user_id={self.user_id}, error_message={self.error_message}, timestamp={self.timestamp})")
