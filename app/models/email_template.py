from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db_config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class EmailTemplateSetting(Base):
    __tablename__ = "email_template_settings"

    id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), primary_key=True ,
            default=uuid.uuid4, index=True
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    can_resend: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"EmailTemplateSetting(name={self.name}, can_resend={self.can_resend})"
