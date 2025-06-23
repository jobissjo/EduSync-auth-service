from fastapi import APIRouter, Depends, Header, HTTPException
from app.core.security import verify_token_get_user
from app.schemas.email_schema import EmailRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_config import get_db
from typing import Annotated
from app.core.settings import setting
from app.services import EmailService, EmailSettingLogService
from app.repositories import UserRepository


router = APIRouter(prefix="/email", tags=["Auth"])


router.post("/send")
async def send_internal_email(
    payload: EmailRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    x_service_token: str = Header(...),
):
    if x_service_token != setting.EMAIL_SERVICE_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user = None
    if not payload.is_admin_email or payload.email_setting_user_id:
        user = await UserRepository.get_user_by_id(payload.user_id, db)

    EmailService.send_email(
        payload.to,
        payload.subject,
        payload.template_name,
        payload.body,
        user,
        payload.is_admin_email,
        db,
    )


@router.post("/resend/{id}")
async def resend_email(id:int):
    await EmailSettingLogService
