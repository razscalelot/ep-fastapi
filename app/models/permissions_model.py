from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Permissions(BaseModel):
    permission_name: str
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None


class UserPermissions(BaseModel):
    user_id: str
    permission_id: str
    createdBy: Optional[int] = None
    updatedBy: Optional[int] = None


