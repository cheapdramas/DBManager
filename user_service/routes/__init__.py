from fastapi import APIRouter
from routes.get import router as read_router
from routes.post import router as create_router

MainRouter = APIRouter(prefix='/user')
MainRouter.include_router(create_router)
MainRouter.include_router(read_router)

