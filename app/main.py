from fastapi import FastAPI
from app.admin import setup_admin
from app.utils.common import CustomException
from app.middlewares import exception_handler
from app.routes.v1 import router as v1_router
from app.core.settings import setting

app = FastAPI(
    title="EduSyncAuthService",
    description="This is an API for EduSyncAuthService",
    version="1.0.0",
)

app.add_exception_handler(CustomException, exception_handler.custom_exception_handler)

if setting.ENABLE_ADMIN:
    setup_admin(app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


app.include_router(v1_router, prefix="/api/v1")
