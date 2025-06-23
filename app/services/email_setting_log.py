from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import EmailSettingLogRepository
from app.schemas import EmailLogSchema


class EmailSettingLogService:
    @staticmethod
    async def is_store_failed_email_sending(
        template_name: str, db: AsyncSession
    ) -> bool:
        return await EmailSettingLogRepository.is_store_failed_email_sending(
            template_name, db
        )

    @staticmethod
    async def save_failed_email_sending_log(
        log_data: EmailLogSchema, db: AsyncSession
    ) -> bool:
        return await EmailSettingLogRepository.store_failed_email_sending_log(
            log_data, db
        )

    @staticmethod
    async def get_failed_email_sending_logs(db: AsyncSession) -> list[EmailLogSchema]:
        return await EmailSettingLogRepository.get_failed_email_sending_logs(db)

    @staticmethod
    async def get_failed_email_sending_log_by_id(
        log_id: int, db: AsyncSession
    ) -> EmailLogSchema:
        return await EmailSettingLogRepository.get_failed_email_sending_log_by_id(
            log_id, db
        )

    @staticmethod
    async def delete_failed_email_sending_log_by_id(
        log_id: int, db: AsyncSession
    ) -> bool:
        return await EmailSettingLogRepository.delete_failed_email_sending_log_by_id(
            log_id, db
        )

    @staticmethod
    async def resend_failed_email_sending_log_by_id(
        log_id: int, db: AsyncSession
    ) -> bool:
        email_log_data = (
            await EmailSettingLogRepository.get_failed_email_sending_log_by_id(
                log_id, db
            )
        )
        from app.services.email_service import EmailService

        await EmailService.send_email(
            email_log_data.to_email,
            email_log_data.subject,
            email_log_data.template_name,
            email_log_data.payload,
            email_log_data.user_id,
            False,
            db,
        )
        await EmailSettingLogRepository.delete_failed_email_sending_log_by_id(
            log_id, db
        )
