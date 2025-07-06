from sqlalchemy.ext.asyncio import AsyncSession
from app.models import EmailSetting
from sqlalchemy.future import select

class EmailRepository:
    @staticmethod
    async def get_email_setting(
        db: AsyncSession,
        user_id: int
        
    ) -> EmailSetting:
        query = select(EmailSetting).where(
            EmailSetting.is_active.is_(True), EmailSetting.user_id == user_id
        )
        result = await db.execute(query)
        return result.scalars().first()


    @staticmethod
    async def get_admin_email_setting(db: AsyncSession) -> EmailSetting:
        query = select(EmailSetting).where(EmailSetting.is_admin_mail.is_(True))
        result = await db.execute(query)
        return result.scalars().first()