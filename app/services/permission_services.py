# from schemas.permission_schema import PermissionSchema
# from models.permissions_model import Permissions

# class PermissionService:
#     @staticmethod
#     async def create_permission(permission: PermissionSchema):
#         permission_in = Permissions(
#             permission_name=permission.permission_name,
#         )
#         await permission_in.save()
#         return permission_in