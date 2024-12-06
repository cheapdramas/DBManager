from fastapi import APIRouter
from routes.get import router as get_router
from routes.post import router as post_router
from routes.delete import router as delete_router
from routes.put import router as put_router

MainRouter = APIRouter(prefix='/user')
MainRouter.include_router(get_router)
MainRouter.include_router(post_router)
MainRouter.include_router(delete_router)
MainRouter.include_router(put_router)
