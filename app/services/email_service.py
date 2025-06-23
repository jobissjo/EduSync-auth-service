from email.message import EmailMessage
from typing import Union, Optional
import aiosmtplib
import ssl
from app.models import User, EmailSetting
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger_config import logger
from app.schemas import EmailLogSchema
from app.utils import render_email_template
from app.services.email_setting_log import EmailSettingLogService

class EmailService:
    @staticmethod
    async def get_email_setting(
        db: AsyncSession,
        user: Optional[User] = None,
        use_admin_email: bool = False,
        
    ) -> EmailSetting:
        if use_admin_email:
            query = select(EmailSetting).where(
                EmailSetting.is_admin_mail.is_(True)
            )
        else:
            query = select(EmailSetting).where(
                EmailSetting.is_active.is_(True), EmailSetting.user_id == user.id
            )
        result = await db.execute(query)
        print(result)
        return result.scalars().first()

    @staticmethod
    async def send_email(
        recipient: str,
        subject: str,
        template_name: str,
        template_data: dict[str, Union[str, int, bool]],
        user: Optional[User] = None,
        use_admin_email: bool = False,
        db: Optional[AsyncSession] = None,
    ):
        is_failed_email = False
        email_setting = await EmailService.get_email_setting(db, user, use_admin_email)
        email_body = await render_email_template(template_name, template_data)
        is_store_failed_email_sending = await EmailSettingLogService.is_store_failed_email_sending(template_name, db)
        ERROR_MESSAGE = "Failed to send email"
        if not email_setting:
            user = user.first_name if user else "admin"
            is_failed_email = True
            ERROR_MESSAGE = 'No email setting found for user'
            logger.error(f"Email setting not found for user")
            
        if not is_failed_email:
            EMAIL_HOST_NAME = email_setting.host
            EMAIL_HOST_PORT = email_setting.port
            EMAIL_HOST_USERNAME = email_setting.email
            EMAIL_HOST_PASSWORD = email_setting.password
            message = EmailMessage()

            message["From"] = EMAIL_HOST_USERNAME
            message["To"] = recipient
            message["subject"] = subject
            message.set_content(email_body, subtype="html")

            context = ssl.create_default_context()

            try:
                await aiosmtplib.send(
                    message,
                    hostname=EMAIL_HOST_NAME,
                    port=EMAIL_HOST_PORT,
                    username=EMAIL_HOST_USERNAME,
                    password=EMAIL_HOST_PASSWORD,
                    start_tls=True,
                    tls_context=context,
                    # For compatibility with older versions of aiosmtplib
                )
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                is_failed_email = True
                ERROR_MESSAGE = f"Failed to send email: {e}"

        if is_store_failed_email_sending and is_failed_email:
            user_id = email_setting.user_id if email_setting else user.id
            log_data = EmailLogSchema(to_email=recipient, template_name=template_name, status="failed", payload=template_data, send_by_id=user_id, user_id=user_id, error_message=ERROR_MESSAGE)
            await EmailSettingLogService.save_failed_email_sending_log(log_data, db)

    
    
