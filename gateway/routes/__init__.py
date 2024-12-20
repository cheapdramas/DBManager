from fastapi import APIRouter
from .databases_service import router as db_service
from .user_service import router as user_service


MainRouter = APIRouter()
MainRouter.include_router(db_service)
MainRouter.include_router(user_service)