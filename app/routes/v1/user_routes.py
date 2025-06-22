from fastapi import APIRouter, Depends
from app.core.permissions import any_user_role
from app.models import User
from app.schemas import BaseUserResponse, BaseResponse


router = APIRouter(prefix="/user", tags=["User"])

@router.get("/",)
async def get_user(user:User=Depends(any_user_role))->BaseResponse[BaseUserResponse]:
    return BaseResponse(status="success", message="User fetched successfully", data=BaseUserResponse(**user.__dict__))