from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import EmailSettingLogRepository
from app.schemas import EmailLogSchema

class EmailSettingLogService:
    @staticmethod
    async def is_store_failed_email_sending(log_data: EmailLogSchema, db: AsyncSession) -> bool:
        return await EmailSettingLogRepository.is_store_failed_email_sending(log_data, db)
    
    @staticmethod
    async def save_failed_email_sending_log(template_name: str, db: AsyncSession) -> bool:
        return False