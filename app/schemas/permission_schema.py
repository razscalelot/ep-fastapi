# from fastapi import HTTPException, status
# from pydantic import BaseModel, EmailStr, Field
# from uuid import UUID

# class PermissionSchema(BaseModel):
#     permission_name: str = Field(..., description="permission name")

# class PermissionSchemaOut(BaseModel):
#     status_code=status.HTTP_201_CREATED
#     detail="Created new permission."
#     permission_name: str