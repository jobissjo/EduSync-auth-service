from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import EmailTemplateSetting, EmailLog
from app.schemas import EmailLogSchema


class EmailSettingLogRepository:
    @staticmethod
    async def is_store_failed_email_sending(template_name: str, db: AsyncSession):
        query = select(EmailTemplateSetting).where(
            EmailTemplateSetting.name == template_name,
            EmailTemplateSetting.can_resend.is_(True),
        )
        result = await db.execute(query).scalar_one_or_none()
        return result is not None

    @staticmethod
    async def store_failed_email_sending_log(
        template_name: EmailLogSchema, db: AsyncSession
    ) -> bool:
        email_log = EmailLog(**template_name.model_dump())
        db.add(email_log)
        await db.commit()
        return True

    @staticmethod
    async def get_failed_email_sending_logs(db: AsyncSession) -> list[EmailLog]:
        query = select(EmailLog)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_failed_email_sending_log_by_id(
        log_id: int, db: AsyncSession
    ) -> EmailLog:
        query = select(EmailLog).where(EmailLog.id == log_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_failed_email_sending_log_by_id(
        log_id: int, db: AsyncSession
    ) -> bool:
        email_log = await EmailSettingLogRepository.get_failed_email_sending_log_by_id(
            log_id, db
        )
        if email_log is None:
            return False
        await db.delete(email_log)
        await db.commit()
        return True
