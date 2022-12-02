from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    phone_no: str = Field(..., min_length=5, max_length=50, description="user phone no")
    password: str = Field(..., min_length=5, max_length=25, description="user password")

class UserOut(BaseModel):
    user_id: UUID
    name: Optional[str]
    email: EmailStr
    phone_no: str
    address: Optional[str]
    profile_pic: Optional[str]
    country_code: Optional[str]
    my_refer_code: Optional[str]