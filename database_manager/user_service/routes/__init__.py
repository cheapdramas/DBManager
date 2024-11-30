from routes.read import router as read_router
from fastapi import APIRouter

MainRouter = APIRouter(prefix='/user')
MainRouter.include_router(read_router)

