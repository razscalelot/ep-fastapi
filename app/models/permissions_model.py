# from datetime import datetime
# from uuid import UUID, uuid4
# from beanie import Document, Indexed, Link
# from pydantic import Field
# from typing import Optional
# from models.users_model import Users

# class Permissions(Document):
#     permission_id: UUID = Field(default_factory=uuid4)
#     permission_name: Indexed(str, unique=True)
#     createdBy: Optional[int] = None
#     updatedBy: Optional[int] = None

#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, Permissions):
#             return self.permission_name == other.permission_name
#         return False

#     @property
#     def create(self) -> datetime:
#         return self.id.generation_time


#     class Collection:
#         name = "permissions"


# class UserPermissions(Document):
#     userpermission_id: UUID = Field(default_factory=uuid4)
#     user_id: Link[Users]
#     permission_id: Link[Permissions]
#     createdBy: Optional[int] = None
#     updatedBy: Optional[int] = None

#     @property
#     def create(self) -> datetime:
#         return self.id.generation_time

#     class Collection:
#         name = "userpermissions"


