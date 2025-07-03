from typing import Annotated
from fastapi import APIRouter, Depends, Header
from app.core.permissions import any_user_role
from app.models import User
from app.schemas import BaseUserResponse, BaseResponse
from app.utils.common import CustomException
from app.core.settings import setting
from app.services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_config import get_db
import uuid

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/",
)
async def get_user(
    user: User = Depends(any_user_role),
) -> BaseResponse[BaseUserResponse]:
    return BaseResponse(
        status="success",
        message="User fetched successfully",
        data=BaseUserResponse(**user.__dict__),
    )


@router.get("/{id}")
async def get_user_by_id(
    id: uuid, 
    db: Annotated[AsyncSession, Depends(get_db)],
    x_service_token: str = Header(...),
    
) -> BaseResponse[BaseUserResponse]:
    if x_service_token != setting.AUTH_SERVICE_TOKEN:
        raise CustomException(status_code=403, detail="Unauthorized service")
    return UserService.get_user_by_id(id, db)