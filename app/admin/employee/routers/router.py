from fastapi import APIRouter
from ..services.employee_post_get import router as employee_post_get_router
from ..services.excel_api import router as excel_api_router
from ..services.cards import router as cards_router

api_router = APIRouter()


api_router.include_router(employee_post_get_router,prefix='/employees')
api_router.include_router(excel_api_router,prefix='/api')
api_router.include_router(cards_router,prefix='/api')



