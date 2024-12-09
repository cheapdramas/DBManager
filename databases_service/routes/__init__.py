from fastapi import APIRouter
from .get import router as get_router
from.post import router as post_router

MainRouter = APIRouter(prefix='/db')
MainRouter.include_router(get_router)
MainRouter.include_router(post_router) 