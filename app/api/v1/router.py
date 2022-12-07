from fastapi import APIRouter
from .handlers import user, permission

router = APIRouter()

router.include_router(user.user_router, prefix="/users", tags=["users"])
router.include_router(permission.permission_router, prefix="/permission", tags=["permissions"])
