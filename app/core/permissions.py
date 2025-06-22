from app.core.security import verify_token_get_user
from app.models import User
from fastapi import Depends
from app.models.enums import UserRole
from app.utils import CustomException

YOU_DO_NOT_HAVE_ACCESS = 'You do not have access to this resource'

async def admin_only(user: User = Depends(verify_token_get_user)):
    if user.role != UserRole.ADMIN:
        raise CustomException(status_code=403, message=YOU_DO_NOT_HAVE_ACCESS)
    return user

async def student_only(user: User = Depends(verify_token_get_user)):
    if user.role != UserRole.STUDENT:
        raise CustomException(status_code=403, message=YOU_DO_NOT_HAVE_ACCESS)
    return user

async def instructor_only(user: User = Depends(verify_token_get_user)):
    if user.role != UserRole.INSTRUCTOR:
        raise CustomException(status_code=403, message=YOU_DO_NOT_HAVE_ACCESS)
    return user

async def moderator_only(user: User = Depends(verify_token_get_user)):
    if user.role != UserRole.MODERATOR:
        raise CustomException(status_code=403, message=YOU_DO_NOT_HAVE_ACCESS)
    return user

async def any_user_role(user: User = Depends(verify_token_get_user)):
    if user.role not in {UserRole.ADMIN, UserRole.STUDENT, UserRole.INSTRUCTOR, UserRole.MODERATOR}:
        raise CustomException(status_code=403, message=YOU_DO_NOT_HAVE_ACCESS)
    return user