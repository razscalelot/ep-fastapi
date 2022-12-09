from pydantic import BaseModel
from typing import Optional, List


class ContentType(BaseModel):
    collection_name: str
    createdBy: Optional[int] = None
    updatedBy: Optional[int] = None

class Permissions(BaseModel):
    contenttype_id: str
    permission_name: str
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None


class UserPermissions(BaseModel):
    user_id: str
    permission_id: List[str] = []
    createdBy: Optional[int] = None
    updatedBy: Optional[int] = None




