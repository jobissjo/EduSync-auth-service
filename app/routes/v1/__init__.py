from fastapi import APIRouter
from app.routes.v1 import auth_routes, user_routes, email_routes

router = APIRouter()
router.include_router(auth_routes.router)
router.include_router(user_routes.router)
router.include_router(email_routes.router)
