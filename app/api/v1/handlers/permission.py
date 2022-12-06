# from fastapi import APIRouter, HTTPException, status
# from schemas.permission_schema import PermissionSchema, PermissionSchemaOut
# from services.permission_services import PermissionService
# import pymongo
# from core.response import *


# permission_router = APIRouter()

# @permission_router.post("/create", summary="Create new permission", response_model=PermissionSchemaOut)
# async def create_permission(data: PermissionSchema):
#     if data.permission_name is not "":
#         try:
#             return await PermissionService.create_permission(data)
#         except pymongo.errors.DuplicateKeyError:
#             return badRequest("Permission with this name already exist, please try again")
#     else:
#         return badRequest("Invalid add permission name can not be empty, please try again")


# @permission_router.get("/", summary="Get permission list", response_model=PermissionSchemaOut)
# async def permission():
#     pass
