from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.restaurant import router as restaurant_router
from app.api.v1.endpoints.cashier import router as cashier_router
from app.api.v1.endpoints.inventory import router as inventory_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(admin_router)
api_router.include_router(restaurant_router)
api_router.include_router(cashier_router)
api_router.include_router(inventory_router)
