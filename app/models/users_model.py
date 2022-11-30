from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional


class Users(Document):
    user_id: UUID = Field(default_factory=uuid4)
    name: Indexed(str)
    email: Indexed(EmailStr, unique=True)
    phone_no: Indexed(str, unique=True)
    password: str
    address: Optional[str] = None
    profile_pic = Optional[str] = None
    country_code: Optional[str] = None
    refer_code: Optional[str] = None
    my_refer_code: Optional[str] = None
    fcm_token: Optional[str] = None
    status: Optional[bool] = False
    createdBy: Optional[int] = None
    updatedBy: Optional[int] = None

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Users):
            return self.email == other.email
        return False

    @property
    def create(self) -> datetime:
        return self.id.generation_time


    @classmethod
    async def by_email(self, email: str) -> "Users":
        return await self.find_one(self.email == email)

    class Collection:
        name = "users"
